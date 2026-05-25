import { useState } from "react";
import { UploadZone } from "./UploadZone";
import { AnalysisStatus, type StatusState } from "./AnalysisStatus";
import { ResultsTable } from "./ResultsTable";

type Verdict = "high-value sell" | "mid-value consider" | "low-value keep";

interface ItemResult {
  name: string;
  ducats: number;
  recommendation: Verdict;
}

interface Totals {
  items_detected: number;
  items_matched: number;
  ducats_sum: number;
}

interface AnalyzeResult {
  items: ItemResult[];
  totals: Totals;
}

export default function DucatAnalyzer() {
  const [status, setStatus] = useState<StatusState>({ type: "idle" });
  const [result, setResult] = useState<AnalyzeResult | null>(null);

  const handleFile = async (file: File) => {
    setStatus({ type: "loading" });
    setResult(null);

    const apiUrl = import.meta.env.PUBLIC_API_URL ?? "http://localhost:8000";

    const form = new FormData();
    form.append("image", file);

    try {
      const res = await fetch(`${apiUrl}/analyze`, {
        method: "POST",
        body: form,
      });

      if (res.status === 422) {
        setStatus({ type: "empty" });
        return;
      }

      if (!res.ok) {
        let message = "could not reach lookup service";
        try {
          const body = (await res.json()) as { detail?: string };
          if (body.detail) message = body.detail;
        } catch {
          // use default message
        }
        setStatus({ type: "error", message });
        return;
      }

      const data = (await res.json()) as AnalyzeResult;

      if (!data.items || data.items.length === 0) {
        setStatus({ type: "empty" });
        return;
      }

      setResult(data);
      setStatus({ type: "success", itemCount: data.totals.items_matched });
    } catch {
      setStatus({
        type: "error",
        message: "could not reach lookup service",
      });
    }
  };

  const handleReset = () => {
    setStatus({ type: "idle" });
    setResult(null);
  };

  const isLoading = status.type === "loading";
  const showUploadZone = status.type !== "loading";
  const errorMessage =
    status.type === "error" ? status.message : null;

  return (
    <div
      role="region"
      aria-label="Ducat analyzer"
      className="w-full flex flex-col gap-4"
    >
      {showUploadZone && (
        <UploadZone
          onFile={handleFile}
          isLoading={isLoading}
          error={errorMessage}
        />
      )}

      <AnalysisStatus status={status} onReset={handleReset} />

      {result && (status.type === "success" || status.type === "idle") && (
        <ResultsTable items={result.items} totals={result.totals} />
      )}
    </div>
  );
}
