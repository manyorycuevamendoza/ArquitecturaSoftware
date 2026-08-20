import { evaluatePreliminaryEligibility } from "../domain/preliminaryEligibilityPolicy.js";

export class LeaseApplicationService {
  constructor(repository, { now, generateId }) {
    this.repository = repository;
    this.now = now;
    this.generateId = generateId;
  }

  submit(request, idempotencyKey) {
    const existing = this.repository.findByIdempotencyKey(idempotencyKey);
    if (existing) return existing;
    const normalized = normalizeAndValidate(request);
    const application = evaluatePreliminaryEligibility({ id: this.generateId(), idempotencyKey, request: normalized, createdAt: this.now() });
    this.repository.add(application);
    return application;
  }

  acceptQuote(applicationId, acknowledgedPreliminary) {
    if (!acknowledgedPreliminary) throw new Error("You must acknowledge that the quote is preliminary and non-binding.");
    const application = this.repository.find(applicationId);
    if (!application) throw new Error("Lease application was not found.");
    if (application.status === "FORMAL_REVIEW") return application;
    if (application.status !== "PRE_APPROVED") throw new Error("Only a pre-approved quote can be accepted.");
    const accepted = { ...application, status: "FORMAL_REVIEW", quoteAcceptedAt: this.now(), ownerRole: "Credit-risk analyst", nextAction: "Credit analyst validates supporting evidence" };
    this.repository.save(accepted);
    return accepted;
  }
}

function normalizeAndValidate(request) {
  const normalized = {
    companyName: String(request.companyName ?? "").trim(),
    ruc: String(request.ruc ?? "").trim(),
    machinery: String(request.machinery ?? "").trim(),
    equipmentValue: Number(request.equipmentValue),
    initialPaymentPercent: Number(request.initialPaymentPercent),
    termMonths: Number(request.termMonths),
    monthsOperating: Number(request.monthsOperating),
    expectedMonthlyProjectCashFlow: Number(request.expectedMonthlyProjectCashFlow)
  };
  const errors = [];
  if (!normalized.companyName) errors.push("Company name is required.");
  if (!normalized.ruc) errors.push("RUC is required.");
  if (!normalized.machinery) errors.push("Machinery description is required.");
  if (!(normalized.equipmentValue > 0)) errors.push("Equipment value must be greater than zero.");
  if (normalized.initialPaymentPercent < 0 || normalized.initialPaymentPercent > 100) errors.push("Initial payment percentage must be between 0 and 100.");
  if (!(normalized.termMonths > 0)) errors.push("Term must be greater than zero.");
  if (normalized.monthsOperating < 0) errors.push("Months operating cannot be negative.");
  if (normalized.expectedMonthlyProjectCashFlow < 0) errors.push("Expected project cash flow cannot be negative.");
  if (errors.length > 0) throw new Error(errors.join(" "));
  return normalized;
}
