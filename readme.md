# Summary Chatbot

A web application that allows users to upload text files, generate summaries, and engage in conversational chat about the content using AI.

## Features

- **File Upload & Summarization**: Upload `.txt` files to generate AI-powered summaries
- **Conversational Chat**: Chat with an AI assistant about the uploaded content
- **Streaming Responses**: Real-time streaming of chat responses for a smooth user experience
- **Persistent Chat History**: Maintains conversation context using LangGraph's memory features

## Technology Stack

- **Backend**: FastAPI - High-performance web framework for building APIs
- **Frontend**: Streamlit - Easy-to-use web app framework for data science and ML
- **AI/ML**:
  - LangChain - Framework for building applications with LLMs
  - LangGraph - Library for building stateful, multi-actor applications with LLMs
  - OpenAI API - For language model interactions
- **Package Management**: uv - Fast Python package installer and resolver

## Installation

### Prerequisites

- Python 3.12 or higher
- uv package manager

### Setup

1. Clone or download the project repository
2. Navigate to the project directory:
   ```bash
   cd Summary_Chatbot
   ```

3. Install dependencies using uv:
   ```bash
   uv sync
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

### Start the Backend (FastAPI)

In a terminal, run:
```bash
PYTHONPATH=src uv run uvicorn summary_chatbot.main:app --reload
```

The backend will start on `http://127.0.0.1:8000`

### Start the Frontend (Streamlit)

In another terminal, run:
```bash
uv run streamlit run app/app.py
```

The frontend will start on `http://localhost:8501`

## Usage

1. Open the Streamlit app in your browser
2. Upload a `.txt` file using the file uploader
3. Click "Summarize" to generate an initial summary
4. Use the chat input to ask questions about the content
5. The AI will respond with streaming text based on the uploaded document

## Project Structure

```
Summary_Chatbot/
├── app/
│   └── app.py              # Streamlit frontend
├── src/
│   └── summary_chatbot/
│       ├── __init__.py
│       ├── main.py         # FastAPI backend
│       ├── api/
│       │   └── chain.py    # LangChain/LangGraph logic
│       └── prompts/
│           └── prompt.py   # AI prompts
├── tests/                  # Test notebooks
├── 1_notebooks/           # Development notebooks
├── 2_data/                # Sample data
├── pyproject.toml         # Project configuration and dependencies
└── README.md
```

## API Endpoints

- `GET /` - Health check
- `POST /summarise` - Summarize uploaded text file
- `POST /initialize` - Initialize chat session with uploaded file
- `POST /update` - Send chat message and receive streaming response