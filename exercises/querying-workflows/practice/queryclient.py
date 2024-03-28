import asyncio
import time

from temporalio.client import Client
from workflow import MyWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle("queries")
    # TODO Part B: Send a Query using `handle.query()`.
    # Note that `MyWorkflow` has been imported from `workflow.py` above.
    # You can use this to call the Query definition.

if __name__ == "__main__":
    asyncio.run(main())
