# Phi Agent Showcase
A showcase of Phi Agent capabilities featuring a Streamlit-powered Research and Finance AI assistant built with Meta Llama 3.3 70B Instruct Turbo.

## Features
- 📰 Research Assistant: Generates comprehensive articles on any topic using web research
- 📊 Finance Assistant: Provides detailed financial analysis and market insights
- 🤖 Multiple LLM Support: Compatible with various AI models:
  - Together AI (Meta Llama 3.3 70B Instruct Turbo)
  - OpenAI (GPT-4, GPT-3.5)
  - Anthropic (Claude)
  - Groq
  - Grok
  - And more!
- 💬 Interactive chat interface
- 🔄 Real-time responses
- 🎯 Easy-to-use Streamlit interface

## Demo
![Demo GIF](placeholder_for_demo.gif)

## Prerequisites
- Python 3.8+
- Together AI API key (or API key for your preferred LLM provider)
- Internet connection for web research

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/phi-agent-showcase.git
cd phi-agent-showcase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```env
# Required for Together AI (default)
TOGETHER_API_KEY=your_together_api_key_here

# Optional: For using other models
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GROQ_API_KEY=your_groq_key_here
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Select the assistant type from the sidebar:
   - Research Assistant: For article generation and research
   - Finance Assistant: For stock analysis and market insights

3. Enter your query in the chat input:
   - For Research: Enter any topic
   - For Finance: Enter a stock symbol (e.g., AAPL)

## Switching Models

To use a different LLM provider, modify the `AIAgentFactory` class in `app.py`:

```python
# For OpenAI
from phi.model.openai import OpenAIChat

self.base_model = OpenAIChat(model="model name of your choice")

# For Anthropic
from phi.model.anthropic import Anthropic

self.base_model = Anthropic(model="model name of your choice")

# For Groq
from phi.model.groq import Groq

self.base_model = Groq(model="model name of your choice")
```

## Project Structure
```
phi-agent-showcase/
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
├── .env.example       # Example environment variables
├── .gitignore         # Git ignore file
├── LICENSE            # MIT License
└── README.md          # Project documentation
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Phi Framework](https://github.com/phidatahq/phidata) for the excellent agent framework
- The open-source community for various tools and libraries used in this project

## Disclaimer
This is a demonstration project to showcase the capabilities of Phi Agent. Please ensure you comply with the terms of service and usage policies of the respective LLM providers.
