import React, { useState, useEffect, useRef } from 'react';
import Swal from 'sweetalert2';

function App() {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({ title: '', content: '', imageUrl: null });
  const [editingNoteId, setEditingNoteId] = useState(null);
  const [editingNoteContent, setEditingNoteContent] = useState('');
  const [isImageUploading, setIsImageUploading] = useState(false);
  const fileInputRef = useRef();

  // Function to handle image upload
  const handleImageUpload = async (event) => {
    setIsImageUploading(true);  // set isImageUploading to true when image upload starts
    const file = event.target.files[0];
    if (file) {
      const convertedFile = await convertToBase64(file);
      const data = {
        file: convertedFile,
        filename: file.name
      };

      // Post request to upload image
      const response = await fetch(import.meta.env.VITE_REACT_APP_IMAGE_UPLOAD, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      const responseData = await response.json();
      setNewNote({ ...newNote, imageUrl: responseData.imageUrl });
    }
    setIsImageUploading(false);  // set isImageUploading back to false when image upload is complete or if no image is being uploaded
  };

  // Function to convert file to base64
  const convertToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            const base64String = reader.result;
            const pureBase64Image = base64String.split(',')[1]; 
            resolve(pureBase64Image);
        };
        reader.onerror = error => reject(error);
    });
  };

  // Fetch notes on component mount and when notes state changes
  useEffect(() => {
    fetchNotes();
  }, [notes]);

  // Function to fetch notes
  const fetchNotes = async () => {
    const response = await fetch(import.meta.env.VITE_REACT_APP_GET_NOTES);
    const data = await response.json();
    setNotes(data);
  };

  // Function to create a new note
  const createNote = async () => {
    if (!newNote.title || !newNote.content) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: 'Note title and content cannot be empty!',
      });
      return;
    }
  
    // Post request to create a new note
    const response = await fetch(import.meta.env.VITE_REACT_APP_CREATE_NOTE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newNote),
    });
  
    const noteId = await response.json();
  
    // Add the new note to the notes state and reset the new note state
    setNotes(prevNotes => [...prevNotes, { ...newNote, id: noteId }]);
    setNewNote({ title: '', content: '', imageUrl: '' });
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Function to start editing a note
  const startEditingNote = (id, content) => {
    setEditingNoteId(id);
    setEditingNoteContent(content);
  };

  // Function to finish editing a note
  const finishEditingNote = async () => {
    const newContent = typeof editingNoteContent === 'object' ? { content: editingNoteContent.content } : { content: editingNoteContent };

    // Put request to update the note
    await fetch(`${import.meta.env.VITE_REACT_APP_EDIT_NOTE}/${editingNoteId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newContent),
    });

    // Update the note in the notes state and reset the editing note id and content
    setNotes(prevNotes => prevNotes.map(note => note.id === editingNoteId ? { ...note, ...newContent } : note));
    setEditingNoteId(null);
    setEditingNoteContent('');
  };

  // Function to delete a note
  const deleteNote = async (noteId) => {
    try {
      // Ensure noteId is a string or number, not an object
      const id = typeof noteId === 'object' ? noteId.id : noteId;
  
      // Delete request to delete the note
      const response = await fetch(`${import.meta.env.VITE_REACT_APP_DELETE_NOTE}/${id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const responseData = await response.json();

      // Remove the note from the notes state
      setNotes(prevNotes => prevNotes.filter(note => note.id !== noteId));
      
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <>
      <div className="max-w-xl mx-auto mt-36">
        <h1 className="text-3xl font-bold text-center mb-9 text-sky-700">NOTES APP</h1>
        <input className="border p-2 w-full" value={newNote.title} onChange={e => setNewNote({ ...newNote, title: e.target.value })} placeholder="Note title" />
        <input className="border p-2 w-full mt-2" value={newNote.content} onChange={e => setNewNote({ ...newNote, content: e.target.value })} placeholder="Note content" />
        <input ref={fileInputRef} className="border p-2 w-full mt-2" type="file" onChange={handleImageUpload} />
        <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={createNote} disabled={isImageUploading}>Create Note</button>
        {notes.map(note => (
          <div key={note.id} className="border m-2 p-2">
            <h2 className="font-bold text-xl">{note.title}</h2>
            {note.imageUrl && <img className="w-full h-auto" src={note.imageUrl} alt={note.title} />}
            {note.id === editingNoteId ? (
              <input className="border p-2 w-full mt-2" value={editingNoteContent} onChange={e => setEditingNoteContent(e.target.value)} onBlur={finishEditingNote} autoFocus />
            ) : (
              <p className="mt-2 cursor-pointer" onClick={() => startEditingNote(note.id, note.content)}>{note.content}</p>
            )}
            <button className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mt-2" onClick={() => deleteNote(note.id)}>Delete</button>
          </div>
        ))}
      </div>
      <footer className="bg-white rounded-lg shadow m-4">
          <div className="w-full mx-auto max-w-screen-xl p-4">
            <h1 className="text-3xl text-center font-bold text-black-500 ">All Notes Are Public</h1>
          </div>
      </footer>
    </>
  );
}

export default App;