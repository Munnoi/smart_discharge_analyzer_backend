from dotenv import load_dotenv

import os
import google.generativeai as genai
import json

load_dotenv()
# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash-lite")


async def analyze_text(text: str) -> dict:
    try:
        prompt = build_prompt(text)

        response = model.generate_content(prompt)

        raw_output = response.text

        # Try parsing JSON safely
        parsed = safe_parse_json(raw_output)

        return parsed

    except Exception as e:
        print("Gemini Error:", e)
        return {
            "summary": "Error analyzing document",
            "errors": [str(e)],
            "icd_suggestions": [],
        }


# -------- PROMPT --------
def build_prompt(text: str) -> str:
    return f"""
You are a medical AI assistant.

Analyze the following discharge summary carefully.

Tasks:
1. Provide a clean and simple summary
2. Identify errors or missing information
3. Detect inconsistencies
4. Suggest possible ICD-11 codes

Return ONLY in valid JSON format:

{{
  "summary": "...",
  "errors": ["..."],
  "inconsistencies": ["..."],
  "icd_suggestions": ["..."]
}}

Discharge Summary:
{text[:15000]}
"""


# -------- JSON PARSER --------
def safe_parse_json(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except:
        # fallback if Gemini adds extra text
        try:
            start = raw_text.find("{")
            end = raw_text.rfind("}") + 1
            return json.loads(raw_text[start:end])
        except:
            return {
                "summary": raw_text,
                "errors": ["Could not parse structured output"],
                "inconsistencies": [],
                "icd_suggestions": [],
            }
