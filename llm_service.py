from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from prompts import meeting_prompt

load_dotenv()

class ActionItem(BaseModel):
    task: str = Field(
        description = "The action that needs to be completed"
    )
    responsible_person: str = Field(
        description = "The person responsible for the action"
    )
    deadline: str = Field(
        description = "The deadline if mentioned, otherwise 'Not specified'"
    )

class MeetingMinutes(BaseModel):
    summary: str = Field(
        description="A concise summary of the meeting"
    )

    decisions: list[str] = Field(
        description="Important decisions made during the meeting"
    )

    action_items: list[ActionItem] = Field(
        description=(
            "A list of action items. "
            "For every action item, identify the task, "
            "the responsible person, and the deadline. "
            "If a deadline is not mentioned, use 'Not specified'."
        )
    )

    next_meeting: str = Field(
        description=(
            "The next meeting date or time if mentioned. "
            "Otherwise use 'Not specified'."
        )
    )

llm = ChatGoogleGenerativeAI(
    model = "gemini-3.5-flash",
    temperature = 0.5
)

structured_llm = llm.with_structured_output(MeetingMinutes)

meeting_chain = meeting_prompt | structured_llm 
