import { apiRequest } from "./api-client";

export type PdfFileResponse = {
  path: string;
  filename: string;
  url: string;
};

export const printStudentsList = (idYear: string | number) =>
  apiRequest<PdfFileResponse>("/students/print-list", {
    query: { id_year: idYear }
  });

export type PrintCardsPayload = {
  mentionId: string | number;
  academicYearId?: string | number;
  side?: "heads" | "tails";
};

export const printStudentCards = (payload: PrintCardsPayload) =>
  apiRequest<PdfFileResponse>("/students/print-cards", {
    query: {
      id_mention: payload.mentionId,
      id_year: payload.academicYearId,
      side: payload.side ?? "heads"
    }
  });
