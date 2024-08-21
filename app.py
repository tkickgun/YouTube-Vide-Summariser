from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st
from dotenv import load_dotenv
load_dotenv()                                           # load all the environment variables
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a youtube video summarizer. You will be taking the transcript text along with the prompt. You need to summzarize 
        the entire video and provide the important summary in points within 250 words. Please provide the summary of the text given here:"""

def generate_transcript(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript += " "+i['text']
        return transcript
    
    except Exception as e:
        raise e

def generate_summary(prompt,transcript):
    model = genai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt+transcript)
    return response.text

st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter the youtube video URL")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    #st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button('Get Detailed Notes'):
    transcript_text = generate_transcript(youtube_link)

    if transcript_text:
        summary = generate_summary(prompt,transcript_text)
        st.markdown('## Detailed summary')
        st.write(summary)





