import React, { useMemo, useState } from "react";
import { LeaseApplicationService } from "./application/leaseApplicationService.js";
import { InMemoryLeaseApplicationRepository } from "./adapters/inMemoryLeaseApplicationRepository.js";
import { SimulatedCreditBureauProvider, SimulatedNegativeRecordProvider } from "./adapters/simulatedCreditRiskProviders.js";

const SAMPLE = {
  companyName: "Constructora Andina SAC",
  ruc: "20123456789",
  machinery: "Hydraulic excavator",
  equipmentValue: 450000,
  initialPaymentPercent: 20,
  termMonths: 36,
  monthsOperating: 48,
  expectedMonthlyProjectCashFlow: 18000
};
const ROLES = [
  { id: "pedro", name: "Pedro", label: "Applicant SME" },
  { id: "carlos", name: "Carlos", label: "Credit review" },
  { id: "julia", name: "Julia", label: "Operations" }
];
const money = new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN", minimumFractionDigits: 2 });

export default function App() {
  const service = useMemo(() => new LeaseApplicationService(new InMemoryLeaseApplicationRepository(), {
    now: () => new Date().toISOString(),
    generateId: () => crypto.randomUUID(),
    negativeRecordProvider: new SimulatedNegativeRecordProvider(),
    creditBureauProvider: new SimulatedCreditBureauProvider()
  }), []);
  const [activeRole, setActiveRole] = useState("pedro");
  const [application, setApplication] = useState(null);
  const [error, setError] = useState("");
  const [acknowledged, setAcknowledged] = useState(false);

  function run(action, nextRole) {
    setError("");
    try {
      const updated = action();
      setApplication(updated);
      if (nextRole) setActiveRole(nextRole);
    } catch (actionError) {
      setError(actionError.message);
    }
  }

  function submit(event) {
    event.preventDefault();
    run(() => service.submit(Object.fromEntries(new FormData(event.currentTarget)), crypto.randomUUID()));
  }

  function acceptQuote() {
    run(() => service.acceptQuote(application.id, acknowledged), "carlos");
  }

  function evaluateCredit(review) {
    setError("");
    try {
      const updated = service.evaluateCredit(application.id, review);
      setApplication(updated);
      setActiveRole(updated.status === "CREDIT_APPROVED" ? "julia" : "pedro");
    } catch (evaluationError) {
      setError(evaluationError.message);
    }
  }

  function scheduleDelivery(coordination) {
    run(() => service.scheduleDelivery(application.id, coordination), "pedro");
  }

  return <>
    <header className="topbar">
      <div><span className="brand">LeaseNow Peru</span><span className="badge">React end-to-end POC</span></div>
      {application && <span className="case-id">Case {shortId(application.id)}</span>}
    </header>
    <nav className="role-nav" aria-label="POC role views">
      {ROLES.map((role) => <button key={role.id} type="button" className={activeRole === role.id ? "active" : ""} onClick={() => { setActiveRole(role.id); setError(""); }}>
        <strong>{role.name}</strong><span>{role.label}</span>
      </button>)}
    </nav>
    <main>
      {error && <p className="error card" role="alert">{error}</p>}
      {activeRole === "pedro" && <PedroView application={application} onSubmit={submit} acknowledged={acknowledged} onAcknowledged={setAcknowledged} onAccept={acceptQuote} />}
      {activeRole === "carlos" && <CarlosView application={application} onEvaluate={evaluateCredit} />}
      {activeRole === "julia" && <JuliaView application={application} onSchedule={scheduleDelivery} />}
    </main>
  </>;
}

