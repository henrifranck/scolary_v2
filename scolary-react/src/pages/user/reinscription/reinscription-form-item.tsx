import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Check, Pencil } from "lucide-react";
import { useCallback } from "react";
import {
  EditableSection,
  FormItemComponentType,
  FormItemType,
  ReinscriptionFormState
} from "./reinscription-form-type";
import { InfoItem } from "./reinscription-form-info-item";

interface ReinscriptionFormItemProps {
  name: string;
  editingSections: Record<EditableSection, boolean>;
  setEditingSections: (value: any) => any;
  handleFormChange: (key: keyof ReinscriptionFormState, value: any) => any;
  formState: ReinscriptionFormState;
  inputComponent: FormItemComponentType;
  classnNames?: string;
}

export const ReinscriptionFormItem = ({
  name,
  editingSections,
  setEditingSections,
  handleFormChange,
  formState,
  inputComponent,
  classnNames
}: ReinscriptionFormItemProps) => {
  const toggleSectionEditing = useCallback((section: EditableSection) => {
    setEditingSections((previous: any) => ({
      ...previous,
      [section]: !previous[section]
    }));
  }, []);

  return (
    <div className="space-y-4 rounded-xl border bg-muted/20 p-5 max-h-[320px] overflow-y-auto">
      <div className="flex items-center justify-between gap-2">
        <p className="text-sm font-semibold text-foreground">{name}</p>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="h-8 gap-2 px-3"
          onClick={() => toggleSectionEditing(inputComponent.key)}
        >
          {editingSections[inputComponent.key] ? (
            <>
              <Check className="h-4 w-4" />
              Terminer
            </>
          ) : (
            <>
              <Pencil className="h-4 w-4" />
              Modifier
            </>
          )}
        </Button>
      </div>

      {editingSections[inputComponent.key] ? (
        <div className="space-y-3">
          <div className="space-y-1.5">
            {inputComponent.value.length === 3 ? (
              <>
                <div className={classnNames}>
                  {inputComponent.value
                    .slice(0, 2)
                    .map((value: FormItemType) => (
                      <div className="space-y-1.5">
                        <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          {value.label}
                        </label>
                        {value.type === "textarea" ? (
                          <>
                            <Textarea
                              rows={3}
                              value={formState.address}
                              onChange={(event) =>
                                handleFormChange(
                                  value.formKey,
                                  event.target.value
                                )
                              }
                              placeholder={value.placeHolder}
                            />
                          </>
                        ) : (
                          <>
                            <Input
                              type={value.inputType}
                              value={formState[value.formKey]}
                              onChange={(event) =>
                                handleFormChange(
                                  value.formKey,
                                  event.target.value
                                )
                              }
                              placeholder={value.placeHolder}
                            />
                          </>
                        )}
                      </div>
                    ))}
                </div>
                <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  {inputComponent.value[2].label}
                </label>
                {inputComponent.value[2].type === "textarea" ? (
                  <Textarea
                    rows={3}
                    value={formState[inputComponent.value[2].formKey]}
                    onChange={(event) =>
                      handleFormChange(
                        inputComponent.value[2].formKey,
                        event.target.value
                      )
                    }
                    placeholder="Saisir l'adresse complète"
                  />
                ) : (
                  <Input
                    type={inputComponent.value[2].inputType}
                    value={formState[inputComponent.value[2].formKey]}
                    onChange={(event) =>
                      handleFormChange(
                        inputComponent.value[2].formKey,
                        event.target.value
                      )
                    }
                    placeholder="nom@domaine.com"
                  />
                )}
              </>
            ) : (
              <div className={classnNames}>
                {inputComponent.value.map((value: FormItemType) => (
                  <div className="space-y-1.5">
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      {value.label}
                    </label>
                    {value.type === "textarea" ? (
                      <>
                        <Textarea
                          rows={3}
                          value={formState.address}
                          onChange={(event) =>
                            handleFormChange(value.formKey, event.target.value)
                          }
                          placeholder={value.placeHolder}
                        />
                      </>
                    ) : (
                      <>
                        <Input
                          type={value.inputType}
                          value={formState[value.formKey]}
                          onChange={(event) =>
                            handleFormChange(value.formKey, event.target.value)
                          }
                          placeholder={value.placeHolder}
                        />
                      </>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      ) : (
        <>
          {inputComponent.value.length === 3 ? (
            <>
              <div className={classnNames}>
                {inputComponent.value.slice(0, 2).map((value: FormItemType) => (
                  <InfoItem
                    key={value.formKey}
                    label={value.label}
                    value={formState[value.formKey]}
                  />
                ))}
              </div>
              <InfoItem
                label={inputComponent.value[2].label}
                value={formState[inputComponent.value[2].formKey]}
              />
            </>
          ) : (
            <div className={classnNames}>
              {inputComponent.value.map((value: FormItemType) => (
                <InfoItem
                  key={value.formKey}
                  label={value.label}
                  value={formState[value.formKey]}
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};
