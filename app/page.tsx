"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import {
  BarChart3,
  Bell,
  CheckCircle2,
  FileText,
  LayoutDashboard,
  Loader2,
  RefreshCw,
  Settings,
  Sparkles,
  Tag,
  Truck,
} from "lucide-react";
import { DetailModal } from "@/components/dashboard/detail-modal";
import { TabContent } from "@/components/dashboard/tab-content";
import { ToastStack } from "@/components/dashboard/toast-stack";
import { TopNavTabs } from "@/components/dashboard/top-nav-tabs";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { downloadWeeklyPulse, exportPulsePdf } from "@/lib/export-pulse";
import { getFilteredKpis } from "@/lib/filter-data";
import { deliveryStatus, kpis } from "@/lib/mock-data";
import type {
  DeliveryState,
  NavId,
  PlatformFilter,
  TimeRangeFilter,
  ToastMessage,
} from "@/lib/types";
import { cn } from "@/lib/utils";

const NAV = [
  { id: "reviews" as const, label: "Reviews", icon: LayoutDashboard },
  { id: "analytics" as const, label: "Analytics", icon: BarChart3 },
  { id: "themes" as const, label: "Themes", icon: Tag },
  { id: "pulse" as const, label: "Weekly Pulse", icon: Sparkles },
  { id: "delivery" as const, label: "Delivery", icon: Truck },
];

const NAV_DESCRIPTIONS: Record<NavId, string> = {
  reviews: "Review corpus overview, KPIs, word cloud, and PM radar",
  analytics: "Rating, sentiment, and volume charts",
  themes: "Top 5 themed insights — click to expand",
  pulse: "Executive weekly note (≤250 words)",
  delivery: "Email draft preview and export actions",
};

function simulateDelivery(
  setter: React.Dispatch<React.SetStateAction<DeliveryState>>,
  onDone: () => void
) {
  setter("pending");
  window.setTimeout(() => {
    setter("success");
    onDone();
  }, 1800);
}

export default function Home() {
  const [activeNav, setActiveNav] = useState<NavId>("reviews");
  const [platform, setPlatform] = useState<PlatformFilter>("all");
  const [timeRange, setTimeRange] = useState<TimeRangeFilter>("12w");
  const [selectedKpi, setSelectedKpi] = useState<string | null>(null);
  const [expandedTheme, setExpandedTheme] = useState<string | null>(null);
  const [selectedKeyword, setSelectedKeyword] = useState<string | null>(null);
  const [selectedRadarId, setSelectedRadarId] = useState<string | null>(null);

  const [syncing, setSyncing] = useState(false);
  const [syncSuccess, setSyncSuccess] = useState(false);
  const [gmailStatus, setGmailStatus] = useState<DeliveryState>("idle");
  const [docsStatus, setDocsStatus] = useState<DeliveryState>("idle");
  const [pdfStatus, setPdfStatus] = useState<DeliveryState>("idle");
  const [lastRun, setLastRun] = useState(deliveryStatus.lastRun);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);
  const toastId = useRef(0);

  const addToast = useCallback((title: string, description?: string) => {
    const id = ++toastId.current;
    setToasts((t) => [...t, { id, title, description, variant: "success" }]);
    window.setTimeout(() => {
      setToasts((t) => t.filter((x) => x.id !== id));
    }, 4500);
  }, []);

  useEffect(() => {
    if (!syncSuccess) return;
    const timer = window.setTimeout(() => setSyncSuccess(false), 5000);
    return () => window.clearTimeout(timer);
  }, [syncSuccess]);

  const handleSyncReviews = useCallback(() => {
    if (syncing) return;
    setSyncing(true);
    setSyncSuccess(false);
    window.setTimeout(() => {
      setSyncing(false);
      setSyncSuccess(true);
      setLastRun("Just now");
      addToast("Reviews synced", `Platform: ${platform} · Range: ${timeRange}`);
    }, 2000);
  }, [syncing, platform, timeRange, addToast]);

  const handleToggleTheme = useCallback((title: string) => {
    setExpandedTheme((prev) => (prev === title ? null : title));
  }, []);

  const filteredKpis = getFilteredKpis(platform, timeRange);
  const selectedKpiData = filteredKpis.find((k) => k.label === selectedKpi)
    ?? kpis.find((k) => k.label === selectedKpi);

  return (
    <div className="flex min-h-screen">
      <aside className="glass-sidebar fixed inset-y-0 left-0 z-30 hidden w-60 flex-col px-4 py-6 md:flex lg:static">
        <div className="mb-8 px-2">
          <p className="text-xs font-medium uppercase tracking-widest text-primary">
            Intelligence Pro
          </p>
          <p className="mt-0.5 text-sm text-muted-foreground">Review Analyst</p>
        </div>
        <nav className="flex flex-1 flex-col gap-1">
          {NAV.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              type="button"
              onClick={() => setActiveNav(id)}
              className={cn(
                "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all",
                activeNav === id
                  ? "bg-primary text-primary-foreground shadow-[0_0_24px_rgba(0,212,146,0.25)]"
                  : "text-muted-foreground hover:bg-white/[0.04] hover:text-foreground"
              )}
            >
              <Icon className="size-4 shrink-0" />
              {label}
            </button>
          ))}
        </nav>
        <SidebarFooter />
      </aside>

      <div className="flex min-h-screen w-full flex-1 flex-col md:pl-60 lg:pl-0">
        <nav className="flex gap-1 overflow-x-auto border-b border-white/[0.06] px-4 py-2 md:hidden">
          {NAV.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              type="button"
              onClick={() => setActiveNav(id)}
              className={cn(
                "flex shrink-0 items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium",
                activeNav === id
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground"
              )}
            >
              <Icon className="size-3.5" />
              {label}
            </button>
          ))}
        </nav>

        <header className="sticky top-0 z-20 border-b border-white/[0.06] bg-background/80 backdrop-blur-xl">
          <div className="px-4 py-4 sm:px-6 lg:px-8">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <div className="mb-1 flex flex-wrap items-center gap-2">
                  <h1 className="text-xl font-semibold tracking-tight sm:text-2xl">
                    Groww Review Intelligence
                  </h1>
                  <Badge variant="outline" className="text-[10px] uppercase tracking-wider">
                    AI-Powered
                  </Badge>
                  {syncSuccess && (
                    <Badge className="gap-1 bg-primary/20 text-primary">
                      <CheckCircle2 className="size-3" />
                      Synced
                    </Badge>
                  )}
                </div>
                <p className="text-sm text-muted-foreground">
                  AI-powered App Review Pulse Dashboard
                </p>
                <p className="mt-1 text-xs text-muted-foreground/80">
                  {NAV_DESCRIPTIONS[activeNav]}
                </p>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2"
                  disabled={syncing}
                  onClick={handleSyncReviews}
                >
                  {syncing ? (
                    <Loader2 className="size-3.5 animate-spin" />
                  ) : (
                    <RefreshCw className="size-3.5" />
                  )}
                  {syncing ? "Syncing…" : "Sync Reviews"}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="gap-2"
                  onClick={() => {
                    downloadWeeklyPulse();
                    addToast("Pulse exported", "Downloaded .txt weekly pulse");
                  }}
                >
                  <FileText className="size-3.5" />
                  Export Pulse
                </Button>
                <Button variant="ghost" size="icon" aria-label="Notifications">
  <Bell className="size-4" />
