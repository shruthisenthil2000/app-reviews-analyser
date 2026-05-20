"use client";

import { ChevronDown, ChevronUp, TrendingDown, TrendingUp } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export type ThemeItem = {
  title: string;
  summary: string;
  pct: number;
  sentiment: "negative" | "positive" | "mixed";
  severity: "critical" | "high" | "medium";
  trend: string;
  trendDir: "up" | "down";
  reviewCount: number;
  insights: string[];
};

function severityVariant(severity: string) {
  if (severity === "critical") return "destructive" as const;
  if (severity === "high") return "outline" as const;
  return "secondary" as const;
}

function severityLabel(severity: string) {
  return severity.charAt(0).toUpperCase() + severity.slice(1);
}

function sentimentLabel(s: ThemeItem["sentiment"]) {
  if (s === "negative") return "Negative";
  if (s === "positive") return "Positive";
  return "Mixed";
}

type ThemeCardProps = {
  theme: ThemeItem;
  expanded: boolean;
  onToggle: () => void;
  dimmed?: boolean;
};

export function ThemeCard({ theme, expanded, onToggle, dimmed }: ThemeCardProps) {
  const TrendIcon = theme.trendDir === "up" ? TrendingUp : TrendingDown;

  return (
    <Card
      className={cn(
        "glass-card cursor-pointer transition hover:-translate-y-0.5 hover:border-primary/15",
        expanded && "border-primary/25 ring-1 ring-primary/20",
        dimmed && "opacity-40"
      )}
      onClick={onToggle}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onToggle();
        }
      }}
      role="button"
      tabIndex={0}
      aria-expanded={expanded}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-sm leading-snug">{theme.title}</CardTitle>
          <div className="flex shrink-0 items-center gap-1">
            <Badge variant="outline" className="font-mono text-[10px]">
              {theme.pct}%
            </Badge>
            {expanded ? (
              <ChevronUp className="size-4 text-muted-foreground" />
            ) : (
              <ChevronDown className="size-4 text-muted-foreground" />
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        <p className="text-xs leading-relaxed text-muted-foreground">{theme.summary}</p>
        <div className="flex flex-wrap items-center gap-2">
          <Badge
            variant={theme.sentiment === "negative" ? "destructive" : "secondary"}
            className="text-[10px]"
          >
            {sentimentLabel(theme.sentiment)}
          </Badge>
          <span className="text-[10px] text-muted-foreground">{theme.reviewCount} reviews</span>
        </div>
        <div className="flex items-center justify-between">
          <Badge variant={severityVariant(theme.severity)}>{severityLabel(theme.severity)}</Badge>
          <span
            className={cn(
              "flex items-center gap-0.5 text-[10px] font-medium",
              theme.trendDir === "up" ? "text-red-400" : "text-primary"
            )}
          >
            <TrendIcon className="size-3" />
            {theme.trend}
          </span>
        </div>
        {expanded && (
          <div
            className="space-y-2 border-t border-white/[0.06] pt-3"
            onClick={(e) => e.stopPropagation()}
          >
            <p className="text-[10px] font-semibold uppercase tracking-wider text-primary">
              AI Insights · {theme.reviewCount} reviews
            </p>
            <ul className="space-y-1.5">
              {theme.insights.map((insight) => (
                <li key={insight} className="text-xs leading-relaxed text-muted-foreground">
                  • {insight}
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
