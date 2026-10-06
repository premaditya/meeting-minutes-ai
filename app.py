import os
import time
import streamlit as st

from dotenv import load_dotenv
from langsmith import Client

from llm_service import meeting_chain


# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

LANGSMITH_PROJECT = os.getenv(
    "LANGSMITH_PROJECT",
    "meeting-minutes-ai"
)

client = Client()


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Meeting Assistant",
    page_icon="📝",
    layout="wide"
)


# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #070a12 0%,
        #0d1222 45%,
        #17132a 75%,
        #1d1533 100%
    );
    color: #e6e8f5;
}

.stApp h2,
.stApp h3,
.stApp label,
.stApp p {
    color: #e6e8f5;
}


/* --------------------------------------------------
   Hero
-------------------------------------------------- */

.hero {
    text-align: center;
    padding: 2rem;
    border-radius: 14px;
    background: linear-gradient(
        135deg,
        #6366f1,
        #a855f7
    );
    color: white;
    margin-bottom: 1.5rem;
    box-shadow: 0 6px 18px rgba(99, 102, 241, 0.10);
    transition:
        translate 0.3s ease,
        box-shadow 0.3s ease;
}

.hero:hover {
    translate: -2px -4px;
    box-shadow: 0 8px 22px rgba(99, 102, 241, 0.15);
}

.hero h1 {
    margin: 0;
    color: white;
}

.hero p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}


/* --------------------------------------------------
   Cards
-------------------------------------------------- */

.card {
    padding: 1rem 1.25rem;
    border-radius: 12px;
    background: #131627;
    border: 1px solid #252a48;
    color: #e6e8f5;
    margin-top: 1rem;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        box-shadow 0.25s ease;
}

.card:hover {
    transform: translateY(-2px);
    border-color: #6366f1;
    box-shadow: 0 8px 22px rgba(99, 102, 241, 0.2);
}

.card h3 {
    margin-top: 0;
    color: #e6e8f5;
}

.card p,
.card li {
    color: #e6e8f5;
    line-height: 1.6;
}


/* --------------------------------------------------
   Action Item
-------------------------------------------------- */

.action-item {
    padding: 1rem;
    margin-top: 0.75rem;
    border-radius: 10px;
    background: #1a1e35;
    border: 1px solid #252a48;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease;
}

.action-item:hover {
    transform: translateY(-2px);
    border-color: #6366f1;
}

.action-item strong {
    color: #e6e8f5;
}

.action-item span {
    color: #8b90b0;
}


/* --------------------------------------------------
   Metrics
-------------------------------------------------- */

