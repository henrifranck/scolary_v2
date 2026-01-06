import { apiRequest } from "./api-client";

export type PdfFileResponse = {
  path: string;
  filename: string;
  url: string;
};

export type PdfListPayload = {
  idYear: string | number;
  semester: string | number;
  journeyId: string | number;
};

export const printStudentsList = (payload: PdfListPayload) =>
  apiRequest<PdfFileResponse>("/liste/list_registered/", {
    query: {
      id_year: payload.idYear,
      semester: payload.semester,
      id_journey: payload.journeyId
    }
  });

export const printStudentsListByGroup = (payload: PdfListPayload) =>
  apiRequest<PdfFileResponse>("/liste/list_by_group/", {
    query: {
      id_year: payload.idYear,
      semester: payload.semester,
      id_journey: payload.journeyId
    }
  });

export const printSelectionList = (payload: {
  idYear: string | number;
  mentionId: string | number;
}) =>
  apiRequest<PdfFileResponse>("/liste/list_selection/", {
    query: {
      id_year: payload.idYear,
      id_mention: payload.mentionId
    }
  });

export type PrintCardsPayload = {
  mentionId: string | number;
  academicYearId: string | number;
  journeyId?: string | number;
  level?: string;
};

export const printStudentCards = (payload: PrintCardsPayload) =>
  apiRequest<PdfFileResponse[]>("/carte/carte_student/", {
    query: {
      id_year: payload.academicYearId,
      id_mention: payload.mentionId,
      id_journey: payload.journeyId ?? "",
      level: payload.level ?? "M2"
    }
  });
