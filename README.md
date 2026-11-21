# 🍽️ Restaurant AI Agent

A conversational restaurant assistant built with **LangChain**, **Claude Haiku 5.5** and **Streamlit**. The agent uses tool calling to search restaurants by cuisine, look up restaurant details and check reservation availability, all inside a simple chat interface.

## Features

- **Search by cuisine**: Indian, Italian, Chinese and Mexican restaurants, with ratings and price categories.
- **Restaurant details**: cuisine, rating, address, phone, opening hours and specialities.
- **Reservation availability**: checks whether a restaurant has a table for a given date and party size.
- **Multi-turn memory**: conversation history is passed to the agent, so follow-ups such as "what are its opening hours?" work.
- **Guardrails**: the system prompt tells the agent not to invent data, not to answer off-topic questions, and not to claim a booking was made (it can only check availability).
- **Clear conversation** button in the sidebar.

## Tech Stack

| Component | Technology |
|-----------|------------|
| LLM | Claude Haiku 5.5 (`claude-haiku-5-5`) via `langchain-anthropic` |
| Agent framework | LangChain (`create_agent`, `@tool`) |
| UI | Streamlit chat components |
| Config | `python-dotenv` |

## Project Structure

```
.
├── app.py             # Agent, tools, system prompt and Streamlit UI
├── requirements.txt   # Python dependencies
├── .gitignore
└── .env               # Your API key (not committed)
```

## How It Works

1. The user types a message in the Streamlit chat input.
2. `chat_with_agent()` appends it to the stored history and calls `agent.invoke()`.
3. The agent decides which tool(s) to call, then writes the final reply.
4. The reply is shown and the updated history is saved in `st.session_state`.

### Tools

| Tool | Input | Output |
|------|-------|--------|
| `search_restaurants_by_cuisine` | `cuisine_type` | List of restaurants (name, rating, price) |
| `get_restaurant_details` | `restaurant_name` | Cuisine, rating, address, phone, hours, speciality, or an error |
| `check_reservation_availability` | `restaurant_name`, `date` (YYYY-MM-DD), `party_size` | Available, fully booked, or not found |

> **Note:** Data is mock data hardcoded in `app.py`.
> - Details exist for 7 restaurants, so some restaurants listed by cuisine search (e.g. Pasta Dreams) return "not found" for details.
> - Reservation data covers only **2024-11-15 to 2024-11-17** for 6 restaurants. Other dates return "not found".

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

```bash
git clone <your-repo-url>
cd rohith-rathan-restaurant-agent

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

If the key is missing, the app shows an error and stops.

### Run

```bash
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Example Prompts

- "Show me Italian restaurants."
- "Tell me more about Spice Palace."
- "Is Dragon House available on 2024-11-16 for 4 people?"
- "What are its opening hours?" (follow-up)
- "Who is the president of France?" (politely declined, out of scope)

## Limitations & Ideas for Improvement

- Replace the hardcoded dictionaries with a database or a real restaurants API.
- Fill in missing details/availability for all listed restaurants.
- Add real booking support (currently availability checks only).
- Stream responses for a more responsive UI.
- Add automated tests for the tools.

## License

Add a license of your choice.
