// Frontend/src/components/LanguageSelector.jsx
const LANGUAGES = ['English', 'Hindi', 'Telugu', 'Tamil', 'Marathi', 'Kannada', 'Bengali', 'Gujarati'];

export default function LanguageSelector({ value, onChange }) {
    return (
        <select
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="border rounded px-3 py-2"
        >
            {LANGUAGES.map((lang) => <option key={lang} value={lang}>{lang}</option>)}
        </select>
    );
}