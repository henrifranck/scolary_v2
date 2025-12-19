import { Journey } from "@/services/journey-service";

export type ReinscriptionFormState = {
  studentRecordId: string;
  studentId: string;
  cardNumber: string;
  firstName: string;
  lastName: string;
  email: string;
  address: string;
  cinNumber: string;
  cinIssueDate: string;
  cinIssuePlace: string;
  birthDate: string;
  birthPlace: string;
  mentionId: string;
  journeyId: string;
  semester: string;
  status: string;
  notes: string;
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
  | "personal";
export type FormItemInputType = "input" | "textarea";
export type FormItemComponentStyle = "column" | "row" | "mixte";

export type FormItemType = {
  label: string;
  type: FormItemInputType;
  inputType?: string;
  formKey: keyof ReinscriptionFormState;
  placeHolder?: string;
};

export type FormItemComponentType = {
  value: Array<FormItemType>;
  key: EditableSection;
  style: FormItemComponentStyle;
};

export type ReinscriptionAnnualProps = {
  payment: Array<ReinscriptionPaymentState>;
  register_semester: Array<ReinscriptionSemesterState>;
};

export type ReinscriptionPaymentState = {
  num_receipt: string;
  date_receipt: string;
  payed: number;
};

export type ReinscriptionSemesterState = {
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
  num_of_cin?: string | null;
  num_cin?: string | null;
  date_of_cin?: string | null;
  place_of_cin?: string | null;
  date_of_birth?: string | null;
  place_of_birth?: string | null;
  id_mention?: number | string | null;
  id_journey?: number | string | null;
  active_semester?: string | null;
  enrollment_status?: string | null;
  annual_register?: Array<ReinscriptionAnnualProps> | [];
}
