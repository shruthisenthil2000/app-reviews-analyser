export const DELIVERY_EMAIL = "ar.shruthi17@gmail.com";
export const DELIVERY_SUBJECT = "Groww Weekly Review Pulse";

export const kpis = [
  {
    label: "Reviews Analysed",
    value: "2,110",
    change: "+12.4%",
    trend: "up" as const,
    icon: "reviews",
    detail: {
      description:
        "Total Play Store reviews ingested, deduped, and analysed in the rolling 12-week window.",
      metrics: [
        { label: "This week", value: "312" },
        { label: "Prior week", value: "278" },
        { label: "With text body", value: "1,847" },
        { label: "1★ share", value: "41%" },
      ],
    },
  },
  {
    label: "Average Rating",
    value: "3.2",
    change: "-0.3",
    trend: "down" as const,
    icon: "rating",
    detail: {
      description: "Weighted mean star rating across all reviews in the analysis window.",
      metrics: [
        { label: "5★ share", value: "38%" },
        { label: "1★ share", value: "41%" },
        { label: "WoW change", value: "-0.3" },
        { label: "Median rating", value: "3" },
      ],
    },
  },
  {
    label: "Sentiment Score",
    value: "42%",
    change: "-8%",
    trend: "down" as const,
    icon: "sentiment",
    detail: {
      description:
        "Share of reviews classified as positive by the sentiment model (non-neutral).",
      metrics: [
        { label: "Positive", value: "42%" },
        { label: "Negative", value: "51%" },
        { label: "Neutral", value: "7%" },
        { label: "WoW change", value: "-8%" },
      ],
    },
  },
  {
    label: "Theme Count",
    value: "5",
    change: "+0",
    trend: "up" as const,
    icon: "themes",
    detail: {
      description: "Top themes retained for pulse synthesis (max 5 per LIP spec).",
      metrics: [
        { label: "In pulse (top 3)", value: "3" },
        { label: "Critical severity", value: "2" },
        { label: "High severity", value: "2" },
        { label: "Medium severity", value: "1" },
      ],
    },
  },
];

export const ratingDistribution = [
  { star: "5★", count: 800, pct: 38 },
  { star: "4★", count: 200, pct: 9 },
  { star: "3★", count: 143, pct: 7 },
  { star: "2★", count: 114, pct: 5 },
  { star: "1★", count: 853, pct: 41 },
];

export const sentimentSplit = [
  { name: "Negative", value: 51, fill: "#f87171" },
  { name: "Positive", value: 42, fill: "#00d492" },
  { name: "Neutral", value: 7, fill: "#8b9a94" },
];

export const reviewVolumeTrend = [
  { week: "W17", reviews: 198 },
  { week: "W18", reviews: 245 },
  { week: "W19", reviews: 267 },
  { week: "W20", reviews: 278 },
  { week: "W21", reviews: 312 },
];

/** Max 5 themes — aligned with project Stage A outputs */
export const themes = [
  {
    title: "High Brokerage Charges",
    summary: "Charges exceed expectations on sell orders; users compare unfavourably vs discount brokers.",
    pct: 34,
    sentiment: "negative" as const,
    severity: "high" as const,
    trend: "+6%",
    trendDir: "up" as const,
    reviewCount: 718,
    insights: [
      "Sell-order charges cited most often in 1★ reviews.",
      "Users report cuts higher than stated (e.g. ₹30 vs ₹7–8 expected).",
      "Fee breakdown screen requested in related reviews.",
    ],
  },
  {
    title: "Poor Customer Support",
    summary: "Unresponsive agents; Demat and investment issues unresolved for days.",
    pct: 28,
    sentiment: "negative" as const,
    severity: "critical" as const,
    trend: "+11%",
    trendDir: "up" as const,
    reviewCount: 591,
    insights: [
      "Account setup delays exceed one week in complaints.",
      "Chat handoffs fail to reach humans for payout issues.",
      "Support SLAs mentioned as missing for money-movement tickets.",
    ],
  },
  {
    title: "Withdrawal Issues",
    summary: "Payouts pending beyond SLA; bank linking errors; +28% WoW complaint spike.",
    pct: 22,
    sentiment: "negative" as const,
    severity: "critical" as const,
    trend: "+28%",
    trendDir: "up" as const,
    reviewCount: 464,
    insights: [
      "Highest WoW mover this pulse.",
      "Withdrawals fail for days without response.",
      "Bank linking blocks first-time payouts.",
    ],
  },
  {
    title: "Technical Glitches",
    summary: "Crashes, login OTP failures, and order timeouts during peak trading.",
    pct: 18,
    sentiment: "negative" as const,
    severity: "critical" as const,
    trend: "+4%",
    trendDir: "up" as const,
    reviewCount: 380,
    insights: [
      "App crashes during market open sessions.",
      "Login OTP failures on Android 14.",
      "Order placement timeouts in high-volume windows.",
    ],
  },
  {
    title: "Order Execution Problems",
    summary: "Selling/buying charges confusion; orders stuck in processing.",
    pct: 14,
    sentiment: "negative" as const,
    severity: "high" as const,
    trend: "+3%",
    trendDir: "up" as const,
    reviewCount: 295,
    insights: [
      "Sell flow charges feel like a scam to some users.",
      "Investments stuck in processing for a week+.",
      "Execution reliability tied to retention risk.",
    ],
  },
];

