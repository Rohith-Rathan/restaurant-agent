
# ============================================================
# RESTAURANT AI AGENT
# Built with LangChain, Claude Haiku 5.5 and Streamlit
# ============================================================


# ============================================================
# 1. IMPORT REQUIRED LIBRARIES
# ============================================================

import os
import streamlit as st

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain.agents import create_agent


# ============================================================
# 2. STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Restaurant AI Agent",
    page_icon="🍽️",
    layout="centered"
)


# ============================================================
# 3. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

if not ANTHROPIC_API_KEY:
    st.error(
        "Anthropic API key not found. "
        "Please configure ANTHROPIC_API_KEY in your .env file."
    )
    st.stop()


# ============================================================
# 4. INITIALIZE CLAUDE HAIKU 5.5 MODEL
# ============================================================

model = ChatAnthropic(
    model="claude-haiku-5-5",
    api_key=ANTHROPIC_API_KEY
)


# ============================================================
# 5. TOOL 1: SEARCH RESTAURANTS BY CUISINE
# ============================================================

@tool
def search_restaurants_by_cuisine(cuisine_type: str) -> list:
    """
    Search for restaurants by cuisine type.

    Supported cuisines: Indian, Italian, Chinese and Mexican.

    Returns a list containing restaurant names, ratings
    and price categories.
    """

    restaurants = {

        "indian": [
            {
                "name": "Spice Palace",
                "rating": 4.5,
                "price": "₹₹"
            },
            {
                "name": "Curry House",
                "rating": 4.3,
                "price": "₹₹"
            },
            {
                "name": "Taj Flavors",
                "rating": 4.7,
                "price": "₹₹₹"
            }
        ],

        "italian": [
            {
                "name": "Pizza Bella",
                "rating": 4.4,
                "price": "₹₹"
            },
            {
                "name": "Pasta Dreams",
                "rating": 4.6,
                "price": "₹₹₹"
            },
            {
                "name": "Roma Kitchen",
                "rating": 4.2,
                "price": "₹₹"
            }
        ],

        "chinese": [
            {
                "name": "Dragon House",
                "rating": 4.5,
                "price": "₹₹"
            },
            {
                "name": "Ming's Kitchen",
                "rating": 4.3,
                "price": "₹₹"
            },
            {
                "name": "Golden Wok",
                "rating": 4.8,
                "price": "₹₹₹"
            }
        ],

        "mexican": [
            {
                "name": "Taco Fiesta",
                "rating": 4.4,
                "price": "₹₹"
            },
            {
                "name": "Salsa Nights",
                "rating": 4.6,
                "price": "₹₹₹"
            },
            {
                "name": "Burrito House",
                "rating": 4.2,
                "price": "₹₹"
            }
        ]
    }

    cuisine_lower = cuisine_type.lower().strip()

    return restaurants.get(cuisine_lower, [])


# ============================================================
# 6. TOOL 2: GET RESTAURANT DETAILS
# ============================================================

@tool
def get_restaurant_details(restaurant_name: str) -> dict:
    """
    Get detailed information about a restaurant.

    Returns cuisine, rating, address, phone number,
    opening hours and speciality.

    Returns an error dictionary if the restaurant is not found.
    """

    details = {

        "Spice Palace": {
            "cuisine": "Indian",
            "rating": 4.5,
            "address": "123 Food Street, City Center",
            "phone": "9876543210",
            "hours": "11 AM - 11 PM",
            "speciality": "Butter Chicken, Biryani"
        },

        "Pizza Bella": {
            "cuisine": "Italian",
            "rating": 4.4,
            "address": "456 Dine Avenue, Downtown",
            "phone": "9123456789",
            "hours": "12 PM - 10:30 PM",
            "speciality": "Margherita Pizza, Tiramisu"
        },

        "Dragon House": {
            "cuisine": "Chinese",
            "rating": 4.5,
            "address": "789 Noodle Lane, Market Area",
            "phone": "9111222333",
            "hours": "11:30 AM - 11 PM",
            "speciality": "Hakka Noodles, Fried Rice"
        },

        "Taco Fiesta": {
            "cuisine": "Mexican",
            "rating": 4.4,
            "address": "321 Spice Row, Hip District",
            "phone": "9222333444",
            "hours": "1 PM - 12 AM",
            "speciality": "Fish Tacos, Guacamole"
        },

        "Curry House": {
            "cuisine": "Indian",
            "rating": 4.3,
            "address": "555 Flavor Street, Old Town",
            "phone": "9333444555",
            "hours": "11 AM - 10 PM",
            "speciality": "Paneer Tikka, Dal Makhani"
        },

        "Taj Flavors": {
            "cuisine": "Indian",
            "rating": 4.7,
            "address": "999 Taste Lane, Premium Zone",
            "phone": "9444555666",
            "hours": "12 PM - 11 PM",
            "speciality": "Biryani, Tandoori Chicken"
        },

        "Golden Wok": {
            "cuisine": "Chinese",
            "rating": 4.8,
            "address": "777 Wok Street, Central Market",
            "phone": "9555666777",
            "hours": "11 AM - 11 PM",
            "speciality": "Szechuan Noodles, Dim Sum"
        }
    }

    # Case-insensitive restaurant lookup

    for name, information in details.items():

        if name.lower() == restaurant_name.strip().lower():
            return information

    return {
        "error": f"Restaurant '{restaurant_name}' not found."
    }


