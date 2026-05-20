"use client";

import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

type DetailModalProps = {
  open: boolean;
  title: string;
  description: string;
  metrics: { label: string; value: string }[];
  onClose: () => void;
};

export function DetailModal({
  open,
  title,
  description,
  metrics,
  onClose,
}: DetailModalProps) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <button
        type="button"
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        aria-label="Close dialog"
        onClick={onClose}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="detail-modal-title"
        className="relative z-10 w-full max-w-md rounded-xl border border-white/[0.1] bg-[#141a18] p-6 shadow-[0_24px_80px_rgba(0,0,0,0.5)]"
      >
        <div className="mb-4 flex items-start justify-between gap-4">
          <div>
            <h2 id="detail-modal-title" className="text-lg font-semibold">
              {title}
            </h2>
            <p className="mt-2 text-sm text-muted-foreground">{description}</p>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose} aria-label="Close">
            <X className="size-4" />
          </Button>
        </div>
        <dl className="grid gap-3">
          {metrics.map((m) => (
            <div
              key={m.label}
              className="flex items-center justify-between rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2"
            >
              <dt className="text-xs text-muted-foreground">{m.label}</dt>
              <dd className="text-sm font-medium">{m.value}</dd>
            </div>
          ))}
        </dl>
        <Button className="mt-6 w-full" onClick={onClose}>
          Close
        </Button>
      </div>
    </div>
  );
}
