import streamlit as st
import os
from dotenv import load_dotenv
from utils.youtube_handler import YouTubeHandler
from utils.batch_processor import BatchProcessor
from utils.context_cache import ContextCache
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize handlers
youtube_handler = YouTubeHandler()
batch_processor = BatchProcessor()
context_cache = ContextCache()

# Initialize session state for conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

def main():
    # Page config
    st.set_page_config(
        page_title="Video Content Analysis",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Title with icon
    st.title("👥 Video Content Analysis with Gemini API")

    # Description and features
    st.write("This application helps you analyze video content by asking multiple questions about the transcript. Features:")
    
    # Features as bullet points
    st.markdown("""
    * 🔄 Batch processing of questions
    * 📝 Long context handling
    * 💾 Context caching
    * 🔗 Interconnected questions
    """)

    # Input section
    st.header("Input")
    video_url = st.text_input("YouTube Video URL", placeholder="Paste your YouTube video URL here...", help="Enter a valid YouTube video URL")
    
    # Main content area
    if video_url:
        try:
            # Extract and display transcript
            with st.spinner("Extracting video transcript..."):
                transcript = youtube_handler.get_transcript(video_url)
            
            if transcript:
                # Display transcript in expandable section
                with st.expander("📜 Video Transcript", expanded=False):
                    st.text_area("", value=transcript, height=200, disabled=True)
                
                # Two-column layout for questions and conversation
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Question input section
                    st.subheader("Ask Questions")
                    questions = st.text_area(
                        "Enter your questions (one per line):",
                        height=150,
                        placeholder="What is the main topic?\nWhat are the key points?\n..."
                    )
                    
                    if st.button("Process Questions", type="primary"):
                        if questions:
                            with st.spinner("Processing questions..."):
                                question_list = [q.strip() for q in questions.split('\n') if q.strip()]
                                results = batch_processor.process_questions(question_list, transcript)
                                
                                # Add to conversation history
                                for question, answer in results.items():
                                    st.session_state.conversation_history.append({
                                        "question": question,
                                        "answer": answer
                                    })
                        else:
                            st.warning("Please enter at least one question.")
                    
                    # Generate and display suggested questions
                    st.subheader("Suggested Questions")
                    with st.spinner("Generating questions..."):
                        suggested_questions = batch_processor.generate_questions(transcript, limit=5)
                        for question in suggested_questions:
                            if st.button(f"▶️ {question}", key=question):
                                with st.spinner("Processing question..."):
                                    results = batch_processor.process_questions([question], transcript)
                                    # Add to conversation history
                                    st.session_state.conversation_history.append({
                                        "question": question,
                                        "answer": results[question]
                                    })
                
                with col2:
                    # Conversation History
                    st.subheader("Conversation History")
                    if not st.session_state.conversation_history:
                        st.info("No conversation history yet. Start by asking some questions!")
                    else:
                        for i, qa in enumerate(st.session_state.conversation_history):
                            with st.expander(f"Q: {qa['question']}", expanded=True):
                                st.markdown(qa['answer'])
                                
                        # Clear history button
                        if st.button("Clear History"):
                            st.session_state.conversation_history = []
                            st.experimental_rerun()
            
        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            logger.error(f"Error in main: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit and Google's Gemini API | "
        "[GitHub repository](https://github.com/yourusername/your-repo)"
    )

if __name__ == "__main__":
    main() 