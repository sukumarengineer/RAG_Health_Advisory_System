// Frontend/src/pages/LibraryPage.jsx
import { useEffect, useState } from 'react';
import { listDocuments, deleteDocument } from '../lib/api';

export default function LibraryPage() {
    const [documents, setDocuments] = useState([]);
    const [status, setStatus] = useState('loading'); // 'loading' | 'ready' | 'error'
    const [confirmingId, setConfirmingId] = useState(null);

    useEffect(() => {
        listDocuments()
            .then((docs) => { setDocuments(docs); setStatus('ready'); })
            .catch(() => setStatus('error'));
    }, []);

    async function handleDelete(id) {
        await deleteDocument(id);
        setDocuments((docs) => docs.filter((d) => d.id !== id));
        setConfirmingId(null);
    }

    if (status === 'loading') return <p>Loading your library…</p>;
    if (status === 'error') return <p className="text-red-600">Couldn't load your documents.</p>;

    return (
        <div className="space-y-4">
            <h1 className="text-2xl font-bold text-teal-900">Document Library</h1>

            {documents.length === 0 && (
                <p className="text-gray-600">
                    No documents yet — <a href="/upload" className="text-teal-700 underline">upload one</a> to get started.
                </p>
            )}

            <div className="space-y-3">
                {documents.map((doc) => (
                    <div key={doc.id} className="border rounded p-4 bg-white flex justify-between items-start">
                        <div>
                            <p className="font-semibold">{doc.title}</p>
                            {!doc.collection_reference && (
                                <p className="text-amber-600 text-sm mt-1">Not indexed yet — try re-uploading.</p>
                            )}
                        </div>

                        {confirmingId === doc.id ? (
                            <div className="flex gap-2">
                                <button onClick={() => handleDelete(doc.id)} className="text-red-600 font-medium">Confirm</button>
                                <button onClick={() => setConfirmingId(null)} className="text-gray-500">Cancel</button>
                            </div>
                        ) : (
                            <button onClick={() => setConfirmingId(doc.id)} className="text-red-500">Delete</button>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}