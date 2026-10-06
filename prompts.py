from langchain_core.prompts import ChatPromptTemplate

meeting_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """Extract structured meeting minutes from the transcript.

Return:
- summary
- decisions
- action_items with task, responsible_person, deadline
- next_meeting

Keep the summary and decisions concise.
For each action item, provide only the required task, responsible person, and deadline.
Use "Not specified" when a deadline or next meeting is not mentioned.
Do not invent information or add unnecessary details."""
    ),
    (
        "human",
        "Transcript:\n{transcript}"
    )
])