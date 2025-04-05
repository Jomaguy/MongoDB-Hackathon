import React, { useState } from 'react';

function VideoUploadForm() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('Please select a video file');
      return;
    }
    
    // Validate file type
    if (!file.type.includes('video/')) {
      setMessage('Please upload a video file');
      return;
    }
    
    const formData = new FormData();
    formData.append('video', file);
    
    setLoading(true);
    setMessage('');
    
    try {
      const response = await fetch('http://localhost:5000/api/videos/upload', {
        method: 'POST',
        body: formData,
        // Note: Fetch API doesn't have built-in progress tracking
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      setMessage('Video uploaded successfully!');
      console.log(data);
    } catch (error) {
      setMessage('Error uploading video. Please try again.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload Video</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="video">Select Video:</label>
          <input 
            type="file" 
            id="video" 
            accept="video/*"
            onChange={handleFileChange} 
          />
        </div>
        
        <button type="submit" disabled={loading || !file}>
          {loading ? 'Uploading...' : 'Upload Video'}
        </button>
        
        {loading && (
          <div className="progress-bar">
            <div 
              className="progress" 
              style={{ width: `${progress}%` }}
            ></div>
            <span>{progress}%</span>
          </div>
        )}
        
        {message && <p className="message">{message}</p>}
      </form>
    </div>
  );
}