import asyncio
from datetime import timedelta

from temporalio import workflow
from temporalio.exceptions import ApplicationError

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import PizzaOrderActivities
    from shared import Bill, OrderConfirmation, PizzaOrder

@workflow.defn
class PizzaOrderWorkflow:
    def __init__(self) -> None:
        self._pending_confirmation: asyncio.Queue[str] = asyncio.Queue()

    @workflow.run
    async def order_pizza(self, order: PizzaOrder) -> OrderConfirmation:
        workflow.logger.info(f"order_pizza workflow invoked with {input}")

        address = order.address

        total_price = 0
        for pizza in order.items:
            total_price += pizza.price

        distance = await workflow.execute_activity_method(
            PizzaOrderActivities.get_distance,
            address,
            start_to_close_timeout=timedelta(seconds=5),
        )

        if order.is_delivery and distance.kilometers > 25:
            error_message = "customer lives outside the service area"
            workflow.logger.error(error_message)
            raise ApplicationError(error_message)

        workflow.logger.info(f"distance is {distance.kilometers}")

        while True:
            await workflow.wait_condition(
                lambda: not self._pending_confirmation.empty() or self._exit
            )

            while not self._pending_confirmation.empty():
                bill = Bill(
                    customer_id=order.customer.customer_id,
                    order_number=order.order_number,
                    description="Pizza order",
                    amount=total_price,
                )
                confirmation = await workflow.execute_activity_method(
                    PizzaOrderActivities.send_bill,
                    bill,
                    start_to_close_timeout=timedelta(seconds=5),
                )
                return confirmation

    @workflow.signal
    async def fulfill_order_signal(self, success: bool) -> None:
        await self._pending_confirmation.put(True)


@workflow.defn
class FulfillOrderWorkflow:
    @workflow.run
    async def fulfill_order(self, order: PizzaOrder) -> OrderConfirmation:
        workflow.logger.info(f"fulfill_order workflow invoked with {input}")

        await workflow.execute_activity_method(
            PizzaOrderActivities.make_pizzas,
            PizzaOrder,
            start_to_close_timeout=timedelta(seconds=5),
        )

        await workflow.execute_activity_method(
            PizzaOrderActivities.deliver_pizzas,
            PizzaOrder,
            start_to_close_timeout=timedelta(seconds=5),
        )

        handle = workflow.get_external_workflow_handle("signals")
        await handle.signal("fulfill_order_signal", True)

        return None
