"use client";
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { isNum, mn, pct } from "@/lib/format";

function List({ items, tone = "accent" }: { items: string[]; tone?: "accent" | "neg" | "ink" }) {
  const dot = tone === "neg" ? "bg-[var(--div-neg)]" : tone === "ink" ? "bg-[var(--ink-2)]" : "bg-accent";
  return (
    <ul className="space-y-2 text-[13.5px] leading-snug">
      {items.map((t, i) => (
        <li key={i} className="flex gap-2.5">
          <span className={`mt-[7px] inline-block h-[5px] w-[5px] shrink-0 rounded-full ${dot}`} />
          <span>{t}</span>
        </li>
      ))}
    </ul>
  );
}

export function Thesis({ doc }: { doc: any }) {
  const rs = doc.research || {};
  const dp = rs.debt_profile || {};
  const rsn = rs.rate_sensitivity || {};
  const kd = (rs.key_data || []) as { label: string; value: string; context?: string }[];
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="panel p-4">
          <div className="h3 mb-2">Por que pode ser oportunidade</div>
          <List items={(rs.thesis || []) as string[]} />
        </div>
        <div className="panel p-4">
          <div className="h3 mb-2">Riscos</div>
          <List items={(rs.risks || []) as string[]} tone="neg" />
        </div>
        <div className="panel p-4">
          <div className="h3 mb-2">Catalisadores</div>
          <List items={(rs.catalysts || []) as string[]} tone="ink" />
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="panel p-4">
          <div className="h3">O que a eleição muda para a empresa</div>
          <p className="prose-report mt-2 text-[14.5px]">{rs.election_impact || "—"}</p>
        </div>
        <div className="panel p-4">
          <div className="h3">Dívida e juros</div>
          <div className="mt-2 grid grid-cols-2 gap-3 text-[12.5px] sm:grid-cols-3">
            <div>
              <div className="label">Dívida bruta</div>
              <div className="num font-semibold">{isNum(dp.gross_debt_mn) ? mn(dp.gross_debt_mn) : "—"}</div>
            </div>
            <div>
              <div className="label">Indexada ao CDI</div>
              <div className="num font-semibold">{isNum(dp.pct_floating_cdi) ? pct(dp.pct_floating_cdi, 0) : "—"}</div>
            </div>
            <div>
              <div className="label">Custo médio</div>
              <div className="font-semibold">{dp.avg_cost || "—"}</div>
            </div>
            <div>
              <div className="label">Prazo médio</div>
              <div className="num font-semibold">{isNum(dp.avg_maturity_years) && dp.avg_maturity_years > 0 ? `${dp.avg_maturity_years.toLocaleString("pt-BR")} anos` : "—"}</div>
            </div>
            <div>
              <div className="label">Vencimentos em 24 meses</div>
              <div className="num font-semibold">{isNum(dp.next_24m_maturities_mn) && dp.next_24m_maturities_mn > 0 ? mn(dp.next_24m_maturities_mn) : "—"}</div>
            </div>
            <div>
              <div className="label">Lucro a cada +100 bp de CDI</div>
              <div className="num font-semibold">{isNum(rsn.ni_impact_per_100bp_cdi_mn) ? mn(rsn.ni_impact_per_100bp_cdi_mn) : "—"}</div>
            </div>
          </div>
          {rsn.notes && <p className="mt-3 text-[12.5px] leading-relaxed text-ink-2">{rsn.notes}</p>}
        </div>
      </div>
      {kd.length > 0 && (
        <div className="panel overflow-x-auto p-4">
          <div className="h3">Dados-chave</div>
          <table className="data mt-2 text-[13px]">
            <tbody>
              {kd.map((k, i) => (
                <tr key={i}>
                  <td className="text-ink-2">{k.label}</td>
                  <td className="font-semibold">{k.value}</td>
                  <td className="whitespace-normal text-left text-[12.5px] text-muted">{k.context || ""}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function Sources({ doc, notesHtml }: { doc: any; notesHtml?: string }) {
  const rs = doc.research || {};
  const src = (rs.sources || []) as { title: string; url: string }[];
  const [open, setOpen] = useState(false);
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
      <div className="panel p-4 lg:col-span-5">
        <div className="h3">Fontes consultadas</div>
        <ul className="mt-2 space-y-1.5 text-[12.5px]">
          <li className="text-ink-2">CVM: DFP 2015–2025 e ITR 2022–2026 (demonstrações consolidadas), composição do capital</li>
          <li className="text-ink-2">B3: cotações ao vivo, série histórica COTAHIST, proventos e eventos societários</li>
          {src.map((s, i) => (
            <li key={i}>
              <a href={s.url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                {s.title}
              </a>
            </li>
          ))}
        </ul>
      </div>
      <div className="panel p-4 lg:col-span-7">
        <div className="flex items-center justify-between">
          <div className="h3">Dossiê do analista</div>
          <button type="button" onClick={() => setOpen((v) => !v)} className="no-print rounded border border-hairline px-2 py-0.5 text-[12px] text-ink-2 hover:bg-surface-2">
            {open ? "Recolher" : "Expandir"}
          </button>
        </div>
        {notesHtml ? (
          <div className={`dossier mt-3 ${open ? "" : "max-h-[260px] overflow-hidden [mask-image:linear-gradient(to_bottom,black_70%,transparent)]"}`} dangerouslySetInnerHTML={{ __html: notesHtml }} />
        ) : (
          <p className="mt-2 text-[12.5px] text-muted">Sem dossiê.</p>
        )}
      </div>
    </div>
  );
}