function PedroView({ application, onSubmit, acknowledged, onAcknowledged, onAccept }) {
  if (!application) return <>
    <Intro eyebrow="Pedro · Applicant SME" title="Know whether the machinery lease is viable before committing your working capital">
      Submit the project once and see the preliminary result, payment term, monthly installment, current owner and next step.
    </Intro>
    <section className="card">
      <form onSubmit={onSubmit}>
        <div className="grid">
          <Field label="Company name" name="companyName" defaultValue={SAMPLE.companyName} />
          <Field label="RUC" name="ruc" defaultValue={SAMPLE.ruc} maxLength="11" />
          <Field label="Required machinery" name="machinery" defaultValue={SAMPLE.machinery} wide />
          <Field label="Equipment value (S/)" name="equipmentValue" type="number" defaultValue={SAMPLE.equipmentValue} />
          <Field label="Initial payment (%)" name="initialPaymentPercent" type="number" defaultValue={SAMPLE.initialPaymentPercent} />
          <Field label="Requested payment term (months)" name="termMonths" type="number" defaultValue={SAMPLE.termMonths} />
          <Field label="Operating history (months)" name="monthsOperating" type="number" defaultValue={SAMPLE.monthsOperating} />
          <Field label="Expected monthly project cash flow (S/)" name="expectedMonthlyProjectCashFlow" type="number" defaultValue={SAMPLE.expectedMonthlyProjectCashFlow} wide hint="Money the project is expected to generate each month to cover the lease installment." />
        </div>
        <button type="submit">Check preliminary eligibility</button>
      </form>
    </section>
  </>;

  return <>
    <Intro eyebrow="Pedro · Applicant SME" title="Your machinery-leasing request">
      The same case follows you through credit review and delivery coordination; you do not need to enter the information again.
    </Intro>
    <CaseOverview application={application} audience="Pedro" />
    <Progress application={application} />
    {application.quote && <section className="card section-gap">
      <h2>Payment information</h2>
      <p className="supporting">This is the information Pedro needs before deciding whether the project can afford the machinery.</p>
      <Quote quote={application.quote} />
    </section>}
    {["PRE_APPROVED", "MANUAL_REVIEW", "REJECTED"].includes(application.status) && <PreliminaryResult application={application} acknowledged={acknowledged} onAcknowledged={onAcknowledged} onAccept={onAccept} />}
    {application.status === "FORMAL_REVIEW" && <Callout title="Formal approval is pending" tone="warning">Carlos now owns the case and must validate the evidence. The preliminary result is not a final approval.</Callout>}
    {application.creditDecision && <CreditAssessment assessment={application.creditAssessment} />}
    {application.creditDecision && <Callout title={application.creditDecision.outcome === "APPROVED" ? "The lease was formally approved" : "The credit assessment was rejected"} tone={application.creditDecision.outcome === "APPROVED" ? "success" : "danger"}>Carlos recorded this decision. Reason: {application.creditDecision.reason}</Callout>}
    {application.operation && <section className="card section-gap"><h2>Delivery confirmed</h2><DefinitionGrid items={[
      ["Supplier", application.operation.supplierName],
      ["Contract reference", application.operation.contractReference],
      ["Scheduled date", application.operation.deliveryDate],
      ["Coordinated by", application.operation.coordinatedBy]
    ]} /></section>}
    <Timeline events={application.timeline} />
  </>;
}

function CarlosView({ application, onEvaluate }) {
  return <>
    <Intro eyebrow="Carlos · Credit-risk analyst" title="Review one complete and explainable case">
      Validate the same data Pedro submitted, see every automatic rule and record a formal decision without rebuilding the application from emails.
    </Intro>
    {!application && <EmptyState title="No application is waiting">Pedro must submit and accept a preliminary quote before Carlos can review it.</EmptyState>}
    {application && <>
      <CaseOverview application={application} audience="Carlos" />
      <Progress application={application} />
      <section className="card section-gap">
        <h2>Applicant and requested terms</h2>
        <DefinitionGrid items={[
          ["Company", application.request.companyName], ["RUC", application.request.ruc],
          ["Machinery", application.request.machinery], ["Operating history", `${application.request.monthsOperating} months`],
          ["Project cash flow", money.format(application.request.expectedMonthlyProjectCashFlow)], ["Payment term", `${application.quote?.termMonths ?? application.request.termMonths} months`]
        ]} />
        {application.quote && <Quote quote={application.quote} compact />}
      </section>
      <RuleResults rules={application.ruleResults} />
      {["FORMAL_REVIEW", "MANUAL_REVIEW"].includes(application.status) && <CreditReviewForm evidence={application.evidence} onEvaluate={onEvaluate} />}
      {application.status === "PRE_APPROVED" && <EmptyState title="Waiting for Pedro">The quote is pre-approved, but Pedro must acknowledge and accept it before formal review.</EmptyState>}
      {application.status === "REJECTED" && <EmptyState title="Case rejected at intake">The structural failures are listed above. This case cannot enter the happy path.</EmptyState>}
      {application.creditAssessment && <CreditAssessment assessment={application.creditAssessment} />}
      {application.creditDecision && !application.creditAssessment.negativeRecord.found && <EvidenceSummary evidence={application.evidence} />}
      {application.creditDecision && <Callout title={`Decision recorded: ${application.creditDecision.outcome}`} tone={application.creditDecision.outcome === "APPROVED" ? "success" : "danger"}>{application.creditDecision.analyst} recorded: {application.creditDecision.reason}</Callout>}
      <Timeline events={application.timeline} />
    </>}
  </>;
}

