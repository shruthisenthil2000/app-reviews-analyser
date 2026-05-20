export type NavId = "reviews" | "analytics" | "themes" | "pulse" | "delivery";

export type PlatformFilter = "all" | "android" | "ios";

export type TimeRangeFilter = "today" | "7d" | "30d" | "12w";

export type DeliveryState = "idle" | "pending" | "success";

export type ToastMessage = {
  id: number;
  title: string;
  description?: string;
  variant?: "success" | "default";
};
