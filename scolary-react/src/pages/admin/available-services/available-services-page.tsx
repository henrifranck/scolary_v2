import { Pencil, Trash2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import { useForm } from "react-hook-form";

import { Button } from "../../../components/ui/button";
import {
  DataTable,
  type ColumnDef
} from "../../../components/data-table/data-table";
import { ConfirmDialog } from "../../../components/confirm-dialog";
import { Input } from "../../../components/ui/input";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle
} from "../../../components/ui/dialog";
import { cn } from "../../../lib/utils";
import {
  type AvailableService,
  type AvailableServicePayload,
  useAvailableServices,
  useCreateAvailableService,
  useUpdateAvailableService,
  useDeleteAvailableService
} from "../../../services/available-service";
import { useRequiredDocuments } from "../../../services/required-document-service";
import {
  createAvailableServiceRequiredDocument,
  deleteAvailableServiceRequiredDocument,
  useAvailableServiceRequiredDocuments
} from "../../../services/available-service-required-document";
import { ActionButton } from "@/components/action-button";
import { RequiredDocument } from "@/models/required-document";

type AvailableServiceFormValues = {
  name: string;
  routeUi: string;
};

const defaultFormValues: AvailableServiceFormValues = {
  name: "",
  routeUi: ""
};

const toFormValues = (
  service?: AvailableService | null
): AvailableServiceFormValues => ({
  name: service?.name ?? "",
  routeUi: service?.route_ui ?? ""
});

const toPayload = (
  values: AvailableServiceFormValues
): AvailableServicePayload => {
  const route = values.routeUi.trim();
  return {
    name: values.name.trim(),
    route_ui: route || undefined
  };
};

interface AvailableServiceFormProps {
  mode: "create" | "edit";
  initialValues?: AvailableServiceFormValues;
  isSubmitting: boolean;
  onSubmit: (values: AvailableServiceFormValues) => Promise<void>;
  onCancel: () => void;
  requiredDocuments: RequiredDocument[];
  selectedDocuments: number[];
  onToggleDocument: (documentId: number) => void;
  onToggleAllDocuments: () => void;
}

const AvailableServiceForm = ({
  mode,
  initialValues,
  onSubmit,
  onCancel,
  isSubmitting,
  requiredDocuments,
  selectedDocuments,
  onToggleDocument,
  onToggleAllDocuments
}: AvailableServiceFormProps) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<AvailableServiceFormValues>({
    defaultValues: initialValues ?? defaultFormValues
  });

  useEffect(() => {
    reset(initialValues ?? defaultFormValues);
  }, [initialValues, reset]);

  return (
    <form className="space-y-4" onSubmit={handleSubmit(onSubmit)}>
      <div className="space-y-2">
        <label className="text-sm font-medium" htmlFor="available-service-name">
          Name
        </label>
        <Input
          id="available-service-name"
          placeholder="Library card, transcript..."
          className={cn(errors.name && "border-destructive text-destructive")}
          {...register("name", { required: "Name is required" })}
        />
        {errors.name ? (
          <p className="text-xs text-destructive">{errors.name.message}</p>
        ) : null}
      </div>
      <div className="space-y-2">
        <label
          className="text-sm font-medium"
          htmlFor="available-service-route"
        >
          Route UI
        </label>
        <Input
          id="available-service-route"
          placeholder="/student/services"
          className={cn(
            errors.routeUi && "border-destructive text-destructive"
          )}
          {...register("routeUi")}
        />
        {errors.routeUi ? (
          <p className="text-xs text-destructive">{errors.routeUi.message}</p>
        ) : null}
      </div>
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-sm font-medium">Required documents</label>
          <label className="flex items-center gap-2 text-sm font-medium text-muted-foreground">
            <input
              type="checkbox"
              className="h-4 w-4"
              checked={
                requiredDocuments.length > 0 &&
                selectedDocuments.length === requiredDocuments.length
              }
              onChange={onToggleAllDocuments}
              disabled={isSubmitting || requiredDocuments.length === 0}
            />
            Select all
          </label>
        </div>
        {requiredDocuments.length ? (
          <div className="grid gap-2 sm:grid-cols-2">
            {requiredDocuments.map((doc) => (
              <label
                key={doc.id}
                className="flex items-center gap-2 rounded-md border px-3 py-2 text-sm"
              >
                <input
                  type="checkbox"
                  className="h-4 w-4"
                  checked={selectedDocuments.includes(doc.id)}
                  onChange={() => onToggleDocument(doc.id)}
                  disabled={isSubmitting}
                />
                <span>{doc.name}</span>
              </label>
            ))}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">
            No required documents available.
          </p>
        )}
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
              : "Create service"}
        </Button>
      </div>
    </form>
  );
};

