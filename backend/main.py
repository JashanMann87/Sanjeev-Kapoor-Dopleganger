from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware # Import the CORS middleware

app = FastAPI()

# --- CORS Configuration STARTS HERE ---
# List of origins that are allowed to make requests to this API
origins = [
    "http://localhost:5173", # The address of your React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# --- CORS Configuration ENDS HERE ---


# Defines the shape of the data we expect to receive
class RecipeInput(BaseModel):
    text: str

# Defines the shape for a single recipe step in the output
class StepOutput(BaseModel):
    step_text: str
    image_url: str

# Defines the shape of the final output we will send back
class RecipeOutput(BaseModel):
    steps: List[StepOutput]


# This is our mock endpoint
@app.post("/process-recipe", response_model=RecipeOutput)
async def process_recipe(input_data: RecipeInput):
    mock_steps = [
        {"step_text": "This is a fake step 1: Mix the ingredients.", "image_url": "https://via.placeholder.com/150"},
        {"step_text": "This is a fake step 2: Bake in the oven.", "image_url": "https://via.placeholder.com/150"}
    ]
    return {"steps": mock_steps}


@app.get("/")
def read_root():
    return {"message": "Recipe Chef API is running!"}