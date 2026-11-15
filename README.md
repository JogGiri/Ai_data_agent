# 🤖 AI Data Agent

An intelligent AI-powered database assistant that uses LangChain and Streamlit to answer questions about your PostgreSQL database. The agent can fetch database schema and execute SQL queries automatically.

## Features

✨ **Smart Database Assistant**
- Ask natural language questions about your database
- Automatic schema fetching and SQL query generation
- Real-time query execution and results

🎨 **Beautiful Streamlit UI**
- Interactive chat interface with conversation history
- Toggle to show/hide tool calls and execution details
- Real-time streaming responses
- Session metrics and configuration panel

🔧 **Multiple Agent Modes**
- OpenAI GPT support (main agent in `data_agent.py`)
- Google Generative AI support (optional in `main.py`)
- Configurable model selection and temperature

🛡️ **Security**
- Environment variables for API keys
- Sensitive data hidden from version control
- No credentials in repository

## Prerequisites

- Python 3.12+
- PostgreSQL database
- API Keys:
  - OpenAI API key (for ChatOpenAI)
  - Google API key (optional, for ChatGoogleGenerativeAI)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/JogGiri/Ai_data_agent.git
cd Ai_data_agent
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 3. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

## Usage

### Option 1: Streamlit Web UI (Recommended)
```bash
uv run streamlit run streamlit_app.py
```

The web UI will open at `http://localhost:8501`

**Features:**
- Chat interface with history
- Toggle to show/hide tool calls
- Model selection (gpt-4o-mini, gpt-4-turbo, gpt-4)
- Temperature control
- Session metrics

### Option 2: CLI Agent (data_agent.py)
```bash
uv run python data_agent.py
```

Interactive command-line interface for asking database questions.

### Option 3: CLI with Google GenAI (main.py)
```bash
uv run python main.py
```

Uses Google Generative AI instead of OpenAI.

## Project Structure

```
.
├── streamlit_app.py        # 🎨 Main Streamlit UI
├── data_agent.py           # 🤖 OpenAI-based agent
├── main.py                 # 🌐 Google GenAI agent
├── agent_tools.py          # 🔧 Database tools (schema & query)
├── tools.py                # 📦 Additional tools
├── pyproject.toml          # 📋 Project dependencies (uv)
├── .env.example            # 🔑 Environment variables template
├── .gitignore              # 🛡️ Security exclusions
└── README.md               # 📖 This file
```

## How It Works

1. **User Question** → User asks a question in natural language
2. **Agent Processing** → AI agent determines which tools to use
3. **Tool Execution** → Fetches database schema or executes SQL queries
4. **Response Generation** → Agent synthesizes results into a readable answer
5. **Display** → Results shown with optional tool call details

### Available Tools

**get_schema()**
- Retrieves all tables and columns from PostgreSQL
- Used for understanding database structure

**execute_query(query)**
- Executes any SQL query on the database
- Returns results as formatted text

## Configuration

### Model Selection (Streamlit UI)
In the sidebar, you can:
- Select different GPT models
- Adjust temperature (0.0 = deterministic, 1.0 = creative)
- Toggle tool call visibility

### System Prompt
The agent uses this system prompt:
```
You are a helpful database assistant who can answer questions 
about the PostgreSQL database. Use the available tools to:
1. Fetch schema to understand database structure
2. Execute SQL queries to fetch data
3. Provide clear explanations of results
```

## Example Questions

- "What tables are in my database?"
- "How many rows are in the returns table?"
- "Show me the schema of the orders table"
- "What's the total revenue from sales in 2024?"
- "Join customers and orders and show me recent transactions"

## Environment Variables

Required:
```
OPENAI_API_KEY          # Your OpenAI API key
DATABASE_URL            # PostgreSQL connection string
```

Optional:
```
GOOGLE_API_KEY          # For Google GenAI models
LANGSMITH_API_KEY       # For LangSmith tracing
```

## Security

⚠️ **Important:** 
- `.env` file is in `.gitignore` and won't be pushed to GitHub
- Never commit files containing API keys or passwords
- Use `.env.example` as a template for new installations
- Rotate API keys regularly

## Troubleshooting

### ModuleNotFoundError
```bash
# Make sure dependencies are installed
uv sync
```

### Database Connection Error
- Check `DATABASE_URL` in `.env`
- Verify PostgreSQL is running
- Ensure credentials are correct

### API Key Errors
- Verify API keys are in `.env`
- Check key validity in API dashboards
- Ensure no extra whitespace in `.env`

## Dependencies

Key packages:
- **langchain** & **langchain-core** - Agent framework
- **langgraph** - Agentic workflow
- **langchain-openai** - OpenAI integration
- **langchain-google-genai** - Google GenAI integration
- **streamlit** - Web UI
- **sqlalchemy** & **psycopg** - Database drivers
- **python-dotenv** - Environment variable management

See `pyproject.toml` for complete dependencies.

## Development

### Adding New Tools

1. Create a function in `agent_tools.py`
2. Decorate with `@tool`
3. Add to `tools` list in agent creation

Example:
```python
@tool
def my_tool(input_data):
    '''Tool description for AI agent'''
    return result
```

### Using UV Package Manager

```bash
# Sync dependencies
uv sync

# Run commands with environment
uv run python script.py

# Add new dependency
uv add package_name
```

## Performance Tips

1. **Temperature Setting**: Lower temperature (0.0-0.3) for consistent query generation
2. **Model Choice**: Use gpt-4o-mini for faster, cheaper responses
3. **Schema Caching**: Agent automatically learns schema for better queries
4. **Database Indexes**: Ensure frequently queried columns are indexed

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with detailed description
- Include error messages and environment info

## Roadmap

- [ ] Multi-turn conversation memory
- [ ] Query caching for performance
- [ ] Advanced visualization of results
- [ ] Support for other databases (MySQL, PostgreSQL, etc.)
- [ ] API endpoint for programmatic access
- [ ] Custom agent behavior configuration
- [ ] Query result export (CSV, JSON)

---

**Made with ❤️ for database exploration**
