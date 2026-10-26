export type Template = "industrial" | "financial" | "holding";

export type Engine = {
  template: Template;
  ke_base?: number;
  g?: number;
  roe_T?: number;
  f26?: number;
  taus?: number[];
  tau_T?: number;
  div?: number[];
  ni_last?: number;
  eps?: number[];
  dps?: number[];
  n_sh?: number;
  per_unit?: number;
  values_share?: Record<string, number | null>;
  weights?: Record<string, number>;
  fcff?: number[];
  nopat_last?: number;
  roic_T?: number;
  kd?: number;
  wd?: number;
  nd_base?: number;
  minority_value?: number;
  eq_bridge_extra?: number;
  fair_value?: number | null;
  nav_mkt_share?: number | null;
};

export type Today = {
  chg: number | null;
  price: number | null;
  prev_close: number | null;
  expected_beta: number | null;
  residual: number | null;
  z_idio: number | null;
  xsec_predicted?: number | null;
  xsec_residual?: number | null;
};

export type Row = {
  ticker: string;
  name: string;
  group: string;
  sector: { setor?: string; subsetor?: string; segmento?: string };
  template: Template;
  has_model: boolean;
  has_research: boolean;
  price_ref: number | null;
  prev_close: number | null;
  chg_snapshot: number | null;
  fair_value: number | null;
  upside: number | null;
  irr_implied: number | null;
  irr_3y: number | null;
  dy: (number | null)[];
  roe_3y: (number | null)[] | null;
  pe_fwd: number | null;
  pe_ltm: number | null;
  pbv: number | null;
  ev_ebitda_fwd: number | null;
  ev_ebitda_ltm: number | null;
  prob_mc: number | null;
  mc_p10: number | null;
  mc_p90: number | null;
  mc_q?: number[] | null;
  mcap: number | null;
  adtv: number | null;
  beta: number | null;
  today: Today | null;
  mom_12_1: number | null;
  ret_12m_pre: number | null;
  vol_1y: number | null;
  max_dd_10y: number | null;
  price_pre_rally?: number | null;
  rally_to_2310?: number | null;
  now_vs_pre_rally?: number | null;
  piotroski: number | null;
  altman: { z: number; zone: string; x: number[] } | null;
  interest_cov: number | null;
  nd_ebitda: number | null;
  roe_avg_5y: number | null;
  summary: string | null;
  confidence: string | null;
  spark: number[];
  engine: Engine | null;
  per_unit: number;
  listed_classes?: { ticker: string; class: string }[] | null;
  scores?: Record<string, number | null>;
  score?: number | null;
  rank?: number;
};

export type Overview = {
  generated_at: string;
  ke: number;
  valuation_date: string;
  companies: Row[];
  opportunities: string[];
  market: MarketStats;
  xsec: XSec;
  sectors: Record<string, { setor?: string; subsetor?: string; segmento?: string }>;
  sector_stats: { setor: string; n: number; median: number; mean: number }[];
  macro: Record<string, { data: string; valor: string }[] | null>;
  coverage_rule: string;
};

export type XSec = {
  n: number;
  r2: number;
  r2_beta_only: number;
  coef: Record<string, number>;
  t: Record<string, number>;
  points: { ticker: string; actual: number; predicted: number; residual: number }[];
};

export type FwdStats = { n: number; mean: number | null; median: number | null; pct_pos: number | null; p10: number | null; p90: number | null };

export type MarketStats = {
  ibov_today: { price: number | null; chg: number | null; prev_close: number; rank_since_1998: number | null; pre_rally?: number; pre_rally_date?: string };
  ibov_daily_return_stats: { mean: number; std: number; n: number; z_today: number | null };
  worst_days: { date: string; ret: number; f1m: number | null; f3m: number | null; f6m: number | null; f12m: number | null }[];
  crash_forward_stats: Record<"f1m" | "f3m" | "f6m" | "f12m", FwdStats>;
  crash_threshold: number;
  elections: { date: string; label: string; ret_d1: number; f1m: number | null; f3m: number | null; f6m: number | null; f12m: number | null }[];
  drawdowns_25: { peak: string; trough: string; depth: number; recovered: string; days_to_recover: number; fwd12m_from_trough: number | null }[];
  ibov_weekly: [string, number][];
  ibov_return_hist: { counts: number[]; edges: number[] };
  indices_last: Record<string, [string, number] | null>;
  crash_paths?: { date: string; ret: number; path: number[] }[];
  election_paths?: { date: string; label: string; path: number[] | null }[];
};

export type Quote = { price: number; chg: number | null; prevClose: number | null; ts: string | null; source: string };
