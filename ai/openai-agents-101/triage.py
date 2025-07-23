import asyncio

from agents import Agent, Runner

import utils

utils.setup_trace(name="agents_101")
utils.setup_openai()

async def main():
    spanish_agent = Agent(
        name="Spanish agent",
        instructions="You only speak Spanish.",
    )

    english_agent = Agent(
        name="English agent",
        instructions="You only speak English",
    )

    triage_agent = Agent(
        name="Triage agent",
        instructions="Handoff to the appropriate agent based on the language of the request.",
        handoffs=[spanish_agent, english_agent],
    )

    result = await Runner.run(triage_agent, input="Hola, ¿cómo estás?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
