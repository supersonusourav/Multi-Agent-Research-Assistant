from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("""
You are an expert research planner.

Convert the user's research topic into EXACTLY 5 concise search queries optimized for web search.

STRICT FORMAT REQUIREMENTS:
- Output EXACTLY 5 lines of text.
- One query per line.
- Do NOT include line numbers (do NOT write "1.", "3.", etc.).
- Do NOT include bullet points or dashes.
- Do NOT write question sentences. Use short search keywords only (3 to 7 words per line).

User Query:
{query}
""")


def planner_agent(llm):
    chain = prompt | llm | StrOutputParser()

    def run(state):
        raw_queries = chain.invoke({"query": state["query"]})
        
        # Split lines and drop empty lines / headers
        cleaned_lines = []
        for line in raw_queries.splitlines():
            line = line.strip()
            if line and not line.lower().startswith("here"):
                cleaned_lines.append(line)

        # Enforce exactly 5 queries
        state["sub_questions"] = "\n".join(cleaned_lines[:5])
        return state

    return run