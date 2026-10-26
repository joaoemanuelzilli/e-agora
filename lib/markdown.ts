import "server-only";
import { marked } from "marked";

/** Markdown do dossiê -> HTML seguro: escapa tags HTML e só permite links http(s). */
export function mdToSafeHtml(md: string | null | undefined): string {
  if (!md) return "";
  const escaped = md.replace(/</g, "&lt;");
  let html = marked.parse(escaped, { async: false, gfm: true }) as string;
  html = html.replace(/<a href="([^"]*)"/g, (_m, href: string) =>
    /^https?:\/\//i.test(href) ? `<a target="_blank" rel="noopener noreferrer" href="${href}"` : `<a href="#"`,
  );
  html = html.replace(/<img[^>]*>/g, "");
  return html;
}
