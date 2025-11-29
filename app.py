from dotenv import load_dotenv
from agents import Agent, Runner, trace, OpenAIChatCompletionsModel
from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
import os
import gradio as gr
import asyncio
from pathlib import Path
from datetime import datetime

load_dotenv(override=True)

# Gemini configuration
google_api_key = os.getenv('GOOGLE_API_KEY')
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Create Gemini client and model
gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)

# MCP server parameters 
files_params = {
    "command": "python3",
    "args": ["server.py"],
    "env": {}
}


import gradio as gr

async def gradio_story_writer(prompt):
    async with MCPServerStdio(params=files_params, client_session_timeout_seconds=300) as file_server:
        agent = Agent(
            name="writer", 
            model=gemini_model,
            mcp_servers=[file_server],
        )
        with trace("writer"):
            result = await Runner.run(agent, prompt)
            return result.final_output

def launch_gradio():
    # Gradio can't run async functions directly, so we wrap the coroutine
    def blocking_func(prompt):
        return asyncio.run(gradio_story_writer(prompt))
    iface = gr.Interface(
        fn=blocking_func,
        inputs=gr.Textbox(label="Enter your writing prompt"),
        outputs=gr.Textbox(label="Agent Output"),
        title="Gemini Story Writer",
        description="Enter a prompt for the Gemini-powered agent to write and save a file."
    )
    iface.launch()

if __name__ == "__main__":
    launch_gradio()