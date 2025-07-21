import { useState } from 'react';
import './App.css';

function App() {
  const [recipeText, setRecipeText] = useState('');
  // State to store the recipe steps from the API
  const [recipeSteps, setRecipeSteps] = useState([]);

  // Function to call the backend API
  const handleGenerate = async () => {
    // Call your mock backend endpoint
    const response = await fetch('http://localhost:8000/process-recipe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: recipeText }),
    });

    const data = await response.json();
    setRecipeSteps(data.steps); // Save the steps in our state
  };

  return (
    <div className="App">
      <h1>Interactive Recipe Chef 🧑‍🍳</h1>
      <textarea
        rows="10"
        cols="50"
        placeholder="Paste your recipe here..."
        value={recipeText}
        onChange={(e) => setRecipeText(e.target.value)}
      />
      <div>
        {/* Make the button call our new function */}
        <button onClick={handleGenerate}>Generate Recipe</button>
      </div>

      {/* Section to display the results */}
      <div className="results">
        {recipeSteps.map((step, index) => (
          <div key={index} className="step">
            <p>{step.step_text}</p>
            <img src={step.image_url} alt={`Step ${index + 1}`} />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;