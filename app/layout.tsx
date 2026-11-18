
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "گروه ساختمانی برتر",
    template: "%s | گروه ساختمانی برتر",
  },
  description: "معرفی پروژه‌های ساختمانی، مشخصات فنی، وضعیت اجرایی و خدمات گروه ساختمانی برتر.",
  openGraph: {
    type: "website",
    locale: "fa_IR",
    siteName: "گروه ساختمانی برتر",
    title: "گروه ساختمانی برتر",
    description: "معرفی پروژه‌ها و خدمات گروه ساختمانی برتر.",
  },
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
