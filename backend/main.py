from fastapi import FastAPI, Request # Import Request
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from ai_image_generator import generate_image_for_step, load_image_model
from ai_parser import generate_recipe_from_dish, parse_recipe_with_ai
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

# --- Lifespan Event Handler ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Server starting up, loading AI models... ---")
    static_dir = "static"
    os.makedirs(static_dir, exist_ok=True)
    app.mount(f"/{static_dir}", StaticFiles(directory=static_dir), name=static_dir)
    load_image_model()
    yield
    print("--- Server shutting down. ---")

app = FastAPI(lifespan=lifespan)

# --- CORS Configuration ---
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class RecipeInput(BaseModel):
    text: str
class StepOutput(BaseModel):
    step_text: str
    image_url: str
class RecipeOutput(BaseModel):
    full_text: str
    steps: List[StepOutput]

# --- Updated Endpoint Logic ---
# Add 'request: Request' to the function signature
@app.post("/process-recipe", response_model=RecipeOutput)
async def process_recipe(input_data: RecipeInput, request: Request):
    dish_name = input_data.text
    full_recipe_text = await generate_recipe_from_dish(dish_name)
    parsed_steps_text = await parse_recipe_with_ai(full_recipe_text)

    final_steps = []
    for step_text in parsed_steps_text:
        # Generate the relative path (e.g., /static/image.png)
        relative_image_path = generate_image_for_step(step_text)
        
        # --- NEW: Create the full, absolute URL ---
        # This combines the server's address with the image path
        base_url = str(request.base_url)
        absolute_image_url = f"{base_url.rstrip('/')}{relative_image_path}"

        final_steps.append({
            "step_text": step_text,
            "image_url": absolute_image_url # Use the new absolute URL
        })

    return {"full_text": full_recipe_text, "steps": final_steps}

@app.get("/")
def read_root():
    return {"message": "Recipe Chef API is running!"}
