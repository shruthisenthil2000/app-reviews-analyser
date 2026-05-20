import { weeklyPulse } from "@/lib/mock-data";

export function buildPulseText(): string {
  return weeklyPulse.body;
}

export function downloadWeeklyPulse(): void {
  const content = buildPulseText();
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `groww-pulse-${weeklyPulse.week}.txt`;
  anchor.click();
  URL.revokeObjectURL(url);
}

export function exportPulsePdf(): void {
  const html = `<!DOCTYPE html><html><head><title>Groww Pulse ${weeklyPulse.week}</title>
<style>body{font-family:system-ui;max-width:640px;margin:2rem auto;padding:1rem;line-height:1.5}</style>
</head><body><pre>${weeklyPulse.body.replace(/</g, "&lt;")}</pre></body></html>`;
  const win = window.open("", "_blank");
  if (!win) return;
  win.document.write(html);
  win.document.close();
  win.focus();
  win.print();
}