export const quotes = [
  {
    text: "They cut more charges than what they said — I sell a stock and they cut ₹30 instead of ₹7–8.",
    author: "Play Store user",
    rating: 1,
  },
  {
    text: "Support never responds when withdrawals fail for days.",
    author: "Verified investor",
    rating: 2,
  },
  {
    text: "App crashes during trading sessions on market open.",
    author: "Active trader",
    rating: 1,
  },
];

export const actionIdeas = [
  {
    title: "Review brokerage and fee transparency in-app",
    body: "Show all-in cost preview before sell orders; align with competitor benchmarks.",
    priority: "P0",
  },
  {
    title: "Stabilize withdrawals and order execution",
    body: "Proactive payout status; escalation when processing exceeds 24h.",
    priority: "P0",
  },
  {
    title: "Improve support SLAs and escalation paths",
    body: "Tier-1 response under 4h for money-movement tickets.",
    priority: "P1",
  },
];

export const weeklyPulse = {
  week: "2026-W21",
  /** Executive note — under 250 words */
  body: `Groww Play Store pulse (${"2026-W21"}): sentiment skews negative. Support, fees, and reliability dominate.

TOP 3 THEMES
1. High brokerage charges — sell-side fees exceed expectations; transparency gaps drive 1★ reviews.
2. Poor customer support — slow or missing responses on Demat, investments, and payouts.
3. Withdrawal issues — delays and failures spiked +28% WoW; trust risk for money movement.

Also tracked: technical glitches (crashes at market open) and order execution problems (stuck sells, charge confusion).

USER QUOTES
• "They cut more charges than what they said — ₹30 instead of ₹7–8 on a sell."
• "Support never responds when withdrawals fail for days."
• "App crashes during trading sessions on market open."

ACTION IDEAS
1. Review brokerage and fee transparency in-app before order placement.
2. Stabilize withdrawals and order execution with proactive status updates.
3. Improve support SLAs and escalation paths for payout and trading tickets.`,
  topThemes: [
    "High brokerage charges",
    "Poor customer support",
    "Withdrawal issues",
  ],
  quotes: quotes.map((q) => q.text),
  actions: actionIdeas.map((a) => a.title),
};

export const pmPriorityRadar = [
  {
    id: "withdrawal",
    label: "Withdrawal failures",
    emoji: "🔥",
    quadrant: "high-impact",
    frequency: 88,
    impact: 92,
    severity: "critical" as const,
    explanation: "High frequency + high impact; +28% WoW spike on payouts.",
  },
  {
    id: "brokerage",
    label: "Brokerage confusion",
    emoji: "⚠️",
    quadrant: "high-impact",
    frequency: 76,
    impact: 85,
    severity: "high" as const,
    explanation: "Largest theme share; charge mismatch drives churn language.",
  },
  {
    id: "crash",
    label: "App crash during trading",
    emoji: "📉",
    quadrant: "high-frequency",
    frequency: 72,
    impact: 78,
    severity: "critical" as const,
    explanation: "Peak-hour crashes correlate with market open; retention risk.",
  },
  {
    id: "support",
    label: "Support non-response",
    emoji: "⚠️",
    quadrant: "high-frequency",
    frequency: 68,
    impact: 70,
    severity: "high" as const,
    explanation: "Amplifies withdrawal and fee pain when agents are unreachable.",
  },
  {
    id: "orders",
    label: "Order execution stuck",
    emoji: "📉",
    quadrant: "monitor",
    frequency: 54,
    impact: 65,
    severity: "high" as const,
    explanation: "Processing delays and sell-flow charge disputes rising.",
  },
];

export const trendingKeywords = [
  { word: "brokerage", weight: 92 },
  { word: "withdrawal", weight: 88 },
  { word: "support", weight: 84 },
  { word: "fees", weight: 80 },
  { word: "trading", weight: 72 },
  { word: "crash", weight: 68 },
  { word: "sell", weight: 64 },
  { word: "login", weight: 58 },
  { word: "delay", weight: 55 },
  { word: "charges", weight: 52 },
  { word: "demat", weight: 48 },
  { word: "order", weight: 45 },
];

export const trendAlert = {
  message: "Withdrawal complaints increased +28% this week.",
  severity: "warning" as const,
};

export const deliveryStatus = {
  gmail: "ready" as const,
  docs: "synced" as const,
  lastRun: "2 hours ago",
};

export function buildEmailBody(): string {
  return weeklyPulse.body;
}
