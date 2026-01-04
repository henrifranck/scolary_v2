import { useMemo } from "react";
import { cn } from "@/lib/utils";

const PRESET_COLORS = [
  "#3b82f6",
  "#0ea5e9",
  "#14b8a6",
  "#22c55e",
  "#f59e0b",
  "#eab308",
  "#ef4444",
  "#a855f7",
  "#8b5cf6",
  "#64748b"
];

interface ColorPickerProps {
  id?: string;
  value: string;
  onChange: (value: string) => void;
  className?: string;
}

export const ColorPicker = ({
  id,
  value,
  onChange,
  className
}: ColorPickerProps) => {
  const swatches = useMemo(() => PRESET_COLORS, []);

  return (
    <div className={cn("flex flex-wrap items-center gap-2", className)}>
      <input
        id={id}
        type="color"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="h-9 w-12 cursor-pointer rounded border bg-transparent p-1"
      />
      <div className="flex flex-wrap gap-2">
        {swatches.map((color) => (
          <button
            key={color}
            type="button"
            className={cn(
              "h-8 w-8 rounded-full border",
              value === color ? "ring-2 ring-offset-1 ring-primary" : ""
            )}
            style={{ background: color }}
            onClick={() => onChange(color)}
            aria-label={`Select color ${color}`}
          />
        ))}
      </div>
    </div>
  );
};
