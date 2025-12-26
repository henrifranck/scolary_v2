import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useForm } from "react-hook-form";
import type { Row } from "@tanstack/react-table";
import { Plus } from "lucide-react";

import { Button } from "../../components/ui/button";
import {
  DataTable,
  type ColumnDef
} from "../../components/data-table/data-table";
import { ConfirmDialog } from "../../components/confirm-dialog";
import { Input } from "../../components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue
} from "../../components/ui/select";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger
} from "../../components/ui/tabs";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "../../components/ui/dialog";
import { cn } from "../../lib/utils";
import {
  type User,
  type UserPayload,
  useCreateUser,
  useDeleteUser,
  useUpdateUser,
  useUsers,
  uploadUserPicture
} from "../../services/user-service";
import { useRoles } from "../../services/role-service";
import { useMentions } from "../../services/mention-service";
import { ActionButton } from "@/components/action-button";

type UserFormValues = {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  is_superuser: boolean;
  is_active: boolean;
  roleIds: string[];
  mentionIds: string[];
  pictureFile?: FileList;
};

const defaultFormValues: UserFormValues = {
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  is_superuser: false,
  is_active: true,
  roleIds: [],
  mentionIds: [],
  pictureFile: undefined
};

const resolvePictureUrl = (picture?: string | null) => {
  if (!picture) {
    return null;
  }

  if (/^https?:\/\//i.test(picture)) {
    return picture;
  }

  const apiBase = import.meta.env.VITE_SCOLARY_API_URL;
  if (!apiBase) {
    return picture;
  }

  try {
    const baseUrl = new URL(apiBase);
    const origin = baseUrl.origin;
    const normalizedPath = picture.startsWith("/") ? picture : `/${picture}`;
    return `${origin}${normalizedPath}`;
  } catch {
    return picture;
  }
};

const getUserAvatarUrl = (user: User) => {
  const resolvedPicture = resolvePictureUrl(user.picture);
  if (resolvedPicture) {
    return resolvedPicture;
  }

  const initialsSource =
    `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim() ||
    user.email ||
    "User";
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(initialsSource)}&background=random&color=fff&size=128`;
};

const toFormValues = (user?: User | null): UserFormValues => ({
  first_name: user?.first_name ?? "",
  last_name: user?.last_name ?? "",
  email: user?.email ?? "",
  password: "",
  is_superuser: user?.is_superuser ?? false,
  is_active: user?.is_active ?? true,
  roleIds: (() => {
    if (!user) {
      return [];
    }

    const collectedIds = new Set<number>();
    const addId = (value?: number | null) => {
      if (typeof value === "number" && Number.isFinite(value) && value > 0) {
        collectedIds.add(value);
      }
    };

    user.roles?.forEach((role) => addId(role?.id));
    user.user_role?.forEach((assignment) => {
      addId(assignment.role?.id);
      addId(assignment.role_id);
    });
    user.role_ids?.forEach((roleId) => addId(roleId));
    addId(user.role_id);
    addId(user.role?.id);

    return Array.from(collectedIds).map((id) => String(id));
  })(),
  mentionIds: (() => {
    if (!user) {
      return [];
    }

    const collectedIds = new Set<number>();
    const addId = (value?: number | null) => {
      if (typeof value === "number" && Number.isFinite(value) && value > 0) {
        collectedIds.add(value);
      }
    };

    user.mentions?.forEach((mention) => addId(mention?.id));
    user.user_mention?.forEach((assignment) => {
      addId(assignment.mention?.id);
      addId(assignment.id_mention);
    });
    user.mention_ids?.forEach((mentionId) => addId(mentionId));

    return Array.from(collectedIds).map((id) => String(id));
  })(),
  pictureFile: undefined
});

