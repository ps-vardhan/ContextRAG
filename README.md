# Gemini RAG Console Chatbot

A simple console-based RAG (Retrieval Augmented Generation) chatbot powered by Google Gemini AI.

## Overview

This project provides a clean, console-based interface for chatting with your documents using Google Gemini AI. The system loads text documents, searches through them based on your questions, and provides contextual answers using the retrieved information.

## Features

-  **Google Gemini AI**: Powered by gemini-2.5-flash model
-  **Document RAG**: Load and search through text documents
-  **Conversation History**: Maintains context across the chat session
-  **Source Attribution**: Shows which documents were used for answers
-  **Simple Commands**: `quit`, `exit`, `clear`
-  **No Dependencies**: Only requires Python standard library + requests

## Quick Start

1. **Run the application**:
   ```bash
   python working_gemini_rag.py
   ```

2. **Add your documents**: Place `.txt` files in the `data/docs/` directory

3. **Start chatting**: Ask questions about your documents!

## File Structure

```
├── working_gemini_rag.py          # Main application
├── data/
│   └── docs/
│       └── rag_project_info.txt   # Sample document
├── requirements.txt               # Dependencies
└── README.md                     # This file
```

## Usage Example

```
 Welcome to Gemini RAG Console!
 Using model: gemini-2.5-flash
 Loaded: rag_project_info.txt
Successfully loaded 1 documents!

 Gemini RAG Chatbot Ready!
 1 documents loaded for context

 You: What is this RAG project about?
 Assistant: This is a RAG (Retrieval Augmented Generation) chatbot project that connects Large Language Models to external documents for more reliable answers...

 Sources:
   1. rag_project_info.txt
```

## Commands

- **Chat**: Simply type your questions
- **Clear history**: Type `clear`
- **Exit**: Type `quit` or `exit`

## Requirements

- Python 3.6+
- `requests` library
- Google Gemini API access

## API Key

The application currently uses a pre-configured API key for immediate testing. For production use, you should:

1. Get your own API key from: https://makersuite.google.com/app/apikey
2. Replace the API key in `working_gemini_rag.py`

## Document Format

- Supports `.txt` files
- Place documents in `data/docs/` directory
- The system will automatically load all text files from this directory

## Technical Details

- **Model**: Google Gemini 2.5 Flash
- **Search**: Simple keyword-based document retrieval
- **Context**: Uses top 2 most relevant documents per query
- **History**: Maintains last 4 conversation turns for context