interface StudentFormInfoItemProps {
  label: string;
  value?: string;
  selectValue?: string;
}

export const StudentFormInfoItem = ({
  label,
  value,
  selectValue
}: StudentFormInfoItemProps) => (
  <div className="space-y-1 rounded-md border border-dashed border-border/60 bg-background/50 p-3">
    <p className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
      {label}
    </p>
    <p className="text-sm font-semibold text-foreground">
      {selectValue ? selectValue : value ? value : "-"}
    </p>
  </div>
);
