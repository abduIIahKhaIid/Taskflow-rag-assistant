import { render, screen } from "@testing-library/react";
import { beforeEach, expect, test, vi } from "vitest";

import { SystemStatus } from "@/components/system-status";

const configuredApiBaseUrl = "https://api.example.test";

beforeEach(() => {
  vi.stubEnv("NEXT_PUBLIC_API_BASE_URL", configuredApiBaseUrl);
});

function installFetchMock() {
  const fetchMock = vi.fn<typeof fetch>();
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

test("renders the loading state while the API request is pending", () => {
  const fetchMock = installFetchMock();
  fetchMock.mockImplementation(() => new Promise<Response>(() => undefined));

  render(<SystemStatus />);

  expect(screen.getByRole("status").textContent).toContain("Checking API...");
});

test("renders the connected state after a successful health request", async () => {
  const fetchMock = installFetchMock();
  fetchMock.mockResolvedValue(
    new Response(
      JSON.stringify({
        status: "ok",
        service: "taskflow-rag-api",
        version: "0.1.0",
        environment: "development",
      }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    ),
  );

  render(<SystemStatus />);

  expect((await screen.findByRole("status")).textContent).toContain("API connected");
});

test("renders the unavailable state after a failed health request", async () => {
  const fetchMock = installFetchMock();
  fetchMock.mockRejectedValue(new TypeError("Test-only network failure"));

  render(<SystemStatus />);

  expect((await screen.findByRole("status")).textContent).toContain("API unavailable");
});

test("uses the configured API base URL with Codespaces-compatible credentials", async () => {
  const fetchMock = installFetchMock();
  fetchMock.mockResolvedValue(
    new Response(
      JSON.stringify({
        status: "ok",
        service: "taskflow-rag-api",
        version: "0.1.0",
        environment: "development",
      }),
      { status: 200, headers: { "Content-Type": "application/json" } },
    ),
  );

  render(<SystemStatus />);
  await screen.findByText("API connected");

  const [requestUrl, requestOptions] = fetchMock.mock.calls[0];
  expect(requestUrl).toBe(`${configuredApiBaseUrl}/api/v1/health`);
  expect(requestOptions?.credentials).toBe("include");
  expect(requestOptions?.signal).toBeInstanceOf(AbortSignal);
});
