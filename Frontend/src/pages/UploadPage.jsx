// Frontend/src/pages/UploadPage.jsx
import { useState } from 'react';
import { uploadDocument } from '../lib/api';

export default function UploadPage() {
    const [title, setTitle] = useState('');
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // 'idle' | 'submitting' | 'error'
    const [error, setError] = useState('');

    async function handleSubmit(e) {
        e.preventDefault();
        if (!title || !file) return;

        setStatus('submitting');
        setError('');
        try {
            await uploadDocument(title, file);
            setTitle('');
            setFile(null);
            setStatus('idle');
            alert('Document uploaded and indexed!');
        } catch (err) {
            setError(err.message);
            setStatus('error');
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <h1 className="text-2xl font-bold text-teal-900">Upload a Health Document</h1>
            <p className="text-gray-600 text-sm">
                A WHO guideline, health ministry advisory, or disease fact sheet — PDF, plain text, or Markdown.
            </p>

            <div>
                <label className="block font-medium mb-1">Title</label>
                <input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    disabled={status === 'submitting'}
                    className="border rounded px-3 py-2 w-full"
                    placeholder="e.g. WHO Dengue Fact Sheet"
                />
            </div>

            <div>
                <label className="block font-medium mb-1">Document (.pdf, .txt, or .md)</label>
                <input
                    type="file"
                    accept=".pdf,.txt,.md"
                    onChange={(e) => setFile(e.target.files[0])}
                    disabled={status === 'submitting'}
                />
            </div>

            {status === 'submitting' && (
                <p className="text-teal-700">Uploading and analyzing your document — this can take a few seconds…</p>
            )}
            {status === 'error' && <p className="text-red-600">{error}</p>}

            <button
                type="submit"
                disabled={status === 'submitting' || !title || !file}
                className="bg-teal-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
                Upload
            </button>
        </form>
    );
}