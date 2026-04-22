# RAG System Example

Build a complete Retrieval Augmented Generation system for question answering.

## What You'll Learn

- Document loading and chunking strategies
- Building a vector store from documents
- Retrieval with ranking
- Combining retrieval with LLM generation
- Complete Q&A system implementation

## Files

- `document_loader.py` - Load and chunk documents
- `build_vector_store.py` - Create searchable index
- `retriever.py` - Retrieve relevant context
- `rag_qa.py` - Complete Q&A system
- `requirements.txt` - Dependencies

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

## RAG Architecture

1. **Indexing**: Load documents → Chunk → Embed → Store
2. **Retrieval**: Query → Embed → Search → Rank
3. **Generation**: Context + Query → LLM → Answer

## Running the System

```bash
# Build vector store from documents
python build_vector_store.py --docs ./data

# Run Q&A system
python rag_qa.py --query "What is the main topic?"
```

## Key Decisions

### Chunk Size
- Too small: Loses context
- Too large: Irrelevant information
- Sweet spot: 500-1000 tokens with 100-200 overlap

### Retrieval Strategy
- Top-k similarity search
- Metadata filtering
- Hybrid search (vector + keyword)
- Re-ranking retrieved results

## Resources

- [RAG Paper](https://arxiv.org/abs/2005.11401)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)