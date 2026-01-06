export const formatMadagascarPhone = (raw: string): string => {
  const digitsOnly = raw.replace(/\D/g, "");
  if (!digitsOnly) return "";

  let local = digitsOnly;
  if (local.startsWith("261")) {
    local = local.slice(3);
  }
  if (local.startsWith("0")) {
    local = local.slice(1);
  }

  local = local.slice(0, 9); // keep at most 9 digits for local part
  if (local && local[0] !== "3") {
    local = `3${local.slice(1)}`;
  }

  const groups = [2, 2, 3, 2];
  const parts: string[] = [];
  let index = 0;
  groups.forEach((len) => {
    if (index >= local.length) return;
    parts.push(local.slice(index, index + len));
    index += len;
  });

  const formatted = parts.join(" ");
  return `+261${formatted ? ` ${formatted}` : ""}`;
};
