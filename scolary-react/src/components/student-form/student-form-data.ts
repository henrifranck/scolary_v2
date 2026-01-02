import { FormItemComponentType } from "./student-form-types";

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
    },
    {
      label: "Profession",
      type: "input",
      inputType: "text",
      formKey: "job",
      placeHolder: "Profession actuelle"
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

export const studentFatherInformation: FormItemComponentType = {
  value: [
    {
      label: "Nom du père",
      type: "input",
      inputType: "text",
      formKey: "fatherName",
      placeHolder: "Saisir le du père"
    },
    {
      label: "Proffession",
      type: "input",
      inputType: "text",
      formKey: "fatherJob",
      placeHolder: "Saisir la proffession"
    },
    {
      label: "Nom de la mère",
      type: "input",
      inputType: "text",
      formKey: "motherName",
      placeHolder: "Saisir le nom de la mèere"
    },
    {
      label: "Proffession",
      type: "input",
      inputType: "text",
      formKey: "motherJob",
      placeHolder: "Saisir la proffession"
    }
  ],
  key: "parentInfo",
  style: "row"
};

export const studentInformationPersonnel: FormItemComponentType = {
  value: [
    {
      label: "Nom",
      type: "input",
      inputType: "text",
      formKey: "lastName",
      placeHolder: "Saisir le nom"
    },
    {
      label: "Prénom",
      type: "input",
      inputType: "text",
      formKey: "firstName",
      placeHolder: "Saisir le prénom"
    },
    {
      label: "Email",
      type: "input",
      inputType: "text",
      formKey: "email",
      placeHolder: "Saisir l'Email"
    },

    {
      label: "Téléphone",
      type: "input",
      inputType: "text",
      formKey: "phoneNumber",
      placeHolder: "Numéro de téléphone"
    }
  ],
  key: "identity",
  style: "mixte"
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
    }
  ],
  key: "social",
  style: "mixte"
};
export const enrollementFees: any = {
  pending: "En attente",
  selected: "Sélectionné(e)",
  rejected: "Rejeté(e)",
  registered: "Inscrit(e)",
  former: "Ancien(ne)"
};