type Feedback = { type: "success" | "error"; text: string };

export const AvailableServicesPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingService, setEditingService] = useState<AvailableService | null>(
    null
  );
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [serviceToDelete, setServiceToDelete] =
    useState<AvailableService | null>(null);
  const [selectedDocumentIds, setSelectedDocumentIds] = useState<number[]>([]);

  const offset = (page - 1) * pageSize;
  const {
    data: servicesResponse,
    isPending,
    isError,
    error
  } = useAvailableServices({ offset, limit: pageSize });
  const { data: requiredDocsResponse } = useRequiredDocuments({ limit: 1000 });
  const requiredDocuments = requiredDocsResponse?.data ?? [];
  const { data: serviceRequiredDocsResponse, isPending: isLoadingServiceDocs } =
    useAvailableServiceRequiredDocuments(
      editingService
        ? {
            where: JSON.stringify([
              {
                key: "id_available_service",
                operator: "==",
                value: editingService.id
              }
            ])
          }
        : undefined,
      Boolean(editingService)
    );
  const existingServiceDocs = serviceRequiredDocsResponse?.data ?? [];
  const services = servicesResponse?.data ?? [];
  const totalServices = servicesResponse?.count ?? services.length;

  const createService = useCreateAvailableService();
  const updateService = useUpdateAvailableService();
  const deleteService = useDeleteAvailableService();

  const openCreateForm = useCallback(() => {
    setEditingService(null);
    setSelectedDocumentIds([]);
    setIsFormOpen(true);
  }, []);

  const handleEdit = useCallback((service: AvailableService) => {
    setEditingService(service);
    setIsFormOpen(true);
  }, []);

  const closeForm = useCallback(() => {
    setEditingService(null);
    setSelectedDocumentIds([]);
    setIsFormOpen(false);
  }, []);

  const handleSubmit = useCallback(
    async (values: AvailableServiceFormValues) => {
      const payload = toPayload(values);
      try {
        if (editingService) {
          await updateService.mutateAsync({ id: editingService.id, payload });
          await syncRequiredDocuments(
            editingService.id,
            existingServiceDocs,
            selectedDocumentIds
          );
          setFeedback({
            type: "success",
            text: "Service updated successfully."
          });
        } else {
          const created = await createService.mutateAsync(payload);
          if (created?.id) {
            await syncRequiredDocuments(created.id, [], selectedDocumentIds);
          }
          setFeedback({
            type: "success",
            text: "Service created successfully."
          });
        }
        closeForm();
      } catch (mutationError) {
        const message =
          mutationError instanceof Error
            ? mutationError.message
            : "Unable to save the available service.";
        setFeedback({ type: "error", text: message });
      }
    },
    [
      closeForm,
      createService,
      editingService,
      existingServiceDocs,
      selectedDocumentIds,
      updateService
    ]
  );

  const handleDelete = useCallback(async () => {
    if (!serviceToDelete) {
      return;
    }
    try {
      await deleteService.mutateAsync(serviceToDelete.id);
      setFeedback({ type: "success", text: "Service deleted successfully." });
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to delete the service.";
      setFeedback({ type: "error", text: message });
    } finally {
      setServiceToDelete(null);
    }
  }, [deleteService, serviceToDelete]);

  const handlePageChange = useCallback((nextPage: number) => {
    setPage(nextPage);
  }, []);

  const handlePageSizeChange = useCallback((nextPageSize: number) => {
    setPageSize(nextPageSize);
    setPage(1);
  }, []);

  const columns = useMemo<ColumnDef<AvailableService>[]>(() => {
    return [
      {
        accessorKey: "name",
        header: "Name"
      },
      {
        id: "actions",
        header: "Actions",
        cell: ({ row }) => (
          <ActionButton
            row={row}
            setConfirmDelete={setServiceToDelete}
            handleEdit={handleEdit}
          />
        )
      }
    ];
  }, [handleEdit]);

  const isSubmitting = createService.isPending || updateService.isPending;
  const allDocumentsSelected =
    requiredDocuments.length > 0 &&
    selectedDocumentIds.length === requiredDocuments.length;

  useEffect(() => {
    if (editingService && !isLoadingServiceDocs) {
      setSelectedDocumentIds(
        existingServiceDocs.map((doc) => doc.id_required_document)
      );
    }
  }, [editingService, existingServiceDocs, isLoadingServiceDocs]);

  useEffect(() => {
    if (!editingService) {
      setSelectedDocumentIds([]);
    }
  }, [editingService]);

  const toggleDocument = useCallback((documentId: number) => {
    setSelectedDocumentIds((prev) =>
      prev.includes(documentId)
        ? prev.filter((id) => id !== documentId)
        : [...prev, documentId]
    );
  }, []);

  const toggleAllDocuments = useCallback(() => {
    if (allDocumentsSelected) {
      setSelectedDocumentIds([]);
    } else {
      setSelectedDocumentIds(requiredDocuments.map((doc) => doc.id));
    }
  }, [allDocumentsSelected, requiredDocuments]);

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Available services
          </h1>
          <p className="text-sm text-muted-foreground">
            Manage the services students can request.
          </p>
        </div>
        <Button size="sm" onClick={openCreateForm}>
          Add service
        </Button>
      </div>

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
            setEditingService(null);
          }
        }}
      >
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>
              {editingService ? "Edit service" : "Create new service"}
            </DialogTitle>
            <DialogDescription>
              {editingService
                ? "Update the service information."
                : "Add a service that can be associated with student requests."}
            </DialogDescription>
          </DialogHeader>
          <AvailableServiceForm
            mode={editingService ? "edit" : "create"}
            initialValues={toFormValues(editingService)}
            onSubmit={handleSubmit}
            onCancel={closeForm}
            isSubmitting={isSubmitting}
            requiredDocuments={requiredDocuments}
            selectedDocuments={selectedDocumentIds}
            onToggleDocument={toggleDocument}
            onToggleAllDocuments={toggleAllDocuments}
          />
        </DialogContent>
      </Dialog>

      <ConfirmDialog
        open={Boolean(serviceToDelete)}
        title="Delete service"
        description={
          serviceToDelete ? (
            <>
              Are you sure you want to delete{" "}
              <strong>{serviceToDelete.name}</strong>? This action cannot be
              undone.
            </>
          ) : null
        }
        confirmLabel="Delete"
        destructive
        isConfirming={deleteService.isPending}
        onCancel={() => setServiceToDelete(null)}
        onConfirm={handleDelete}
      />

      <DataTable
        columns={columns}
        data={services}
        isLoading={isPending}
        searchPlaceholder="Search services"
        emptyText={
          isError
            ? (error?.message ?? "Unable to load services")
            : "No services found"
        }
        totalItems={totalServices}
        page={page}
        pageSize={pageSize}
        onPageChange={handlePageChange}
        onPageSizeChange={handlePageSizeChange}
      />
    </div>
  );
};

const syncRequiredDocuments = async (
  serviceId: number,
  existingDocs: { id: number; id_required_document: number }[],
  selectedDocIds: number[]
) => {
  const currentIds = existingDocs.map((doc) => doc.id_required_document);
  const toAdd = selectedDocIds.filter((id) => !currentIds.includes(id));
  const toRemove = currentIds.filter((id) => !selectedDocIds.includes(id));

  if (toAdd.length) {
    await Promise.all(
      toAdd.map((id_required_document) =>
        createAvailableServiceRequiredDocument({
          id_available_service: serviceId,
          id_required_document
        })
      )
    );
  }

  if (toRemove.length) {
    const removalTargets = existingDocs.filter((doc) =>
      toRemove.includes(doc.id_required_document)
    );
    await Promise.all(
      removalTargets.map((doc) =>
        deleteAvailableServiceRequiredDocument(doc.id)
      )
    );
  }
};
