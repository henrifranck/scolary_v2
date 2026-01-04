import { useEffect, useMemo, useRef, useState, type PointerEvent } from "react";
import { useForm } from "react-hook-form";

import { Button } from "../../../components/ui/button";
import { Input } from "../../../components/ui/input";
import { Textarea } from "../../../components/ui/textarea";
import { cn } from "../../../lib/utils";
import { Eye, EyeOff, Pencil } from "lucide-react";
import {
  type University,
  type UniversityPayload,
  useSaveUniversity,
  useUniversityInfo
} from "../../../services/university-service";
import { useUploadFile } from "../../../services/file-manager-service";

type UniversityFormValues = {
  province: string;
  department_name: string;
  department_other_information: string;
  department_address: string;
  email: string;
  logo_university: string;
  logo_departement: string;
  phone_number: string;
  admin_signature: string;
};

const defaultValues: UniversityFormValues = {
  province: "",
  department_name: "",
  department_other_information: "",
  department_address: "",
  email: "",
  logo_university: "",
  logo_departement: "",
  phone_number: "",
  admin_signature: ""
};

const toFormValues = (
  university?: University | null
): UniversityFormValues => ({
  province: university?.province ?? "",
  department_name: university?.department_name ?? "",
  department_other_information: university?.department_other_information ?? "",
  department_address: university?.department_address ?? "",
  email: university?.email ?? "",
  logo_university: university?.logo_university ?? "",
  logo_departement: university?.logo_departement ?? "",
  phone_number: university?.phone_number ?? "",
  admin_signature: university?.admin_signature ?? ""
});

const toPayload = (values: UniversityFormValues): UniversityPayload => ({
  province: values.province.trim(),
  department_name: values.department_name.trim() || null,
  department_other_information:
    values.department_other_information.trim() || null,
  department_address: values.department_address.trim() || null,
  email: values.email.trim(),
  logo_university: values.logo_university.trim() || null,
  logo_departement: values.logo_departement.trim() || null,
  phone_number: values.phone_number.trim() || null,
  admin_signature: values.admin_signature.trim() || null
});

type Feedback = { type: "success" | "error"; text: string };

