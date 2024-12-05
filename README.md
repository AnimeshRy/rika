# Rika

A simple, multi-user, multi-conversation, web-based ChatBit.

## Features
### Multi User
### Multi Conversation
### Streaming
## Architecture
## Deployment


## Configuration

Key | Default Value | Description
---|---|---
LLM__URL | `http://localhost:8080` | llm service url
LLM__MODEL | `cognitivecomputations/dolphin-2.6-mistral-7b-dpo-laser` | llm model
LLM__CREDS | `EMPTY` | llm service credentials
DB_URL | `postgresql+psycopg://postgres:postgres@localhost:5432/` | Database url to persist messages and metadata
LOG_LEVEL | `INFO` | log level
