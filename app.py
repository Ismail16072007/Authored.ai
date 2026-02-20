import streamlit as st
from openai import OpenAI
import requests

# --- TOOL LOGIC ---
def humanize_text(text, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional human editor. Rewrite the text to bypass AI detectors by using natural sentence variation, slight idioms, and a personal tone while keeping the exact same meaning."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def check_plagiarism(text, api_key):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Analyze the following text. Give it a 'Plagiarism Score' from 0-100% and explain why it looks like AI or copied content."},
            {"role": "user", "content": text}
        ]
    }
    try:
        response = requests.post("https://api.deepseek.com/v1/chat/completions", json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "Error connecting to DeepSeek. Check your API key."

# --- WEBSITE INTERFACE ---
st.set_page_config(page_title="Authored.ai", layout="wide")
st.title("🛡️ AI Humanizer & Plagiarism Checker")

# CORRECT WAY: Use the name of the secret, NOT the key itself
openai_api_key = st.secrets["OPENAI_API_KEY"]
deepseek_api_key = st.secrets["DEEPSEEK_API_KEY"]

input_text = st.text_area("Paste your content here:", height=250)

if st.button("Humanize & Check"):
    if input_text:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Plagiarism Analysis (DeepSeek)")
            analysis = check_plagiarism(input_text, deepseek_api_key)
            st.write(analysis)
        with col2:
            st.subheader("Humanized Text (OpenAI)")
            result = humanize_text(input_text, openai_api_key)
            st.success("Rewrite Complete!")
            st.write(result)
    else:
        st.error("Please enter text first.")
