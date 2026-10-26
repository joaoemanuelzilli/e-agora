import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CompanyView } from "@/components/company/CompanyView";
import { getCompany, getOverview, tickers } from "@/lib/data";
import { mdToSafeHtml } from "@/lib/markdown";

export const dynamicParams = false;

export function generateStaticParams() {
  return tickers().map((ticker) => ({ ticker }));
}

export async function generateMetadata({ params }: { params: Promise<{ ticker: string }> }): Promise<Metadata> {
  const { ticker } = await params;
  const doc = getCompany(ticker);
  return { title: doc ? `${doc.row.ticker} ${doc.row.name}: valuation pós-eleição` : "Empresa" };
}

export default async function Page({ params }: { params: Promise<{ ticker: string }> }) {
  const { ticker } = await params;
  const doc = getCompany(ticker);
  if (!doc) notFound();
  const isOpp = getOverview().opportunities.includes(doc.row.ticker) || !!doc.report;
  const notesHtml = mdToSafeHtml(doc.notes_md);
  const reviewHtml = mdToSafeHtml(doc.review_md);
  const { notes_md: _omit, review_md: _omit2, ...slim } = doc;
  void _omit;
  void _omit2;
  return <CompanyView doc={slim} isOpp={isOpp} notesHtml={notesHtml} reviewHtml={reviewHtml} />;
}
