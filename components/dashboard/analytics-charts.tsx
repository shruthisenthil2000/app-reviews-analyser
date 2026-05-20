"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

type RatingRow = { star: string; count: number; pct: number };
type SentimentRow = { name: string; value: number; fill: string };
type VolumeRow = { week: string; reviews: number };

export function RatingDistributionCard({ data }: { data: RatingRow[] }) {
  const chartData = [...data].reverse();

  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Rating Distribution</CardTitle>
        <CardDescription>1–5 star breakdown</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[220px] min-w-0 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} layout="vertical" margin={{ left: 4, right: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" horizontal={false} />
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
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Bar dataKey="count" fill="#00d492" radius={[0, 6, 6, 0]} maxBarSize={18} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}

export function SentimentSplitCard({ data }: { data: SentimentRow[] }) {
  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Sentiment Split</CardTitle>
        <CardDescription>Positive · negative · neutral</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[220px] min-w-0 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={80}
                paddingAngle={2}
                dataKey="value"
              >
                {data.map((entry) => (
                  <Cell key={entry.name} fill={entry.fill} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#141a18",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="mt-3 flex justify-center gap-4">
          {data.map((d) => (
            <div key={d.name} className="flex items-center gap-1.5 text-xs text-muted-foreground">
              <span className="size-2 rounded-full" style={{ background: d.fill }} />
              {d.name} {d.value}%
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export function ReviewVolumeTrendCard({ data }: { data: VolumeRow[] }) {
  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle>Review Volume Trend</CardTitle>
        <CardDescription>Weekly ingest volume</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="h-[220px] min-w-0 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 8, right: 8, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="week" tick={{ fill: "#8b9a94", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#8b9a94", fontSize: 11 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{
                  background: "#141a18",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: 8,
                  fontSize: 12,
                }}
              />
              <Line
                type="monotone"
                dataKey="reviews"
                stroke="#00d492"
                strokeWidth={2}
                dot={{ fill: "#00d492", r: 4 }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
