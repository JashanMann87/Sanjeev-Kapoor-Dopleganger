import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

# --- MODIFIED FUNCTION ---
async def generate_recipe_from_dish(dish_name: str):
    """Takes a dish name and asks the AI to generate a full recipe."""
    prompt = f"""
You are a world-renowned chef creating unique recipes.
Generate a high-quality, well-reviewed, and creative recipe for the following dish: "{dish_name}".
Provide a title, a short description, a list of ingredients, and a list of clear, step-by-step instructions.
IMPORTANT: Do not use any markdown formatting like **, ##, or *.
"""
    try:
        response = await model.generate_content_async(prompt)
        # As a backup, we will also manually remove any markdown characters
        cleaned_text = response.text.replace("**", "").replace("##", "").replace("* ", "")
        return cleaned_text.strip()
    except Exception as e:
        print(f"Error generating recipe from dish: {e}")
        return "Error: Could not generate recipe."

# --- UNCHANGED FUNCTION ---
async def parse_recipe_with_ai(recipe_text: str):
    """Takes a full recipe text and extracts just the steps into a JSON list."""
    prompt = f"""
Your role is to act as a recipe data extraction service.
You will be given raw text of a recipe.
Your ONLY output should be a valid JSON array of strings, where each string is a single cooking step.
Do not include the ingredients list or title. Just the instructions.
Do not include any explanation, preamble, or markdown formatting. Just the JSON array.

Recipe Text:
---
{recipe_text}
---
"""
    try:
        response = await model.generate_content_async(prompt)
        json_text = response.text.strip().replace("```json", "").replace("```", "")
        if not json_text:
            print("AI returned an empty response for parsing.")
            return []
        return json.loads(json_text)
    except Exception as e:
        print(f"A specific error occurred while parsing JSON: {e}")
        print(f"Raw text from AI that caused error: {response.text}")
        return ["Error: Could not parse recipe steps from AI response."]
