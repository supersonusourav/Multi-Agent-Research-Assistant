from datetime import datetime

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


prompt = ChatPromptTemplate.from_template("""
You are a senior research paper writer.

IMPORTANT RULES

- Use ONLY the supplied research.
- Do NOT use your own knowledge.
- If the research is insufficient, clearly state that.
- Every factual statement should be supported by the supplied research.

Write a professional report using the following format.

# Title

# Generated On
{date}

# Research Query

# Abstract

# Keywords

# Introduction

# Objectives

# Methodology

Explain that the report was generated from retrieved web sources.

# Findings

Discuss each research question separately.

# Discussion

# Limitations

Clearly explain missing evidence.

# Conclusion

# References

List every citation exactly as provided.

Research Query:
{query}

Research:
{research}

References:
{citations}
""")


def writer_agent(llm):

    chain = prompt | llm | StrOutputParser()

    def run(state):

        state["date"] = datetime.now().strftime("%d %B %Y")

        research_text = ""

        for item in state["research"]:

            research_text += (
                f"\nResearch Question:\n"
                f"{item['question']}\n\n"
            )

            if not item["sources"]:

                research_text += (
                    "No sources were retrieved.\n\n"
                )

                continue

            for source in item["sources"]:

                research_text += (
                    f"Title: {source['title']}\n"
                    f"URL: {source['url']}\n"
                    f"Content: {source['content']}\n\n"
                )

        citations_text = ""

        for i, citation in enumerate(state["citations"], start=1):

            citations_text += (
                f"[{i}] {citation['title']}\n"
                f"{citation['url']}\n\n"
            )

        report = chain.invoke(
            {
                "query": state["query"],
                "date": state["date"],
                "research": research_text,
                "citations": citations_text,
            }
        )

        state["draft"] = report

        return state

    return run