# Text-to-SQL Analytics Copilot

A local AI-powered analytics application that converts natural-language questions into SQL queries and executes them against the Online Retail II dataset. Users can explore retail transaction data without writing SQL manually.

The project uses a locally running Qwen 2.5 model through Ollama, SQLite for data storage and querying, and Streamlit for the user interface. No paid LLM API key is required.

## Features

- **Natural-language querying:** Ask questions about retail transactions in everyday English.
- **Local LLM integration:** Generate SQL using Qwen 2.5 (1.5B) through Ollama.
- **Predefined SQL templates:** Handle common questions with predictable SQL queries.
- **SQLite integration:** Query the Online Retail II database.
- **Read-only database access:** Use SQLite read-only mode and an authorizer to restrict database operations.
- **Interactive results:** Display query results in Streamlit tables.
- **Data visualization:** Generate basic bar charts for suitable query results.
- **SQL cleaning and validation:** Remove Markdown code fences and perform basic checks before execution.
- **Free and local:** No paid LLM API is required.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.11 |
| Local LLM runtime | Ollama |
| Language model | Qwen 2.5 (1.5B) |
| Database | SQLite |
| User interface | Streamlit |
| Data processing | Pandas |
| HTTP requests | Requests |
| Visualization | Streamlit charts |

## Architecture

1. The user enters a question in the Streamlit interface.
2. `streamlit_app.py` passes the question to `generate_sql()` in `llm.py`.
3. Predefined SQL templates handle supported common questions. Other questions are sent to the local Qwen model through Ollama.
4. The generated SQL is cleaned and subjected to basic validation.
5. `database.py` executes the query against `online_retail.db` using read-only SQLite access and an authorizer.
6. Results are displayed in a table, with a chart when appropriate.

## Project Structure

```text
TextToSQL_Copilot/
├── data/                  # Dataset and related data files
├── .conda/                # Local Python environment (not for GitHub)
├── app.py                 # Additional application script
├── clean_data.py          # Data cleaning
├── create_database.py     # Creates a small sample sales.db database
├── database.py            # Read-only SQLite query execution
├── inspect_data.py        # Dataset inspection
├── llm.py                 # SQL generation using templates and Ollama
├── llm.py.backup           # Backup of an earlier LLM implementation
├── online_retail.db       # Main database (not for GitHub)
├── preprocess_data.py     # Data preprocessing
├── README.md              # Project documentation
├── sales.db               # Sample database (not for GitHub)
├── streamlit_app.py       # Main Streamlit interface
└── verify_database.py     # Database verification
```

## Requirements

- Python 3.11
- [Ollama](https://ollama.com/)
- Qwen 2.5 1.5B model
- Python packages: Streamlit, Pandas, and Requests

## Setup

### 1. Download the project

Clone the repository or download the project files, then open a terminal in the project directory.

### 2. Install Ollama and download the model

Install Ollama from its official website, then run:

```powershell
ollama pull qwen2.5:1.5b
```

Make sure Ollama is running before using the application.

### 3. Create and activate a Python environment

For a fresh setup, create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 4. Install Python dependencies

```powershell
python -m pip install streamlit pandas requests
```

### 5. Prepare the database

The application expects `online_retail.db` in the project directory. Obtain the Online Retail II dataset and follow the data preparation workflow using `clean_data.py`, `preprocess_data.py`, and the project's database utilities if you need to recreate the database.

The main database is large and is intentionally excluded from GitHub. It must be provided or generated locally.

### 6. Run the application

```powershell
python -m streamlit run streamlit_app.py
```

Open the local URL displayed in the terminal, usually `http://localhost:8501`.

## Example Questions

- How many orders are in the database?
- Which product has the highest price?
- What is the average product price?
- What is the average unit price by country?
- Which five products generated the highest revenue?
- What is the total revenue of each product?
- What is the total revenue across all orders?
- Show the top 10 countries by total revenue.

Results depend on the generated SQL and the data in the local database.

## Safety and Limitations

- Database access is configured as read-only, with an SQLite authorizer restricting permitted operations.
- SQL validation in the interface is basic and is not a complete SQL security parser. The database-level restrictions are an additional safeguard.
- Local model output can be incorrect or fail to match the intended question. Review generated SQL and results for important analyses.
- The project is a prototype and has not been established as production-ready.
- No paid LLM API is required, but local computation uses your computer's resources.

## Future Enhancements

- Improve SQL generation and error recovery.
- Add more query validation and automated tests.
- Support richer charts and downloadable query results.
- Add query history and more detailed explanations of generated SQL.

## License

Add a license before distributing or reusing this project publicly. Until a license is selected, do not assume that others have permission to reuse the code.
