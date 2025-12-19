import { FormItemComponentType } from "./reinscription-form-type";

export const informationDataContact: FormItemComponentType = {
  value: [
    {
      label: "Adresse",
      type: "textarea",
      inputType: "text",
      formKey: "address",
      placeHolder: "Saisir l'adresse complète"
    }
  ],
  key: "contact",
  style: "row"
};

export const informationDataBirth: FormItemComponentType = {
  value: [
    {
      label: "Date de naissance",
      type: "input",
      inputType: "date",
      formKey: "birthDate"
    },
    {
      label: "Lieu de naissance",
      type: "input",
      inputType: "text",
      formKey: "birthPlace",
      placeHolder: "Saisir le lieu de naissance"
    }
  ],
  key: "birth",
  style: "row"
};

export const informationDataIdentity: FormItemComponentType = {
  value: [
    {
      label: "Numéro CIN",
      type: "input",
      inputType: "text",
      formKey: "cinNumber",
      placeHolder: "Saisir le numéro de CIN"
    },
    {
      label: "Date de délivrance CIN",
      type: "input",
      inputType: "date",
      formKey: "cinIssueDate"
    },
    {
      label: "Lieu de délivrance CIN",
      type: "input",
      inputType: "text",
      formKey: "cinIssuePlace",
      placeHolder: "Saisir le lieu de délivrance"
    }
  ],
  key: "identity",
  style: "mixte"
};
