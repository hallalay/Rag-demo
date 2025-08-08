'use client';
import React, { useState } from 'react';
import { ask } from '../api';

interface Props {
  docIds: string[];
  onAnswer: (res: any) => void;
}

export default function QueryBox({ docIds, onAnswer }: Props) {
  const [question, setQuestion] = useState('');
  const submit = async () => {
    const res = await ask(question, docIds);
    onAnswer(res);
  };
  return (
    <div className="my-2">
      <input
        value={question}
        onChange={e => setQuestion(e.target.value)}
        className="border p-1 mr-2"
      />
      <button onClick={submit} className="px-2 py-1 bg-blue-500 text-white">
        Ask
      </button>
    </div>
  );
}
