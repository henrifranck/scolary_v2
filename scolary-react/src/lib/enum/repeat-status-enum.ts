// Enum pour le statut de redoublement
export enum RepeatStatusEnum {
  PASSING = "0",
  REPEATING = "1",
  TRIPLING = "2"
}

// Fonction utilitaire pour formater l'affichage du statut
const formatRepeatStatus = (status: string): string => {
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
