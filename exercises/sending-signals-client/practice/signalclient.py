import asyncio
import time

from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")
    # TODO Part B: Get a Handle on your Workflow.
    # TODO Part C: Send Signals to your Workflow.

if __name__ == "__main__":
    asyncio.run(main())
