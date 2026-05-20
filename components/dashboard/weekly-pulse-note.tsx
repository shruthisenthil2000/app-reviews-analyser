"use client";

import { Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { weeklyPulse } from "@/lib/mock-data";

const WORD_COUNT = weeklyPulse.body.split(/\s+/).filter(Boolean).length;

export function WeeklyPulseNote() {
  return (
    <Card className="glass-card overflow-hidden border-primary/15">
      <CardHeader className="border-b border-white/[0.06] bg-white/[0.02]">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="size-5 text-primary" />
            Weekly Pulse Note
          </CardTitle>
          <div className="flex gap-2">
            <Badge variant="outline" className="font-mono text-[10px]">
              {weeklyPulse.week}
            </Badge>
            <Badge variant="secondary" className="text-[10px]">
              {WORD_COUNT} words
            </Badge>
          </div>
        </div>
        <p className="text-xs text-muted-foreground">
          Executive one-pager · LIP limit ≤250 words
        </p>
      </CardHeader>
      <CardContent className="p-6">
        <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-muted-foreground">
          {weeklyPulse.body}
        </pre>
      </CardContent>
    </Card>
  );
}
