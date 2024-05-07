import asyncio
from typing import List

from temporalio import activity, workflow
from temporalio.client import Client
from datetime import timedelta

class GreetingComposer:
    def __init__(self, client: Client) -> None:
        self.client = client

    @activity.defn
    async def compose_greeting(self) -> str:
        print("Completing activity asynchronously")
        asyncio.create_task(
            self.complete_greeting(activity.info().task_token)
        )
        activity.raise_complete_async()

    async def complete_greeting(self, task_token: bytes) -> None:
        handle = self.client.get_async_activity_handle(task_token=task_token)
        for _ in range(0, 3):
            print("Waiting one second...")
            await handle.heartbeat()
            await asyncio.sleep(1)

        # Complete using the handle
        await handle.complete()
        print("Activity complete!")


@workflow.defn
class MyWorkflow:
    @workflow.run
    async def run(self) -> List[str]:
        workflow.logger.info("Running workflow.")
        print("Running workflow.")
        return await workflow.execute_activity_method(
            GreetingComposer.compose_greeting,
            start_to_close_timeout=timedelta(seconds=10),
            heartbeat_timeout=timedelta(seconds=2),
        )
