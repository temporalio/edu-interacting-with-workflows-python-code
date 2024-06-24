import asyncio
import time

from temporalio.client import Client

async def main():
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle("signals")
    await handle.signal("submit_greeting", "User 1")
    await asyncio.sleep(1)
    await handle.signal("exit")

if __name__ == "__main__":
    asyncio.run(main())
