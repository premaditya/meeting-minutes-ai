# 📝 AI Meeting Assistant

An AI-powered meeting minutes generator built with **LangChain**, **Google Gemini**, **Streamlit**, and **LangSmith**. Paste in a meeting transcript and the app returns structured minutes: a summary, key decisions, action items (task, owner, deadline), and the next meeting. It also shows per-request observability metrics pulled from LangSmith.

## ✨ Features

- **Concise meeting summary** based only on the transcript
- **Decisions list** capturing the important outcomes
- **Action items** with task, responsible person, and deadline
- **Next meeting detection**, or "Not specified" when none is mentioned
- **Structured output** via nested Pydantic models and `with_structured_output`
- **LangSmith tracing** with a live metrics panel showing:
  - App latency
  - Input, output, and total tokens
  - Estimated cost
  - LLM latency
- **Custom dark-themed UI** with hover effects, built with Streamlit and custom CSS

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM framework | LangChain |
| Model | Google Gemini (`langchain-google-genai`) |
| Observability | LangSmith |
| Data validation | Pydantic |
| Config | python-dotenv |

## 📁 Project Structure

```
meeting-minutes-ai/
├── app.py              # Streamlit UI, minutes generation flow, LangSmith metrics
├── llm_service.py      # Gemini model, Pydantic schemas, and meeting chain
├── prompts.py          # System and human prompt templates
├── requirements.txt    # Python dependencies
├── .env                # API keys and config (not committed)
└── README.md
```

## ⚙️ How It Works

1. The user pastes a meeting transcript into the Streamlit app.
2. `meeting_chain` (prompt → Gemini with structured output) analyzes the transcript.
3. The model returns a validated `MeetingMinutes` object containing:
   - `summary`
   - `decisions` (list of strings)
   - `action_items` (list of `ActionItem` with `task`, `responsible_person`, `deadline`)
   - `next_meeting`
4. The app renders each part as a styled card.
5. After a short delay, the app queries LangSmith for the latest `Meeting Minutes Request` trace and displays token usage, cost, and latency.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/premaditya/meeting-minutes-ai.git
cd meeting-minutes-ai
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Google Gemini
GOOGLE_API_KEY=your_google_api_key

# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=meeting-minutes-ai
```

- Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).
- Get a LangSmith API key from [LangSmith](https://smith.langchain.com/).
- If `LANGSMITH_PROJECT` is not set, the app defaults to `meeting-minutes-ai`.

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 🧪 Example

**Input transcript**

```
Rahul: We need to finish the website by Friday.
Priya: I'll complete the login page.
Amit: I'll test the payment module tomorrow.
Rahul: Let's meet again next Monday.
```

**Sample output**

| Section | Result |
|---|---|
| Summary | The team discussed finishing the website by Friday and assigned the login page and payment testing. |
| Decisions | Website to be completed by Friday |
| Action item 1 | Complete the login page, Priya, Not specified |
| Action item 2 | Test the payment module, Amit, Tomorrow |
| Next meeting | Next Monday |

*(Actual output varies by model response.)*

## 📊 Observability with LangSmith

Each request is traced under the run name **Meeting Minutes Request**. In the LangSmith dashboard you can inspect:

- The full prompt sent to the model
- The structured response
- Token usage and estimated cost
- Latency for each step of the chain

## 🛠️ Customization

- **Change the model or temperature:** edit `llm_service.py`
- **Adjust extraction rules or tone:** edit `prompts.py`
- **Add or remove output fields:** update the `MeetingMinutes` / `ActionItem` models in `llm_service.py` and render the new field in `app.py`
- **Restyle the UI:** edit the CSS block at the top of `app.py`

## ⚠️ Notes

- LangSmith metrics may take a couple of seconds to appear because traces are processed asynchronously. If they aren't ready, the app shows a friendly message instead of failing.
- The model is instructed not to invent information, so missing deadlines and next meetings appear as "Not specified".
- Never commit your `.env` file. Add it to `.gitignore`.

## 📄 License

This project is for educational purposes. Add a license of your choice here.