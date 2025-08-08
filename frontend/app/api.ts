const API_BASE = 'http://localhost:8000';

export async function uploadFiles(files: File[]) {
  const form = new FormData();
  files.forEach(f => form.append('files', f));
  const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: form });
  return res.json();
}

export async function getSources() {
  const res = await fetch(`${API_BASE}/sources`);
  return res.json();
}

export async function ask(question: string, docIds: string[]) {
  const res = await fetch(`${API_BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, docIds }),
  });
  return res.json();
}
