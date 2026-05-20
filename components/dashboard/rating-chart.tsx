"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { ratingDistribution } from "@/lib/mock-data";

export function RatingChart() {
  const data = [...ratingDistribution].reverse();

  return (
    <div>
      <div className="h-[220px] min-w-0 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 4, right: 16 }}>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="rgba(255,255,255,0.06)"
              horizontal={false}
            />
            <XAxis type="number" hide />
            <YAxis
              type="category"
              dataKey="star"
              width={36}
              tick={{ fill: "#8b9a94", fontSize: 12 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip
              cursor={{ fill: "rgba(0,212,146,0.08)" }}
              contentStyle={{
                background: "#141a18",
                border: "1px solid rgba(255,255,255,0.1)",
                borderRadius: "8px",
                fontSize: "12px",
              }}
              formatter={(value) => [`${value} reviews`, "Count"]}
            />
            <Bar
              dataKey="count"
              fill="#00d492"
              radius={[0, 6, 6, 0]}
              maxBarSize={18}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <div className="mt-3 flex justify-between text-xs text-muted-foreground">
        {ratingDistribution.map((r) => (
          <span key={r.star}>
            {r.star} · {r.pct}%
          </span>
        ))}
      </div>
    </div>
  );
}
