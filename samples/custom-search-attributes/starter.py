import asyncio

from shared import TASK_QUEUE_NAME, WORKFLOW_ID_PREFIX, create_pizza_order, is_order_failed_key
from temporalio.client import Client
from temporalio.common import TypedSearchAttributes, SearchAttributePair
from workflow import PizzaOrderWorkflow


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
        search_attributes=TypedSearchAttributes([
            SearchAttributePair(is_order_failed_key, False)
        ]),
    )

    result = await handle.result()

    print(f"Result:\n{result}")


if __name__ == "__main__":
    asyncio.run(main())
