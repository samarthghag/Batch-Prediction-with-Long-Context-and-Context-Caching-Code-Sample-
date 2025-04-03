import streamlit as st
import uuid
from utils.batch_processor import BatchProcessor
from utils.text_chunker import TextChunker
from utils.context_cache import context_cache
from utils.youtube_handler import extract_video_id, get_transcript, suggest_questions

# Initialize session state
if 'conversation_id' not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if 'processor' not in st.session_state:
    st.session_state.processor = BatchProcessor()
if 'text_chunker' not in st.session_state:
    st.session_state.text_chunker = TextChunker()
if 'transcript' not in st.session_state:
    st.session_state.transcript = None

# Set page config
st.set_page_config(
    page_title="Video Content Analysis",
    page_icon="🎥",
    layout="wide"
)

# Title and description
st.title("🎥 Video Content Analysis with Gemini API")
st.markdown("""
This application helps you analyze video content by asking multiple questions about the transcript.
Features:
- 📦 Batch processing of questions
- 📏 Long context handling
- 💾 Context caching
- 🔗 Interconnected questions
""")

# Sidebar
with st.sidebar:
    st.header("Settings")
    if st.button("Clear Conversation"):
        context_cache.clear_conversation(st.session_state.conversation_id)
        st.success("Conversation history cleared!")

# Main content
# Input section
st.header("Input")
youtube_url = st.text_input(
    "YouTube Video URL",
    placeholder="Paste your YouTube video URL here...",
    help="Supported formats: youtube.com/watch?v=, youtu.be/, youtube.com/embed/"
)

if youtube_url:
    try:
        with st.spinner("Extracting transcript..."):
            video_id = extract_video_id(youtube_url)
            transcript = get_transcript(video_id)
            st.session_state.transcript = transcript
            
            # Display transcript preview
            with st.expander("View Transcript", expanded=False):
                st.text_area("Transcript", transcript, height=200)
            
            # Generate and display suggested questions
            suggested_questions = suggest_questions(transcript)
            st.subheader("Suggested Questions")
            for i, question in enumerate(suggested_questions, 1):
                st.write(f"{i}. {question}")
            
            # Allow custom questions
            st.subheader("Ask Your Own Questions")
            questions = st.text_area(
                "Questions",
                height=150,
                placeholder="Enter your questions (one per line)...",
                help="Each question should be on a new line"
            )
            
            if st.button("Process Questions", type="primary"):
                if not questions:
                    st.error("Please provide at least one question.")
                else:
                    with st.spinner("Processing questions..."):
                        # Split questions into a list
                        question_list = [q.strip() for q in questions.split('\n') if q.strip()]
                        
                        # Process the batch
                        results = st.session_state.processor.process_batch(
                            question_list,
                            transcript,
                            st.session_state.conversation_id
                        )
                        
                        # Display results
                        st.header("Results")
                        for result in results:
                            with st.expander(f"Q: {result['question']}", expanded=True):
                                if result['status'] == 'success':
                                    st.markdown(result['answer'])
                                else:
                                    st.error(result['answer'])
    except Exception as e:
        st.error(f"Error processing video: {str(e)}")

# Display conversation history
st.header("Conversation History")
history = context_cache.get_conversation_history(st.session_state.conversation_id)
if history:
    for msg in history:
        if msg['role'] == 'user':
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Assistant:** {msg['content']}")
else:
    st.info("No conversation history yet. Start by asking some questions!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Built with ❤️ using Streamlit and Google's Gemini API</p>
    <p>For more information, check out the <a href='https://github.com/yourusername/video-content-analysis'>GitHub repository</a></p>
</div>
""", unsafe_allow_html=True) 