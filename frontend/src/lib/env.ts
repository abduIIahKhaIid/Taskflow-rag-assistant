import { z } from "zod";

const optionalUrl = z.preprocess(
  (value) => (value === "" ? undefined : value),
  z.string().url().optional(),
);

const optionalString = z.preprocess(
  (value) => (value === "" ? undefined : value),
  z.string().min(1).optional(),
);

const publicEnvironmentSchema = z.object({
  apiBaseUrl: z
    .string()
    .url()
    .default("http://localhost:8000")
    .transform((value) => value.replace(/\/+$/, "")),
  supabaseUrl: optionalUrl,
  supabasePublishableKey: optionalString,
});

export type PublicEnvironment = z.infer<typeof publicEnvironmentSchema>;

export function readPublicEnvironment(): PublicEnvironment {
  return publicEnvironmentSchema.parse({
    apiBaseUrl: process.env.NEXT_PUBLIC_API_BASE_URL,
    supabaseUrl: process.env.NEXT_PUBLIC_SUPABASE_URL,
    supabasePublishableKey: process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY,
  });
}
