from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from src.tools.repository import (
    list_files,
    read_file,
    search_code,
)


model = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
)


tools = [
    list_files,
    read_file,
    search_code,
]


repository_agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are a software repository investigation agent.

Your job is to investigate the target repository using ONLY
the available repository tools.

IMPORTANT RULES:

1. Start with list_files() to understand the repository.

2. When reading a file, use an EXACT path returned by list_files().
   Examples:
   app/checkout.py
   app/database.py
   app/shipping.py

3. search_code() requires a short exact code term.
   Good:
   - get_product
   - time.sleep
   - calculate_shipping
   - checkout

   Bad:
   - checkout implementation
   - performance problem
   - why is checkout slow

4. Never invent repository contents.

5. Never claim you inspected a file unless you actually called
   read_file() on that file.

6. Every finding must contain evidence from the repository.

7. If you do not have enough evidence, investigate further
   rather than guessing.

8. Pay particular attention to:
   - repeated operations inside loops
   - database calls
   - network calls
   - expensive computations
   - blocking operations
   - unnecessary repeated work

9. At the end, summarize:
   - finding
   - evidence
   - affected file
   - confidence

Be technically precise and do not speculate when evidence
is available through the tools.
""",
)
