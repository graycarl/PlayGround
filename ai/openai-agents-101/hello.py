import asyncio

from agents import Agent, Runner

import utils

utils.setup_trace(name="agents_101")
utils.setup_openai()

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus. in chinese.",
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
