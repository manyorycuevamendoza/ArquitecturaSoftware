const NEGATIVE_RUC = "20999999999";
const LOW_SCORE_RUC = "20666666666";

export class SimulatedNegativeRecordProvider {
  queryCount = 0;

  findByRuc(ruc, checkedAt) {
    this.queryCount += 1;
    return {
      source: "Simulated negative-record database",
      checkedAt,
      found: ruc === NEGATIVE_RUC,
      reference: ruc === NEGATIVE_RUC ? "NEG-POC-001" : null
    };
  }
}

export class SimulatedCreditBureauProvider {
  queryCount = 0;

  getBehaviorByRuc(ruc, checkedAt) {
    this.queryCount += 1;
    if (ruc === LOW_SCORE_RUC) {
      return {
        source: "Simulated Equifax-like credit bureau",
        checkedAt,
        score: 580,
        overdueDebt: 8500,
        latePaymentsLast12Months: 4
      };
    }
    return {
      source: "Simulated Equifax-like credit bureau",
      checkedAt,
      score: ruc === "20123456789" ? 780 : 700,
      overdueDebt: 0,
      latePaymentsLast12Months: 0
    };
  }
}

export const SIMULATED_RISK_EXAMPLES = {
  APPROVED_RUC: "20123456789",
  NEGATIVE_RECORD_RUC: NEGATIVE_RUC,
  LOW_SCORE_RUC
};
