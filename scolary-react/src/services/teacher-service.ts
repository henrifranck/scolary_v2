import { apiRequest } from './api-client';

export type Grade = 'MR' | 'DR' | 'PR' | 'Mme';

export interface TeacherPayload {
  id_user: number;
  grade: Grade;
  max_hours_per_day?: number;
  max_days_per_week?: number;
}

export const createTeacher = (payload: TeacherPayload) =>
  apiRequest('/teacher/', {
    method: 'POST',
    json: payload
  });

export const teacherService = {
  createTeacher
};
