import type { Metadata } from "next";
import type { ReactNode } from "react";

import "./globals.css";

type RootLayoutProps = {
  children: ReactNode;
};

export const metadata: Metadata = {
  title: "TaskFlow AI Assistant | Project Foundation",
  description:
    "Phase 2 project foundation for the fictional TaskFlow customer-support knowledge assistant.",
};

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
