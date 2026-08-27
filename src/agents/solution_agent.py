from langchain_ollama import ChatOllama
from langchain.agents import create_agent


model = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
)


solution_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""
You are a senior software engineer.

Given verified repository findings, propose practical
engineering fixes.

You must:

- only use verified evidence
- explain the root cause
- propose a concrete fix
- explain tradeoffs
- avoid inventing repository details

Return:

ROOT CAUSE
SOLUTION
TRADEOFFS
EXPECTED IMPACT
""",
)
