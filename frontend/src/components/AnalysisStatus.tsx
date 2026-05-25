import { useEffect, useRef, useState } from "react";
import { AlertTriangle, FileSearch, ScanLine } from "lucide-react";

export type StatusState =
  | { type: "idle" }
  | { type: "loading" }
  | { type: "success"; itemCount: number }
  | { type: "empty" }
  | { type: "error"; message: string };

interface AnalysisStatusProps {
  status: StatusState;
  onReset: () => void;
}

export function AnalysisStatus({ status, onReset }: AnalysisStatusProps) {
  const [successVisible, setSuccessVisible] = useState(false);
  const successTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    if (status.type === "success") {
      setSuccessVisible(true);
      successTimerRef.current = setTimeout(() => {
        setSuccessVisible(false);
      }, 3000);
    } else {
      setSuccessVisible(false);
      if (successTimerRef.current) {
        clearTimeout(successTimerRef.current);
      }
    }
    return () => {
      if (successTimerRef.current) {
        clearTimeout(successTimerRef.current);
      }
    };
  }, [status.type]);

  if (status.type === "idle") {
    return null;
  }

  if (status.type === "loading") {
    return (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        aria-busy="true"
        className="w-full"
      >
        <div
          className="h-0.5 w-full overflow-hidden bg-surface-alt rounded-none"
          role="progressbar"
          aria-label="Analyzing screenshot"
          aria-valuenow={50}
        >
          <div className="h-full bg-accent-blue animate-scan-sweep" />
        </div>
        <div className="mt-3 flex flex-col gap-2">
          {Array.from({ length: 8 }).map((_, i) => (
            <div
              key={i}
              className="h-10 w-full rounded-none bg-surface-alt animate-pulse border-b border-border/20"
            />
          ))}
        </div>
      </div>
    );
  }

  if (status.type === "success") {
    if (!successVisible) return null;
    return (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="w-full transition-opacity duration-500 ease-out mb-2 flex items-center gap-1.5 text-xs font-data text-status-success"
      >
        <ScanLine size={12} aria-hidden="true" />
        <span>ANALYSIS COMPLETE: {status.itemCount} ITEMS IDENTIFIED</span>
      </div>
    );
  }

  if (status.type === "empty") {
    return (
      <div
        role="status"
        aria-live="polite"
        aria-atomic="true"
        className="w-full flex flex-col items-center justify-center gap-3 py-12 border border-border/30 rounded-sm bg-surface"
      >
        <FileSearch size={32} className="text-text-muted" aria-hidden="true" />
        <p className="font-data text-sm uppercase tracking-widest text-text-muted">
          NO ITEMS IDENTIFIED
        </p>
        <p className="font-body text-xs text-text-muted max-w-[40ch] text-center">
          Ensure the Kiosk inventory panel is fully visible and unobscured in the screenshot.
        </p>
        <button
          type="button"
          onClick={onReset}
          className="text-accent-blue hover:underline text-xs font-data min-h-[44px] focus-visible:ring-2 ring-accent-blue/50 outline-none"
        >
          RETRY: upload a new screenshot
        </button>
      </div>
    );
  }

  if (status.type === "error") {
    return (
      <div
        role="alert"
        aria-live="assertive"
        aria-atomic="true"
        className="w-full mt-2 flex flex-col gap-2"
      >
        <div className="flex items-center gap-2 rounded-sm border border-status-error/30 bg-status-error/8 px-3 py-2.5 text-sm text-status-error font-body">
          <AlertTriangle size={16} className="shrink-0" aria-hidden="true" />
          <span>ANALYSIS FAILED: {status.message}</span>
        </div>
        <button
          type="button"
          onClick={onReset}
          className="text-accent-blue hover:underline text-xs font-data min-h-[44px] self-start focus-visible:ring-2 ring-accent-blue/50 outline-none"
        >
          RETRY: upload a new screenshot
        </button>
      </div>
    );
  }

  return null;
}
