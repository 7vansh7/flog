import os
import ecdsa
import hashlib
import json
import time

print(os.urandom(1))

import google.generativeai as genai
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE"
  }
]
genai.configure(api_key='AIzaSyA7eoFGIqKaCA7oUYMqzT83NexlDnRjYfs')
llm = genai.GenerativeModel(model_name='gemini-1.0-pro',safety_settings=safety_settings)
history = []
chat = llm.start_chat(history=history)
psy_prompt = """You name is Aura, you are a psychologist, an expert in 
predicting human behaviour.
You are adept in psychology, philosophy, and literature.
Ask questions from the user to better your analysis and answer.
Give examples from contemporary studies if required.
You give people psychological help and also help them predicting other 
people's behaviour.
Give analysis in tabular format with the probability of things happening if required.
Talk like a HUMAN PSYCHOLOGIST.
Give a good initial response 
"""
print(chat.send_message(psy_prompt).text)