from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# This defines the data structure for the recipe text we will receive.
class RecipeInput(BaseModel):
    text: str

# This defines the data structure for a single step in the recipe.
class StepOutput(BaseModel):
    step_text: str
    image_url: str

# This defines the data structure for the complete list of steps.
class RecipeOutput(BaseModel):
    steps: List[StepOutput]
# Create an instance of the FastAPI class
app = FastAPI()
# This is our new mock endpoint.
@app.post("/process-recipe", response_model=RecipeOutput)
async def process_recipe(input_data: RecipeInput):
    # This is the mock data that we will return for now.
    mock_steps = [
        {"step_text": "This is a fake step 1: Mix the ingredients.", "image_url": "https://via.placeholder.com/150"},
        {"step_text": "This is a fake step 2: Bake in the oven.", "image_url": "https://via.placeholder.com/150"}
    ]
    return {"steps": mock_steps}
# Define a route for the root URL
@app.get("/")
def read_root():
    return {"message": "Recipe Chef API is running!"}