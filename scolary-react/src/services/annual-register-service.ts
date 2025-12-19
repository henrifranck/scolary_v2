import {
  ApiListResponse,
  ReinscriptionAnnualProps
} from "@/pages/user/reinscription/reinscription-form-type";
import { apiRequest } from "./api-client";
import { isListResponse, normalizeList } from "./utils-common";

const relations = JSON.stringify([
  "register_semester",
  "register_semester{id_journey,semester,repeat_status}",
  "register_semester.journey{id_mention,name}",
  "register_semester.journey.mention{name}",
  "payment{id,payed,num_receipt,date_receipt}"
]);
const baseColumn = JSON.stringify(["last_name", "first_name"]);

const buildWhereClause = (cardNumber: string) =>
  JSON.stringify([
    {
      key: "num_carte",
      operator: "==",
      value: cardNumber
    }
  ]);

type ApiAnnualRegisterPayload = ApiListResponse<ReinscriptionAnnualProps>;

export const fetchAnnualRegisterByCardNumber = async (
  cardNumber: string
): Promise<ApiAnnualRegisterPayload> => {
  const trimmed = cardNumber.trim();
  if (!trimmed) {
    throw new Error("Le numéro de carte est requis.");
  }

  const response = await apiRequest<ApiAnnualRegisterPayload>(
    "/annual_registers/",
    {
      query: {
        relation: relations,
        base_column: baseColumn,
        where: buildWhereClause(trimmed)
      }
    }
  );

  return response;
};
