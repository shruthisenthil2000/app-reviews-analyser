"use client";

import { CheckCircle2, X } from "lucide-react";
import type { ToastMessage } from "@/lib/types";
import { cn } from "@/lib/utils";

type ToastStackProps = {
  toasts: ToastMessage[];
  onDismiss: (id: number) => void;
};

export function ToastStack({ toasts, onDismiss }: ToastStackProps) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed bottom-6 right-6 z-[60] flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          role="status"
          className={cn(
            "flex max-w-sm items-start gap-3 rounded-lg border px-4 py-3 text-sm shadow-lg",
            toast.variant === "success"
              ? "border-primary/30 bg-[#141a18]"
              : "border-white/10 bg-[#141a18]"
          )}
        >
          {toast.variant === "success" && (
            <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-primary" />
          )}
          <div className="flex-1">
            <p className="font-medium">{toast.title}</p>
            {toast.description && (
              <p className="mt-0.5 text-xs text-muted-foreground">{toast.description}</p>
            )}
          </div>
          <button
            type="button"
            onClick={() => onDismiss(toast.id)}
            className="text-muted-foreground hover:text-foreground"
            aria-label="Dismiss"
          >
            <X className="size-4" />
          </button>
        </div>
      ))}
    </div>
  );
}

