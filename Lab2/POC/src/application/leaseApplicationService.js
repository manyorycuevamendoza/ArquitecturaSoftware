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
    const acceptedAt = this.now();
    const accepted = {
      ...application,
      status: "FORMAL_REVIEW",
      quoteAcceptedAt: acceptedAt,
      ownerRole: "Credit-risk analyst",
      nextAction: "Carlos validates the supporting evidence and records the formal decision",
      timeline: appendEvent(application, acceptedAt, "Pedro", "SME owner", "Preliminary quote accepted", "Case sent to Carlos for formal review")
    };
    this.repository.save(accepted);
    return accepted;
  }

  approveCredit(applicationId, review) {
    const application = this.repository.find(applicationId);
    if (!application) throw new Error("Lease application was not found.");
    if (["CREDIT_APPROVED", "DELIVERY_SCHEDULED"].includes(application.status)) return application;
    if (!["FORMAL_REVIEW", "MANUAL_REVIEW"].includes(application.status)) throw new Error("Only a case assigned to credit review can be approved.");

    const evidence = normalizeEvidence(review);
    const missing = evidence.filter((item) => item.status !== "VALID");
    if (missing.length > 0) throw new Error(`Carlos must validate all required evidence: ${missing.map((item) => item.label).join(", ")}.`);
    const reason = String(review.reason ?? "").trim();
    if (!reason) throw new Error("Carlos must record the reason for the credit decision.");

    const decidedAt = this.now();
    const approved = {
      ...application,
      status: "CREDIT_APPROVED",
      evidence,
      creditDecision: { outcome: "APPROVED", analyst: "Carlos", reason, decidedAt, policyVersion: application.policyVersion },
      ownerRole: "Leasing-operations coordinator",
      nextAction: "Julia prepares the contract and confirms a delivery date with the supplier",
      timeline: appendEvent(application, decidedAt, "Carlos", "Credit-risk analyst", "Credit approved", reason)
    };
    this.repository.save(approved);
    return approved;
  }

  scheduleDelivery(applicationId, coordination) {
    const application = this.repository.find(applicationId);
    if (!application) throw new Error("Lease application was not found.");
    if (application.status === "DELIVERY_SCHEDULED") return application;
    if (application.status !== "CREDIT_APPROVED") throw new Error("Only a credit-approved case can be coordinated by operations.");

    const operation = normalizeOperation(coordination);
    const scheduledAt = this.now();
    const scheduled = {
      ...application,
      status: "DELIVERY_SCHEDULED",
      operation: { ...operation, coordinatedBy: "Julia", scheduledAt },
      ownerRole: "SME owner",
      nextAction: `Pedro reviews the delivery scheduled for ${operation.deliveryDate}`,
      timeline: appendEvent(application, scheduledAt, "Julia", "Leasing-operations coordinator", "Delivery scheduled", `${operation.supplierName} confirmed delivery for ${operation.deliveryDate}`)
    };
    this.repository.save(scheduled);
    return scheduled;
  }
}

function normalizeEvidence(review) {
  return [
    { code: "RUC_RECORD", label: "RUC record", status: review.rucRecord ? "VALID" : "MISSING" },
    { code: "PROJECT_CONTRACT", label: "Signed project contract", status: review.projectContract ? "VALID" : "MISSING" },
    { code: "BANK_STATEMENTS", label: "Recent bank statements", status: review.bankStatements ? "VALID" : "MISSING" }
  ];
}

function normalizeOperation(coordination) {
  const operation = {
    supplierName: String(coordination.supplierName ?? "").trim(),
    contractReference: String(coordination.contractReference ?? "").trim(),
    deliveryDate: String(coordination.deliveryDate ?? "").trim()
  };
  const missing = Object.entries(operation).filter(([, value]) => !value).map(([key]) => key);
  if (missing.length > 0) throw new Error(`Julia must complete: ${missing.join(", ")}.`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(operation.deliveryDate)) throw new Error("Delivery date must use YYYY-MM-DD format.");
  return operation;
}

function appendEvent(application, at, actor, role, action, detail) {
  return [...(application.timeline ?? []), { at, actor, role, action, detail }];
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
