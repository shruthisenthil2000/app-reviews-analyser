"use client";

import { AlertTriangle, MessageSquareQuote, Star } from "lucide-react";
import {
  RatingDistributionCard,
  ReviewVolumeTrendCard,
  SentimentSplitCard,
} from "@/components/dashboard/analytics-charts";
import { DeliveryPanel } from "@/components/dashboard/delivery-panel";
import { FiltersBar } from "@/components/dashboard/filters-bar";
import { KpiGrid } from "@/components/dashboard/kpi-grid";
import { PmPriorityRadar } from "@/components/dashboard/pm-priority-radar";
import { ThemeCard } from "@/components/dashboard/theme-card";
import { WeeklyPulseNote } from "@/components/dashboard/weekly-pulse-note";
import { WordCloud } from "@/components/dashboard/word-cloud";
import { Card, CardContent } from "@/components/ui/card";
import {
  getFilteredKpis,
  getFilteredRatingDistribution,
  getFilteredSentimentSplit,
  getFilteredThemes,
  getFilteredVolumeTrend,
} from "@/lib/filter-data";
import { quotes, trendAlert } from "@/lib/mock-data";
import type {
  DeliveryState,
  NavId,
  PlatformFilter,
  TimeRangeFilter,
} from "@/lib/types";
import { cn } from "@/lib/utils";

export type { NavId, DeliveryState };

type TabContentProps = {
  activeNav: NavId;
  platform: PlatformFilter;
  timeRange: TimeRangeFilter;
  onPlatformChange: (p: PlatformFilter) => void;
  onTimeRangeChange: (t: TimeRangeFilter) => void;
  onSelectKpi: (label: string) => void;
  expandedTheme: string | null;
  onToggleTheme: (title: string) => void;
  selectedKeyword: string | null;
  onSelectKeyword: (word: string | null) => void;
  selectedRadarId: string | null;
  onSelectRadar: (id: string | null) => void;
  gmailStatus: DeliveryState;
  docsStatus: DeliveryState;
  pdfStatus: DeliveryState;
  onDraftEmail: () => void;
  onAppendDoc: () => void;
  onExportPdf: () => void;
  lastRun: string;
};

function TrendAlertBanner() {
  return (
    <div
      role="status"
      className="flex items-start gap-3 rounded-xl border border-amber-500/25 bg-amber-500/10 px-4 py-3 text-sm"
    >
      <AlertTriangle className="mt-0.5 size-4 shrink-0 text-amber-400" />
      <div>
        <p className="font-medium text-amber-100">Trend Alert</p>
        <p className="text-amber-200/80">{trendAlert.message}</p>
      </div>
    </div>
  );
}

function QuoteCard({ quote }: { quote: (typeof quotes)[0] }) {
  return (
    <Card className="glass-card relative overflow-hidden transition hover:border-primary/15">
      <CardContent className="pt-5">
        <p className="text-sm leading-relaxed">&ldquo;{quote.text}&rdquo;</p>
        <div className="mt-4 flex items-center justify-between">
          <p className="text-xs text-muted-foreground">{quote.author}</p>
          <div className="flex gap-0.5">
            {Array.from({ length: 5 }).map((_, i) => (
              <Star
                key={i}
                className={cn(
                  "size-3",
                  i < quote.rating ? "fill-amber-400 text-amber-400" : "text-white/10"
                )}
              />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export function TabContent(props: TabContentProps) {
  const {
    activeNav,
    platform,
    timeRange,
    onPlatformChange,
    onTimeRangeChange,
    onSelectKpi,
    expandedTheme,
    onToggleTheme,
    selectedKeyword,
    onSelectKeyword,
    selectedRadarId,
    onSelectRadar,
    gmailStatus,
    docsStatus,
    pdfStatus,
    onDraftEmail,
    onAppendDoc,
    onExportPdf,
    lastRun,
  } = props;

  const filteredKpis = getFilteredKpis(platform, timeRange);
  const filteredThemes = getFilteredThemes(platform, timeRange);
  const ratingData = getFilteredRatingDistribution(platform, timeRange);
  const sentimentData = getFilteredSentimentSplit(platform, timeRange);
  const volumeData = getFilteredVolumeTrend(platform, timeRange);

  const themeMatchesKeyword = (title: string) => {
    if (!selectedKeyword) return true;
    const k = selectedKeyword.toLowerCase();
    const t = title.toLowerCase();
    const map: Record<string, string[]> = {
      brokerage: ["brokerage", "charges", "fees"],
      withdrawal: ["withdrawal"],
      support: ["support", "customer"],
      fees: ["brokerage", "charges"],
      trading: ["technical", "order", "trading", "crash"],
      crash: ["technical", "glitch"],
      sell: ["order", "brokerage"],
      login: ["technical", "glitch"],
      delay: ["withdrawal"],
      charges: ["brokerage"],
      demat: ["support", "order"],
      order: ["order", "execution"],
    };
    const keys = map[k] ?? [k];
    return keys.some((part) => t.includes(part));
  };

  return (
    <div className="space-y-6">
      <FiltersBar
        platform={platform}
        timeRange={timeRange}
        onPlatformChange={onPlatformChange}
        onTimeRangeChange={onTimeRangeChange}
      />

      {activeNav === "reviews" && (
        <>
          <TrendAlertBanner />
          <KpiGrid kpis={filteredKpis} onSelectKpi={onSelectKpi} />
          <WordCloud selectedWord={selectedKeyword} onSelectWord={onSelectKeyword} />
          <PmPriorityRadar selectedId={selectedRadarId} onSelect={onSelectRadar} />
          <section>
            <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold">
              <MessageSquareQuote className="size-5 text-primary" />
              User Voices
            </h2>
            <div className="grid gap-4 md:grid-cols-3">
              {quotes.map((q) => (
                <QuoteCard key={q.text} quote={q} />
              ))}
            </div>
          </section>
        </>
      )}

      {activeNav === "analytics" && (
        <>
          <KpiGrid kpis={filteredKpis} onSelectKpi={onSelectKpi} />
          <div className="grid gap-6 lg:grid-cols-2">
            <RatingDistributionCard data={ratingData} />
            <SentimentSplitCard data={sentimentData} />
          </div>
          <ReviewVolumeTrendCard data={volumeData} />
          <PmPriorityRadar selectedId={selectedRadarId} onSelect={onSelectRadar} />
        </>
      )}

      {activeNav === "themes" && (
        <section>
          <div className="mb-4">
            <h2 className="text-lg font-semibold tracking-tight">Top Themes</h2>
            <p className="text-sm text-muted-foreground">
              Max 5 themes · click to expand insights
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
            {filteredThemes.map((theme) => (
              <ThemeCard
                key={theme.title}
                theme={theme}
                expanded={expandedTheme === theme.title}
                onToggle={() => onToggleTheme(theme.title)}
                dimmed={!themeMatchesKeyword(theme.title)}
              />
            ))}
          </div>
        </section>
      )}

      {activeNav === "pulse" && <WeeklyPulseNote />}

      {activeNav === "delivery" && (
        <DeliveryPanel
          gmailStatus={gmailStatus}
          docsStatus={docsStatus}
          pdfStatus={pdfStatus}
          lastRun={lastRun}
          onDraftEmail={onDraftEmail}
          onAppendDoc={onAppendDoc}
          onExportPdf={onExportPdf}
        />
      )}
    </div>
  );
}
