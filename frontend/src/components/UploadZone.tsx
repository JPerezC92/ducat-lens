import { useCallback, useRef, useState } from "react";
import { useDropzone, type FileRejection } from "react-dropzone";
import { Upload, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface UploadZoneProps {
  onFile: (file: File) => void;
  isLoading: boolean;
  error?: string | null;
}

const MAX_SIZE_BYTES = 10 * 1024 * 1024; // 10 MB

export function UploadZone({ onFile, isLoading, error }: UploadZoneProps) {
  const [pendingFile, setPendingFile] = useState<File | null>(null);
  const [rejectReason, setRejectReason] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const onDrop = useCallback(
    (acceptedFiles: File[], rejectedFiles: FileRejection[]) => {
      setRejectReason(null);
      if (rejectedFiles.length > 0) {
        const code = rejectedFiles[0]?.errors[0]?.code;
        if (code === "file-too-large") {
          setRejectReason("FILE TOO LARGE: maximum 10 MB");
        } else {
          setRejectReason("UNSUPPORTED FORMAT: use PNG, JPG, or WebP");
        }
        setPendingFile(null);
        return;
      }
      if (acceptedFiles.length > 0) {
        setPendingFile(acceptedFiles[0]);
      }
    },
    []
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "image/png": [".png"],
      "image/jpeg": [".jpg", ".jpeg"],
      "image/webp": [".webp"],
    },
    multiple: false,
    maxSize: MAX_SIZE_BYTES,
    disabled: isLoading,
  });

  const handleAnalyze = () => {
    if (pendingFile) {
      onFile(pendingFile);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInputRef.current?.click();
    }
    if (e.key === "Escape" && isDragActive) {
      e.preventDefault();
    }
  };

  const rootProps = getRootProps({
    onKeyDown: handleKeyDown,
  });

  const getZoneClasses = () => {
    if (isLoading) {
      return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-accent-blue/20 bg-surface p-6 cursor-not-allowed transition-all duration-150 ease-out bracket-corners";
    }
    if (error) {
      return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-status-error bg-surface p-6 cursor-pointer transition-all duration-150 ease-out bracket-corners focus-visible:ring-2 ring-accent-blue/50 outline-none";
    }
    if (rejectReason) {
      return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-status-error bg-surface p-6 cursor-pointer transition-all duration-150 ease-out bracket-corners focus-visible:ring-2 ring-accent-blue/50 outline-none";
    }
    if (pendingFile) {
      return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-status-success bg-surface p-6 cursor-pointer transition-all duration-150 ease-out bracket-corners focus-visible:ring-2 ring-accent-blue/50 outline-none";
    }
    if (isDragActive) {
      return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-accent-blue bg-surface-alt p-6 cursor-pointer transition-all duration-150 ease-out bracket-corners focus-visible:ring-2 ring-accent-blue/50 outline-none [box-shadow:0_0_12px_rgba(63,200,224,0.35)]";
    }
    return "relative w-full min-h-[160px] flex flex-col items-center justify-center gap-3 rounded-sm border border-accent-blue/40 bg-surface p-6 cursor-pointer transition-all duration-150 ease-out bracket-corners hover:[box-shadow:0_0_12px_rgba(63,200,224,0.35)] hover:border-accent-blue focus-visible:ring-2 ring-accent-blue/50 outline-none";
  };

  const getIconAndText = () => {
    if (isLoading) {
      return {
        icon: <Loader2 size={24} className="text-text-muted animate-spin" aria-hidden="true" />,
        primary: <span className="font-heading text-sm tracking-widest uppercase text-text-muted">ANALYZING SCREENSHOT...</span>,
        secondary: null,
      };
    }
    if (pendingFile) {
      return {
        icon: <CheckCircle size={24} className="text-status-success" aria-hidden="true" />,
        primary: <span className="font-heading text-sm tracking-widest uppercase text-status-success">{pendingFile.name}</span>,
        secondary: <span className="font-body text-xs text-text-secondary">File ready. Click ANALYZE to process.</span>,
      };
    }
    if (rejectReason || error) {
      return {
        icon: <XCircle size={24} className="text-status-error" aria-hidden="true" />,
        primary: <span className="font-heading text-sm tracking-widest uppercase text-status-error">DROP SCREENSHOT OR CLICK TO BROWSE</span>,
        secondary: <span className="font-body text-xs text-text-secondary">PNG, JPG, WebP. Max 10 MB. Kiosk inventory screen only.</span>,
      };
    }
    return {
      icon: <Upload size={24} className="text-accent-blue" aria-hidden="true" />,
      primary: <span className="font-heading text-sm tracking-widest uppercase text-text-primary">DROP SCREENSHOT OR CLICK TO BROWSE</span>,
      secondary: <span className="font-body text-xs text-text-secondary">PNG, JPG, WebP. Max 10 MB. Kiosk inventory screen only.</span>,
    };
  };

  const { icon, primary, secondary } = getIconAndText();

  return (
    <div className="w-full flex flex-col gap-2">
      <div
        {...rootProps}
        role="button"
        tabIndex={0}
        aria-label="Upload Warframe Kiosk screenshot for ducat analysis"
        aria-disabled={isLoading}
        className={getZoneClasses()}
      >
        <input {...getInputProps()} ref={fileInputRef} />
        {icon}
        {primary}
        {secondary}
      </div>

      {rejectReason && !error && (
        <div
          role="alert"
          className="mt-1 flex items-center gap-1.5 text-xs text-status-error font-body"
        >
          <XCircle size={12} aria-hidden="true" />
          <span>{rejectReason}</span>
        </div>
      )}

      {pendingFile && !isLoading && (
        <Button
          type="button"
          onClick={handleAnalyze}
          className="w-full bg-accent-blue text-bg hover:bg-[#5cd5ea] font-heading text-sm tracking-widest uppercase rounded-sm transition-colors duration-150 ease-out min-h-[44px] focus-visible:ring-2 ring-accent-blue/50"
        >
          ANALYZE
        </Button>
      )}

      <div className="block md:hidden">
        {!pendingFile && !isLoading && (
          <Button
            type="button"
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
            className="w-full border-accent-blue/40 text-accent-blue font-heading text-xs tracking-widest uppercase rounded-sm min-h-[44px]"
          >
            BROWSE FILES
          </Button>
        )}
      </div>
    </div>
  );
}
