import { useState } from 'react';
import './App.css';
import aifood from './assets/react.svg'; // We'll add this icon

function App() {
  const [dishName, setDishName] = useState('');
  const [fullRecipeText, setFullRecipeText] = useState('');
  const [recipeSteps, setRecipeSteps] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!dishName) {
      setError("Please enter a dish name.");
      return;
    }
    setIsLoading(true);
    setError(null);
    setFullRecipeText('');
    setRecipeSteps([]);

    try {
      const response = await fetch('http://localhost:8000/process-recipe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: dishName }),
      });

      if (!response.ok) throw new Error('The server failed to respond. Please try again.');
      
      const data = await response.json();

      if (!data.steps || data.steps.length === 0) {
        setError("The AI couldn't generate a recipe for that. Please try a different dish name.");
      } else {
        setFullRecipeText(data.full_text);
        setRecipeSteps(data.steps);
      }

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* --- LEFT CONTROL PANEL --- */}
      <div className="left-panel">
        <div className="logo-header">
          <img src={aifood} alt="AI Food Icon" className="logo-icon" />
          <h2>AI Recipe Generator</h2>
        </div>
        <p className="description">
          Enter the name of a dish and let our AI create a unique, step-by-step recipe for you, complete with images for every step.
        </p>
        <div className="input-group">
          <label htmlFor="dish-input">Dish Name</label>
          <input
            id="dish-input"
            type="text"
            placeholder="e.g., 'Spicy Thai Noodles'"
            value={dishName}
            onChange={(e) => setDishName(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleGenerate()}
          />
          <button onClick={handleGenerate} disabled={isLoading}>
            {isLoading ? 'Creating...' : 'Generate Recipe'}
          </button>
        </div>
      </div>

      {/* --- RIGHT RESULTS PANEL --- */}
      <div className="right-panel">
        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Crafting your recipe... This may take a moment.</p>
          </div>
        )}
        {error && <p className="error-message">Error: {error}</p>}
        
        {!isLoading && !error && recipeSteps.length === 0 && (
          <div className="placeholder-view">
            <h3>Your recipe will appear here</h3>
            <p>Enter a dish name on the left to get started.</p>
          </div>
        )}

        {fullRecipeText && (
          <div className="full-recipe-card">
            <pre>{fullRecipeText}</pre>
          </div>
        )}

        {recipeSteps.length > 0 && (
          <div className="steps-grid">
            {recipeSteps.map((step, index) => (
              <div key={index} className="step-card">
                <img 
                  src={step.image_url} 
                  alt={`AI generated visual for: ${step.step_text}`} 
                  className="step-image"
                />
                <div className="step-content">
                  <span className="step-number">Step {index + 1}</span>
                  <p className="step-text">{step.step_text}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
