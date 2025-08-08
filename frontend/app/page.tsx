'use client';
import React, { useEffect, useState } from 'react';
import Upload from './components/Upload';
import Sources from './components/Sources';
import QueryBox from './components/QueryBox';
import Result from './components/Result';
import { getSources } from './api';

interface Doc { id: string; title: string }

export default function Page() {
  const [docs, setDocs] = useState<Doc[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [result, setResult] = useState<{ answer: string; citations: any[] }>({
    answer: '',
    citations: [],
  });

  const load = async () => {
    const data = await getSources();
    setDocs(data.docs || []);
  };

  useEffect(() => {
    load();
  }, []);

  const toggle = (id: string) => {
    setSelected(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  return (
    <main className="p-4">
      <Upload onUploaded={load} />
      <Sources docs={docs} selected={selected} toggle={toggle} />
      <QueryBox docIds={selected} onAnswer={setResult} />
      <Result answer={result.answer} citations={result.citations} />
    </main>
  );
}
