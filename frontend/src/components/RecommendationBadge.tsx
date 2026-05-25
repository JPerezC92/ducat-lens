import { cn } from "@/lib/utils";

type Verdict = "high-value sell" | "mid-value consider" | "low-value keep";

interface RecommendationBadgeProps {
  verdict: Verdict;
}

const VERDICT_CONFIG: Record<
  Verdict,
  { label: string; className: string }
> = {
  "high-value sell": {
    label: "SELL",
    className:
      "inline-flex items-center gap-1 rounded-[1px] border border-status-success/30 bg-status-success/12 px-2 py-0.5 font-heading text-xs tracking-widest uppercase text-status-success",
  },
  "mid-value consider": {
    label: "CONSIDER",
    className:
      "inline-flex items-center gap-1 rounded-[1px] border border-status-warning/30 bg-status-warning/12 px-2 py-0.5 font-heading text-xs tracking-widest uppercase text-status-warning",
  },
  "low-value keep": {
    label: "KEEP",
    className:
      "inline-flex items-center gap-1 rounded-[1px] border border-text-secondary/20 bg-text-secondary/10 px-2 py-0.5 font-heading text-xs tracking-widest uppercase text-text-secondary",
  },
};

export function RecommendationBadge({ verdict }: RecommendationBadgeProps) {
  const config = VERDICT_CONFIG[verdict];
  return (
    <span className={cn(config.className)}>
      {config.label}
    </span>
  );
}
