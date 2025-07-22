import React, { useState } from "react";
import axios from "axios";
import { Button, Snackbar, Alert } from '@mui/material';

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [file, setFile] = useState(null);
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [severity, setSeverity] = useState('success');
  const [open, setOpen] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [loadingChat, setLoadingChat] = useState(false);
  const [loadingAsk, setLoadingAsk] = useState(false);

  const sendMessage = async () => {
    setLoadingChat(true);
    try {
      const res = await axios.post("http://localhost:8000/chat", { message });
      setResponse(res.data.response);
    } catch (err) {
      setResponse("Error sending message.");
    } finally {
      setLoadingChat(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return alert("Select a file first.");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadMessage(res.data.message);
      setSeverity('success');
    } catch (err) {
      setUploadMessage(err.response?.data?.detail || 'Upload failed');
      setSeverity('error');
      alert("Upload failed");
      console.error(err);
    }
    finally {
      setOpen(true);
    }
  };

  const askDocument = async () => {
    setLoadingAsk(true);
    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/ask",
        { question: query },
        { headers: { "Content-Type": "application/json" } }
      );
      setAnswer(res.data.answer);
    } catch (err) {
      alert("Failed to get answer");
      setAnswer("Failed to get answer");
      console.error(err);
    }finally {
    setLoadingAsk(false);
  }
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Chat UI</h1>
      <textarea
        rows={4}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        style={{ width: "100%" }}
      />
      <button onClick={sendMessage} disabled={loadingChat}>{loadingChat ? "Generating.." : "Send"}</button>
      <div>
        <strong>Response:</strong>
        <p>{response}</p>
        <br/>
      </div>
      <hr />
      <h1>Document Query</h1>
      <div style={{ marginBottom: 20, marginTop: 20 }}>
      <input
        type="file"
        accept=".txt,.pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload</button>
    </div>
    <Snackbar
        open={open}
        autoHideDuration={4000}
        onClose={() => setOpen(false)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setOpen(false)} severity={severity} sx={{ width: '100%' }}>
          {uploadMessage}
        </Alert>
      </Snackbar>
      <h4>Ask Questions About the Document</h4>
      <input
        type="text"
        placeholder="Enter your question"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", marginBottom: 8 }}
      />
      <button onClick={askDocument} disabled={loadingAsk}>{loadingAsk ? "Generating.." : "Ask"}</button>
      <div>
        <strong>Answer:</strong>
        <p>{answer}</p>
      </div>
    </div>
    
  );
}

export default App;
