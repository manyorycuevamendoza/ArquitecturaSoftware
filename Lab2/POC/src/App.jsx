import React, { useMemo, useState } from "react";
import { LeaseApplicationService } from "./application/leaseApplicationService.js";
import { InMemoryLeaseApplicationRepository } from "./adapters/inMemoryLeaseApplicationRepository.js";

const SAMPLE = { companyName: "Constructora Andina SAC", ruc: "20123456789", machinery: "Hydraulic excavator", equipmentValue: 450000, initialPaymentPercent: 20, termMonths: 36, monthsOperating: 48, expectedMonthlyProjectCashFlow: 18000 };
const money = new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN", minimumFractionDigits: 2 });

export default function App() {
  const service = useMemo(() => new LeaseApplicationService(new InMemoryLeaseApplicationRepository(), { now: () => new Date().toISOString(), generateId: () => crypto.randomUUID() }), []);
  const [application, setApplication] = useState(null);
  const [error, setError] = useState("");
  const [acknowledged, setAcknowledged] = useState(false);

  function submit(event) {
    event.preventDefault();
    setError("");
    try {
      setApplication(service.submit(Object.fromEntries(new FormData(event.currentTarget)), crypto.randomUUID()));
    } catch (submissionError) {
      setError(submissionError.message);
      setApplication(null);
    }
  }

  function acceptQuote() {
    setError("");
    try { setApplication(service.acceptQuote(application.id, acknowledged)); }
    catch (acceptanceError) { setError(acceptanceError.message); }
  }

  return <>
    <header className="topbar"><div><span className="brand">LeaseNow Peru</span><span className="badge">React POC — preliminary quote only</span></div><span>Applicant view</span></header>
    <main>
      <section className="intro"><p className="eyebrow">Machinery leasing</p><h1>Check a project&apos;s preliminary leasing eligibility</h1><p>Receive an explainable estimate without consuming the project&apos;s working capital.</p></section>
      <section className="card"><form onSubmit={submit}><div className="grid">
        <Field label="Company name" name="companyName" defaultValue={SAMPLE.companyName} />
        <Field label="RUC" name="ruc" defaultValue={SAMPLE.ruc} maxLength="11" />
        <Field label="Required machinery" name="machinery" defaultValue={SAMPLE.machinery} wide />
        <Field label="Equipment value (S/)" name="equipmentValue" type="number" defaultValue={SAMPLE.equipmentValue} />
        <Field label="Initial payment (%)" name="initialPaymentPercent" type="number" defaultValue={SAMPLE.initialPaymentPercent} />
        <Field label="Requested term (months)" name="termMonths" type="number" defaultValue={SAMPLE.termMonths} />
        <Field label="Operating history (months)" name="monthsOperating" type="number" defaultValue={SAMPLE.monthsOperating} />
        <Field label="Expected monthly project cash flow (S/)" name="expectedMonthlyProjectCashFlow" type="number" defaultValue={SAMPLE.expectedMonthlyProjectCashFlow} wide />
      </div><button type="submit">Calculate preliminary quote</button></form></section>
      {error && <p className="error card" role="alert">{error}</p>}
      {application && <Result application={application} acknowledged={acknowledged} onAcknowledged={setAcknowledged} onAccept={acceptQuote} />}
    </main>
  </>;
}

function Field({ label, wide = false, ...inputProps }) {
  return <label className={wide ? "wide" : ""}>{label}<input required min={inputProps.type === "number" ? "0" : undefined} step={inputProps.type === "number" ? "0.01" : undefined} {...inputProps} /></label>;
}

function Result({ application, acknowledged, onAcknowledged, onAccept }) {
  if (application.status === "FORMAL_REVIEW") return <section className="card result"><p className="eyebrow">Application {application.id}</p><h2>Quote accepted</h2><p>Your request is now in <strong>{formatStatus(application.status)}</strong>.</p><p><strong>Owner:</strong> {application.ownerRole}</p><p><strong>Next step:</strong> {application.nextAction}</p><p className="disclaimer">No contract has been signed and no final credit approval has been issued.</p></section>;
  return <section className="card result" aria-live="polite">
    <div className="result-header"><div><p className="eyebrow">Preliminary decision</p><h2>{formatStatus(application.status)}</h2></div><span className={`status ${application.status === "PRE_APPROVED" ? "success" : "warning"}`}>{formatStatus(application.status)}</span></div>
    {application.quote && <Quote quote={application.quote} />}
    <h3>Eligibility checks</h3><ul className="checks">{application.ruleResults.map((item) => <li key={item.code} className={item.passed ? "passed" : "failed"}>{item.passed ? "✓" : "!"} {item.message}</li>)}</ul>
    <p><strong>Next step:</strong> {application.nextAction}</p>
    {application.status === "PRE_APPROVED" && <><label className="acknowledgement"><input type="checkbox" checked={acknowledged} onChange={(event) => onAcknowledged(event.target.checked)} />I understand this quote is preliminary, non-binding and subject to formal review.</label><button type="button" onClick={onAccept}>Accept preliminary quote</button></>}
    <p className="disclaimer">Policy {application.policyVersion}. This result is not final credit approval.</p>
  </section>;
}

function Quote({ quote }) { return <div className="quote-grid"><Metric label="Equipment value" value={money.format(quote.equipmentValue)} /><Metric label="Initial payment" value={money.format(quote.initialPayment)} /><Metric label="Financed amount" value={money.format(quote.financedAmount)} /><Metric label="Estimated installment" value={money.format(quote.estimatedMonthlyInstallment)} /></div>; }
function Metric({ label, value }) { return <div><span>{label}</span><strong>{value}</strong></div>; }
function formatStatus(status) { return status.toLowerCase().split("_").map((word) => word[0].toUpperCase() + word.slice(1)).join(" "); }
