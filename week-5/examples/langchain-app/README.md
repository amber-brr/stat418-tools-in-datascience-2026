# LangChain Application Example

Build production-ready LLM applications using LangChain framework.

## What You'll Learn

- LangChain chains and prompts
- Conversation memory management
- Agents with tools
- Vector store integration
- Production patterns and best practices

## Files

- `simple_chain.py` - Basic LangChain chains
- `conversation_memory.py` - Stateful conversations
- `agent_with_tools.py` - LangChain agents
- `rag_with_langchain.py` - RAG using LangChain
- `requirements.txt` - Dependencies

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

## LangChain Components

### Chains
Combine multiple steps into a pipeline:
```python
chain = prompt | llm | output_parser
result = chain.invoke({"input": "question"})
```

### Memory
Maintain conversation context:
```python
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory)
```

### Agents
LLMs that can use tools:
```python
agent = create_react_agent(llm, tools, prompt)
```

## Running Examples

```bash
# Simple chain
python simple_chain.py

# Conversation with memory
python conversation_memory.py

# Agent with tools
python agent_with_tools.py

# RAG with LangChain
python rag_with_langchain.py
```

## Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangChain Cookbook](https://github.com/langchain-ai/langchain/tree/master/cookbook)
- [LangSmith](https://smith.langchain.com/) - Debugging tool