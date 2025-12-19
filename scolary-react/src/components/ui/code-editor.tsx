import Editor from "react-simple-code-editor";
import Prism from "prismjs";
import "prismjs/components/prism-markup-templating";
import "prismjs/components/prism-css";
import "prismjs/components/prism-json";
import "prismjs/themes/prism-tomorrow.css";

import { cn } from "../../lib/utils";

type SupportedLanguage = "html" | "css" | "json";

export interface CodeEditorProps {
  id?: string;
  value: string;
  onChange: (value: string) => void;
  language: SupportedLanguage;
  className?: string;
  placeholder?: string;
  disabled?: boolean;
  minHeight?: number;
}

const languageMap: Record<SupportedLanguage, Prism.Grammar> = {
  html: Prism.languages.markup,
  css: Prism.languages.css,
  json: Prism.languages.json
};

export const CodeEditor = ({
  id,
  value,
  onChange,
  language,
  className,
  placeholder,
  disabled,
  minHeight = 260
}: CodeEditorProps) => {
  const highlight = (code: string) =>
    Prism.highlight(code, languageMap[language], language);

  return (
    <div
      className={cn(
        "rounded-md border bg-background text-sm shadow-sm focus-within:ring-2 focus-within:ring-ring focus-within:ring-offset-2",
        disabled && "opacity-60",
        className
      )}
    >
      <Editor
        value={value}
        onValueChange={onChange}
        highlight={highlight}
        padding={12}
        textareaId={id}
        disabled={disabled}
        textareaClassName="font-mono outline-none"
        placeholder={placeholder}
        style={{
          minHeight,
          maxHeight: 320,
          overflow: "auto",
          fontFamily:
            "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace",
          background: "transparent"
        }}
      />
    </div>
  );
};
