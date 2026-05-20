"use client";

import type { PlatformFilter, TimeRangeFilter } from "@/lib/types";
import { cn } from "@/lib/utils";

const PLATFORMS: { id: PlatformFilter; label: string }[] = [
  { id: "all", label: "All" },
  { id: "android", label: "Android" },
  { id: "ios", label: "iOS" },
];

const TIME_RANGES: { id: TimeRangeFilter; label: string }[] = [
  { id: "today", label: "Today" },
  { id: "7d", label: "7 Days" },
  { id: "30d", label: "30 Days" },
  { id: "12w", label: "8–12 Weeks" },
];

type FiltersBarProps = {
  platform: PlatformFilter;
  timeRange: TimeRangeFilter;
  onPlatformChange: (p: PlatformFilter) => void;
  onTimeRangeChange: (t: TimeRangeFilter) => void;
};

function FilterPill({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "rounded-lg px-3 py-1.5 text-xs font-medium transition-all",
        active
          ? "bg-primary text-primary-foreground shadow-[0_0_16px_rgba(0,212,146,0.2)]"
          : "border border-white/[0.08] bg-white/[0.03] text-muted-foreground hover:border-primary/20 hover:text-foreground"
      )}
    >
      {children}
    </button>
  );
}

export function FiltersBar({
  platform,
  timeRange,
  onPlatformChange,
  onTimeRangeChange,
}: FiltersBarProps) {
  return (
    <div className="glass-card flex flex-col gap-4 rounded-xl border border-white/[0.08] p-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-wrap items-center gap-2">
        <span className="mr-1 text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Platform
        </span>
        {PLATFORMS.map((p) => (
          <FilterPill
            key={p.id}
            active={platform === p.id}
            onClick={() => onPlatformChange(p.id)}
          >
            {p.label}
          </FilterPill>
        ))}
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <span className="mr-1 text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Time range
        </span>
        {TIME_RANGES.map((t) => (
          <FilterPill
            key={t.id}
            active={timeRange === t.id}
            onClick={() => onTimeRangeChange(t.id)}
          >
            {t.label}
          </FilterPill>
        ))}
      </div>
    </div>
  );
}
