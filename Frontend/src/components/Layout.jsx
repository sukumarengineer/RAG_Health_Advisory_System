import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
    return (
        <div className="min-h-screen bg-teal-50">
            <nav className="bg-teal-800 text-white px-6 py-4 flex gap-6">
                <Link to="/" className="font-bold">Health Advisory</Link>
                <Link to="/ask">Ask a Question</Link>
                <Link to="/upload">Upload Document</Link>
                <Link to="/library">Library</Link>
                <Link to="/history">History</Link>
            </nav>
            <main className="max-w-3xl mx-auto p-6">
                <Outlet />
            </main>
        </div>
    );
}