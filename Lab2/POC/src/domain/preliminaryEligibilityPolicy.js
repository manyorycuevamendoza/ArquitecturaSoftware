export const POLICY_VERSION = "POC-2026-08-v1";

const ANNUAL_REFERENCE_RATE = 0.14;

function rule(code, passed, requirement) {
  return { code, passed, message: `${passed ? "Passed" : "Failed"}: ${requirement}` };
}

export function evaluatePreliminaryEligibility({ id, idempotencyKey, request, createdAt }) {
  const quote = calculateQuote(request);
  const rules = [
    rule("RUC_FORMAT", /^\d{11}$/.test(request.ruc), "RUC must contain exactly 11 digits."),
    rule("EQUIPMENT_VALUE", request.equipmentValue >= 50_000 && request.equipmentValue <= 2_000_000, "Equipment value must be between S/ 50,000 and S/ 2,000,000 for this POC."),
    rule("INITIAL_PAYMENT", request.initialPaymentPercent >= 10 && request.initialPaymentPercent <= 50, "Initial payment must be between 10% and 50%."),
    rule("TERM", request.termMonths >= 12 && request.termMonths <= 60, "Requested term must be between 12 and 60 months."),
    rule("OPERATING_HISTORY", request.monthsOperating >= 12, "At least 12 months of operating history is required for automatic pre-approval."),
    rule("PAYMENT_COVERAGE", quote !== null && request.expectedMonthlyProjectCashFlow >= quote.estimatedMonthlyInstallment * 1.25, "Expected monthly project cash flow must cover at least 125% of the estimated installment.")
  ];

  const structuralCodes = new Set(["RUC_FORMAT", "EQUIPMENT_VALUE", "INITIAL_PAYMENT", "TERM"]);
  const structuralFailure = rules.some((item) => structuralCodes.has(item.code) && !item.passed);
  const reviewFailure = rules.some((item) => !structuralCodes.has(item.code) && !item.passed);
  const status = structuralFailure ? "REJECTED" : reviewFailure ? "MANUAL_REVIEW" : "PRE_APPROVED";

  return {
    id,
    idempotencyKey,
    request: structuredClone(request),
    status,
    quote,
    policyVersion: POLICY_VERSION,
    ruleResults: rules,
    createdAt,
    quoteAcceptedAt: null,
    ownerRole: status === "PRE_APPROVED" ? "SME owner" : "Credit-risk analyst",
    nextAction: status === "PRE_APPROVED"
      ? "Review and accept the preliminary quote"
      : status === "MANUAL_REVIEW"
        ? "Credit analyst performs manual review"
        : "Review the failed eligibility rules"
  };
}

function calculateQuote(request) {
  if (request.equipmentValue <= 0 || request.initialPaymentPercent < 0 || request.initialPaymentPercent > 100 || request.termMonths <= 0) return null;
  const initialPayment = roundMoney(request.equipmentValue * request.initialPaymentPercent / 100);
  const financedAmount = roundMoney(request.equipmentValue - initialPayment);
  const monthlyRate = ANNUAL_REFERENCE_RATE / 12;
  const factor = (1 + monthlyRate) ** request.termMonths;
  const estimatedMonthlyInstallment = roundMoney(financedAmount * monthlyRate * factor / (factor - 1));
  return { equipmentValue: request.equipmentValue, initialPayment, financedAmount, annualReferenceRate: ANNUAL_REFERENCE_RATE, termMonths: request.termMonths, estimatedMonthlyInstallment };
}

function roundMoney(value) {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}
