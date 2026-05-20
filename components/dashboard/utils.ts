export function bucketStyles(bucket: string) {
  switch (bucket) {
    case "critical":
      return "border-red-500/30 bg-red-500/5";
    case "high":
      return "border-amber-500/30 bg-amber-500/5";
    case "growth":
      return "border-primary/30 bg-primary/5";
    default:
      return "border-white/10 bg-white/[0.02]";
  }
}
