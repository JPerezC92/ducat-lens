import { useState } from "react";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  type SortingState,
  type ColumnDef,
} from "@tanstack/react-table";
import { ArrowUpDown, ArrowUp, ArrowDown } from "lucide-react";
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { RecommendationBadge } from "./RecommendationBadge";
import { cn } from "@/lib/utils";

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

interface ResultsTableProps {
  items: ItemResult[];
  totals: Totals;
}

const VERDICT_SORT_ORDER: Record<Verdict, number> = {
  "high-value sell": 0,
  "mid-value consider": 1,
  "low-value keep": 2,
};

const columns: ColumnDef<ItemResult>[] = [
  {
    id: "index",
    header: "#",
    cell: ({ row }) => (
      <span className="px-3 py-2.5 font-data text-sm text-text-muted tabular-nums">
        {row.index + 1}
      </span>
    ),
    enableSorting: false,
  },
  {
    accessorKey: "name",
    header: "ITEM NAME",
    sortingFn: "alphanumeric",
    cell: ({ getValue }) => (
      <span className="font-data text-sm text-text-primary">
        {getValue() as string}
      </span>
    ),
  },
  {
    accessorKey: "ducats",
    header: "DUCATS",
    sortingFn: "basic",
    cell: ({ getValue }) => (
      <span className="font-data text-sm text-token-gold tabular-nums">
        {getValue() as number}
      </span>
    ),
  },
  {
    accessorKey: "recommendation",
    header: "VERDICT",
    sortingFn: (rowA, rowB) => {
      const a = VERDICT_SORT_ORDER[rowA.original.recommendation] ?? 2;
      const b = VERDICT_SORT_ORDER[rowB.original.recommendation] ?? 2;
      return a - b;
    },
    cell: ({ getValue }) => (
      <RecommendationBadge verdict={getValue() as Verdict} />
    ),
  },
];