const toPayload = (values: UserFormValues): UserPayload => {
  const roleIds = (values.roleIds ?? [])
    .map((roleId) => Number(roleId))
    .filter((roleId) => Number.isFinite(roleId) && roleId > 0);
  if (roleIds.length === 0) {
    throw new Error("Select at least one role");
  }

  const mentionIds = (values.mentionIds ?? [])
    .map((mentionId) => Number(mentionId))
    .filter((mentionId) => Number.isFinite(mentionId) && mentionId > 0);

  const payload: UserPayload = {
    email: values.email.trim(),
    first_name: values.first_name.trim(),
    last_name: values.last_name.trim(),
    is_superuser: values.is_superuser,
    is_active: values.is_active,
    role_ids: Array.from(new Set(roleIds)),
    mention_ids: Array.from(new Set(mentionIds))
  };

  const normalizedPassword = values.password.trim();
  if (normalizedPassword) {
    payload.password = normalizedPassword;
  }

  return payload;
};

interface UserFormProps {
  mode: "create" | "edit";
  initialValues?: UserFormValues;
  isSubmitting: boolean;
  onSubmit: (values: UserFormValues) => Promise<void>;
  onCancel: () => void;
  roleOptions: { id: string; label: string }[];
  isRolesLoading: boolean;
  initialPicture?: string | null;
  mentionOptions: { id: string; label: string }[];
  isMentionsLoading: boolean;
}

const UserForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  roleOptions,
  isRolesLoading,
  initialPicture,
  mentionOptions,
  isMentionsLoading
}: UserFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue
  } = useForm<UserFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(() =>
    initialPicture ? resolvePictureUrl(initialPicture) : null
  );
  const pictureFileField = register("pictureFile");

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  const roleValue = watch("is_superuser") ? "admin" : "standard";
  const statusValue = watch("is_active") ? "active" : "inactive";
  const selectedRoleIds = watch("roleIds") ?? [];
  const selectedMentionIds = watch("mentionIds") ?? [];
  const watchedPictureFiles = watch("pictureFile");
  const roleSelectionError = (
    errors.roleIds as { message?: string } | undefined
  )?.message;

  useEffect(() => {
    register("roleIds", {
      validate: (value) => (value?.length ? true : "Select at least one role")
    });
  }, [register]);

  const hasRoleOptions = roleOptions.length > 0;
  const disableRoleSelection = isRolesLoading || !hasRoleOptions;
  const hasMentionOptions = mentionOptions.length > 0;
  const disableMentionSelection = isMentionsLoading || !hasMentionOptions;

  useEffect(() => {
    setPreviewUrl(initialPicture ? resolvePictureUrl(initialPicture) : null);
  }, [initialPicture]);

  useEffect(() => {
    const file = watchedPictureFiles?.[0];
    if (!file) {
      if (!initialPicture) {
        setPreviewUrl(null);
      }
      return;
    }

    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [watchedPictureFiles, initialPicture]);

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  const toggleRoleSelection = (roleId: string) => {
    if (disableRoleSelection) {
      return;
    }

    setValue(
      "roleIds",
      selectedRoleIds.includes(roleId)
        ? selectedRoleIds.filter((id) => id !== roleId)
        : [...selectedRoleIds, roleId],
      { shouldDirty: true, shouldValidate: true }
    );
  };

  const toggleMentionSelection = (mentionId: string) => {
    if (disableMentionSelection) {
      return;
    }

    setValue(
      "mentionIds",
      selectedMentionIds.includes(mentionId)
        ? selectedMentionIds.filter((id) => id !== mentionId)
        : [...selectedMentionIds, mentionId],
      { shouldDirty: true, shouldValidate: true }
    );
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-col gap-4 md:flex-row md:items-start">
        <div className="flex-1 space-y-4">
          <div className="grid gap-4 md:grid-cols-1">
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="user-first-name">
                First name
              </label>
              <Input
                id="user-first-name"
                placeholder="Amina"
                className={cn(
                  errors.first_name && "border-destructive text-destructive"
                )}
                {...register("first_name", {
                  required: "First name is required"
                })}
              />
              {errors.first_name ? (
                <p className="text-xs text-destructive">
                  {errors.first_name.message}
                </p>
              ) : null}
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium" htmlFor="user-last-name">
                Last name
              </label>
              <Input
                id="user-last-name"
                placeholder="Bennani"
                className={cn(
                  errors.last_name && "border-destructive text-destructive"
                )}
                {...register("last_name", {
                  required: "Last name is required"
                })}
              />
              {errors.last_name ? (
                <p className="text-xs text-destructive">
                  {errors.last_name.message}
                </p>
              ) : null}
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="user-email">
              Email
            </label>
            <Input
              id="user-email"
              type="email"
              placeholder="amine@scolary.com"
              className={cn(
                errors.email && "border-destructive text-destructive"
              )}
              {...register("email", { required: "Email is required" })}
            />
            {errors.email ? (
              <p className="text-xs text-destructive">{errors.email.message}</p>
            ) : null}
          </div>
        </div>
        <div className="w-full max-w-[180px] rounded-lg border bg-muted/10 p-4 shadow-sm">
          <p className="text-sm font-medium text-foreground">Profile picture</p>
          <div className="mt-3 flex flex-col items-center gap-3">
            {previewUrl ? (
              <img
                src={previewUrl}
                alt="Selected picture preview"
                className="h-20 w-20 rounded-full border object-cover"
              />
            ) : (
              <div className="flex h-20 w-20 items-center justify-center rounded-full border border-dashed bg-muted text-xs text-muted-foreground">
                No photo
              </div>
            )}
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="w-full gap-2"
              onClick={openFileDialog}
            >
              <Plus className="h-4 w-4" />
              Upload
            </Button>
            <p className="text-center text-[11px] text-muted-foreground">
              JPG or PNG, max 2 MB. Click upload to select a picture.
            </p>
          </div>
          <input
            id="user-picture-file"
            type="file"
            accept="image/*"
            className="hidden"
            {...pictureFileField}
            ref={(node) => {
              pictureFileField.ref(node);
              fileInputRef.current = node;
            }}
          />
        </div>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="user-role">
            Role
          </label>
          <Select
            value={roleValue}
            onValueChange={(value) =>
              setValue("is_superuser", value === "admin", { shouldDirty: true })
            }
          >
            <SelectTrigger id="user-role">
              <SelectValue placeholder="Select role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="standard">Standard user</SelectItem>
              <SelectItem value="admin">Administrator</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="user-status">
            Status
          </label>
          <Select
            value={statusValue}
            onValueChange={(value) =>
              setValue("is_active", value === "active", { shouldDirty: true })
            }
          >
            <SelectTrigger id="user-status">
              <SelectValue placeholder="Select status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="active">Active</SelectItem>
              <SelectItem value="inactive">Inactive</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
      <Tabs defaultValue="roles" className="space-y-3">
        <TabsList className="grid w-full grid-cols-2 md:w-auto">
          <TabsTrigger value="roles">Roles</TabsTrigger>
          <TabsTrigger value="mentions">Mentions</TabsTrigger>
        </TabsList>
        <TabsContent value="roles" className="space-y-2">
          <div className="rounded-md border border-input px-3 py-2">
            {isRolesLoading ? (
              <p className="text-sm text-muted-foreground">Loading roles…</p>
            ) : hasRoleOptions ? (
              <div className="space-y-2">
                {roleOptions.map((role) => {
                  const checkboxId = `user-role-${role.id}`;
                  const checked = selectedRoleIds.includes(role.id);
                  return (
                    <label
                      key={role.id}
                      className="flex items-center gap-2 text-sm"
                      htmlFor={checkboxId}
                    >
                      <input
                        id={checkboxId}
                        type="checkbox"
                        className="h-4 w-4 rounded border border-input text-primary"
                        checked={checked}
                        onChange={() => toggleRoleSelection(role.id)}
                        disabled={disableRoleSelection}
                      />
                      <span
                        className={cn(
                          "flex-1",
                          !checked && "text-muted-foreground"
                        )}
                      >
                        {role.label}
                      </span>
                    </label>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                Create a role first before assigning it to users.
              </p>
            )}
          </div>
          {roleSelectionError ? (
            <p className="text-xs text-destructive">{roleSelectionError}</p>
          ) : null}
        </TabsContent>
        <TabsContent value="mentions" className="space-y-2">
          <div className="rounded-md border border-input px-3 py-2">
            {isMentionsLoading ? (
              <p className="text-sm text-muted-foreground">Loading mentions…</p>
            ) : hasMentionOptions ? (
              <div className="space-y-2">
                {mentionOptions.map((mention) => {
                  const checkboxId = `user-mention-${mention.id}`;
                  const checked = selectedMentionIds.includes(mention.id);
                  return (
                    <label
                      key={mention.id}
                      className="flex items-center gap-2 text-sm"
                      htmlFor={checkboxId}
                    >
                      <input
                        id={checkboxId}
                        type="checkbox"
                        className="h-4 w-4 rounded border border-input text-primary"
                        checked={checked}
                        onChange={() => toggleMentionSelection(mention.id)}
                        disabled={disableMentionSelection}
                      />
                      <span
                        className={cn(
                          "flex-1",
                          !checked && "text-muted-foreground"
                        )}
                      >
                        {mention.label}
                      </span>
                    </label>
                  );
                })}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                Create a mention first before assigning it to users.
              </p>
            )}
          </div>
          <p className="text-xs text-muted-foreground">
            Mention selection is optional. Leave empty to keep current
            assignment.
          </p>
        </TabsContent>
      </Tabs>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="user-password">
          Password
        </label>
        <Input
          id="user-password"
          type="password"
          placeholder="••••••••"
          className={cn(
            errors.password && "border-destructive text-destructive"
          )}
          {...register("password", {
            ...(mode === "create" ? { required: "Password is required" } : {}),
            minLength: {
              value: 6,
              message: "Password must be at least 6 characters"
            }
          })}
        />
        {mode === "edit" ? (
          <p className="text-xs text-muted-foreground">
            Leave blank to keep the current password.
          </p>
        ) : null}
        {errors.password ? (
          <p className="text-xs text-destructive">{errors.password.message}</p>
        ) : null}
      </div>
      <div className="flex items-center justify-end gap-2">
        <Button
          type="button"
          variant="ghost"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
        <Button type="submit" disabled={isSubmitting}>
          {isSubmitting
            ? "Saving…"
            : mode === "edit"
              ? "Save changes"
              : "Create user"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const UsersPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [userToDelete, setUserToDelete] = useState<User | null>(null);

  const {
    data: rolesResponse,
    isPending: areRolesLoading,
    isError: isRolesError,
    error: rolesError
  } = useRoles();
  const rolesData = rolesResponse?.data ?? [];
  const {
    data: mentionsResponse,
    isPending: areMentionsLoading,
    isError: areMentionsError,
    error: mentionsError
  } = useMentions();
  const mentionsData = mentionsResponse?.data ?? [];
  const usersQuery = useMemo(
    () => ({
      relation: JSON.stringify(["user_role.role", "user_mention.mention"]),
      offset: (page - 1) * pageSize,
      limit: pageSize
    }),
    [page, pageSize]
  );
  const {
    data: usersResponse,
    isPending,
    isError,
    error
  } = useUsers(usersQuery);
  const users = usersResponse?.data ?? [];
  const totalUsers = usersResponse?.count ?? users.length;
  const createUser = useCreateUser();
  const updateUser = useUpdateUser();
  const deleteUser = useDeleteUser();

  const openCreateForm = useCallback(() => {
    setEditingUser(null);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((user: User) => {
    setEditingUser(user);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingUser(null);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: UserFormValues) => {
      try {
        const payload = toPayload(values);
        const pictureFile = values.pictureFile?.[0];
        let userId: number | null = editingUser?.id ?? null;
        if (editingUser) {
          const updated = await updateUser.mutateAsync({
            id: editingUser.id,
            payload
          });
          userId = updated?.id ?? editingUser.id;
          if (pictureFile && userId) {
            await uploadUserPicture(userId, pictureFile);
          }
          setFeedback({ type: "success", text: "User updated successfully." });
        } else {
          const created = await createUser.mutateAsync(payload);
          userId = created?.id ?? null;
          if (pictureFile && userId) {
            await uploadUserPicture(userId, pictureFile);
          }
          setFeedback({ type: "success", text: "User created successfully." });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save user.";
        setFeedback({ type: "error", text: message });
      }
    },
    [closeForm, createUser, editingUser, updateUser, uploadUserPicture]
  );

  const handleDelete = useCallback(async () => {
    if (!userToDelete) {
      return;
    }
    try {
      await deleteUser.mutateAsync(userToDelete.id);
      setFeedback({ type: "success", text: "User deleted successfully." });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete user.";
      setFeedback({ type: "error", text: message });
    } finally {
      setUserToDelete(null);
    }
  }, [deleteUser, userToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextSize: number) => {
    setPageSize(nextSize);
    setPage(1);
  }, []);

  const roleOptions = useMemo(
    () => rolesData.map((role) => ({ id: String(role.id), label: role.name })),
    [rolesData]
  );
  const roleNameMap = useMemo(() => {
    const map = new Map<number, string>();
    rolesData.forEach((role) => {
      if (typeof role.id === "number" && role.name) {
        map.set(role.id, role.name);
      }
    });
    return map;
  }, [rolesData]);
  const rolesErrorMessage =
    isRolesError && rolesError instanceof Error
      ? rolesError.message
      : isRolesError
        ? "Unable to load roles"
        : null;
  const mentionOptions = useMemo(
    () =>
      mentionsData.map((mention) => ({
        id: String(mention.id),
        label: mention.name
      })),
    [mentionsData]
  );
  const mentionNameMap = useMemo(() => {
    const map = new Map<number, string>();
    mentionsData.forEach((mention) => {
      if (typeof mention.id === "number" && mention.name) {
        map.set(mention.id, mention.name);
      }
    });
    return map;
  }, [mentionsData]);
  const mentionsErrorMessage =
    areMentionsError && mentionsError instanceof Error
      ? mentionsError.message
      : areMentionsError
        ? "Unable to load mentions"
        : null;

  const resolveRoleLabels = useCallback(
    (user: User) => {
      const labels: string[] = [];
      const labelSet = new Set<string>();
      const addLabel = (label?: string | null) => {
        if (!label || labelSet.has(label)) {
          return;
        }
        labelSet.add(label);
        labels.push(label);
      };
      const idSet = new Set<number>();
      const addId = (id?: number | null) => {
        if (typeof id === "number" && Number.isFinite(id) && id > 0) {
          idSet.add(id);
        }
      };

      user.roles?.forEach((role) => {
        addLabel(role?.name ?? null);
        addId(role?.id);
      });
      if (user.role?.name) {
        addLabel(user.role.name);
      }
      addId(user.role?.id);
      addId(user.role_id);
      user.role_ids?.forEach(addId);
      user.user_role?.forEach((assignment) => {
        const roleId = assignment.role?.id ?? assignment.role_id;
        addId(roleId);
        if (assignment.role && "name" in assignment.role) {
          addLabel(assignment.role.name ?? null);
        }
      });

      if (labels.length === 0) {
        Array.from(idSet).forEach((id) =>
          addLabel(roleNameMap.get(id) ?? `#${id}`)
        );
      } else {
        Array.from(idSet).forEach((id) => {
          const resolved = roleNameMap.get(id);
          if (resolved && !labelSet.has(resolved)) {
            addLabel(resolved);
          }
        });
      }

      return labels;
    },
    [roleNameMap]
  );

  const resolveMentionLabels = useCallback(
    (user: User) => {
      const labels: string[] = [];
      const labelSet = new Set<string>();
      const addLabel = (label?: string | null) => {
        if (!label || labelSet.has(label)) {
          return;
        }
        labelSet.add(label);
        labels.push(label);
      };
      const idSet = new Set<number>();
      const addId = (id?: number | null) => {
        if (typeof id === "number" && Number.isFinite(id) && id > 0) {
          idSet.add(id);
        }
      };

      user.mentions?.forEach((mention) => {
        addLabel(mention?.name ?? null);
        addId(mention?.id);
      });
      user.user_mention?.forEach((assignment) => {
        const mentionId = assignment.mention?.id ?? assignment.id_mention;
        addId(mentionId);
        if (assignment.mention && "name" in assignment.mention) {
          addLabel(assignment.mention.name ?? null);
        }
      });
      user.mention_ids?.forEach(addId);

      if (labels.length === 0) {
        Array.from(idSet).forEach((id) =>
          addLabel(mentionNameMap.get(id) ?? `#${id}`)
        );
      } else {
        Array.from(idSet).forEach((id) => {
          const resolved = mentionNameMap.get(id);
          if (resolved && !labelSet.has(resolved)) {
            addLabel(resolved);
          }
        });
      }

      return labels;
    },
    [mentionNameMap]
  );

  const columns = useMemo<ColumnDef<User>[]>(() => {
    return [
      {
        accessorKey: "first_name",
        header: "User",
        cell: ({ row }) => {
          const user = row.original;
          const fullName =
            `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim();
          return (
            <div className="flex flex-col">
              <span className="font-medium">{fullName || user.email}</span>
              <span className="text-xs text-muted-foreground">
                {user.email}
              </span>
            </div>
          );
        }
      },
      {
        accessorKey: "is_superuser",
        header: "Role",
        cell: ({ row }) => (
          <span className="inline-flex items-center rounded-full bg-secondary px-2 py-1 text-xs font-medium text-secondary-foreground">
            {row.original.is_superuser ? "Administrator" : "Standard user"}
          </span>
        )
      },
      {
        accessorKey: "role_name",
        header: "Assigned roles",
        cell: ({ row }) => {
          const labels = resolveRoleLabels(row.original);
          return (
            <span className="text-sm text-muted-foreground">
              {labels.length ? labels.join(", ") : "—"}
            </span>
          );
        }
      },
      {
        accessorKey: "mention_names",
        header: "Assigned mentions",
        cell: ({ row }) => {
          const labels = resolveMentionLabels(row.original);
          return (
            <span className="text-sm text-muted-foreground">
              {labels.length ? labels.join(", ") : "—"}
            </span>
          );
        }
      },
      {
        accessorKey: "is_active",
        header: "Status",
        cell: ({ row }) => {
          const isActive = row.original.is_active ?? true;
          return (
            <span
              className={
                isActive
                  ? "text-xs font-semibold text-emerald-600"
                  : "text-xs font-semibold text-muted-foreground"
              }
            >
              {isActive ? "Active" : "Inactive"}
            </span>
          );
        }
      },
      {
        id: "actions",
        header: "",
        cell: ({ row }) => (
          // <div className="flex justify-end gap-2">
          //   <Button
          //     size="sm"
          //     variant="outline"
          //     onClick={() => handleEdit(row.original)}
          //   >
          //     Edit
          //   </Button>
          //   <Button
          //     size="sm"
          //     variant="ghost"
          //     className="text-destructive hover:text-destructive"
          //     onClick={() => setUserToDelete(row.original)}
          //   >
          //     Delete
          //   </Button>
          // </div>
          <ActionButton
            row={row}
            handleEdit={handleEdit}
            setConfirmDelete={setUserToDelete}
          />
        )
      }
    ];
  }, [handleEdit, resolveRoleLabels, resolveMentionLabels]);

  const renderUserCard = useCallback(
    (row: Row<User>) => {
      const user = row.original;
      const fullName =
        `${user.first_name ?? ""} ${user.last_name ?? ""}`.trim() || user.email;
      const avatarUrl = getUserAvatarUrl(user);
      const roleLabels = resolveRoleLabels(user);
      const mentionLabels = resolveMentionLabels(user);
      const statusLabel = (user.is_active ?? true) ? "Active" : "Inactive";

      return (
        <div className="flex h-full flex-col gap-4 rounded-lg border bg-background p-5 shadow-sm">
          <div className="flex items-start gap-3">
            <img
              src={avatarUrl}
              alt={fullName}
              className="h-12 w-12 rounded-full border"
            />
            <div className="flex-1">
              <p className="text-sm font-semibold leading-tight text-foreground">
                {fullName}
              </p>
              <p className="text-xs text-muted-foreground">{user.email}</p>
            </div>
            <span
              className={cn(
                "rounded-full px-2 py-1 text-xs font-medium",
                (user.is_active ?? true)
                  ? "bg-emerald-100 text-emerald-700"
                  : "bg-muted text-muted-foreground border border-dashed"
              )}
            >
              {statusLabel}
            </span>
          </div>
          <div className="space-y-3 text-sm">
            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Role level
              </p>
              <p className="font-medium text-foreground">
                {user.is_superuser ? "Administrator" : "Standard user"}
              </p>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Assigned roles
              </p>
              <p className="text-sm text-foreground">
                {roleLabels.length ? roleLabels.join(", ") : "—"}
              </p>
            </div>
            <div>
              <p className="text-xs font-medium text-muted-foreground">
                Assigned mentions
              </p>
              <p className="text-sm text-foreground">
                {mentionLabels.length ? mentionLabels.join(", ") : "—"}
              </p>
            </div>
            <div className="flex justify-end gap-2">
              <Button
                size="sm"
                variant="outline"
                onClick={() => handleEdit(user)}
              >
                Edit
              </Button>
              <Button
                size="sm"
                variant="ghost"
                className="text-destructive hover:text-destructive"
                onClick={() => setUserToDelete(user)}
              >
                Delete
              </Button>
            </div>
          </div>
        </div>
      );
    },
    [handleEdit, resolveRoleLabels, resolveMentionLabels]
  );

  const isSubmitting = createUser.isPending || updateUser.isPending;

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Users</h1>
          <p className="text-sm text-muted-foreground">
            Create and manage Scolary accounts.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add user
        </Button>
      </div>

      {rolesErrorMessage ? (
        <div className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-2 text-sm text-destructive">
          {rolesErrorMessage}
        </div>
      ) : null}
      {!rolesErrorMessage && !areRolesLoading && roleOptions.length === 0 ? (
        <div className="rounded-md border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-800">
          Create at least one role before inviting users.
        </div>
      ) : null}
      {mentionsErrorMessage ? (
        <div className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-2 text-sm text-destructive">
          {mentionsErrorMessage}
        </div>
      ) : null}
      {!mentionsErrorMessage &&
      !areMentionsLoading &&
      mentionOptions.length === 0 ? (
        <div className="rounded-md border border-amber-200 bg-amber-50 px-4 py-2 text-sm text-amber-800">
          Create at least one mention before inviting users.
        </div>
      ) : null}

      {feedback ? (
        <div
          className={cn(
            "flex items-start justify-between gap-4 rounded-md border px-4 py-3 text-sm",
            feedback.type === "success"
              ? "border-emerald-200 bg-emerald-50 text-emerald-800"
              : "border-destructive/30 bg-destructive/10 text-destructive"
          )}
        >
          <span>{feedback.text}</span>
          <button
            className="text-xs font-medium underline"
            onClick={() => setFeedback(null)}
          >
            Dismiss
          </button>
        </div>
      ) : null}

      <Dialog
        open={isFormOpen}
        onOpenChange={(open) => {
          setIsFormOpen(open);
          if (!open) {
            setEditingUser(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingUser ? "Edit user" : "Create new user"}
            </DialogTitle>
            <DialogDescription>
              {editingUser
                ? "Update the user to align permissions and status."
                : "Invite a new user to access the administration portal."}
            </DialogDescription>
          </DialogHeader>
          <UserForm
            mode={editingUser ? "edit" : "create"}
            initialValues={toFormValues(editingUser)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            roleOptions={roleOptions}
            isRolesLoading={areRolesLoading}
            initialPicture={editingUser?.picture ?? null}
            mentionOptions={mentionOptions}
            isMentionsLoading={areMentionsLoading}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(userToDelete)}
        title="Delete user"
        description={
          userToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>
                {`${userToDelete.first_name ?? ""} ${userToDelete.last_name ?? ""}`.trim() ||
                  userToDelete.email ||
                  "this user"}
              </strong>
              ? This action cannot be undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteUser.isPending}
        onCancel={() => setUserToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={users}
        isLoading={isPending}
        searchPlaceholder="Search users"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load users")
            : "No users found"
        }
        enableViewToggle
        renderGridItem={renderUserCard}
        gridClassName="sm:grid-cols-2 xl:grid-cols-3"
        gridEmptyState={
          <div className="flex h-40 items-center justify-center rounded-lg border border-dashed text-sm text-muted-foreground">
            No users available.
          </div>
        }
        totalItems={totalUsers}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};
