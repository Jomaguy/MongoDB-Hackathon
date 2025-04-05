import { useState } from 'react';
import './App.css';

function App() {
  const handleSubmit = (event) => {
    event.preventDefault(); // prevent default reload behavior of submission form when submitted
    createPost(dataForm);
  };

  //HTTP REQUEST POST
  const createPost = async (anyArg) => {
    
      try{
        const response = await fetch ("http://localhost:4000/api", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(anyArg),
      })

      if(!response.ok) {
        throw new Error(`HTTP Error ${response.status}`) // error instance is created to be passed to catch block
      }
        
      }catch(err){
      console.error(`Error creating post:`, err)
      }
  };
  };

  return {}

export default App;

