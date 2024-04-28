"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
gemini_api_key=os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

system_instruction = "\"Hello RelationAI,\n\nI have a series of WhatsApp conversations between two users, [User A] and [User B]. These conversations span over a period of time and cover various topics, including personal discussions, shared experiences, plans, emotions, and interactions.\n\nHere are some key aspects I'd like you to evaluate and analyze based on the conversations:\n\nRelationship Dynamics: Analyze the overall tone and sentiment of the conversations to determine the nature of the relationship between [User A] and [User B]. Are they friends, acquaintances, romantic partners, colleagues, or family members? Provide insights into the level of closeness, trust, mutual respect, and emotional connection between them.\nCommunication Patterns: Identify recurring themes, topics, and patterns in their conversations. Are there specific topics they frequently discuss? How do they communicate with each other? Analyze the language used, including vocabulary, tone, humor, and emotional expressions, to gain insights into their communication style and dynamics.\nEmotional Expression: Evaluate how [User A] and [User B] express their emotions and feelings towards each other. Do they openly share their thoughts, concerns, and vulnerabilities? How do they respond to each other's emotions and support each other during challenging times? Assess the level of empathy, understanding, and emotional intimacy in their interactions.\nConflict Resolution: Examine how [User A] and [User B] handle disagreements, conflicts, or misunderstandings in their conversations. Do they communicate openly and respectfully, or do they avoid confrontation? Analyze their conflict resolution strategies, including negotiation, compromise, apology, and forgiveness, to understand the strength of their relationship.\nFuture Outlook: Based on the conversations, speculate on the future trajectory of their relationship. Do you foresee their relationship evolving, stabilizing, deteriorating, or undergoing significant changes? Provide recommendations or suggestions for improving their communication, resolving conflicts, and strengthening their bond, if applicable.\nPlease analyze the provided WhatsApp conversations thoroughly and provide detailed insights and observations on the aforementioned aspects. Feel free to include specific quotes, examples, or excerpts from the conversations to support your analysis.\n\n\nThank you for your assistance!"

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              system_instruction=system_instruction,
                              safety_settings=safety_settings)

uploaded_files = []

def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  pages = []
  for index, page in enumerate(pages):
    parts.append(f"--- PAGE {index} ---")
    parts.append(page)
  return parts

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": extract_pdf_pages("<path>/document0.pdf")
  }
])

convo.send_message("YOUR_USER_INPUT")
print(convo.last.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)