# ============================================================
# 7. TOOL 3: CHECK RESERVATION AVAILABILITY
# ============================================================

@tool
def check_reservation_availability(
    restaurant_name: str,
    date: str,
    party_size: int
) -> str:
    """
    Check reservation availability for a restaurant.

    Inputs:
    - restaurant_name: Name of the restaurant.
    - date: Reservation date in YYYY-MM-DD format.
    - party_size: Number of people.

    Returns available, fully booked or not found.
    """

    available_slots = {

        "Spice Palace": {
            "2024-11-15": True,
            "2024-11-16": False,
            "2024-11-17": True
        },

        "Pizza Bella": {
            "2024-11-15": False,
            "2024-11-16": True,
            "2024-11-17": True
        },

        "Dragon House": {
            "2024-11-15": True,
            "2024-11-16": True,
            "2024-11-17": False
        },

        "Taco Fiesta": {
            "2024-11-15": True,
            "2024-11-16": True,
            "2024-11-17": True
        },

        "Curry House": {
            "2024-11-15": True,
            "2024-11-16": False,
            "2024-11-17": True
        },

        "Taj Flavors": {
            "2024-11-15": False,
            "2024-11-16": True,
            "2024-11-17": True
        }
    }

    # Validate party size

    if party_size < 1:
        return "Please provide a valid party size."

    # Find restaurant case-insensitively

    matched_name = None

    for name in available_slots:

        if name.lower() == restaurant_name.strip().lower():
            matched_name = name
            break

    if matched_name is None:
        return "Not found: Restaurant does not exist."

    # Check whether the requested date exists

    if date not in available_slots[matched_name]:
        return "Not found: Reservation date is not available."

    # Check availability

    is_available = available_slots[matched_name][date]

    if is_available:

        return (
            f"✓ {matched_name} has availability "
            f"for {party_size} people on {date}."
        )

    return (
        f"✗ {matched_name} is fully booked "
        f"for {date}."
    )


# ============================================================
# 8. REGISTER ALL THREE TOOLS
# ============================================================

tools = [
    search_restaurants_by_cuisine,
    get_restaurant_details,
    check_reservation_availability
]


# ============================================================
# 9. DEFINE SYSTEM PROMPT
# ============================================================

system_prompt = """

You are a helpful restaurant recommendation assistant.

You have access to exactly three tools:

1. Search restaurants by cuisine.
2. Get restaurant details.
3. Check reservation availability.

INSTRUCTIONS:

- Use the appropriate tool whenever necessary.
- Never invent restaurant information.
- Never make up restaurant names, ratings, addresses,
  phone numbers, opening hours or reservation availability.
- Only provide information supported by the available tools.
- Do not answer general knowledge questions.
- If a user asks something outside your available capabilities,
  politely explain that you can only help with restaurant searches,
  restaurant details and reservation availability.
- Use conversation history to understand follow-up questions.
- If the user mentions a restaurant discussed previously,
  use the restaurant details tool when appropriate.
- If the requested restaurant or date is not found,
  communicate that clearly.
- Do not claim that a reservation has actually been booked.
  You can only check availability.
- Be friendly, conversational and concise.

"""


# ============================================================
# 10. CREATE RESTAURANT AI AGENT
# ============================================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt
)


# ============================================================
# 11. CREATE CHAT FUNCTION
# ============================================================

def chat_with_agent(user_message, chat_history=None):
    """
    Send a user message to the restaurant AI agent.

    Maintains conversation history so that the agent
    can understand follow-up questions.
    """

    if chat_history is None:
        chat_history = []

    # Add new user message to existing history

    messages = chat_history + [
        {
            "role": "user",
            "content": user_message
        }
    ]

    # Invoke the AI agent

    result = agent.invoke({
        "messages": messages
    })

    # Extract final assistant response

    content = result["messages"][-1].content

    # Handle text and structured response formats

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict) and item.get("type") == "text":
                text_parts.append(item.get("text", ""))

        response = "".join(text_parts)

    else:

        response = str(content)

    # Update conversation history

    updated_history = messages + [
        {
            "role": "assistant",
            "content": response
        }
    ]

    return response, updated_history


# ============================================================
# 12. STREAMLIT CHAT INTERFACE
# ============================================================

st.title("🍽️ Restaurant AI Assistant")

st.caption(
    "Your AI assistant for restaurant recommendations, "
    "restaurant details and reservation availability."
)

st.divider()


# Initialize conversation history

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# Sidebar

with st.sidebar:

    st.header("Restaurant Assistant")

    st.write(
        "I can help you with:"
    )

    st.markdown(
        """
        - Search restaurants by cuisine.
        - Get restaurant details.
        - Check reservation availability.
        """
    )

    st.divider()

    if st.button("Clear Conversation", use_container_width=True):

        st.session_state.chat_history = []

        st.rerun()


# Display previous conversation messages

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# Get user input

if user_input := st.chat_input("Ask me about restaurants..."):

    # Display user message

    with st.chat_message("user"):

        st.markdown(user_input)

    # Generate assistant response

    with st.chat_message("assistant"):

        with st.spinner("Finding the best answer for you..."):

            try:

                response, updated_history = chat_with_agent(
                    user_input,
                    st.session_state.chat_history
                )

                st.markdown(response)

                # Save updated conversation

                st.session_state.chat_history = updated_history

            except Exception as error:

                st.error(
                    "Something went wrong while processing "
                    "your request. Please try again."
                )

                st.exception(error)
