export const sexOptions = [
  { label: 'Féminin', value: 'Feminin' },
  { label: 'Masculin', value: 'Masculin' }
];

export const situationOptions = [
  { label: 'Célibataire', value: 'Célibataire' },
  { label: 'Marié(e)', value: 'Marié(e)' }
];

export const studentStatusOptions = [
  { label: 'Passant', value: 'Passant' },
  { label: 'Redoublant', value: 'Redoublant' },
  { label: 'Triplant ou plus', value: 'Triplant ou plus' }
];

export const semesters = Array.from({ length: 10 }, (_, index) => ({
  label: `Semestre ${index + 1}`,
  value: `S${index + 1}`
}));
