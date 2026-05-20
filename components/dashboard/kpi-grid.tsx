"use client";

import { Activity, Minus, Star, Tag, TrendingDown, TrendingUp, Zap } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { kpis as defaultKpis } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

type KpiItem = (typeof defaultKpis)[number];

const KPI_ICONS: Record<string, React.ElementType> = {
  reviews: Activity,
  rating: Star,
  sentiment: Zap,
  themes: Tag,
};

type KpiGridProps = {
  kpis?: KpiItem[];
  onSelectKpi: (label: string) => void;
};

export function KpiGrid({ kpis = defaultKpis, onSelectKpi }: KpiGridProps) {
  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {kpis.map((kpi) => {
        const Icon = KPI_ICONS[kpi.icon] ?? Activity;
        const TrendIcon =
          kpi.trend === "up" ? TrendingUp : kpi.trend === "down" ? TrendingDown : Minus;

        return (
          <Card
            key={kpi.label}
            role="button"
            tabIndex={0}
            onClick={() => onSelectKpi(kpi.label)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onSelectKpi(kpi.label);
              }
            }}
            className={cn(
              "glass-card cursor-pointer transition duration-300",
              "hover:-translate-y-1 hover:border-primary/25 hover:shadow-[0_12px_40px_rgba(0,212,146,0.12)]",
              "active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50"
            )}
          >
            <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
              <div className="rounded-lg bg-primary/10 p-2 text-primary transition group-hover:bg-primary/20">
                <Icon className="size-4" />
              </div>
              <Badge
                variant={kpi.trend === "down" ? "destructive" : "secondary"}
                className="gap-1 font-mono text-[10px]"
              >
                <TrendIcon className="size-3" />
                {kpi.change}
              </Badge>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-semibold tracking-tight">{kpi.value}</p>
              <p className="text-xs text-muted-foreground">{kpi.label}</p>
              <p className="mt-2 text-[10px] text-primary/80">Click for details</p>
            </CardContent>
          </Card>
        );
      })}
    </section>
  );
}
