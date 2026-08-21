export const CREDIT_POLICY_VERSION = "POC-CREDIT-2026-08-v1";

const MINIMUM_CREDIT_SCORE = 650;
const MAXIMUM_LATE_PAYMENTS_LAST_12_MONTHS = 2;

export function evaluateCreditAssessment({ negativeRecord, bureauReport }) {
  const negativeRecordRule = evaluatedRule(
    "NEGATIVE_RECORD_CLEAR",
    !negativeRecord.found,
    "The applicant RUC must not appear in the simulated negative-record database."
  );

  if (negativeRecord.found) {
    const stopReason = "Credit evaluation stopped because the applicant RUC appears in the simulated negative-record database.";
    return {
      outcome: "REJECTED",
      policyVersion: CREDIT_POLICY_VERSION,
      negativeRecord,
      bureauReport: null,
      ruleResults: [
        negativeRecordRule,
        notEvaluatedRule("CREDIT_SCORE", stopReason),
        notEvaluatedRule("OVERDUE_DEBT", stopReason),
        notEvaluatedRule("LATE_PAYMENTS", stopReason)
      ],
      explanation: stopReason
    };
  }

  const bureauRules = [
    evaluatedRule("CREDIT_SCORE", bureauReport.score >= MINIMUM_CREDIT_SCORE, `The simulated credit-bureau score must be at least ${MINIMUM_CREDIT_SCORE}.`),
    evaluatedRule("OVERDUE_DEBT", bureauReport.overdueDebt === 0, "The simulated credit-bureau report must show no overdue debt."),
    evaluatedRule("LATE_PAYMENTS", bureauReport.latePaymentsLast12Months <= MAXIMUM_LATE_PAYMENTS_LAST_12_MONTHS, `The simulated report must show no more than ${MAXIMUM_LATE_PAYMENTS_LAST_12_MONTHS} late payments in the last 12 months.`)
  ];
  const ruleResults = [negativeRecordRule, ...bureauRules];
  const outcome = ruleResults.every((item) => item.passed) ? "APPROVED" : "REJECTED";

  return {
    outcome,
    policyVersion: CREDIT_POLICY_VERSION,
    negativeRecord,
    bureauReport,
    ruleResults,
    explanation: outcome === "APPROVED"
      ? "The applicant cleared the negative-record check and passed every simulated credit-behavior rule."
      : "The applicant cleared the negative-record check but failed one or more simulated credit-behavior rules."
  };
}

function evaluatedRule(code, passed, requirement) {
  return { code, status: passed ? "PASSED" : "FAILED", passed, message: `${passed ? "Passed" : "Failed"}: ${requirement}` };
}

function notEvaluatedRule(code, reason) {
  return { code, status: "NOT_EVALUATED", passed: null, message: `Not evaluated: ${reason}` };
}
