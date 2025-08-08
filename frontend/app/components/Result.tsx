'use client';
import React from 'react';

interface Citation { docId: string; page: number; text: string }

interface Props {
  answer: string;
  citations: Citation[];
}

export default function Result({ answer, citations }: Props) {
  if (!answer) return null;
  return (
    <div className="my-4">
      <p>{answer}</p>
      {citations.map((c, i) => (
        <details key={i} className="my-2">
          <summary>
            {c.docId} p.{c.page}
          </summary>
          <p className="ml-4">{c.text}</p>
        </details>
      ))}
    </div>
  );
}
