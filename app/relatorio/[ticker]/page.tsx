import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ReportView } from "@/components/report/ReportView";
import { getCompany, getOverview } from "@/lib/data";
import { mdToSafeHtml } from "@/lib/markdown";

export const dynamicParams = false;

export function generateStaticParams() {
  return getOverview().opportunities.map((ticker) => ({ ticker }));
}

export async function generateMetadata({ params }: { params: Promise<{ ticker: string }> }): Promise<Metadata> {
  const { ticker } = await params;
  const doc = getCompany(ticker);
  return { title: doc ? `Relatório ${doc.row.ticker}: ${doc.report?.headline ?? doc.row.name}` : "Relatório" };
}

export default async function Page({ params }: { params: Promise<{ ticker: string }> }) {
  const { ticker } = await params;
  const ov = getOverview();
  const doc = getCompany(ticker);
  if (!doc || !ov.opportunities.includes(doc.row.ticker)) notFound();
  const notesHtml = mdToSafeHtml(doc.notes_md);
  const { notes_md: _omit, ...slim } = doc;
  void _omit;
  const rule = (ov as unknown as { opportunity_rule?: string }).opportunity_rule ?? "";
  return <ReportView doc={slim} notesHtml={notesHtml} rank={ov.opportunities.indexOf(doc.row.ticker) + 1} total={ov.opportunities.length} rule={rule} />;
}