export function ResultsTable({ items, totals }: ResultsTableProps) {
  const [sorting, setSorting] = useState<SortingState>([
    { id: "ducats", desc: true },
  ]);

  const table = useReactTable({
    data: items,
    columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  const getSortIcon = (columnId: string) => {
    const sorted = sorting.find((s) => s.id === columnId);
    if (!sorted) return <ArrowUpDown size={12} className="text-text-muted" aria-hidden="true" />;
    if (sorted.desc) return <ArrowDown size={12} className="text-accent-blue" aria-hidden="true" />;
    return <ArrowUp size={12} className="text-accent-blue" aria-hidden="true" />;
  };

  const getAriaSortValue = (columnId: string): "ascending" | "descending" | "none" => {
    const sorted = sorting.find((s) => s.id === columnId);
    if (!sorted) return "none";
    return sorted.desc ? "descending" : "ascending";
  };

  const getRowClass = (recommendation: Verdict): string => {
    if (recommendation === "high-value sell") {
      return "border-b border-border/40 bg-status-success/5 hover:bg-status-success/10 transition-colors duration-[80ms]";
    }
    return "";
  };

  return (
    <div
      aria-label="Ducat analysis results"
      aria-busy="false"
      className="w-full rounded-sm border border-border bg-surface overflow-hidden animate-in fade-in duration-200"
    >
      {/* Desktop table */}
      <div className="hidden md:block">
        <Table>
          <TableHeader>
            <TableRow className="border-b border-border bg-bg hover:bg-bg">
              <TableHead
                scope="col"
                className="px-3 py-3 font-heading text-xs tracking-widest uppercase text-accent-blue text-left select-none"
              >
                #
              </TableHead>
              {table.getFlatHeaders().filter((h) => h.id !== "index").map((header) => {
                const canSort = header.column.getCanSort();
                const ariaSortVal = canSort ? getAriaSortValue(header.id) : undefined;
                return (
                  <TableHead
                    key={header.id}
                    scope="col"
                    aria-sort={ariaSortVal}
                    className={cn(
                      "px-3 py-3 font-heading text-xs tracking-widest uppercase text-accent-blue text-left select-none transition-colors duration-150",
                      canSort && "cursor-pointer hover:text-text-primary",
                      sorting.find((s) => s.id === header.id) && "text-text-primary"
                    )}
                    onClick={canSort ? header.column.getToggleSortingHandler() : undefined}
                    onKeyDown={
                      canSort
                        ? (e) => {
                            if (e.key === "Enter" || e.key === " ") {
                              e.preventDefault();
                              header.column.getToggleSortingHandler()?.(e);
                            }
                          }
                        : undefined
                    }
                    tabIndex={canSort ? 0 : undefined}
                    aria-label={canSort ? `Sort by ${header.id}` : undefined}
                  >
                    <span className="inline-flex items-center gap-1">
                      {header.id === "name"
                        ? "ITEM NAME"
                        : header.id === "ducats"
                        ? "DUCATS"
                        : header.id === "recommendation"
                        ? "VERDICT"
                        : header.id}
                      {canSort && getSortIcon(header.id)}
                    </span>
                  </TableHead>
                );
              })}
            </TableRow>
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows.map((row, rowIndex) => {
              const recommendation = row.original.recommendation;
              const isEven = rowIndex % 2 === 0;
              const rowClass = getRowClass(recommendation);
              const defaultRowClass = rowClass
                ? rowClass
                : isEven
                ? "border-b border-border/40 bg-bg hover:bg-surface transition-colors duration-[80ms]"
                : "border-b border-border/40 bg-surface-alt hover:bg-surface transition-colors duration-[80ms]";

              return (
                <TableRow key={row.id} className={defaultRowClass}>
                  <TableCell className="px-3 py-2.5 font-data text-sm text-text-muted tabular-nums">
                    {rowIndex + 1}
                  </TableCell>
                  <TableCell className="px-3 py-2.5 font-data text-sm text-text-primary">
                    {row.original.name}
                  </TableCell>
                  <TableCell className="px-3 py-2.5 font-data text-sm text-token-gold text-right tabular-nums">
                    {row.original.ducats}
                  </TableCell>
                  <TableCell className="px-3 py-2.5 text-center">
                    <RecommendationBadge verdict={recommendation} />
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>

      {/* Mobile card layout */}
      <div className="block md:hidden p-3 flex flex-col gap-2">
        {table.getRowModel().rows.map((row, rowIndex) => (
          <div
            key={row.id}
            className="mb-2 rounded-sm border border-border bg-surface p-3 flex flex-col gap-1.5"
          >
            <div className="flex items-center justify-between">
              <span className="font-heading text-xs tracking-widest uppercase text-accent-blue">
                ITEM NAME
              </span>
              <span className="font-data text-xs text-text-muted tabular-nums">
                #{rowIndex + 1}
              </span>
            </div>
            <span className="font-data text-sm text-text-primary">
              {row.original.name}
            </span>
            <div className="flex items-center justify-between mt-1">
              <span className="font-heading text-xs tracking-widest uppercase text-accent-blue">
                DUCATS
              </span>
              <span className="font-data text-sm text-token-gold tabular-nums">
                {row.original.ducats}
              </span>
            </div>
            <div className="flex items-center justify-between mt-1">
              <span className="font-heading text-xs tracking-widest uppercase text-accent-blue">
                VERDICT
              </span>
              <RecommendationBadge verdict={row.original.recommendation} />
            </div>
          </div>
        ))}
      </div>

      {/* Summary row */}
      <div className="border-t border-border px-3 py-2.5 bg-bg flex flex-wrap items-center gap-4 font-data text-xs text-text-muted tabular-nums">
        <span>
          <span className="text-text-secondary">ITEMS DETECTED:</span>{" "}
          {totals.items_detected}
        </span>
        <span>
          <span className="text-text-secondary">MATCHED:</span>{" "}
          {totals.items_matched}
        </span>
        <span>
          <span className="text-text-secondary">TOTAL DUCATS:</span>{" "}
          <span className="text-token-gold">{totals.ducats_sum}</span>
        </span>
      </div>
    </div>
  );
}
