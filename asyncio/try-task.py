"""Test asyncio Tasks behavior."""

import asyncio


async def main():
    async def say_after(delay, what):
        await asyncio.sleep(delay)
        print(what)

    # Create two tasks
    task1 = asyncio.create_task(say_after(2, 'hello'))
    task2 = asyncio.create_task(say_after(1, 'world'))

    print(f'Task1: {task1}')
    print(f'Task2: {task2}')

    # Wait for both tasks to complete
    await task1
    await task2

    print(f'Task1 done: {task1.done()}')
    print(f'Task2 done: {task2.done()}')

    # Await agent
    await task1
    await task2


async def raise_in_task():
    async def faulty_coroutine():
        print("Starting faulty coroutine")
        await asyncio.sleep(1)
        raise ValueError("An error occurred in the task")

    task = asyncio.create_task(faulty_coroutine())

    try:
        await task
    except ValueError as e:
        print(f'Caught exception from task: {e}')

    # await agent
    await task


async def return_in_task():
    async def returning_coroutine():
        print("Starting returning coroutine")
        await asyncio.sleep(1)
        return "Task completed successfully"

    task = asyncio.create_task(returning_coroutine())

    result = await task
    print(f'Task result: {result}')

    # await agent
    result = await task
    print(f'Task result on second await: {result}')


async def wait_task_done_without_await():
    async def simple_coroutine():
        await asyncio.sleep(1)
        print("Simple coroutine completed")

    task = asyncio.create_task(simple_coroutine())

    while not task.done():
        print("Waiting for task to complete...")
        await asyncio.sleep(0.5)

    print("Task is done now.")


if __name__ == '__main__':
    asyncio.run(wait_task_done_without_await())