.metrics {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.metric {
    flex: 1;
    padding: 1rem;
    border-radius: 12px;
    background: #131627;
    border: 1px solid #252a48;
    color: #8b90b0;
    text-align: center;
    font-size: 0.85rem;
    transition:
        transform 0.25s ease,
        border-color 0.25s ease,
        background 0.25s ease;
}

.metric:hover {
    transform: translateY(-3px);
    background: #1a1e35;
    border-color: #6366f1;
}

.metric b {
    display: block;
    font-size: 1.4rem;
    color: #e6e8f5;
}

.note {
    margin-top: 0.5rem;
    font-size: 0.85rem;
    color: #8b90b0;
}

.note:hover {
    color: #e6e8f5;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Helper: Build Metric Card
# --------------------------------------------------

def metric_card(value, label):
    return f'<div class="metric"><b>{value}</b>{label}</div>'


# --------------------------------------------------
# Hero Section
# --------------------------------------------------

hero = """
<div class="hero">
    <h1>📝 Meeting Assistant</h1>
    <p>
        Analyze meeting transcripts and generate structured
        summaries, decisions, and action items.
    </p>
</div>
"""

st.markdown(hero, unsafe_allow_html=True)


# --------------------------------------------------
# Meeting Transcript
# --------------------------------------------------

transcript = st.text_area(
    "Meeting Transcript:",
    placeholder="""Example:

Rahul: We need to finish the website by Friday.
Priya: I'll complete the login page.
Amit: I'll test the payment module tomorrow.
Rahul: Let's meet again next Monday.""",
    height=250
)


# --------------------------------------------------
# Process Meeting
# --------------------------------------------------

if st.button("Generate Minutes"):

    if not transcript.strip():

        st.warning(
            "Please enter a meeting transcript."
        )

    else:

        # Start application latency measurement
        start_time = time.perf_counter()

        with st.spinner("Analyzing meeting transcript..."):

            result = meeting_chain.invoke(
                {
                    "transcript": transcript
                },
                config={
                    "run_name": "Meeting Minutes Request"
                }
            )

        # End application latency measurement
        end_time = time.perf_counter()

        app_latency = end_time - start_time


        # --------------------------------------------------
        # Display Summary
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="card">
                <h3>📋 Summary</h3>
                <p>{result.summary}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # Display Decisions
        # --------------------------------------------------

        decisions_html = ""

        if result.decisions:

            decisions_html = "<ul>"

            for decision in result.decisions:
                decisions_html += f"<li>{decision}</li>"

            decisions_html += "</ul>"

        else:

            decisions_html = "<p>No decisions identified.</p>"


        st.markdown(
            f"""
            <div class="card">
                <h3>✅ Decisions</h3>
                {decisions_html}
            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # Display Action Items
        # --------------------------------------------------

        action_items_html=""

        if result.action_items:
            for index,item in enumerate(result.action_items,start=1):
                action_items_html+=f"""<div class="action-item">
                <strong>Action Item {index}</strong>
                <p><span>Task:</span>{item.task}</p>
                <p><span>Responsible Person:</span>{item.responsible_person}</p>
                <p><span>Deadline:</span>{item.deadline}</p>
                </div>"""
        else:
            action_items_html="<p>No action items identified.</p>"

        st.markdown(f"""<div class="card"><h3>📌 Action Items</h3>{action_items_html}</div>""",unsafe_allow_html=True)


        # --------------------------------------------------
        # Display Next Meeting
        # --------------------------------------------------

        st.markdown(
            f"""
            <div class="card">
                <h3>📅 Next Meeting</h3>
                <p>{result.next_meeting}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # Retrieve LangSmith Trace
        # --------------------------------------------------

        try:

            # Give LangSmith a moment to finish processing
            time.sleep(2)

            runs = list(
                client.list_runs(
                    project_name=LANGSMITH_PROJECT,
                    filter='eq(name, "Meeting Minutes Request")',
                    limit=1
                )
            )

            if runs:

                root_run = runs[0]

                # Retrieve complete trace
                trace = client.read_run(
                    root_run.id,
                    load_child_runs=True
                )

                llm_run = None

                # Find the LLM child run
                for child in trace.child_runs:

                    if child.run_type == "llm":

                        llm_run = child
                        break


                # --------------------------------------------------
                # Display Metrics
                # --------------------------------------------------

                st.subheader("📊 Request Metrics")

                cards = metric_card(
                    f"{app_latency:.2f}s",
                    "App Latency"
                )

                notes = []


                if llm_run:

                    if llm_run.prompt_tokens is not None:

                        cards += metric_card(
                            llm_run.prompt_tokens,
                            "Input Tokens"
                        )

                    if llm_run.completion_tokens is not None:

                        cards += metric_card(
                            llm_run.completion_tokens,
                            "Output Tokens"
                        )

                    if llm_run.total_tokens is not None:

                        cards += metric_card(
                            llm_run.total_tokens,
                            "Total Tokens"
                        )


                    # Cost
                    if llm_run.total_cost is not None:

                        notes.append(
                            f"💰 LangSmith estimated cost: "
                            f"${float(llm_run.total_cost):.6f}"
                        )


                    # LLM latency
                    if (
                        llm_run.start_time
                        and llm_run.end_time
                    ):

                        llm_latency = (
                            llm_run.end_time
                            - llm_run.start_time
                        ).total_seconds()

                        notes.append(
                            f"⚡ LLM latency: "
                            f"{llm_latency:.2f}s"
                        )

                else:

                    notes.append(
                        "LangSmith trace found, but the "
                        "LLM run metrics are not available yet."
                    )


                notes_html = "".join(
                    f'<div class="note">{n}</div>'
                    for n in notes
                )


                st.markdown(
                    f"""
                    <div class="metrics">
                        {cards}
                    </div>
                    {notes_html}
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.info(
                    "LangSmith trace is still being processed."
                )


        except Exception as e:

            st.warning(
                "The meeting minutes were generated successfully, "
                "but LangSmith metrics could not be retrieved."
            )

            st.caption(
                f"LangSmith: {e}"
            )
