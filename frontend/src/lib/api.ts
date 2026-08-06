import { z } from "zod";

import { readPublicEnvironment } from "@/lib/env";

const healthResponseSchema = z.object({
  status: z.literal("ok"),
  service: z.literal("taskflow-rag-api"),
  version: z.string(),
  environment: z.string(),
});

export type HealthResponse = z.infer<typeof healthResponseSchema>;

export async function getBackendHealth(signal: AbortSignal): Promise<HealthResponse> {
  const { apiBaseUrl } = readPublicEnvironment();
  const response = await fetch(`${apiBaseUrl}/api/v1/health`, {
    method: "GET",
    headers: { Accept: "application/json" },
    credentials: "include",
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error("Backend health request failed.");
  }

  return healthResponseSchema.parse(await response.json());
}
