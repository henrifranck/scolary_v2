import { Classroom } from "./classroom";
import { ConstituentElementOffering } from "./constituent-element-offering";
import { Group } from "./group";
import { Teacher } from "@/services/teacher-service";

export type WorkingTimeType = "cours" | "tp" | "td" | "exam";
export type WorkingTimeTypeValue = {
  COURSE: "cours";
  TP: "tp";
  TD: "td";
  EXAM: "exam";
};
export type WorkingSessionType = "Normal" | "Rattrapage";

export interface WorkingTime {
  id: number;
  id_constituent_element_offering: number;
  id_classroom?: number | null;
  id_teacher?: number | null;
  working_time_type: WorkingTimeType;
  day?: string | null;
  start?: string | null;
  end?: string | null;
  id_group?: number | null;
  date?: string | null;
  session?: WorkingSessionType | null;
  constituent_element_offering?: ConstituentElementOffering | null;
  classroom?: Classroom | null;
  group?: Group | null;
  teacher?: Teacher | null;
}

export type WorkingTimePayload = {
  id_constituent_element_offering: number | string;
  id_classroom?: number | string | null;
  id_teacher?: number | string | null;
  working_time_type: WorkingTimeType;
  day?: string | null;
  start?: string | null;
  end?: string | null;
  id_group?: number | string | null;
  date?: string | null;
  session?: WorkingSessionType | null;
};

export type WorkingTimeListQuery = Record<
  string,
  string | number | boolean | undefined
>;
