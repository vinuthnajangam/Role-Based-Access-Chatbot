import type { Metadata } from "next";
// Default create-next-app uses imports from 'next/font/google' usually, trying to match template.
// But template was 'app-tw' (minimal?). Let's check imports.
// Assuming Inter is safe.
import { Inter } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "RBAC Chatbot",
  description: "Secure Enterprise RAG System",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-black text-white antialiased`}>
        {children}
        <Toaster />
      </body>
    </html>
  );
}
