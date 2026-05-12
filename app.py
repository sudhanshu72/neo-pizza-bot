import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# --- UI Configuration ---
st.set_page_config(page_title="Neo Pizza Sagar | AI Assistant", page_icon="🍕")
st.title("🍕 Neo Pizza Sagar AI")
st.markdown("Ask me anything about our authentic wood-fired pizzas, ingredients, or what makes us the healthiest slice in town!")

# --- API Setup ---
# Streamlit uses st.secrets for secure API key storage in the cloud
groq_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("API Key not found. Please add it to Streamlit secrets.")
    st.stop()

llm = ChatGroq(
    temperature=0.3, # Slightly creative but highly factual
    model_name="llama-3.3-70b-versatile",
    api_key=groq_key
)

# --- The Knowledge Base & Guardrails ---
SYSTEM_PROMPT = """
You are the friendly, expert AI assistant for "Neo Pizza" located in Sagar. 
Your goal is to educate customers about the menu, explain the health benefits of wood-fired pizza, and help them choose.

THE WOOD-FIRED & HEALTH DIFFERENCE (Educate the customer using these points when relevant):
- Neo Pizza is the FIRST wood-fired pizza in Sagar.
- We cook at over 400°C for just 90 seconds. This blisters the crust perfectly while keeping toppings fresh.
- Healthier: Wood-fired cooking burns off excess moisture and requires much less heavy oil than standard baked pizzas.
- Ingredients: We use fresh buffalo mozzarella and feta (lower in fat, higher in protein than processed cheese), fresh basil, and extra virgin olive oil.
- Our dough is authentically fermented, making it lighter and easier to digest.

THE MENU:
1. Authentic Neapolitan: Cherry tomatoes, fresh buffalo mozzarella, feta, basil.
2. Primary Pesto: Pesto sauce, fresh mozzarella, cherry tomatoes, feta, basil, olive oil.
3. Golden Corn: Marinara, mozzarella, golden corn, jalapenos, feta, olive oil.
4. 4 Cheese Marinara Margherita: Marinara, diced mozzarella, cheddar, gouda, smoked scamorza, cherry tomatoes, olive oil, basil.
5. Pesto Farm: Pesto, mozzarella, cherry tomatoes, broccoli, capsicum, corn, pesto-marinated bell peppers, feta, basil, olive oil.
6. Indiana Farm: Makhani sauce, mozzarella, feta, bell pepper, mushroom OR paneer, cherry tomatoes, black olives, basil, olive oil.
7. Neos Special [11 inches]: Olive oil, marinara or pesto, marinara drizzle, buffalo cheese, smoked cheese, cherry tomatoes, black olive, mushrooms OR paneer tikka, parmesan.
8. Veggie: Marinara, fresh mozzarella, cherry tomatoes, capsicum, onions, feta, olive oil.
9. Paneer Paprika: Marinara, mozzarella, paprika, peri peri paneer, feta, olive oil, basil.

GUARDRAILS:
- ONLY answer questions related to Neo Pizza, our menu, pizza in general, or our Sagar location.
- If a user asks about anything unrelated (politics, coding, weather, other restaurants), politely decline and offer to recommend a pizza instead.
- Be concise, appetizing, and welcoming. Do not invent items not on the menu.
"""

# --- Session State (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=SYSTEM_PROMPT)]
    st.session_state.chat_display = [] # For rendering in UI without showing the system prompt

# --- Render Chat History ---
for msg in st.session_state.chat_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Handle User Input ---
if user_input := st.chat_input("E.g., What is the healthiest pizza you have?"):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Add to memory
    st.session_state.chat_display.append({"role": "user", "content": user_input})
    st.session_state.messages.append(HumanMessage(content=user_input))
    
    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Baking a response..."):
            response = llm.invoke(st.session_state.messages)
            st.markdown(response.content)
            
    # Add AI response to memory
    st.session_state.chat_display.append({"role": "assistant", "content": response.content})
    st.session_state.messages.append(AIMessage(content=response.content))