import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ReportView } from "@/components/report/ReportView";
import { getCompany, getOverview } from "@/lib/data";
import { mdToSafeHtml } from "@/lib/markdown";

export const dynamicParams = false;

export function generateStaticParams() {
  const ov = getOverview();
  return (ov.reports ?? ov.opportunities).map((ticker) => ({ ticker }));
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
  if (!doc || !doc.report || !(ov.reports ?? ov.opportunities).includes(doc.row.ticker)) notFound();
  const dropped = ov.opportunities_dropped?.find((d) => d.ticker === doc.row.ticker)?.reasons;
  const notesHtml = mdToSafeHtml(doc.notes_md);
  const { notes_md: _omit, review_md: _omit2, ...slim } = doc;
  void _omit;
  void _omit2;
  const rule = (ov as unknown as { opportunity_rule?: string }).opportunity_rule ?? "";
  return (
    <ReportView doc={slim} notesHtml={notesHtml} rank={ov.opportunities.indexOf(doc.row.ticker) + 1} total={ov.opportunities.length} rule={rule} dropped={dropped} />
  );
}
