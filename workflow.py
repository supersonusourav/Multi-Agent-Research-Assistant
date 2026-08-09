import traceback
from time import perf_counter

from config import llm
from state import create_state
from utils.logger import log

from agents.planner import planner_agent
from agents.researcher import researcher_agent
from agents.writer import writer_agent
from agents.critic import critic_agent


# Initialize LLM-based agents
planner = planner_agent(llm)
writer = writer_agent(llm)
critic = critic_agent(llm)


def run_workflow(query: str):
    """
    Executes the complete multi-agent research workflow.

    Flow:
        User Query
            ↓
        Planner
            ↓
        Researcher
            ↓
        Writer
            ↓
        Critic
    """

    state = create_state(query)

    start_time = perf_counter()

    log("=" * 80, state)
    log("NEW RESEARCH SESSION", state)
    log(f"Query: {query}", state)

    try:

        # ==================================================
        # Planner
        # ==================================================

        log("Planner Started", state)

        state = planner(state)

        log("Planner Completed", state)

        log(
            f"Generated {len(state['sub_questions'].splitlines())} sub-questions",
            state,
        )

        # ==================================================
        # Researcher
        # ==================================================

        log("Research Started", state)

        state = researcher_agent(state)

        stats = state["statistics"]

        log(
            (
                f"Research Completed | "
                f"Questions={stats['questions']} | "
                f"Sources={stats['sources']} | "
                f"Unique Domains={stats['unique_domains']}"
            ),
            state,
        )

        # ==================================================
        # Writer
        # ==================================================

        log("Writer Started", state)

        state = writer(state)

        log("Writer Completed", state)

        # ==================================================
        # Critic
        # ==================================================

        log("Critic Started", state)

        state = critic(state)

        log(
            f"Critic Completed | Approved={state['approved']}",
            state,
        )

        # ==================================================
        # Statistics
        # ==================================================

        elapsed = round(perf_counter() - start_time, 2)

        state["statistics"]["execution_time"] = elapsed

        log(f"Execution Time: {elapsed} seconds", state)

        log("Workflow Finished Successfully", state)

        log("=" * 80, state)

        return state

    except Exception:

        error = traceback.format_exc()

        log("Workflow Failed", state)

        log(error, state)

        print(error)

        raise