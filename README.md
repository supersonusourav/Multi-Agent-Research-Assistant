<img width="1387" height="907" alt="image" src="https://github.com/user-attachments/assets/9fa2d0b5-84e3-41fa-9a87-6b69d4f8cd72" />
# 🔍 Multi-Agent Research Assistant

An autonomous multi-agent research and report generation platform built with **Streamlit**, **LangChain**, and **Mistral AI**. The system orchestrates specialized agents to break down complex queries, retrieve live web search results, evaluate sources, synthesize structured reports, and export publication-ready **PDF** and **Word (.docx)** documents.

---

## ✨ Features

- **Autonomous Research Workflow:** Multi-agent collaboration featuring dedicated agents for planning, web research, evaluation, synthesis, and critical review.
- **Live Web Retrieval:** Integrated with Tavily Search API for real-time, domain-filtered factual web extraction.
- **In-Memory Export Engine:** Generates styled PDF and Word (.docx) research reports on-the-fly using custom styling algorithms without persistent disk writes.
- **Interactive Streamlit Dashboard:** Modern visual UI with execution performance metrics, research agenda breakdown, expandable web source content, and interactive execution logs.
- **Cloud-Native & Safe:** Fully optimized for containerized deployments (Streamlit Cloud, Docker, Hugging Face) using stream buffers and standard output logging.

---

## 🏗️ Architecture & Workflow

The pipeline executes through a coordinated workflow:

1. **Planner Agent:** Deconstructs the main query into targeted research sub-questions.
2. **Researcher Agent:** Executes parallel live web retrievals for each sub-question using Tavily.
3. **Writer Agent:** Synthesizes extracted findings into a structured academic research paper (Abstract, Introduction, Findings, Limitations, Conclusion).
4. **Critic Agent:** Conducts a quality assessment to evaluate factual depth and structure.
5. **Export Engine:** Converts the synthesized Markdown into styled PDF and Word files using custom ReportLab and python-docx table and layout parsers.

<img width="3246" height="1191" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/e9206657-a020-4408-bda0-038ebf0c3300" />

---

## 🛠️ Tech Stack

- **Frontend & UI:** Streamlit
- **LLM & Orchestration:** LangChain, LangChain MistralAI (`mistral-large-latest` / `mistral-small-latest`)
- **Web Search Engine:** LangChain Tavily Integration
- **Document Rendering:** ReportLab (PDF), Python-Docx (Word)
- **Environment Management:** Python-Dotenv

---

## 📂 Project Structure

```text
├── agents/
│   ├── planner.py       # Query decomposition agent
│   ├── researcher.py    # Search execution agent
│   ├── writer.py        # Report synthesis agent
│   └── critic.py        # Quality review agent
├── tools/
│   └── search.py        # Tavily search tool integration
├── utils/
│   ├── exporter.py      # PDF & Word document generation engine
│   └── logger.py        # Logging setup
├── app.py               # Streamlit web interface
├── config.py            # Environment & app configuration
├── state.py             # State data structure definition
├── workflow.py          # Core workflow execution graph
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation




# 🚀 Getting Started Locally

## 1. Prerequisites

- Python 3.10 or higher
- Git

## 2. Clone the Repository

```bash
git clone https://github.com/supersonusourav/Multi-Agent-Reseach-Assistant.git
cd Multi-Agent-Reseach-Assistant
```

## 3. Set Up Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## 6. Run the Application

```bash
streamlit run app.py
```

---

# ☁️ Streamlit Cloud Deployment

1. Push your code to GitHub.
2. Log into **Streamlit Community Cloud**.
3. Click **New app**, select your repository (`Multi-Agent-Reseach-Assistant`), and set the main file path to `app.py`.
4. Open **Advanced settings → Secrets** and enter your API keys in TOML format:

```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

5. Click **Deploy!**

---

# 📄 License

Distributed under the MIT License. See the `LICENSE` file for more information.
