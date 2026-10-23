// Frontend/src/pages/HistoryPage.jsx
import { useEffect, useState } from 'react';
import { listHistory, getHistoryEntry, deleteHistoryEntry } from '../lib/api';
import AnswerDisplay from '../components/AnswerDisplay';

export default function HistoryPage() {
    const [entries, setEntries] = useState([]);
    const [status, setStatus] = useState('loading'); // 'loading' | 'ready' | 'error'
    const [expandedId, setExpandedId] = useState(null);
    const [detail, setDetail] = useState(null);

    useEffect(() => {
        listHistory()
            .then((data) => { setEntries(data); setStatus('ready'); })
            .catch(() => setStatus('error'));
    }, []);

    async function toggleExpand(id) {
        if (expandedId === id) {
            setExpandedId(null);
            setDetail(null);
            return;
        }
        setExpandedId(id);
        setDetail(await getHistoryEntry(id));
    }

    async function handleDelete(id) {
        await deleteHistoryEntry(id);
        setEntries((list) => list.filter((e) => e.id !== id));
        if (expandedId === id) { setExpandedId(null); setDetail(null); }
    }

    if (status === 'loading') return <p>Loading your history…</p>;
    if (status === 'error') return <p className="text-red-600">Couldn't load your history.</p>;

    return (
        <div className="space-y-4">
            <h1 className="text-2xl font-bold text-teal-900">Question History</h1>

            {entries.length === 0 && <p className="text-gray-600">No questions asked yet.</p>}

            <div className="space-y-2">
                {entries.map((entry) => (
                    <div key={entry.id} className="border rounded bg-white">
                        <div className="flex justify-between items-center p-3 cursor-pointer" onClick={() => toggleExpand(entry.id)}>
                            <div>
                                <p className="font-medium">{entry.question}</p>
                                <p className="text-sm text-gray-500">
                                    {entry.language} · {new Date(entry.created_at).toLocaleString()}
                                </p>
                            </div>
                            <button
                                onClick={(e) => { e.stopPropagation(); handleDelete(entry.id); }}
                                className="text-red-500 text-sm"
                            >
                                Delete
                            </button>
                        </div>

                        {expandedId === entry.id && detail && (
                            <div className="border-t p-3">
                                <AnswerDisplay answer={detail} />
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}