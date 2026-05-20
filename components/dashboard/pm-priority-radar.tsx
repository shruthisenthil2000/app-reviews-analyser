"use client";

import { pmPriorityRadar } from "@/lib/mock-data";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

const SEVERITY_STYLES = {
  critical: "border-red-500/40 bg-red-500/10 text-red-300",
  high: "border-amber-500/40 bg-amber-500/10 text-amber-200",
  medium: "border-primary/30 bg-primary/5 text-primary",
};

type PmPriorityRadarProps = {
  selectedId: string | null;
  onSelect: (id: string | null) => void;
};

export function PmPriorityRadar({ selectedId, onSelect }: PmPriorityRadarProps) {
  const highImpact = pmPriorityRadar.filter((i) => i.quadrant === "high-impact");
  const highFreq = pmPriorityRadar.filter((i) => i.quadrant === "high-frequency");
  const monitor = pmPriorityRadar.filter((i) => i.quadrant === "monitor");

  return (
    <section>
      <div className="mb-4">
        <h2 className="text-lg font-semibold tracking-tight">PM Priority Radar</h2>
        <p className="text-sm text-muted-foreground">
          High impact × high frequency — executive decision panel
        </p>
      </div>
      <div className="grid gap-4 lg:grid-cols-3">
        <RadarColumn
          title="HIGH IMPACT"
          subtitle="Fix first"
          items={highImpact}
          selectedId={selectedId}
          onSelect={onSelect}
        />
        <RadarColumn
          title="HIGH FREQUENCY"
          subtitle="Volume drivers"
          items={highFreq}
          selectedId={selectedId}
          onSelect={onSelect}
        />
        <RadarColumn
          title="MONITOR"
          subtitle="Watch closely"
          items={monitor}
          selectedId={selectedId}
          onSelect={onSelect}
        />
      </div>
    </section>
  );
}

function RadarColumn({
  title,
  subtitle,
  items,
  selectedId,
  onSelect,
}: {
  title: string;
  subtitle: string;
  items: (typeof pmPriorityRadar)[number][];
  selectedId: string | null;
  onSelect: (id: string | null) => void;
}) {
  return (
    <Card className="glass-card border border-white/[0.08]">
      <CardHeader className="pb-2">
        <CardTitle className="text-xs font-semibold tracking-wider text-primary">
          {title}
        </CardTitle>
        <p className="text-[10px] text-muted-foreground">{subtitle}</p>
      </CardHeader>
      <CardContent className="space-y-2">
        {items.map((item) => {
          const active = selectedId === item.id;
          return (
            <button
              key={item.id}
              type="button"
              onClick={() => onSelect(active ? null : item.id)}
              className={cn(
                "w-full rounded-lg border p-3 text-left transition-all",
                SEVERITY_STYLES[item.severity],
                active && "ring-2 ring-primary/50"
              )}
            >
              <div className="mb-1 flex items-center justify-between gap-2">
                <span className="text-sm font-medium">
                  {item.emoji} {item.label}
                </span>
                <Badge variant="outline" className="font-mono text-[10px]">
                  {item.impact}
                </Badge>
              </div>
              <p className="text-[11px] opacity-90">{item.explanation}</p>
            </button>
          );
        })}
      </CardContent>
    </Card>
  );
}
