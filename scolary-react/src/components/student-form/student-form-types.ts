import { Journey } from "@/services/journey-service";

export type StudentFormState = {
  studentRecordId: string;
  studentId: string;
  cardNumber: string;
  firstName: string;
  lastName: string;
  email: string;
  address: string;
  sex: string;
  maritalStatus: string;
  phoneNumber: string;
  cinNumber: string;
  cinIssueDate: string;
  cinIssuePlace: string;
  birthDate: string;
  birthPlace: string;
  baccalaureateNumber: string;
  baccalaureateCenter: string;
  job: string;
  enrollmentStatus: string;
  mentionId: string;
  journeyId: string;
  semester: string;
  status: string;
  notes: string;
  level?: string;
  picture?: string;
  pictureFile?: File | null;
  annualRegister?: any;
};

export type ApiListResponse<T> = {
  count?: number;
  data: T[];
};

export type EditableSection =
  | "contact"
  | "birth"
  | "identity"
  | "school"
  | "personal"
  | "baccalaureate"
  | "social"
  | "registration";
export type FormItemInputType = "input" | "textarea";
export type FormItemComponentStyle = "column" | "row" | "mixte";

export type FormItemType = {
  label: string;
  type: FormItemInputType | "select";
  inputType?: string;
  formKey: keyof StudentFormState;
  placeHolder?: string;
  options?: Array<{ value: string; label: string }>;
};

export type FormItemComponentType = {
  value: Array<FormItemType>;
  key: EditableSection;
  style: FormItemComponentStyle;
};

export type StudentAnnualProps = {
  id?: number;
  payment: Array<StudentPaymentState>;
  register_semester: Array<StudentSemesterState>;
};

export type StudentPaymentState = {
  id?: number;
  id_annual_register?: number;
  num_receipt: string;
  date_receipt: string;
  payed: number;
};

export type StudentSemesterState = {
  id?: number;
  id_annual_register?: number;
  id_journey?: number;
  semester: string;
  repeat_status: string;
  journey: Journey;
};

export interface StudentProfile {
  id?: number | string | null;
  num_carte?: string | null;
  num_select?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  email?: string | null;
  address?: string | null;
  phone_number?: string | null;
  sex?: string | null;
  martial_status?: string | null;
  num_of_cin?: string | null;
  num_cin?: string | null;
  date_of_cin?: string | null;
  place_of_cin?: string | null;
  date_of_birth?: string | null;
  place_of_birth?: string | null;
  picture?: string | null;
  photo_url?: string | null;
  num_of_baccalaureate?: string | null;
  center_of_baccalaureate?: string | null;
  job?: string | null;
  id_mention?: number | string | null;
  id_journey?: number | string | null;
  active_semester?: string | null;
  level?: string | null;
  enrollment_status?: string | null;
  annual_register?: Array<StudentAnnualProps> | [];
}

// Backwards compatibility exports
export type ReinscriptionFormState = StudentFormState;
export type ReinscriptionAnnualProps = StudentAnnualProps;
