"use client";

import { trendingKeywords } from "@/lib/mock-data";
import { cn } from "@/lib/utils";

type WordCloudProps = {
  selectedWord: string | null;
  onSelectWord: (word: string | null) => void;
};

export function WordCloud({ selectedWord, onSelectWord }: WordCloudProps) {
  const max = Math.max(...trendingKeywords.map((k) => k.weight));

  return (
    <div className="glass-card rounded-xl border border-white/[0.08] p-5">
      <h3 className="mb-1 text-sm font-semibold">Trending Keywords</h3>
      <p className="mb-4 text-xs text-muted-foreground">
        Click a keyword to highlight related themes
      </p>
      <div className="flex flex-wrap items-center justify-center gap-2">
        {trendingKeywords.map(({ word, weight }) => {
          const scale = 0.75 + (weight / max) * 0.65;
          const active = selectedWord === word;
          return (
            <button
              key={word}
              type="button"
              onClick={() => onSelectWord(active ? null : word)}
              className={cn(
                "rounded-full border px-3 py-1 font-medium transition-all hover:scale-105",
                active
                  ? "border-primary bg-primary/20 text-primary"
                  : "border-white/[0.08] bg-white/[0.03] text-muted-foreground hover:border-primary/30 hover:text-foreground"
              )}
              style={{ fontSize: `${scale}rem` }}
            >
              {word}
            </button>
          );
        })}
      </div>
      {selectedWord && (
        <p className="mt-4 text-center text-xs text-primary">
          Filtering insights for: <strong>{selectedWord}</strong>
        </p>
      )}
    </div>
  );
}
