You are a senior AI architect and product engineer.

Build an AI-powered Personal Knowledge OS (Second Brain) with the following constraints:

GOAL:
Help users store, connect, recall, and deeply understand their knowledge.

CORE FEATURES:
1. Ingest PDFs, markdown, text, and YouTube transcripts
2. Chunk, embed, and store content in a vector database
3. Auto-generate:
   - concise summaries
   - flashcards
   - concept maps (text-based)
4. Semantic Q&A over user data
5. Spaced-repetition reminders based on learning science

ARCHITECTURE:
- Use LangChain
- Modular LLM layer (switch between OpenAI, local LLaMA/Qwen)
- FastAPI backend
- FAISS or Chroma vector store
- PostgreSQL for metadata

NON-GOALS:
- No social features
- No collaboration in MVP

OUTPUT REQUIRED:
- System architecture diagram (text)
- API design
- Data flow
- Prompt templates
- MVP development roadmap

Build it clean, scalable, and production-ready.
