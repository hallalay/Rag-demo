'use client';
import React from 'react';
import { uploadFiles } from '../api';

export default function Upload({ onUploaded }: { onUploaded: () => void }) {
  const handle = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return;
    await uploadFiles(Array.from(e.target.files));
    onUploaded();
  };
  return <input type="file" multiple onChange={handle} className="my-2" />;
}
