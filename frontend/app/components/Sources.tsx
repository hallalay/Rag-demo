'use client';
import React from 'react';

interface Doc { id: string; title: string }

interface Props {
  docs: Doc[];
  selected: string[];
  toggle: (id: string) => void;
}

export default function Sources({ docs, selected, toggle }: Props) {
  return (
    <div className="my-2">
      {docs.map(d => (
        <label key={d.id} className="block">
          <input
            type="checkbox"
            checked={selected.includes(d.id)}
            onChange={() => toggle(d.id)}
          />{' '}
          {d.title}
        </label>
      ))}
    </div>
  );
}
