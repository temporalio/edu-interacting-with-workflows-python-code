from time import time

from shared import Address, Bill, Distance, OrderConfirmation, PizzaOrder
from temporalio import activity
from temporalio.exceptions import ApplicationError


class PizzaOrderActivities:
    @activity.defn
    async def get_distance(self, address: Address) -> Distance:
        activity.logger.info(
            "get_distance invoked; determining distance to customer address"
        )

        # This is a simulation, which calculates a fake (but consistent)
        # distance for a customer address based on its length. The value
        # will therefore be different when called with different addresses,
        # but will be the same across all invocations with the same address.

        kilometers = len(address.line1) + len(address.line2) - 10
        if kilometers < 1:
            kilometers = 5

        distance = Distance(kilometers=kilometers)

        activity.logger.info(f"get_distance complete: {distance}")
        return distance

    @activity.defn
    async def send_bill(self, bill: Bill) -> OrderConfirmation:
        activity.logger.info(
            f"send_bill invoked: customer: {bill.customer_id} amount: {bill.amount}"
        )

        charge_amount = bill.amount

        if charge_amount > 3000:
            activity.logger.info("applying discount")

            charge_amount -= 500

        if charge_amount < 0:
            error_message = f"invalid charge amount: {charge_amount}"
            activity.logger.error(error_message)

            raise ApplicationError(error_message)

        confirmation = OrderConfirmation(
            order_number=bill.order_number,
            status="SUCCESS",
            confirmation_number="P24601",
            billing_timestamp=time(),
            amount=charge_amount,
        )

        return confirmation

    @activity.defn
    async def make_pizzas(self, pizza_order: PizzaOrder):
        activity.logger.info(
            f"Starting to make pizzas for order: {pizza_order.order_number}" 
        )

        for item in pizza_order.items:
            activity.logger.info(
                f"Making pizza: {item.description}"
            )
            # Simulate the time taken to make a pizza.
        
        activity.logger.info(
            f"All pizzas for order {pizza_order.order_number} are ready!"
        )

    @activity.defn
    async def deliver_pizzas(self, pizza_order: PizzaOrder):
        activity.logger.info(
            f"Starting delivery {pizza_order.order_number} to {pizza_order.address}"
        )
        # Simulate the time to make delivery
        activity.logger.info(
            f"{pizza_order.order_number} delivered."
        )
