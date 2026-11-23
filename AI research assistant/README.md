# AI Research Assistant

This project is a LangGraph-based AI research assistant. It uses Groq as the
language model and can search Wikipedia and Tavily for supporting information.

## Requirements

- Python 3.10 or newer
- A Groq API key
- A Tavily API key

## Setup

Open PowerShell and move into this project folder:

```powershell
cd "C:\Users\HP\Desktop\python\agentic AI\agentic AI project with langraph\AI research assistant"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell prevents the activation script from running, allow it for the
current session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install --upgrade pip
python -m pip install python-dotenv langchain-groq langgraph langchain-community langchain-tavily langchain-core
```

## Configure API Keys

Create a `.env` file inside this folder with the following values:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Do not commit `.env` or share your API keys.

## Run the Assistant

With the virtual environment activated, run:

```powershell
python main.py
```

The script currently researches:

```text
What is the Riemann hypothesis?
```

To change the research question, edit the `topic` value in `main.py`:

```python
topic = "Your research question"
```
