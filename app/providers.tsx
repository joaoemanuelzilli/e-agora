"use client";
import type { ReactNode } from "react";
import { KeProvider } from "@/lib/live";

export function Providers({ children }: { children: ReactNode }) {
  return <KeProvider>{children}</KeProvider>;
}
