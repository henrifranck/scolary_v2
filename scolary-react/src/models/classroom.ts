export interface Classroom {
  id: number;
  name: string;
  capacity?: Number;
}

export interface ClassroomOption {
  id: string;
  label: string;
}

export type ClassroomPayload = Pick<Classroom, "name" | "capacity">;
export type ClassroomListQuery = Record<
  string,
  string | number | boolean | undefined
>;