function CreditReviewForm({ evidence, onEvaluate }) {
  function submit(event) {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.currentTarget));
    onEvaluate({ rucRecord: data.rucRecord === "on", projectContract: data.projectContract === "on", bankStatements: data.bankStatements === "on", reason: data.reason });
  }
  return <section className="card section-gap">
    <p className="eyebrow">Formal credit decision</p><h2>Evidence and external-risk checks</h2>
    <p className="supporting">The POC checks a simulated negative-record database first. If the RUC is found, it stops and does not query or score the credit-bureau behavior. Otherwise, it applies the simulated score, overdue-debt and late-payment rules.</p>
    <div className="test-data"><strong>Test RUCs</strong><span><code>20123456789</code> passes</span><span><code>20999999999</code> appears in the negative database</span><span><code>20666666666</code> has a low score and overdue debt</span></div>
    <form onSubmit={submit}>
      <div className="evidence-list">
        {evidence.map((item) => <label className="check-row" key={item.code}><input type="checkbox" name={fieldName(item.code)} /> <span><strong>{item.label}</strong><small>Mark as validated by Carlos</small></span></label>)}
      </div>
      <label>Credit decision reason<textarea name="reason" required defaultValue="Verified documents, project capacity and external-risk results support the credit decision." /></label>
      <button type="submit">Run credit assessment</button>
    </form>
  </section>;
}

function JuliaView({ application, onSchedule }) {
  return <>
    <Intro eyebrow="Julia · Leasing-operations coordinator" title="Coordinate an approved case without spreadsheets">
      See the approved terms, current owner and next action, then record the supplier, contract reference and scheduled delivery date.
    </Intro>
    {!application && <EmptyState title="No application exists">The shared operations view will display the same case after Pedro submits it.</EmptyState>}
    {application && <>
      <CaseOverview application={application} audience="Julia" />
      <Progress application={application} />
      {["CREDIT_APPROVED", "DELIVERY_SCHEDULED"].includes(application.status) && <section className="card section-gap"><h2>Credit-approved case</h2><p className="supporting">These are the same applicant, machinery and financial terms Carlos approved.</p><DefinitionGrid items={[
        ["Company", application.request.companyName], ["RUC", application.request.ruc],
        ["Machinery", application.request.machinery], ["Approved by", application.creditDecision.analyst]
      ]} /><Quote quote={application.quote} compact /></section>}
      {application.status === "CREDIT_APPROVED" && <OperationsForm onSchedule={onSchedule} />}
      {application.status !== "CREDIT_APPROVED" && application.status !== "DELIVERY_SCHEDULED" && <EmptyState title="Case is not ready for operations">Current owner: {application.ownerRole}. Julia can act only after Carlos records formal credit approval.</EmptyState>}
      {application.operation && <section className="card section-gap"><p className="eyebrow">Coordination complete</p><h2>Delivery scheduled</h2><DefinitionGrid items={[
        ["Company", application.request.companyName], ["Machinery", application.request.machinery],
        ["Supplier", application.operation.supplierName], ["Contract reference", application.operation.contractReference],
        ["Delivery date", application.operation.deliveryDate], ["Payment term", `${application.quote.termMonths} months`]
      ]} /></section>}
      <Timeline events={application.timeline} />
    </>}
  </>;
}

