# Vector Database Example

Learn to work with vector databases for semantic search and similarity matching.

## What You'll Learn

- Creating embeddings from text
- Storing vectors in ChromaDB
- Performing similarity search
- Filtering with metadata
- Persisting and loading databases

## Files

- `create_embeddings.py` - Generate embeddings
- `chromadb_basics.py` - ChromaDB operations
- `similarity_search.py` - Search and retrieve
- `requirements.txt` - Dependencies

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

## Key Concepts

### Embeddings
Dense vector representations capturing semantic meaning. Similar concepts have similar vectors.

### Vector Similarity
- **Cosine similarity**: Angle between vectors (most common)
- **Euclidean distance**: Straight-line distance
- **Dot product**: Fast but magnitude-sensitive

### ChromaDB
Embedded vector database perfect for prototypes and small-to-medium datasets.

## Running Examples

```bash
# Create embeddings
python create_embeddings.py

# ChromaDB basics
python chromadb_basics.py

# Similarity search
python similarity_search.py
```

## Resources

- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)