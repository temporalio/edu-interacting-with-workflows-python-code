import asyncio
import logging

from activities import PizzaOrderActivities
from shared import TASK_QUEUE_NAME
from temporalio.client import Client
from temporalio.worker import Worker
from workflow import PizzaOrderWorkflow, FulfillOrderWorkflow


async def main():
    logging.basicConfig(level=logging.INFO)
    client = await Client.connect("localhost:7233", namespace="default")

    activities = PizzaOrderActivities()

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[PizzaOrderWorkflow,FulfillOrderWorkflow],
        activities=[activities.get_distance, activities.send_bill, activities.make_pizzas, activities.deliver_pizzas],
    )
    logging.info(f"Starting the worker....{client.identity}")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