function OperationsForm({ onSchedule }) {
  function submit(event) {
    event.preventDefault();
    onSchedule(Object.fromEntries(new FormData(event.currentTarget)));
  }
  return <section className="card section-gap">
    <p className="eyebrow">Operations handoff</p><h2>Prepare contract and delivery</h2>
    <form onSubmit={submit}><div className="grid">
      <Field label="Machinery supplier" name="supplierName" defaultValue="Maquinarias del Peru SAC" />
      <Field label="Contract reference" name="contractReference" defaultValue="LEASE-2026-001" />
      <Field label="Confirmed delivery date" name="deliveryDate" type="date" defaultValue={futureDate(14)} wide />
    </div><button type="submit">Confirm contract and schedule delivery</button></form>
  </section>;
}

function Intro({ eyebrow, title, children }) { return <section className="intro"><p className="eyebrow">{eyebrow}</p><h1>{title}</h1><p>{children}</p></section>; }

function Field({ label, hint, wide = false, ...inputProps }) {
  const numeric = inputProps.type === "number";
  return <label className={wide ? "wide" : ""}>{label}<input required min={numeric ? "0" : undefined} step={numeric ? "0.01" : undefined} {...inputProps} />{hint && <small className="field-hint">{hint}</small>}</label>;
}

function CaseOverview({ application, audience }) {
  return <section className="card case-overview">
    <div><p className="eyebrow">Shared case · visible to {audience}</p><h2>{application.request.companyName}</h2><p>{application.request.machinery}</p></div>
    <div className="status-panel"><span className={`status ${statusTone(application.status)}`}>{formatStatus(application.status)}</span><strong>Owner: {application.ownerRole}</strong><span>Next: {application.nextAction}</span></div>
  </section>;
}

function Progress({ application }) {
  const completed = progressIndex(application.status);
  const steps = ["Request submitted", "Quote accepted", "Credit approved", "Delivery scheduled"];
  return <section className="progress card section-gap" aria-label="Application progress">{steps.map((step, index) => <div className={index <= completed ? "done" : ""} key={step}><span>{index <= completed ? "✓" : index + 1}</span><strong>{step}</strong></div>)}</section>;
}

function PreliminaryResult({ application, acknowledged, onAcknowledged, onAccept }) {
  return <section className="card section-gap" aria-live="polite">
    <div className="result-header"><div><p className="eyebrow">Preliminary decision</p><h2>{formatStatus(application.status)}</h2></div><span className={`status ${statusTone(application.status)}`}>{formatStatus(application.status)}</span></div>
    <RuleResults rules={application.ruleResults} nested />
    <p><strong>Next step:</strong> {application.nextAction}</p>
    {application.status === "PRE_APPROVED" && <><label className="acknowledgement"><input type="checkbox" checked={acknowledged} onChange={(event) => onAcknowledged(event.target.checked)} />I understand this quote is preliminary, non-binding and still requires Carlos&apos;s formal approval.</label><button type="button" onClick={onAccept}>Accept quote and send to Carlos</button></>}
    <p className="disclaimer">Policy {application.policyVersion}. A preliminary result is not final credit approval or a signed contract.</p>
  </section>;
}

function RuleResults({ rules, nested = false }) {
  const content = <><h3>Eligibility checks</h3><ul className="checks">{rules.map((item) => <li key={item.code} className={item.passed ? "passed" : "failed"}>{item.passed ? "✓" : "!"} {item.message}</li>)}</ul></>;
  return nested ? content : <section className="card section-gap">{content}</section>;
}

function EvidenceSummary({ evidence }) { return <section className="card section-gap"><h2>Validated evidence</h2><ul className="checks">{evidence.map((item) => <li className={item.status === "VALID" ? "passed" : "failed"} key={item.code}>{item.status === "VALID" ? "✓" : "!"} {item.label}: {formatStatus(item.status)}</li>)}</ul></section>; }

