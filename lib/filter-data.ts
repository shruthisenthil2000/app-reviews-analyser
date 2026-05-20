import type { PlatformFilter, TimeRangeFilter } from "@/lib/types";
import {
  kpis,
  ratingDistribution,
  reviewVolumeTrend,
  sentimentSplit,
  themes,
} from "@/lib/mock-data";

const PLATFORM_SCALE: Record<PlatformFilter, number> = {
  all: 1,
  android: 0.82,
  ios: 0.38,
};

const TIME_SCALE: Record<TimeRangeFilter, number> = {
  today: 0.08,
  "7d": 0.22,
  "30d": 0.55,
  "12w": 1,
};

export function getFilterScale(platform: PlatformFilter, timeRange: TimeRangeFilter) {
  return PLATFORM_SCALE[platform] * TIME_SCALE[timeRange];
}

export function getFilteredKpis(platform: PlatformFilter, timeRange: TimeRangeFilter) {
  const scale = getFilterScale(platform, timeRange);
  const reviews = Math.round(2110 * scale);
  return kpis.map((k) => {
    if (k.label === "Reviews Analysed") {
      return { ...k, value: reviews.toLocaleString() };
    }
    return k;
  });
}

export function getFilteredRatingDistribution(
  platform: PlatformFilter,
  timeRange: TimeRangeFilter
) {
  const scale = getFilterScale(platform, timeRange);
  return ratingDistribution.map((r) => ({
    ...r,
    count: Math.round(r.count * scale),
  }));
}

export function getFilteredSentimentSplit(
  platform: PlatformFilter,
  timeRange: TimeRangeFilter
) {
  const shift = platform === "ios" ? -3 : platform === "android" ? 2 : 0;
  const timeShift = timeRange === "today" ? -2 : timeRange === "7d" ? -1 : 0;
  const neg = Math.min(60, Math.max(40, sentimentSplit[0].value + shift + timeShift));
  const pos = Math.max(30, 100 - neg - sentimentSplit[2].value);
  return [
    { ...sentimentSplit[0], value: neg },
    { ...sentimentSplit[1], value: pos },
    sentimentSplit[2],
  ];
}

export function getFilteredVolumeTrend(
  platform: PlatformFilter,
  timeRange: TimeRangeFilter
) {
  const scale = getFilterScale(platform, timeRange);
  const slice =
    timeRange === "today"
      ? 1
      : timeRange === "7d"
        ? 2
        : timeRange === "30d"
          ? 4
          : 5;
  return reviewVolumeTrend.slice(-slice).map((w) => ({
    ...w,
    reviews: Math.round(w.reviews * (platform === "ios" ? 0.4 : 1) * scale * 3),
  }));
}

export function getFilteredThemes(platform: PlatformFilter, timeRange: TimeRangeFilter) {
  const scale = getFilterScale(platform, timeRange);
  return themes.map((t) => ({
    ...t,
    reviewCount: Math.round(t.reviewCount * scale),
  }));
}
