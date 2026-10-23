// Frontend/src/pages/AskPage.jsx
import { useState } from 'react';
import { askQuestion } from '../lib/api';
import LanguageSelector from '../components/LanguageSelector';
import AnswerDisplay from '../components/AnswerDisplay';

export default function AskPage() {
    const [question, setQuestion] = useState('');
    const [language, setLanguage] = useState(() => localStorage.getItem('healthLanguage') || 'English');
    const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'ready' | 'error'
    const [answer, setAnswer] = useState(null);

    function handleLanguageChange(lang) {
        setLanguage(lang);
        localStorage.setItem('healthLanguage', lang);
    }

    async function handleSubmit(e) {
        e.preventDefault();
        if (!question.trim()) return;

        setStatus('loading');
        try {
            const result = await askQuestion(question, language);
            setAnswer(result);
            setStatus('ready');
        } catch {
            setStatus('error');
        }
    }

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-teal-900">Ask a Health Question</h1>

            <form onSubmit={handleSubmit} className="space-y-3">
                <textarea
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="e.g. What are dengue symptoms?"
                    className="border rounded px-3 py-2 w-full"
                    rows={3}
                />

                <div className="flex items-center gap-3">
                    <label className="text-sm text-gray-600">Answer in:</label>
                    <LanguageSelector value={language} onChange={handleLanguageChange} />
                </div>

                <button
                    type="submit"
                    disabled={status === 'loading' || !question.trim()}
                    className="bg-teal-700 text-white px-4 py-2 rounded disabled:opacity-50"
                >
                    Ask
                </button>
            </form>

            {status === 'loading' && <p className="text-teal-700">Searching your documents…</p>}
            {status === 'error' && <p className="text-red-600">Something went wrong — try again.</p>}

            {status === 'ready' && answer && (
                <div className="border rounded p-4 bg-white">
                    <AnswerDisplay answer={answer} />
                </div>
            )}
        </div>
    );
}