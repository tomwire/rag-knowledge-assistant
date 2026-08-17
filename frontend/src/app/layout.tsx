import React from 'react';

export const metadata = {
  title: 'RAG Knowledge Assistant',
  description: 'Semantic document search with retrieval-augmented generation',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
