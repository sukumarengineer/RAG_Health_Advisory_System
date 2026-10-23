import { Link } from 'react-router-dom';

export default function HomePage() {
    return (
        <div className="space-y-4">
            <h1 className="text-3xl font-bold text-teal-900">Native Language Health Advisory</h1>
            <p className="text-gray-700">
                Upload WHO guidelines and health ministry documents, then ask plain-English health questions
                and get a clear answer — symptoms, prevention steps, and when to seek care — in the language
                you choose. Every answer comes with a source and a visible medical disclaimer.
            </p>
            <p className="text-sm text-gray-500">
                This is an informational tool, not a substitute for professional medical advice. Always
                consult a healthcare professional for real symptoms, and emergency services for urgent ones.
            </p>
            <div className="flex gap-4">
                <Link to="/ask" className="bg-teal-700 text-white px-4 py-2 rounded">Ask a Question</Link>
                <Link to="/upload" className="border border-teal-700 text-teal-700 px-4 py-2 rounded">
                    Upload a Document
                </Link>
            </div>
        </div>
    );
}