</Button>

<Button variant="ghost" size="icon" aria-label="Settings">
  <Settings className="size-4" />
</Button>
              </div>
            </div>
          </div>
          <div className="px-4 sm:px-6 lg:px-8">
            <TopNavTabs activeNav={activeNav} onChange={setActiveNav} />
          </div>
        </header>

        <main className="flex-1 p-4 sm:p-6 lg:p-8">
          <TabContent
            activeNav={activeNav}
            platform={platform}
            timeRange={timeRange}
            onPlatformChange={setPlatform}
            onTimeRangeChange={setTimeRange}
            onSelectKpi={setSelectedKpi}
            expandedTheme={expandedTheme}
            onToggleTheme={handleToggleTheme}
            selectedKeyword={selectedKeyword}
            onSelectKeyword={setSelectedKeyword}
            selectedRadarId={selectedRadarId}
            onSelectRadar={setSelectedRadarId}
            gmailStatus={gmailStatus}
            docsStatus={docsStatus}
            pdfStatus={pdfStatus}
            onDraftEmail={() =>
              simulateDelivery(setGmailStatus, () =>
                addToast("Gmail draft created", "Saved to drafts (simulated)")
              )
            }
            onAppendDoc={() =>
              simulateDelivery(setDocsStatus, () =>
                addToast("Appended to Google Doc", "Pulse section updated (simulated)")
              )
            }
            onExportPdf={() => {
              if (pdfStatus === "pending") return;
              setPdfStatus("pending");
              window.setTimeout(() => {
                exportPulsePdf();
                setPdfStatus("success");
                addToast("PDF export ready", "Print dialog opened — save as PDF");
              }, 1500);
            }}
            lastRun={lastRun}
          />
        </main>
      </div>

      <ToastStack toasts={toasts} onDismiss={(id) => setToasts((t) => t.filter((x) => x.id !== id))} />

      {syncSuccess && (
        <div
          role="status"
          className="fixed bottom-6 left-6 z-50 flex items-center gap-2 rounded-lg border border-primary/30 bg-[#141a18] px-4 py-3 text-sm shadow-lg md:left-auto md:right-6"
        >
          <CheckCircle2 className="size-4 text-primary" />
          <span>Reviews synced · {lastRun}</span>
        </div>
      )}

      {selectedKpiData?.detail && (
        <DetailModal
          open={!!selectedKpi}
          title={selectedKpiData.label}
          description={selectedKpiData.detail.description}
          metrics={selectedKpiData.detail.metrics}
          onClose={() => setSelectedKpi(null)}
        />
      )}
    </div>
  );
}

function SidebarFooter() {
  return (
    <div className="mt-auto flex items-center gap-3 rounded-xl border border-white/[0.06] bg-white/[0.03] p-3">
      <div className="flex size-9 items-center justify-center rounded-full bg-primary/20 text-sm font-semibold text-primary">
        AR
      </div>
      <div>
        <p className="text-sm font-medium">Alex Rivera</p>
        <Badge variant="secondary" className="mt-0.5 text-[10px]">
          Pro Plan
        </Badge>
      </div>
    </div>
  );
}
