  import React, { useState, useRef } from 'react';
  import './App.css';
  import profilePic1 from './david.png';  // Adjust the path to match your file structure
  import profilePic2 from './harel.png';

  function App() {
    const [searchQuery, setSearchQuery] = useState('');
    const inputRef = useRef(null);
    const fileInputRef = useRef(null); // Ref for the hidden file input
    const [result, setResult] = useState(null);

    const handleSearch = async () => {
      if (searchQuery.trim() === '') {
        alert('Please enter a query!');
        return;
      }
    
      const response = await fetch('http://127.0.0.1:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ input: searchQuery })
      });
      const data = await response.json();
      setResult(data);  // Set the result state variable
    
      if (data && data.result) {
        setTimeout(() => {
          // Get the result container element
          const resultContainer = document.querySelector('.result-container');
    
          // Set the max-height to the scrollHeight to trigger the expanding animation
          resultContainer.style.maxHeight = `${resultContainer.scrollHeight}px`;
        }, 0);
      }
    }

    const handlePDFDrop = () => {
      // Trigger the hidden file input's click event
      fileInputRef.current.click();
    }

    const handlePDFUpload = async (event) => {
      const file = event.target.files[0];
      if (file && file.name.endsWith('.pdf')) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://127.0.0.1:8000/upload-pdf', {
          method: 'POST',
          body: formData
        });

        const data = await response.json();
        console.log(data);
        alert(`Response from server: ${JSON.stringify(data)}`);
      } else {
        alert('Please select a PDF file.');
      }
    }

    return (
      <div className="App">
        <header className="App-header">
          <div className="CyberChad">CyberChad</div>

          <div className="search-container">
            <input 
              type="text" 
              placeholder="Search..." 
              className="search-input" 
              ref={inputRef}
              onChange={() => setSearchQuery(inputRef.current.value)}
            />
            <button className="search-button" onClick={handleSearch}>Go</button>
          </div>

          <div className="madaras-logo">By Madars Podcast</div>
          <div className="pdf-drop-button" onClick={handlePDFDrop}>
            <span>+</span>
            <span>PDF</span>
          </div>

          {/* Hidden file input for PDF uploading */}
          <input 
            type="file" 
            ref={fileInputRef}
            style={{ display: 'none' }}
            onChange={handlePDFUpload}
          />
        </header>
        <div className="profile-pics">
        <img src={profilePic1} alt="Profile 1" className="profile-pic" />
        <img src={profilePic2} alt="Profile 2" className="profile-pic" />
      </div>
      <div>

      {result && result.result && (
      <div className="result-container">
      
        <div className="search-result">
          <div className="query">User: {result.query}</div>
          <div className="result">Chad: {result.result}</div>
          <div className="source-documents">
            <h3>Source Documents:</h3>
            {result.source_documents.map((doc, index) => (
              <div className="document" key={index}>
                <div>Page Content: {doc.page_content}</div>
                <div>Source: {doc.metadata.source}</div>
                <div>Page: {doc.metadata.page}</div>
              </div>
            ))}
          </div>
        </div>

      </div>
    )}
        
    </div>
      </div>
    );
  }

  export default App;