export const UniversityInfoPage = () => {
  const { data: university, isPending, isError, error } = useUniversityInfo();
  const saveUniversity = useSaveUniversity();
  const uploadFile = useUploadFile();
  const [feedback, setFeedback] = useState<Feedback | null>(null);
  const initialValues = useMemo(() => toFormValues(university), [university]);
  const {
    register,
    handleSubmit,
    setValue,
    reset,
    formState: { errors, isSubmitting }
  } = useForm<UniversityFormValues>({
    defaultValues: initialValues
  });
  const [logoPreview, setLogoPreview] = useState<string | null>(null);
  const [departmentLogoPreview, setDepartmentLogoPreview] = useState<
    string | null
  >(null);
  const [signaturePreview, setSignaturePreview] = useState<string | null>(null);
  const [logoFile, setLogoFile] = useState<File | null>(null);
  const [departmentLogoFile, setDepartmentLogoFile] = useState<File | null>(
    null
  );
  const [signatureDirty, setSignatureDirty] = useState(false);
  const [showSignature, setShowSignature] = useState(true);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const isDrawingRef = useRef(false);
  const lastPointRef = useRef<{ x: number; y: number } | null>(null);
  const logoInputRef = useRef<HTMLInputElement | null>(null);
  const departmentLogoInputRef = useRef<HTMLInputElement | null>(null);

  const resolveFileUrl = (path?: string | null) => {
    if (!path) {
      return null;
    }
    if (/^https?:\/\//i.test(path)) {
      return path;
    }
    const cleaned = path.replace(/^\/+/, "");
    const normalized = cleaned.replace(/^(\.\.\/)+/, "");
    const finalPath = normalized.startsWith("files/")
      ? normalized
      : `files/${normalized}`;
    const apiBase = import.meta.env.VITE_SCOLARY_API_URL;
    try {
      const base = new URL(apiBase);

      return `${base.origin}/${finalPath}`;
    } catch {
      return `/${finalPath}`;
    }
  };

  const normalizeStoredPath = (path?: string | null) => {
    if (!path) return "";
    if (path.startsWith("../") || path.startsWith("files/")) return path;
    return `../${path}`;
  };

  useEffect(() => {
    reset(initialValues);
    setLogoPreview(resolveFileUrl(initialValues.logo_university));
    setDepartmentLogoPreview(resolveFileUrl(initialValues.logo_departement));
    setSignaturePreview(resolveFileUrl(initialValues.admin_signature));
    setLogoFile(null);
    setDepartmentLogoFile(null);
    setSignatureDirty(false);
  }, [initialValues, reset]);

  const handleLogoUpload = async (fileList?: FileList | null) => {
    const file = fileList?.[0];
    if (!file) {
      return;
    }
    setFeedback(null);
    setLogoFile(file);
    setLogoPreview(URL.createObjectURL(file));
    setValue("logo_university", file.name, { shouldDirty: true });
  };

  const handleDepartmentLogoUpload = async (fileList?: FileList | null) => {
    const file = fileList?.[0];
    if (!file) {
      return;
    }
    setFeedback(null);
    setDepartmentLogoFile(file);
    setDepartmentLogoPreview(URL.createObjectURL(file));
    setValue("logo_departement", file.name, { shouldDirty: true });
  };

  const resizeCanvas = () => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    const ratio = window.devicePixelRatio || 1;
    const desiredHeight = 200;
    const width = canvas.offsetWidth || 600;
    canvas.width = width * ratio;
    canvas.height = desiredHeight * ratio;
    const ctx = canvas.getContext("2d");
    if (ctx) {
      ctx.setTransform(1, 0, 0, 1, 0, 0); // reset any previous scale
      ctx.scale(ratio, ratio);
      ctx.lineWidth = 2;
      ctx.lineCap = "round";
      ctx.strokeStyle = "#111827";
    }
  };

  useEffect(() => {
    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);
    return () => window.removeEventListener("resize", resizeCanvas);
  }, []);

  const getCoordinates = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return { x: 0, y: 0 };
    }
    const rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  };

  const handlePointerDown = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    canvas.setPointerCapture(event.pointerId);
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      return;
    }
    const { x, y } = getCoordinates(event);
    isDrawingRef.current = true;
    lastPointRef.current = { x, y };
    ctx.beginPath();
    ctx.moveTo(x, y);
  };

  const handlePointerMove = (event: PointerEvent<HTMLCanvasElement>) => {
    if (!isDrawingRef.current) {
      return;
    }
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (!canvas || !ctx) {
      return;
    }
    const { x, y } = getCoordinates(event);
    const lastPoint = lastPointRef.current;
    if (lastPoint) {
      ctx.moveTo(lastPoint.x, lastPoint.y);
    }
    ctx.lineTo(x, y);
    ctx.stroke();
    lastPointRef.current = { x, y };
  };

  const handlePointerUp = (event: PointerEvent<HTMLCanvasElement>) => {
    const canvas = canvasRef.current;
    if (canvas) {
      canvas.releasePointerCapture(event.pointerId);
    }
    isDrawingRef.current = false;
    lastPointRef.current = null;
    setSignatureDirty(true);
  };

  const clearSignature = () => {
    const canvas = canvasRef.current;
    const ctx = canvas?.getContext("2d");
    if (canvas && ctx) {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      setSignaturePreview(null);
      setSignatureDirty(false);
      setValue("admin_signature", "", { shouldDirty: true });
    }
  };

  const canvasToBlob = async (): Promise<Blob | null> =>
    new Promise((resolve) => {
      const canvas = canvasRef.current;
      if (!canvas) {
        resolve(null);
        return;
      }
      canvas.toBlob((blob) => resolve(blob), "image/png");
    });

  const onSubmit = handleSubmit(async (values) => {
    setFeedback(null);
    try {
      const preparedValues = { ...values };

      if (logoFile) {
        const uploadedLogo = await uploadFile.mutateAsync({
          file: logoFile,
          payload: { type: "image", name: logoFile.name }
        });
        preparedValues.logo_university = normalizeStoredPath(uploadedLogo.path);
        setLogoPreview(resolveFileUrl(uploadedLogo.path));
        setValue("logo_university", preparedValues.logo_university, {
          shouldDirty: false
        });
      }

      if (departmentLogoFile) {
        const uploadedDeptLogo = await uploadFile.mutateAsync({
          file: departmentLogoFile,
          payload: { type: "image", name: departmentLogoFile.name }
        });
        preparedValues.logo_departement = normalizeStoredPath(
          uploadedDeptLogo.path
        );
        setDepartmentLogoPreview(resolveFileUrl(uploadedDeptLogo.path));
        setValue("logo_departement", preparedValues.logo_departement, {
          shouldDirty: false
        });
      }

      if (signatureDirty) {
        const blob = await canvasToBlob();
        if (!blob) {
          throw new Error("Unable to read signature.");
        }
        const sigFile = new File([blob], "signature.png", {
          type: "image/png"
        });
        const uploadedSignature = await uploadFile.mutateAsync({
          file: sigFile,
          payload: { type: "image", name: "signature.png" }
        });
        preparedValues.admin_signature = normalizeStoredPath(
          uploadedSignature.path
        );
        setSignaturePreview(resolveFileUrl(uploadedSignature.path));
        setValue("admin_signature", preparedValues.admin_signature, {
          shouldDirty: false
        });
      }

      await saveUniversity.mutateAsync({
        id: university?.id,
        payload: toPayload(preparedValues)
      });
      setFeedback({
        type: "success",
        text: "University information saved successfully."
      });
      setLogoFile(null);
      setDepartmentLogoFile(null);
      setSignatureDirty(false);
    } catch (mutationError) {
      const message =
        mutationError instanceof Error
          ? mutationError.message
          : "Unable to save changes. Please try again.";
      setFeedback({ type: "error", text: message });
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            University info
          </h1>
          <p className="text-sm text-muted-foreground">
            Keep the university identity details up to date for generated
            documents and emails.
          </p>
        </div>
        <Button
          type="button"
          onClick={onSubmit}
          disabled={isSubmitting || saveUniversity.isPending}
        >
          {isSubmitting || saveUniversity.isPending
            ? "Saving…"
            : "Save changes"}
        </Button>
      </div>

      {isError ? (
        <div className="rounded-md border border-destructive/50 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          {error instanceof Error
            ? error.message
            : "Unable to load university information."}
        </div>
      ) : null}

      {feedback ? (
        <div
          className={cn(
            "rounded-md border px-4 py-3 text-sm",
            feedback.type === "success"
              ? "border-emerald-500/50 bg-emerald-500/10 text-emerald-700"
              : "border-destructive/50 bg-destructive/10 text-destructive"
          )}
        >
          {feedback.text}
        </div>
      ) : null}

      <form
        className="grid gap-6 rounded-lg border bg-background p-6 shadow-sm"
        onSubmit={onSubmit}
      >
        <input type="hidden" {...register("logo_university")} />
        <input type="hidden" {...register("logo_departement")} />
        <input type="hidden" {...register("admin_signature")} />

        <div className="grid gap-4 rounded-lg border bg-muted/20 p-4 md:grid-cols-2">
          <div className="flex items-center gap-3">
            <div className="relative h-20 w-20 overflow-hidden rounded-md border bg-background">
              {logoPreview ? (
                <img
                  src={logoPreview}
                  alt="University logo preview"
                  className="h-full w-full object-contain"
                />
              ) : (
                <div className="flex h-full w-full items-center justify-center text-xs text-muted-foreground">
                  No logo
                </div>
              )}
              <input
                ref={logoInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(event) => handleLogoUpload(event.target.files)}
              />
              <Button
                type="button"
                size="icon"
                variant="secondary"
                className="absolute bottom-1 right-1 h-8 w-8 rounded-full shadow-sm"
                onClick={() => logoInputRef.current?.click()}
              >
                <Pencil className="h-4 w-4" />
              </Button>
            </div>
            <div>
              <p className="text-sm font-medium">University logo</p>
              <p className="text-xs text-muted-foreground">
                Click the pencil to change the logo. Upload occurs on save.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="relative h-20 w-20 overflow-hidden rounded-md border bg-background">
              {departmentLogoPreview ? (
                <img
                  src={departmentLogoPreview}
                  alt="Department logo preview"
                  className="h-full w-full object-contain"
                />
              ) : (
                <div className="flex h-full w-full items-center justify-center text-xs text-muted-foreground">
                  No logo
                </div>
              )}
              <input
                ref={departmentLogoInputRef}
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(event) =>
                  handleDepartmentLogoUpload(event.target.files)
                }
              />
              <Button
                type="button"
                size="icon"
                variant="secondary"
                className="absolute bottom-1 right-1 h-8 w-8 rounded-full shadow-sm"
                onClick={() => departmentLogoInputRef.current?.click()}
              >
                <Pencil className="h-4 w-4" />
              </Button>
            </div>
            <div>
              <p className="text-sm font-medium">Department logo</p>
              <p className="text-xs text-muted-foreground">
                Click the pencil to change the logo. Upload occurs on save.
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="province">
              Province *
            </label>
            <Input
              id="province"
              placeholder="e.g. Antananarivo"
              className={cn(
                errors.province && "border-destructive text-destructive"
              )}
              {...register("province", { required: "Province is required" })}
            />
            {errors.province ? (
              <p className="text-xs text-destructive">
                {errors.province.message}
              </p>
            ) : null}
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="department_name">
              Department name
            </label>
            <Input
              id="department_name"
              placeholder="Department of Computer Science"
              {...register("department_name")}
            />
          </div>
        </div>

        <div className="space-y-2">
          <label
            className="text-sm font-medium"
            htmlFor="department_other_information"
          >
            Department other information
          </label>
          <Input
            id="department_other_information"
            placeholder="Additional details"
            {...register("department_other_information")}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="department_address">
            Department address
          </label>
          <Textarea
            id="department_address"
            rows={3}
            placeholder="Street, city, country"
            {...register("department_address")}
          />
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="email">
              Email *
            </label>
            <Input
              id="email"
              type="email"
              placeholder="contact@university.tld"
              className={cn(
                errors.email && "border-destructive text-destructive"
              )}
              {...register("email", { required: "Email is required" })}
            />
            {errors.email ? (
              <p className="text-xs text-destructive">{errors.email.message}</p>
            ) : null}
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="phone_number">
              Phone number
            </label>
            <Input
              id="phone_number"
              placeholder="+261 34 12 345 67"
              {...register("phone_number")}
            />
          </div>
        </div>

        <div className="space-y-4 rounded-lg border p-4">
          <div className="flex items-center justify-between gap-2">
            <div>
              <p className="text-sm font-medium">Admin signature</p>
              <p className="text-xs text-muted-foreground">
                Draw the signature. It will be uploaded when you click "Save
                changes".
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowSignature((prev) => !prev)}
              >
                {showSignature ? (
                  <>
                    <EyeOff className="mr-2 h-4 w-4" />
                    Hide
                  </>
                ) : (
                  <>
                    <Eye className="mr-2 h-4 w-4" />
                    Show
                  </>
                )}
              </Button>
              <Button type="button" variant="outline" onClick={clearSignature}>
                Clear
              </Button>
            </div>
          </div>
          {showSignature ? (
            <div className="flex items-center gap-2">
              <div className="rounded-md border bg-white">
                <canvas
                  ref={canvasRef}
                  className="h-[250px] w-[250px] touch-none"
                  onPointerDown={handlePointerDown}
                  onPointerMove={handlePointerMove}
                  onPointerUp={handlePointerUp}
                  onPointerLeave={handlePointerUp}
                />
              </div>
              <div className="space-y-2">
                {signaturePreview ? (
                  <div className="flex items-start gap-3 rounded-md border bg-muted/30">
                    <div className="h-[250px] w-[300px] overflow-hidden rounded bg-background">
                      <img
                        src={signaturePreview}
                        alt="Signature preview"
                        className="h-full w-full object-contain"
                      />
                    </div>
                    <div className="text-xs text-muted-foreground break-all">
                      <p className="font-medium text-foreground">
                        Current signature
                      </p>
                    </div>
                  </div>
                ) : (
                  <p className="text-xs text-muted-foreground">
                    Draw inside the box above, then click "Save changes".
                  </p>
                )}
              </div>
            </div>
          ) : null}
        </div>

        <div className="flex items-center justify-end gap-2">
          <Button
            type="button"
            variant="outline"
            onClick={() => reset(initialValues)}
            disabled={isPending}
          >
            Reset
          </Button>
          <Button
            type="submit"
            disabled={isSubmitting || saveUniversity.isPending}
          >
            {isSubmitting || saveUniversity.isPending
              ? "Saving…"
              : "Save changes"}
          </Button>
        </div>
      </form>
    </div>
  );
};