function CreditAssessment({ assessment }) {
  const negativeLabel = assessment.negativeRecord.found ? "FOUND — evaluation stopped" : "CLEAR";
  return <section className="card section-gap"><p className="eyebrow">Credit policy {assessment.policyVersion}</p><h2>External-risk assessment</h2>
    <DefinitionGrid items={[
      ["Negative-record source", assessment.negativeRecord.source],
      ["Negative-record result", negativeLabel],
      ["Credit-bureau source", assessment.bureauReport?.source ?? "Not queried"],
      ["Credit score", assessment.bureauReport?.score ?? "Not evaluated"],
      ["Overdue debt", assessment.bureauReport ? money.format(assessment.bureauReport.overdueDebt) : "Not evaluated"],
      ["Late payments (12 months)", assessment.bureauReport?.latePaymentsLast12Months ?? "Not evaluated"]
    ]} />
    <h3>Credit rules</h3><ul className="checks">{assessment.ruleResults.map((item) => <li key={item.code} className={item.status === "PASSED" ? "passed" : item.status === "FAILED" ? "failed" : "skipped"}>{item.status === "PASSED" ? "✓" : item.status === "FAILED" ? "!" : "—"} {item.message}</li>)}</ul>
    <p className="disclaimer">These providers and thresholds are deterministic POC simulations, not real Equifax/SBS responses or an approved lending policy.</p>
  </section>;
}

function Quote({ quote, compact = false }) {
  const items = [
    ["Equipment value", money.format(quote.equipmentValue)],
    ["Initial payment", money.format(quote.initialPayment)],
    ["Financed amount", money.format(quote.financedAmount)],
    ["Monthly installment", money.format(quote.estimatedMonthlyInstallment)],
    ["Number of monthly payments", `${quote.termMonths} months`],
    ["Annual reference rate", `${(quote.annualReferenceRate * 100).toFixed(2)}%`],
    ["Estimated lease payments", money.format(quote.estimatedLeasePayments)],
    ["Estimated total including initial payment", money.format(quote.estimatedTotalPaid)]
  ];
  return <div className={`quote-grid ${compact ? "compact" : ""}`}>{items.map(([label, value]) => <Metric key={label} label={label} value={value} />)}</div>;
}

function Timeline({ events }) { return <section className="card section-gap"><h2>Case history</h2><ol className="timeline">{events.map((event, index) => <li key={`${event.at}-${index}`}><span>{index + 1}</span><div><strong>{event.action}</strong><p>{event.actor} · {event.role}</p><small>{event.detail}</small></div></li>)}</ol></section>; }
function DefinitionGrid({ items }) { return <dl className="definition-grid">{items.map(([term, value]) => <div key={term}><dt>{term}</dt><dd>{value}</dd></div>)}</dl>; }
function Metric({ label, value }) { return <div><span>{label}</span><strong>{value}</strong></div>; }
function EmptyState({ title, children }) { return <section className="card empty-state"><h2>{title}</h2><p>{children}</p></section>; }
function Callout({ title, tone, children }) { return <section className={`card callout ${tone}`}><h2>{title}</h2><p>{children}</p></section>; }
function fieldName(code) { return ({ RUC_RECORD: "rucRecord", PROJECT_CONTRACT: "projectContract", BANK_STATEMENTS: "bankStatements" })[code]; }
function progressIndex(status) { return ({ PRE_APPROVED: 0, MANUAL_REVIEW: 0, REJECTED: 0, FORMAL_REVIEW: 1, CREDIT_REJECTED: 1, CREDIT_APPROVED: 2, DELIVERY_SCHEDULED: 3 })[status] ?? 0; }
function statusTone(status) { return status === "DELIVERY_SCHEDULED" || status === "CREDIT_APPROVED" || status === "PRE_APPROVED" ? "success" : status === "REJECTED" || status === "CREDIT_REJECTED" ? "danger" : "warning"; }
function formatStatus(status) { return status.toLowerCase().split("_").map((word) => word[0].toUpperCase() + word.slice(1)).join(" "); }
function shortId(id) { return String(id).split("-")[0].toUpperCase(); }
function futureDate(days) { const date = new Date(); date.setDate(date.getDate() + days); return date.toISOString().slice(0, 10); }
