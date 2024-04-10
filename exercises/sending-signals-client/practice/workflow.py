import asyncio
from typing import List

from temporalio import workflow
from temporalio.client import Client
from temporalio.worker import Worker


@workflow.defn
class MyWorkflow:
    def __init__(self) -> None:
        self._pending_greetings: asyncio.Queue[str] = asyncio.Queue()
        self._exit = False

    @workflow.run
    async def run(self) -> List[str]:
        greetings: List[str] = []
        workflow.logger.info("Running workflow.")
        print("Running workflow.")
        while True:
            await workflow.wait_condition(
                lambda: not self._pending_greetings.empty() or self._exit
            )

            while not self._pending_greetings.empty():
                greetings.append(f"Hello, {self._pending_greetings.get_nowait()}")

            if self._exit:
                return greetings

    # TODO Part A: Define a Signal function, annoted with @workflow.signal.
    # It should take an additional string argument called `name`.
    # When the signal is received, it should call await self._pending_greetings.put(name).
    # You can use the `exit()` Signal function below as a reference.
    @workflow.signal
    async def submit_greeting(self, name: str) -> None:
        await self._pending_greetings.put(name)

    @workflow.signal
    def exit(self) -> None:
        self._exit = True


async def main():
    # Start client
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    async with Worker(
        client,
        task_queue="signals",
        workflows=[MyWorkflow],
    ):
        result = await client.execute_workflow(
            MyWorkflow.run,
            id="signals",
            task_queue="signals",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
