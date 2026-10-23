// Frontend/src/lib/api.js
export const API_URL = import.meta.env.VITE_API_URL;

export async function uploadDocument(title, file) {
    const formData = new FormData();
    formData.append('title', title);
    formData.append('file', file);

    const response = await fetch(API_URL + '/api/documents', {
        method: 'POST',
        body: formData,
    });
    if (!response.ok) throw new Error('Upload failed');
    return response.json();
}

export async function listDocuments() {
    const response = await fetch(API_URL + '/api/documents');
    if (!response.ok) throw new Error('Failed to load documents');
    return response.json();
}

export async function deleteDocument(id) {
    const response = await fetch(API_URL + '/api/documents/' + id, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete document');
}

export async function askQuestion(question, language) {
    const response = await fetch(API_URL + '/api/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, language }),
    });
    if (!response.ok) throw new Error('Failed to get an answer');
    return response.json();
}

export async function listHistory() {
    const response = await fetch(API_URL + '/api/history');
    if (!response.ok) throw new Error('Failed to load history');
    return response.json();
}

export async function getHistoryEntry(id) {
    const response = await fetch(API_URL + '/api/history/' + id);
    if (!response.ok) throw new Error('Failed to load history entry');
    return response.json();
}

export async function deleteHistoryEntry(id) {
    const response = await fetch(API_URL + '/api/history/' + id, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete history entry');
}
