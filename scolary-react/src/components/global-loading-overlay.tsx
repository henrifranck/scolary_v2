import { useMemo } from "react";
import { useIsFetching, useIsMutating } from "@tanstack/react-query";

export const GlobalLoadingOverlay = () => {
  const fetchingCount = useIsFetching();
  const mutatingCount = useIsMutating();

  const isBusy = useMemo(
    () => fetchingCount > 0 || mutatingCount > 0,
    [fetchingCount, mutatingCount]
  );

  if (!isBusy) {
    return null;
  }

  return (
    <div className="pointer-events-none fixed inset-0 z-[9999] flex items-center justify-center bg-background/50 backdrop-blur-sm">
      <div className="pointer-events-auto flex items-center gap-3 rounded-lg bg-background/90 px-4 py-3 shadow-lg ring-1 ring-border">
        <div className="h-5 w-5 animate-spin rounded-full border-2 border-primary border-t-transparent" />
      </div>
    </div>
  );
};
