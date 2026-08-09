from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


prompt = ChatPromptTemplate.from_template("""
You are a research reviewer.

Review the report for:

- factual completeness
- missing information
- unsupported claims
- clarity

User Query:
{query}

Report:
{draft}

Reply in ONLY one of these formats:

GOOD

or

IMPROVE:
<reason>
""")


def critic_agent(llm):

    chain = prompt | llm | StrOutputParser()

    def run(state):

        review = chain.invoke(
            {
                "query": state["query"],
                "draft": state["draft"],
            }
        )

        state["review"] = review

        state["approved"] = review.strip().upper().startswith("GOOD")

        return state

    return run