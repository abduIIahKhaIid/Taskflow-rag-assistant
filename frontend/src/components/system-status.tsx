"use client";

import { useEffect, useState } from "react";

import { getBackendHealth } from "@/lib/api";

type ApiStatus = "checking" | "connected" | "unavailable";

const statusContent: Record<ApiStatus, { label: string; detail: string }> = {
  checking: {
    label: "Checking API...",
    detail: "Contacting the local FastAPI health endpoint.",
  },
  connected: {
    label: "API connected",
    detail: "The frontend received a valid backend health response.",
  },
  unavailable: {
    label: "API unavailable",
    detail: "Start the local FastAPI service, then refresh this page.",
  },
};

const healthRequestTimeoutMs = 6_000;

export function SystemStatus() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    const controller = new AbortController();
    let isActive = true;
    const timeoutId = window.setTimeout(() => {
      controller.abort();
      if (isActive) {
        setApiStatus("unavailable");
      }
    }, healthRequestTimeoutMs);

    async function checkHealth() {
      try {
        await getBackendHealth(controller.signal);
        if (isActive) {
          setApiStatus("connected");
        }
      } catch {
        if (isActive) {
          setApiStatus("unavailable");
        }
      } finally {
        window.clearTimeout(timeoutId);
      }
    }

    void checkHealth();

    return () => {
      isActive = false;
      window.clearTimeout(timeoutId);
      controller.abort();
    };
  }, []);

  const content = statusContent[apiStatus];

  return (
    <section className="system-status" aria-labelledby="system-status-heading">
      <p className="status-label" id="system-status-heading">
        Backend system status
      </p>
      <div className="status-row">
        <span className={`status-indicator ${apiStatus}`} aria-hidden="true" />
        <p className="status-text" role="status" aria-live="polite">
          {content.label}
        </p>
      </div>
      <p className="status-detail">{content.detail}</p>
      <code className="status-route">GET /api/v1/health</code>
    </section>
  );
}
