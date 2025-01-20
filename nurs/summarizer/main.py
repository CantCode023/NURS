import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
from ..utils import load_config

def summarize(text:str):
    data = load_config()
    
    genai.configure(api_key=data["API_KEYS"]["GEMINI_API_KEY"])
    
    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-exp",
      generation_config=genai.types.GenerationConfig(**{
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
          type = content.Type.OBJECT,
          enum = [],
          required = ["summarize", "review"],
          properties = {
            "summarize": content.Schema(
              type = content.Type.STRING,
            ),
            "review": content.Schema(
              type = content.Type.STRING,
            ),
          },
        ),
        "response_mime_type": "application/json",
      }),
      system_instruction="Start summarize with: This article talks about\nStart review with: What I learned from the article is\nWriting style: Highschooler, <= 70 words",
    )
    
    chat_session = model.start_chat(
      history=[
      ]
    )
    
    response = chat_session.send_message(text)
    
    return response.text