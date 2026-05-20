"use client";

import type { NavId } from "@/lib/types";
import { cn } from "@/lib/utils";
import {
  BarChart3,
  LayoutDashboard,
  Sparkles,
  Tag,
  Truck,
} from "lucide-react";

const TABS: { id: NavId; label: string; icon: React.ElementType }[] = [
  { id: "reviews", label: "Reviews", icon: LayoutDashboard },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
  { id: "themes", label: "Themes", icon: Tag },
  { id: "pulse", label: "Weekly Pulse", icon: Sparkles },
  { id: "delivery", label: "Delivery", icon: Truck },
];

type TopNavTabsProps = {
  activeNav: NavId;
  onChange: (id: NavId) => void;
};

export function TopNavTabs({ activeNav, onChange }: TopNavTabsProps) {
  return (
    <nav
      className="flex gap-1 overflow-x-auto border-b border-white/[0.06] pb-px"
      aria-label="Dashboard sections"
    >
      {TABS.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          type="button"
          onClick={() => onChange(id)}
          className={cn(
            "flex shrink-0 items-center gap-2 border-b-2 px-4 py-2.5 text-sm font-medium transition-all",
            activeNav === id
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:border-white/20 hover:text-foreground"
          )}
        >
          <Icon className="size-4" />
          {label}
        </button>
      ))}
    </nav>
  );
}
