import { FormItemComponentType } from "./student-form-types";

export const studentInformationContact: FormItemComponentType = {
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

export const studentInformationBirth: FormItemComponentType = {
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

export const studentInformationIdentity: FormItemComponentType = {
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

export const studentInformationBaccalaureate: FormItemComponentType = {
  value: [
    {
      label: "Numéro baccalauréat",
      type: "input",
      inputType: "text",
      formKey: "baccalaureateNumber",
      placeHolder: "Numéro baccalauréat"
    },
    {
      label: "Centre baccalauréat",
      type: "input",
      inputType: "text",
      formKey: "baccalaureateCenter",
      placeHolder: "Centre d'examen"
    },
    {
      label: "Téléphone",
      type: "input",
      inputType: "text",
      formKey: "phoneNumber",
      placeHolder: "Numéro de téléphone"
    }
  ],
  key: "baccalaureate",
  style: "row"
};

export const studentInformationSocial: FormItemComponentType = {
  value: [
    {
      label: "Sexe",
      type: "select",
      inputType: "text",
      formKey: "sex",
      options: [
        { value: "Masculin", label: "Masculin" },
        { value: "Féminin", label: "Féminin" }
      ]
    },
    {
      label: "Situation familiale",
      type: "select",
      inputType: "text",
      formKey: "maritalStatus",
      options: [
        { value: "Célibataire", label: "Célibataire" },
        { value: "Marié(e)", label: "Marié(e)" },
        { value: "Divorcé(e)", label: "Divorcé(e)" },
        { value: "Veuf/Veuve", label: "Veuf/Veuve" }
      ],
      placeHolder: "Célibataire / Marié(e) ..."
    },
    {
      label: "Profession",
      type: "input",
      inputType: "text",
      formKey: "job",
      placeHolder: "Profession actuelle"
    }
  ],
  key: "social",
  style: "mixte"
};

export const studentInformationRegistration: FormItemComponentType = {
  value: [
    {
      label: "Statut d'inscription",
      type: "select",
      inputType: "text",
      formKey: "enrollmentStatus",
      options: [
        { value: "pending", label: "En attente" },
        { value: "selected", label: "Sélectionné(e)" },
        { value: "rejected", label: "Rejeté(e)" },
        { value: "registered", label: "Inscrit(e)" },
        { value: "former", label: "Ancien(ne)" }
      ],
      placeHolder: "En attente / Sélectionné(e) / Inscrit(e)"
    }
  ],
  key: "registration",
  style: "row"
};
