import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "@/components/ui/select";
import { Check, Pencil } from "lucide-react";
import { useCallback } from "react";
import {
  EditableSection,
  FormItemComponentType,
  FormItemType,
  StudentFormState
} from "./student-form-types";
import { StudentFormInfoItem } from "./student-form-info-item";

interface StudentFormItemProps {
  name: string;
  editingSections: Record<EditableSection, boolean>;
  setEditingSections: (value: any) => any;
  handleFormChange: (key: keyof StudentFormState, value: any) => any;
  formState: StudentFormState;
  inputComponent: FormItemComponentType;
  classnNames?: string;
  disabledEditing?: boolean;
}

export const StudentFormItem = ({
  name,
  editingSections,
  setEditingSections,
  handleFormChange,
  formState,
  inputComponent,
  classnNames,
  disabledEditing = false
}: StudentFormItemProps) => {
  const toggleSectionEditing = useCallback(
    (section: EditableSection) => {
      if (disabledEditing) return;
      setEditingSections((previous: any) => ({
        ...previous,
        [section]: !previous[section]
      }));
    },
    [disabledEditing]
  );

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
          disabled={disabledEditing}
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
          <div className="space-y-4">
            {inputComponent.value.length === 3 ? (
              <>
                <div className={classnNames}>
                  {inputComponent.value
                    .slice(0, 2)
                    .map((value: FormItemType) => (
                      <div
                        className="space-y-1.5"
                        key={value.formKey as string}
                      >
                        <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                          {value.label}
                        </label>
                        {value.type === "textarea" ? (
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
                            disabled={disabledEditing}
                          />
                        ) : value.type === "select" && value.options ? (
                          <Select
                            value={formState[value.formKey] as string}
                            onValueChange={(val) =>
                              handleFormChange(value.formKey, val)
                            }
                            disabled={disabledEditing}
                          >
                            <SelectTrigger>
                              <SelectValue
                                placeholder={
                                  value.placeHolder ?? "Sélectionner"
                                }
                              />
                            </SelectTrigger>
                            <SelectContent>
                              {value.options.map((option) => (
                                <SelectItem
                                  key={option.value}
                                  value={option.value}
                                >
                                  {option.label}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        ) : (
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
                            disabled={disabledEditing}
                          />
                        )}
                      </div>
                    ))}
                </div>
                <div className="space-y-1.5">
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
                      disabled={disabledEditing}
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
                      disabled={disabledEditing}
                    />
                  )}
                </div>
              </>
            ) : (
              <div className={classnNames}>
                {inputComponent.value.map((value: FormItemType) => (
                  <div className="space-y-1.5" key={value.formKey as string}>
                    <label className="text-xs font-medium uppercase tracking-wide text-muted-foreground">
                      {value.label}
                    </label>
                    {value.type === "textarea" ? (
                      <Textarea
                        rows={3}
                        value={formState.address}
                        onChange={(event) =>
                          handleFormChange(value.formKey, event.target.value)
                        }
                        placeholder={value.placeHolder}
                        disabled={disabledEditing}
                      />
                    ) : value.type === "select" && value.options ? (
                      <Select
                        value={formState[value.formKey] as string}
                        onValueChange={(val) =>
                          handleFormChange(value.formKey, val)
                        }
                        disabled={disabledEditing}
                      >
                        <SelectTrigger>
                          <SelectValue
                            placeholder={value.placeHolder ?? "Sélectionner"}
                          />
                        </SelectTrigger>
                        <SelectContent>
                          {value.options.map((option) => (
                            <SelectItem key={option.value} value={option.value}>
                              {option.label}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    ) : (
                      <Input
                        type={value.inputType}
                        value={formState[value.formKey]}
                        onChange={(event) =>
                          handleFormChange(value.formKey, event.target.value)
                        }
                        placeholder={value.placeHolder}
                        disabled={disabledEditing}
                      />
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
                  <StudentFormInfoItem
                    key={value.formKey}
                    label={value.label}
                    value={formState[value.formKey]}
                  />
                ))}
              </div>
              <StudentFormInfoItem
                label={inputComponent.value[2].label}
                value={formState[inputComponent.value[2].formKey]}
              />
            </>
          ) : (
            <div className={classnNames}>
              {inputComponent.value.map((value: FormItemType) => (
                <StudentFormInfoItem
                  key={value.formKey}
                  label={value.label}
                  value={formState[value.formKey]}
                  selectValue={
                    value.selectValue && formState[value.selectValue]
                  }
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
};
