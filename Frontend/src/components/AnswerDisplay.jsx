export default function AnswerDisplay({ answer }) {
    return (
        <div className="space-y-4">
            <div className="border-2 border-red-400 bg-red-50 rounded-lg p-4">
                <p className="font-bold text-red-800 uppercase text-xs tracking-wide mb-1">Medical Disclaimer</p>
                <p className="text-red-900 text-sm">{answer.disclaimer}</p>
            </div>

            <p className="text-gray-800">{answer.symptom_summary}</p>

            {answer.prevention_steps.length > 0 && (
                <div>
                    <p className="font-medium text-gray-700 mb-1">Prevention</p>
                    <ul className="list-disc list-inside space-y-1">
                        {answer.prevention_steps.map((step, i) => <li key={i}>{step}</li>)}
                    </ul>
                </div>
            )}

            <div className="border-2 border-amber-400 bg-amber-50 rounded-lg p-4">
                <p className="font-bold text-amber-800 text-xs uppercase tracking-wide mb-1">When to Seek Care</p>
                <p className="text-amber-900 text-sm">{answer.when_to_seek_care}</p>
            </div>

            {answer.sources.length > 0 && (
                <div>
                    <p className="font-medium text-sm text-gray-600 mt-2">Sources</p>
                    <ul className="text-sm text-gray-600">
                        {answer.sources.map((s, i) => <li key={i}>{s}</li>)}
                    </ul>
                </div>
            )}
        </div>
    );
}