## Exercise #1: Sending an External Signal

During this exercise, you will:

- Define and handle a Signal
- Retrieve a handle on the Workflow to Signal
- Send an external Signal
- Use a Temporal Client to submit execution requests for both Workflows

Make your changes to the code in the `practice` subdirectory (look for
`TODO` comments that will guide you to where you should make changes to
the code). If you need a hint or want to verify your changes, look at
the complete version in the `solution` subdirectory.

## Part A: Defining and Handling the Signal

1. This exercise contains one Client that runs two different Workflows
   — `PizzaWorkflow.order_pizza` and `FulfillOrderWorkflow.fulfill_order`. Both
   Workflows are defined in `workflow.py`. `PizzaWorkflow.order_pizza` is
   designed not to complete its final activity — `send_bill` — until it receives
   a Signal from `FulfillOrderWorkflow.fulfill_order`. You'll start by defining
   that Signal. Edit `workflow.py`. At the bottom of the `PizzaWorkflow`
   definition, add a Signal function for `fulfill_order_signal()`. It should be
   decorated with `@workflow.signal` and take an additional boolean argument
   called `success`. When the signal is received, if `success==True`, it should
   call `self._pending_confirmation.put(True)`, enabling the `PizzaWorkflow` to
   compelete.
2. Save the file.

## Part B: Getting a Handle on your Workflow

1. Continue editing the `workflow.py` file.
2. Within the `FulfillOrderWorkflow` definition, after running the `make_pizza` and `deliver_pizzas` Activities, call `workflow.get_external_workflow_handle()` using the Workflow ID from `starter.py` to get a Handle on this Workflow. Return it to a variable like `handle`.
3. Save the file.

## Part C: Signaling your Workflow

Now you will add the `handle.signal()` call itself.

1. Continue editing the `workflow.py` file.
2. After the line where you obtain your Workflow `handle` by running `get_external_workflow_handle()`, add another line with a call to `handle.signal()`. It should call the `fulfill_order_signal` Signal with an additional `True` argument. Don't forget to call `handle.signal()` with `await` because it is an asychronous function.
3. Save and close the file.

## Part D: Making your Client start both Workflows

1. Finally, open `starter.py` for editing. Currently, this Client only starts
   the `PizzaWorkflow`. Directly after the `client.start_workflow()` call for
   the `PizzaWorkflow`, add another call that starts the `FulfillOrderWorkflow`.
   You can use the call that starts the `PizzaWorkflow` as a reference. It can
   use the same Task Queue, but needs to use a different Workflow ID. 
2. Save and close the file.

## Part E: Running both Workflows

At this point, you can run your Workflows.

1. In one terminal, run `python worker.py`.
2. In another terminal, run `python starter.py`. You should receive output from
   both Workflows having started and returning the expected result:

   ```
   Result:
   OrderConfirmation(order_number='XD001', status='SUCCESS', confirmation_number='P24601', billing_timestamp=1712947330, amount=2700)
   ```

3. If you look at the terminal running your Worker, you should see logging from
   each individual step run by both Workflows, including the Signal being sent
   and all the related activities:

   ```
   ...
   INFO:temporalio.activity:Starting delivery XD001 to Address(line1='741 Evergreen Terrace', line2='Apartment 221B', city='Albuquerque', state='NM', postal_code='87101') ({'activity_id': '2', 'activity_type': 'deliver_pizzas', 'attempt': 1, 'namespace': 'default', 'task_queue': 'pizza-tasks', 'workflow_id': 'fulfilled-workflow-order-XD001', 'workflow_run_id': 'a87ad640-65c4-478f-9c73-b0a47293148f', 'workflow_type': 'FulfillOrderWorkflow'})
   INFO:temporalio.activity:XD001 delivered. ({'activity_id': '2', 'activity_type': 'deliver_pizzas', 'attempt': 1, 'namespace': 'default', 'task_queue': 'pizza-tasks', 'workflow_id': 'fulfilled-workflow-order-XD001', 'workflow_run_id': 'a87ad640-65c4-478f-9c73-b0a47293148f', 'workflow_type': 'FulfillOrderWorkflow'})
   INFO:temporalio.activity:send_bill invoked: customer: 8675309 amount: 2700 ({'activity_id': '2', 'activity_type': 'send_bill', 'attempt': 1, 'namespace': 'default', 'task_queue': 'pizza-tasks', 'workflow_id': 'pizza-workflow-order-XD001', 'workflow_run_id': '4c7007d9-402c-4eea-b890-cc12f048a3dc', 'workflow_type': 'PizzaOrderWorkflow'})
   ```

### This is the end of the exercise.
