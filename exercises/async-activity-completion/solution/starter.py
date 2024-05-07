import asyncio

from temporalio.client import Client
from workflow import MyWorkflow

async def main():
    # Start client
    client = await Client.connect("localhost:7233")
    print("Running Async Completion Workflow. Check Worker for output.")

    await client.start_workflow(
        MyWorkflow.run,
        id="async",
        task_queue="async",
    )

if __name__ == "__main__":
    asyncio.run(main())
