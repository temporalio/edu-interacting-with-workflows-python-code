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
        self._current_state = "started"
        print("Running workflow.")
        while True:
            self._current_state = "waiting for signal"
            await workflow.wait_condition(
                lambda: not self._pending_greetings.empty() or self._exit
            )

            while not self._pending_greetings.empty():
                greetings.append(f"Hello, {self._pending_greetings.get_nowait()}")

            if self._exit:
                self._current_state = "completed"
                return greetings

    @workflow.query
    def current_state_query(self) -> str:
        return self._current_state

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
        task_queue="queries",
        workflows=[MyWorkflow],
    ):
        result = await client.execute_workflow(
            MyWorkflow.run,
            id="queries",
            task_queue="queries",
        )
        print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
