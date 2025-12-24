#!/usr/bin/env python3
"""
Working Gemini RAG Console Application
"""

import os
import requests
import json
from pathlib import Path

class WorkingGeminiRAG:
    def __init__(self):
        # Use the API key that we know works
        self.gemini_api_key = "AIzaSyA7_vG0eO9EddvDiN9UJwHIbPCJ5hNSTAs"
        self.model = "gemini-2.5-flash"
        self.chat_history = []
        self.documents = []
        
    def load_documents(self):
        """Load documents from data/docs directory"""
        docs_dir = Path("data/docs")
        if not docs_dir.exists():
            print("No data/docs directory found.")
            return False
            
        txt_files = list(docs_dir.glob("**/*.txt"))
        
        if not txt_files:
            print("No .txt files found in data/docs directory.")
            return False
        
        print(f"Loading {len(txt_files)} text files...")
        
        for txt_file in txt_files:
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.documents.append({
                        'source': str(txt_file),
                        'content': content
                    })
                    print(f"✅ Loaded: {txt_file.name}")
            except Exception as e:
                print(f"❌ Error loading {txt_file}: {e}")
        
        print(f"Successfully loaded {len(self.documents)} documents!")
        return True

    def call_gemini_api(self, prompt):
        """Call Gemini API"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.gemini_api_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2048,
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        return candidate['content']['parts'][0]['text']
                    else:
                        return "Response was blocked by safety filters."
                else:
                    return "No response generated."
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def search_documents(self, query):
        """Simple keyword search in documents"""
        if not self.documents:
            return []
        
        query_words = query.lower().split()
        scored_docs = []
        
        for doc in self.documents:
            content_lower = doc['content'].lower()
            score = sum(1 for word in query_words if word in content_lower)
            
            if score > 0:
                scored_docs.append((score, doc))
        
        # Return top 2 documents
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:2]]

    def chat_loop(self):
        """Main chat loop"""
        print("\n🤖 Gemini RAG Chatbot Ready!")
        print("Commands: 'quit', 'exit', 'clear'")
        if self.documents:
            print(f"📚 {len(self.documents)} documents loaded for context")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                    
                if user_input.lower() == 'clear':
                    self.chat_history = []
                    print("🧹 Chat history cleared.")
                    continue
                    
                if not user_input:
                    continue
                
                print("🤖 Assistant: ", end="", flush=True)
                
                # Search for relevant documents
                relevant_docs = self.search_documents(user_input)
                
                # Build prompt
                prompt = ""
                
                # Add conversation history
                if self.chat_history:
                    prompt += "Previous conversation:\n"
                    for msg in self.chat_history[-4:]:  # Last 4 messages
                        prompt += f"{msg['role']}: {msg['content']}\n"
                    prompt += "\n"
                
                # Add document context
                if relevant_docs:
                    prompt += "Relevant documents:\n\n"
                    for i, doc in enumerate(relevant_docs, 1):
                        snippet = doc['content'][:600] + "..." if len(doc['content']) > 600 else doc['content']
                        prompt += f"Document {i} ({doc['source']}):\n{snippet}\n\n"
                
                # Add current question
                prompt += f"Question: {user_input}\n\n"
                
                # Add instructions
                if relevant_docs:
                    prompt += "Please answer based on the provided documents and conversation context. If the documents don't contain relevant information, say so."
                else:
                    prompt += "Please answer based on your general knowledge and the conversation context."
                
                # Get response
                response = self.call_gemini_api(prompt)
                
                if response:
                    print(response)
                    
                    # Show sources
                    if relevant_docs:
                        print(f"\n📖 Sources:")
                        for i, doc in enumerate(relevant_docs, 1):
                            source_name = Path(doc['source']).name
                            print(f"   {i}. {source_name}")
                    
                    # Update history
                    self.chat_history.append({"role": "Human", "content": user_input})
                    self.chat_history.append({"role": "Assistant", "content": response})
                else:
                    print("Sorry, I couldn't get a response. Please try again.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

    def run(self):
        """Run the application"""
        print("🚀 Welcome to Gemini RAG Console!")
        print(f"🔧 Using model: {self.model}")
        
        # Load documents
        self.load_documents()
        
        # Start chat
        self.chat_loop()

if __name__ == "__main__":
    app = WorkingGeminiRAG()
    app.run()