import asyncio
import logging

from temporalio.client import Client
from temporalio.worker import Worker
from workflow import GreetingComposer, MyWorkflow

async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233")

    # Run a worker for the workflow
    composer = GreetingComposer(client)
    worker = Worker(
        client,
        task_queue="async",
        workflows=[MyWorkflow],
        activities=[composer.compose_greeting]
    )
    logging.info(f"Starting the worker....{client.identity}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
