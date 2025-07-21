import torch
from diffusers import StableDiffusionPipeline
import os
import uuid

ml_models = {}

def load_image_model():
    """This function will be called only once at startup to load the model."""
    # --- FINAL VERSION: Reverting to the stable "tiny" model ---
    # This model is guaranteed to work on your system without crashing.
    model_id = "segmind/tiny-sd"
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if device == "cuda" else torch.float32
    
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id, 
        torch_dtype=torch_dtype
    )
    
    # We will keep the VRAM optimization just in case, it doesn't hurt.
    pipe.enable_attention_slicing()
    
    ml_models["sd_pipe"] = pipe.to(device) 
    
    print(f"--- {model_id} Loaded Successfully on {device.upper()} ---")

def generate_image_for_step(step_text: str):
    """Generates an image for a recipe step and returns the file path."""
    if "sd_pipe" not in ml_models:
        return "/static/placeholder_error.png"
        
    try:
        # Using the improved prompt for better image quality
        prompt = (
            f"cinematic food photography of '{step_text}'. "
            "award-winning photo, hyperrealistic, high detail, 8k, "
            "professional color grading, soft lighting, delicious looking, food magazine style."
        )
        
        image = ml_models["sd_pipe"](prompt).images[0]
        
        if not os.path.exists("static"):
            os.makedirs("static")
            
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join("static", filename)
        image.save(filepath)
        
        return f"/{filepath}"

    except Exception as e:
        print(f"Error generating image: {e}")
        return "/static/placeholder_error.png"
