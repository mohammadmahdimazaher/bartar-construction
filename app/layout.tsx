
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "StartUp | شرکت ساختمانی",
  description: "معرفی پروژه‌ها و خدمات ساختمانی",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
