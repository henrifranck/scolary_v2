import { AcademicYear } from "@/models/academic-year";
import { BaccalaureateSerie } from "@/models/baccalaureate-series";
import { Journey } from "@/models/journey";
import { Mention } from "@/models/mentions";

export type Nationality = {
  id: Number;
  name?: string;
};

export type StudentFormState = {
  studentRecordId: string;
  studentId: string;
  cardNumber?: string;
  firstName?: string;
  lastName: string;
  email?: string;
  address?: string;
  sex?: string;
  maritalStatus?: string;
  phoneNumber?: string;
  cinNumber?: string;
  cinIssueDate?: string;
  cinIssuePlace?: string;
  birthDate?: string;
  birthPlace?: string;
  baccalaureateNumber?: string;
  baccalaureateCenter?: string;
  baccalaureateYear?: string;
  baccalaureateSerieId?: string;
  job?: string;
  enrollmentStatus?: string;
  mentionId: string;
  journeyId: string;
  nationalityId?: string;
  semester: string;
  status: string;
  mean?: Number;
  level?: string;
  picture?: string;
  pictureFile?: File | null;
  annualRegister?: any;
  fullName: string;
  journeyLabel?: string;
  mentionLabel: string;
  lastUpdate: string;
  deletedAt?: string;
  fatherName?: string;
  fatherJob?: string;
  motherName?: string;
  motherJob?: string;
  parentAdress?: string;
  baccakaureateSerieLabel?: string;
  nationalityLabel?: string;
  generatedLevel?: string;
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
  | "registration"
  | "parentInfo";
export type FormItemInputType = "input" | "textarea";
export type FormItemComponentStyle = "column" | "row" | "mixte";

export type FormItemType = {
  label: string;
  type: FormItemInputType | "select";
  inputType?: string;
  formKey: keyof StudentFormState;
  selectValue?: keyof StudentFormState;
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
  academic_year?: AcademicYear;
  payment: Array<StudentPaymentState>;
  register_semester: Array<StudentSemesterState>;
  payment_status?: string;
  document?: Array<StudentDocumentState>;
};

export type StudentPaymentState = {
  id?: number;
  id_annual_register?: number;
  num_receipt: string;
  date_receipt: string;
  payed: number;
  description?: string;
};

export type StudentDocumentState = {
  id?: number;
  id_annual_register?: number;
  id_required_document?: number | null;
  name: string;
  description?: string | null;
  url: string;
};

export type StudentSemesterState = {
  id?: number;
  id_annual_register?: number;
  repeat_status?: string | null;
  id_journey?: number;
  semester: string;
  journey: Journey;
};

export interface StudentProfile {
  id?: string | null;
  num_carte?: string;
  num_select?: string | null;
  first_name?: string | null;
  last_name?: string | null;
  email?: string;
  address?: string;
  phone_number?: string;
  sex?: string;
  martial_status?: string;
  num_of_cin?: string | null;
  num_cin?: string;
  date_of_cin?: string;
  place_of_cin?: string;
  date_of_birth?: string;
  place_of_birth?: string;
  picture?: string | null;
  photo_url?: string | null;
  num_of_baccalaureate?: string;
  center_of_baccalaureate?: string;
  id_baccalaureate_series?: string;
  year_of_baccalaureate?: string;
  job?: string;
  id_mention?: number | string | null;
  id_journey?: number | string | null;
  id_nationality?: number | string | null;
  active_semester?: string | null;
  level?: string | null;
  enrollment_status?: string;
  annual_register?: Array<StudentAnnualProps> | [];
  updated_at?: string;
  deleted_at?: string;
  father_name?: string;
  father_job?: string;
  mother_name?: string;
  mother_job?: string;
  parent_address?: string;
  mean?: Number;
  baccalaureate_serie?: BaccalaureateSerie;
  nationality?: Nationality;
  generated_level?: string;
}

// Backwards compatibility exports
export type ReinscriptionFormState = StudentFormState;
export type ReinscriptionAnnualProps = StudentAnnualProps;
