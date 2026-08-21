import { randomUUID } from "node:crypto";
import { LeaseApplicationService } from "../src/application/leaseApplicationService.js";
import { InMemoryLeaseApplicationRepository } from "../src/adapters/inMemoryLeaseApplicationRepository.js";
import { POLICY_VERSION } from "../src/domain/preliminaryEligibilityPolicy.js";
import { CREDIT_POLICY_VERSION } from "../src/domain/creditAssessmentPolicy.js";
import { SimulatedCreditBureauProvider, SimulatedNegativeRecordProvider } from "../src/adapters/simulatedCreditRiskProviders.js";

const repository = new InMemoryLeaseApplicationRepository();
const negativeRecordProvider = new SimulatedNegativeRecordProvider();
const creditBureauProvider = new SimulatedCreditBureauProvider();
const service = new LeaseApplicationService(repository, {
  now: () => "2026-08-20T12:00:00.000Z",
  generateId: randomUUID,
  negativeRecordProvider,
  creditBureauProvider
});
const request = { companyName: "Constructora Andina SAC", ruc: "20123456789", machinery: "Hydraulic excavator", equipmentValue: 450000, initialPaymentPercent: 20, termMonths: 36, monthsOperating: 48, expectedMonthlyProjectCashFlow: 18000 };
const created = service.submit(request, "happy-path-001");
assert(created.status === "PRE_APPROVED", "Valid request must be pre-approved.");
assert(created.quote !== null, "Pre-approved request must include a quote.");
assert(created.policyVersion === POLICY_VERSION, "Decision must expose its policy version.");
assert(created.ruleResults.every((item) => item.passed), "Every happy-path rule must pass.");
assert(service.submit(request, "happy-path-001").id === created.id, "Repeated submission must be idempotent.");
let acknowledgementRejected = false;
try { service.acceptQuote(created.id, false); } catch { acknowledgementRejected = true; }
assert(acknowledgementRejected, "Quote acceptance must require acknowledgement.");
const accepted = service.acceptQuote(created.id, true);
assert(accepted.status === "FORMAL_REVIEW", "Accepted quote must enter formal review.");
assert(service.acceptQuote(created.id, true).status === "FORMAL_REVIEW", "Repeated acceptance must be idempotent.");
assert(accepted.request.ruc === request.ruc && accepted.quote.termMonths === request.termMonths, "The same applicant data and quote must reach Carlos.");
let incompleteEvidenceRejected = false;
try { service.evaluateCredit(created.id, { rucRecord: true, projectContract: false, bankStatements: true, reason: "Incomplete evidence." }); } catch { incompleteEvidenceRejected = true; }
assert(incompleteEvidenceRejected, "Carlos must not approve a case with missing evidence.");
let prematureOperationsRejected = false;
try { service.scheduleDelivery(created.id, { supplierName: "Maquinarias del Peru SAC", contractReference: "LEASE-2026-001", deliveryDate: "2026-09-15" }); } catch { prematureOperationsRejected = true; }
assert(prematureOperationsRejected, "Julia must not coordinate delivery before credit approval.");
const approved = service.evaluateCredit(created.id, { rucRecord: true, projectContract: true, bankStatements: true, reason: "Verified project income supports the requested lease." });
assert(approved.status === "CREDIT_APPROVED", "Carlos must be able to approve a complete formal-review case.");
assert(approved.creditDecision.analyst === "Carlos", "The formal decision must identify Carlos.");
assert(approved.evidence.every((item) => item.status === "VALID"), "Every required document must be valid before approval.");
assert(approved.creditAssessment.policyVersion === CREDIT_POLICY_VERSION, "The formal assessment must expose its credit-policy version.");
assert(approved.creditAssessment.ruleResults.every((item) => item.passed), "The happy-path RUC must pass every external-risk rule.");
assert(creditBureauProvider.queryCount === 1, "The clear happy-path RUC must be queried in the simulated credit bureau once.");
const scheduled = service.scheduleDelivery(created.id, { supplierName: "Maquinarias del Peru SAC", contractReference: "LEASE-2026-001", deliveryDate: "2026-09-15" });
assert(scheduled.status === "DELIVERY_SCHEDULED", "Julia must be able to schedule delivery for an approved case.");
assert(scheduled.operation.coordinatedBy === "Julia", "The operational handoff must identify Julia.");
assert(scheduled.timeline.length === 4, "The end-to-end timeline must contain one event for every completed stage.");
assert(service.scheduleDelivery(created.id, scheduled.operation).status === "DELIVERY_SCHEDULED", "Repeated delivery scheduling must be idempotent.");
const manualReview = service.submit({ ...request, monthsOperating: 6 }, "manual-review-001");
assert(manualReview.status === "MANUAL_REVIEW", "A structurally valid borderline case must enter manual review.");
const negativeCase = service.submit({ ...request, ruc: "20999999999" }, "negative-record-001");
service.acceptQuote(negativeCase.id, true);
const bureauQueriesBeforeNegativeCase = creditBureauProvider.queryCount;
const negativeDecision = service.evaluateCredit(negativeCase.id, { rucRecord: false, projectContract: false, bankStatements: false, reason: "Negative record found." });
assert(negativeDecision.status === "CREDIT_REJECTED", "A RUC in the simulated negative database must be rejected.");
assert(negativeDecision.creditAssessment.bureauReport === null, "A negative-list hit must not include a bureau report.");
assert(negativeDecision.creditAssessment.ruleResults.filter((item) => item.code !== "NEGATIVE_RECORD_CLEAR").every((item) => item.status === "NOT_EVALUATED"), "Score, debt and late-payment rules must be skipped after a negative-list hit.");
assert(creditBureauProvider.queryCount === bureauQueriesBeforeNegativeCase, "The credit bureau must not be queried after a negative-list hit.");
const lowScoreCase = service.submit({ ...request, ruc: "20666666666" }, "low-score-001");
service.acceptQuote(lowScoreCase.id, true);
const lowScoreDecision = service.evaluateCredit(lowScoreCase.id, { rucRecord: true, projectContract: true, bankStatements: true, reason: "External-risk rules did not pass." });
assert(lowScoreDecision.status === "CREDIT_REJECTED", "A clear RUC with failing behavior rules must be rejected.");
assert(lowScoreDecision.creditAssessment.bureauReport.score === 580, "The low-score scenario must expose the simulated bureau score.");
const rejected = service.submit({ ...request, ruc: "123" }, "invalid-ruc-001");
assert(rejected.status === "REJECTED", "Invalid RUC must reject the preliminary request.");
assert(!rejected.ruleResults.find((item) => item.code === "RUC_FORMAT").passed, "RUC failure must be explainable.");
console.log("SELF-TEST PASSED");
console.log(`Estimated installment: S/ ${created.quote.estimatedMonthlyInstallment.toFixed(2)}`);
console.log(`Final POC state: ${scheduled.status}`);
function assert(condition, message) { if (!condition) throw new Error(`SELF-TEST FAILED: ${message}`); }
