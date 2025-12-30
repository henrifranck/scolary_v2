// Enum pour le statut de redoublement
export enum RepeatStatusEnum {
  PASSING = "0",
  REPEATING = "1",
  TRIPLING = "2"
}

// Fonction utilitaire pour formater l'affichage du statut
const formatRepeatStatus = (status?: string | null): string => {
  switch (status) {
    case RepeatStatusEnum.PASSING:
      return "Passant";
    case RepeatStatusEnum.REPEATING:
      return "Redoublant";
    case RepeatStatusEnum.TRIPLING:
      return "Triplant";
    default:
      return "N/A";
  }
};

export default formatRepeatStatus;

export enum RegisterType {
  SELECTION = "SELECTION",
  REGISTRATION = "REGISTRATION"
}

export const RegisterTypeValue: any = {
  SELECTION: "Séléction de dossier",
  REGISTRATION: "Inscription ou Ré-inscription"
};
