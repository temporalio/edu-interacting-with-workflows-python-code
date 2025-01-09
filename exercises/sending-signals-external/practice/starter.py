import asyncio

from shared import TASK_QUEUE_NAME, WORKFLOW_ID_PREFIX, FULFILLED_WORKFLOW_ID_PREFIX, create_pizza_order
from temporalio.client import Client
from workflow import PizzaOrderWorkflow
from workflow import FulfillOrderWorkflow


async def main():
    # Create client connected to server at the given address
    client = await Client.connect("localhost:7233", namespace="default")

    order = create_pizza_order()

    # Execute a workflow
    handle = await client.start_workflow(
        PizzaOrderWorkflow.order_pizza,
        order,
        id=WORKFLOW_ID_PREFIX + f"{order.order_number}",
        task_queue=TASK_QUEUE_NAME,
    )

    # TODO Part D: Start the `FulfillOrderWorkflow`.
    # You can use the `PizzaOrderWorkflow` above as a reference.
    # It can use the same Task Queue, but needs to use a different Workflow ID.
    # Also, you don't need the handle because you don't
    # need to await it or use its return value.

    result = await handle.result()

    print(f"Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
