# Video Content Analysis with Gemini API 🚀🧠

This Streamlit application demonstrates batch prediction capabilities using Google's Gemini API for analyzing video content. It features long context handling, context caching, and efficient batch processing of questions about video content.

## Features

- 📦 Batch Prediction: Efficiently process multiple questions about video content
- 📏 Long Context Handling: Process large video transcripts with smart chunking
- 💾 Context Caching: Cache previous interactions for improved performance
- 🔗 Interconnected Questions: Maintain conversation history for context-aware responses
- ✨ User-Friendly Interface: Clean Streamlit UI with structured output
- 🛡️ Robust Error Handling: Graceful handling of API errors and edge cases
- 🎥 YouTube Integration: Automatic transcript extraction from YouTube videos
- 🤖 Smart Question Suggestions: AI-powered question recommendations based on content

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Gemini API key:
   ```
   google_api_key=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Paste a YouTube video URL in the input field
   - Supported formats:
     - Regular watch URLs (youtube.com/watch?v=...)
     - Short URLs (youtu.be/...)
     - Embed URLs (youtube.com/embed/...)
2. The application will automatically:
   - Extract the video transcript
   - Display suggested questions based on the content
3. You can:
   - Use the suggested questions
   - Ask your own questions (one per line)
4. Click "Process Questions" to analyze the content
5. View the results in the structured output section

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration settings
- `utils/`: Utility modules
  - `context_cache.py`: Context caching implementation
  - `batch_processor.py`: Batch processing logic
  - `text_chunker.py`: Text chunking utilities
  - `youtube_handler.py`: YouTube transcript extraction and processing

## Technical Details

### Context Management
- Smart text chunking with overlap
- Context length optimization
- Chunk recombination for coherent answers

### Caching System
- In-memory cache with TTL
- Conversation history tracking
- Cache invalidation strategies

### Batch Processing
- Question grouping and prioritization
- Rate limiting and retry logic
- Response synthesis

## Error Handling

The application includes robust error handling for:
- Invalid YouTube URLs
- Unavailable transcripts
- API rate limits
- Network issues
- Model initialization errors

## Contributing

Feel free to submit issues and enhancement requests! 

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
