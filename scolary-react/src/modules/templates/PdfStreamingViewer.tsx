import { useEffect, useRef, useState } from "react";
import {
  GlobalWorkerOptions,
  getDocument,
  type PDFDocumentProxy
} from "pdfjs-dist";

// Serve worker from /public for both dev and prod
GlobalWorkerOptions.workerSrc = "/pdf.worker.min.mjs";

type PdfStreamingViewerProps = {
  pdfUrl: string;
  readyPage: number | null; // last generated page or null to render all
  resetKey: string | null; // unique per job/file to reset viewer
};

export function PdfStreamingViewer({
  pdfUrl,
  readyPage,
  resetKey
}: PdfStreamingViewerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [lastRenderedPage, setLastRenderedPage] = useState(0);

  const selectedPageRef = useRef<number | null>(null);
  const selectedWrapperRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    setLastRenderedPage(0);
    selectedPageRef.current = null;
    selectedWrapperRef.current = null;
    if (containerRef.current) {
      containerRef.current.innerHTML = "";
    }
  }, [resetKey, pdfUrl]);

  useEffect(() => {
    if (!pdfUrl || !containerRef.current) return;

    let cancelled = false;

    (async () => {
      try {
        const resp = await fetch(pdfUrl, { credentials: "include" });
        const buf = await resp.arrayBuffer();
        const pdf: PDFDocumentProxy = await getDocument({ data: buf }).promise;

        // Streaming mode: only render new pages
        if (readyPage && readyPage > lastRenderedPage) {
          await renderPagesRange({
            pdf,
            container: containerRef.current!,
            startPage: lastRenderedPage + 1,
            endPage: readyPage,
            cancelledRef: () => cancelled,
            onPageRendered: (pageNum) => {
              selectedPageRef.current ??= pageNum;
            },
            selectedWrapperRef
          });

          if (!cancelled) {
            setLastRenderedPage(readyPage);
          }
          return;
        }

        // Non-streaming: render whole document once
        if (readyPage == null && lastRenderedPage === 0) {
          const totalPages = pdf.numPages;
          await renderPagesRange({
            pdf,
            container: containerRef.current!,
            startPage: 1,
            endPage: totalPages,
            cancelledRef: () => cancelled,
            onPageRendered: (pageNum) => {
              selectedPageRef.current ??= pageNum;
            },
            selectedWrapperRef
          });

          if (!cancelled) {
            setLastRenderedPage(totalPages);
          }
        }
      } catch (error) {
        console.error("Error rendering streaming PDF:", error);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [pdfUrl, readyPage, lastRenderedPage]);

  return (
    <div
      ref={containerRef}
      className="w-full h-full overflow-y-auto bg-muted/20"
      style={{ maxHeight: "80vh", padding: "16px" }}
    />
  );
}

async function renderPagesRange(options: {
  pdf: PDFDocumentProxy;
  container: HTMLDivElement;
  startPage: number;
  endPage: number;
  cancelledRef: () => boolean;
  onPageRendered?: (pageNum: number) => void;
  selectedWrapperRef: React.MutableRefObject<HTMLDivElement | null>;
}) {
  const {
    pdf,
    container,
    startPage,
    endPage,
    cancelledRef,
    onPageRendered,
    selectedWrapperRef
  } = options;

  for (let pageNum = startPage; pageNum <= endPage; pageNum++) {
    if (cancelledRef()) break;

    const page = await pdf.getPage(pageNum);
    const viewport = page.getViewport({ scale: 1.2 }); // 120% zoom

    const canvas = document.createElement("canvas");
    const context = canvas.getContext("2d");
    if (!context) continue;

    canvas.width = viewport.width;
    canvas.height = viewport.height;

    const pageWrapper = document.createElement("div");
    pageWrapper.style.position = "relative";
    pageWrapper.style.background = "white";
    pageWrapper.style.padding = "16px";
    pageWrapper.style.margin = "0 auto 24px auto";
    pageWrapper.style.borderRadius = "10px";
    pageWrapper.style.border = "1px solid rgba(15, 23, 42, 0.14)";
    pageWrapper.style.boxShadow = "0 8px 24px rgba(15, 23, 42, 0.18)";
    pageWrapper.style.width = `${viewport.width}px`;
    pageWrapper.style.boxSizing = "content-box";
    pageWrapper.style.transition =
      "box-shadow 0.18s ease, transform 0.18s ease, border-color 0.18s ease, background-color 0.18s ease, opacity 0.25s ease";
    pageWrapper.style.cursor = "pointer";
    pageWrapper.style.opacity = "0";

    canvas.style.display = "block";
    canvas.style.borderRadius = "6px";

    const pageLabel = document.createElement("div");
    pageLabel.textContent = `Page ${pageNum}`;
    pageLabel.style.position = "absolute";
    pageLabel.style.left = "16px";
    pageLabel.style.bottom = "10px";
    pageLabel.style.fontSize = "11px";
    pageLabel.style.fontFamily =
      "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
    pageLabel.style.color = "rgba(55,65,81,0.9)";
    pageLabel.style.padding = "2px 8px";
    pageLabel.style.borderRadius = "999px";
    pageLabel.style.background = "rgba(243,244,246,0.92)";
    pageLabel.style.border = "1px solid rgba(209,213,219,0.9)";
    pageLabel.style.backdropFilter = "blur(4px)";

    pageWrapper.appendChild(canvas);
    pageWrapper.appendChild(pageLabel);
    container.appendChild(pageWrapper);

    pageWrapper.addEventListener("mouseenter", () => {
      if (selectedWrapperRef.current !== pageWrapper) {
        pageWrapper.style.transform = "translateY(-2px)";
        pageWrapper.style.boxShadow = "0 12px 30px rgba(15, 23, 42, 0.25)";
      }
    });
    pageWrapper.addEventListener("mouseleave", () => {
      if (selectedWrapperRef.current !== pageWrapper) {
        pageWrapper.style.transform = "translateY(0)";
        pageWrapper.style.boxShadow = "0 8px 24px rgba(15, 23, 42, 0.18)";
      }
    });

    pageWrapper.addEventListener("click", () => {
      if (selectedWrapperRef.current) {
        selectedWrapperRef.current.style.border =
          "1px solid rgba(15, 23, 42, 0.14)";
        selectedWrapperRef.current.style.background = "white";
        selectedWrapperRef.current.style.boxShadow =
          "0 8px 24px rgba(15, 23, 42, 0.18)";
        selectedWrapperRef.current.style.transform = "translateY(0)";
      }

      selectedWrapperRef.current = pageWrapper;
      pageWrapper.style.border = "1px solid rgba(59,130,246,0.85)";
      pageWrapper.style.background = "rgba(239,246,255,0.9)";
      pageWrapper.style.boxShadow = "0 14px 36px rgba(37, 99, 235, 0.35)";
    });

    requestAnimationFrame(() => {
      pageWrapper.style.opacity = "1";
    });

    await page.render({
      canvasContext: context,
      viewport
    }).promise;

    onPageRendered?.(pageNum);
  }
}
