# app.py
import streamlit as st
import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from phi.agent import Agent
from phi.model.together import Together
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.newspaper4k import Newspaper4k
from phi.tools.yfinance import YFinanceTools

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = None
if 'config' not in st.session_state:
    st.session_state.config = None
if 'factory' not in st.session_state:
    st.session_state.factory = None

class Config:
    """Configuration class for AI agents"""
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.together_api_key = os.getenv('TOGETHER_API_KEY')
        if not self.together_api_key:
            raise ValueError("TOGETHER_API_KEY environment variable is not set")

class MovieScript(BaseModel):
    """Data model for movie script generation"""
    setting: str = Field(..., description="Setting for a blockbuster movie")
    ending: str = Field(..., description="Movie ending")
    genre: str = Field(..., description="Movie genre")
    name: str = Field(..., description="Movie name")
    characters: List[str] = Field(..., description="Character names")
    storyline: str = Field(..., description="3 sentence storyline")

class AIAgentFactory:
    """Factory class for creating different types of AI agents"""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_model = Together(
            api_key=config.together_api_key,
            id="meta-llama/Llama-3.3-70B-Instruct-Turbo"
        )

    def create_researcher_agent(self) -> Agent:
        """Creates a researcher agent for article writing"""
        return Agent(
            model=self.base_model,
            tools=[DuckDuckGo(), Newspaper4k()],
            description="You are a senior NYT researcher writing an article on a topic.",
            instructions=[
                "For a given topic, search for the top 5 links.",
                "Then read each URL and extract the article text, if a URL isn't available, ignore it.",
                "Analyse and prepare an NYT worthy article based on the information.",
            ],
            markdown=True,
            show_tool_calls=True,
            add_datetime_to_instructions=True,
        )

    def create_finance_agent(self) -> Agent:
        """Creates a finance agent for market analysis"""
        return Agent(
            model=self.base_model,
            tools=[YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True
            )],
            instructions=["Use tables to display data"],
            show_tool_calls=True,
            markdown=True,
        )

def initialize_app():
    """Initialize the application configuration and factory"""
    if st.session_state.config is None:
        try:
            st.session_state.config = Config()
            st.session_state.factory = AIAgentFactory(st.session_state.config)
            st.success("Application initialized successfully!")
        except ValueError as e:
            st.error(f"Initialization failed: {str(e)}")
            st.stop()

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    st.set_page_config(
        page_title="AI Research Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    # Sidebar
    with st.sidebar:
        st.title("🤖 AI Research Assistant")
        st.markdown("---")
        initialize_app()
        
        # Agent selection with icons
        agent_type = st.selectbox(
            "Select Assistant Type",
            ["📰 Researcher", "📊 Finance"],
            format_func=lambda x: x.split(" ")[1]
        )
        
        st.markdown("---")
        # Help section in sidebar
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. Select your assistant type above
            2. For Researcher: Enter any topic to get a researched article
            3. For Finance: Enter a stock symbol to get financial analysis
            4. Use the chat input below to interact
            5. Clear chat history using the button below
            """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.experimental_rerun()
    
    # Main content area
    st.title(f"{agent_type.split(' ')[1]} Assistant")
    
    # Initialize or switch agent based on selection
    selected_type = agent_type.split(" ")[1]
    if selected_type != st.session_state.get('last_agent_type'):
        if selected_type == "Researcher":
            st.session_state.current_agent = st.session_state.factory.create_researcher_agent()
        else:  # Finance
            st.session_state.current_agent = st.session_state.factory.create_finance_agent()
        st.session_state.last_agent_type = selected_type
        st.session_state.chat_history = []

    # Display chat interface
    display_chat_history()

    # Chat input
    if prompt := st.chat_input(
        "Researcher: Enter a topic | Finance: Enter a stock symbol (e.g., AAPL)"
    ):
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = st.session_state.current_agent.run(prompt)
                st.markdown(response.content)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": response.content}
                )

if __name__ == "__main__":
    main()
