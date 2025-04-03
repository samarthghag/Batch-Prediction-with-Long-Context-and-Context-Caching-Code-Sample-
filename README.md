# Video Content Analysis with Gemini API 🚀🧠

This Streamlit application demonstrates batch prediction capabilities for analyzing video content using Google's Gemini API. It features long-context handling, context caching, and efficient batch processing of questions about video content.

## Features

- 📦 Batch Prediction: Efficiently process multiple questions about video content
- 📏 Long Context Handling: Process large video transcripts with smart chunking
- 💾 Context Caching: Cache previous interactions for improved performance
- 🔗 Interconnected Questions: Maintain conversation history for context-aware responses
- ✨ User-Friendly Interface: Clean Streamlit UI with structured output
- 🛡️ Robust Error Handling: Graceful handling of API errors and edge cases

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Upload a video transcript or paste it directly into the text area
2. Enter your questions in the provided text area (one question per line)
3. Click "Process Questions" to analyze the content
4. View the results in the structured output section

## Project Structure

- `app.py`: Main Streamlit application
- `config.py`: Configuration settings
- `utils/`: Utility modules
  - `context_cache.py`: Context caching implementation
  - `batch_processor.py`: Batch processing logic
  - `text_chunker.py`: Text chunking utilities

## Contributing

Feel free to submit issues and enhancement requests! 
