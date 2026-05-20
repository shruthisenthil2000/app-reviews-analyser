"use client";

import { FileText, Loader2, Mail } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  buildEmailBody,
  DELIVERY_EMAIL,
  DELIVERY_SUBJECT,
} from "@/lib/mock-data";
import type { DeliveryState } from "@/lib/types";

type DeliveryPanelProps = {
  gmailStatus: DeliveryState;
  docsStatus: DeliveryState;
  pdfStatus: DeliveryState;
  lastRun: string;
  onDraftEmail: () => void;
  onAppendDoc: () => void;
  onExportPdf: () => void;
};

function StatusBadge({
  label,
  status,
}: {
  label: string;
  status: DeliveryState;
}) {
  const text =
    status === "pending" ? "pending" : status === "success" ? "success" : "ready";
  return (
    <Badge
      variant={
        status === "success" ? "default" : status === "pending" ? "secondary" : "outline"
      }
      className="capitalize"
    >
      {label} · {text}
    </Badge>
  );
}

export function DeliveryPanel({
  gmailStatus,
  docsStatus,
  pdfStatus,
  lastRun,
  onDraftEmail,
  onAppendDoc,
  onExportPdf,
}: DeliveryPanelProps) {
  const body = buildEmailBody();

  return (
    <div className="space-y-6">
      <section className="rounded-xl border border-white/[0.08] bg-surface-elevated/50 p-6">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="text-lg font-semibold">Delivery</h2>
            <p className="text-sm text-muted-foreground">Last pipeline run · {lastRun}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <StatusBadge label="Gmail" status={gmailStatus} />
            <StatusBadge label="Docs" status={docsStatus} />
            <StatusBadge label="PDF" status={pdfStatus} />
          </div>
        </div>

        <Card className="glass-card mb-6 overflow-hidden">
          <div className="border-b border-white/[0.06] bg-white/[0.02] px-5 py-3">
            <p className="text-xs font-medium uppercase tracking-wider text-primary">
              Email draft preview
            </p>
          </div>
          <CardContent className="space-y-3 p-5 text-sm">
            <p>
              <span className="text-muted-foreground">To: </span>
              <span>{DELIVERY_EMAIL}</span>
            </p>
            <p>
              <span className="text-muted-foreground">Subject: </span>
              <span>{DELIVERY_SUBJECT}</span>
            </p>
            <div className="mt-4 rounded-lg border border-white/[0.06] bg-black/30 p-4">
              <pre className="whitespace-pre-wrap font-sans text-xs leading-relaxed text-muted-foreground">
                {body}
              </pre>
            </div>
          </CardContent>
        </Card>

        <div className="flex flex-wrap justify-center gap-4">
          <Button
            size="lg"
            className="gap-2 px-8 shadow-[0_0_32px_rgba(0,212,146,0.2)]"
            disabled={gmailStatus === "pending"}
            onClick={onDraftEmail}
          >
            {gmailStatus === "pending" ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Mail className="size-4" />
            )}
            {gmailStatus === "pending" ? "Drafting…" : "Draft Email"}
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="gap-2 px-8"
            disabled={docsStatus === "pending"}
            onClick={onAppendDoc}
          >
            {docsStatus === "pending" ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <FileText className="size-4" />
            )}
            {docsStatus === "pending" ? "Appending…" : "Append to Docs"}
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="gap-2 px-8"
            disabled={pdfStatus === "pending"}
            onClick={onExportPdf}
          >
            {pdfStatus === "pending" ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <FileText className="size-4" />
            )}
            {pdfStatus === "pending" ? "Exporting…" : "Export PDF"}
          </Button>
        </div>
      </section>
    </div>
  );
}
