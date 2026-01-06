import { apiRequest } from "./api-client";
import { User } from "./user-service";

export type Grade = "MR" | "DR" | "PR" | "Mme";

export interface Teacher {
  id?: number;
  id_user: number;
  grade: Grade;
  max_hours_per_day?: number;
  max_days_per_week?: number;
  user?: User;
}

export interface TeacherPayload {
  id_user: number;
  grade: Grade;
  max_hours_per_day?: number;
  max_days_per_week?: number;
}

export const createTeacher = (payload: TeacherPayload) =>
  apiRequest("/teacher/", {
    method: "POST",
    json: payload
  });

export const teacherService = {
  createTeacher
};
