# Exercise #4: Asynchronous Activity Completion

During this exercise, you will:

- Retrieve a task token from your Activity execution
- Call `activity.raise_complete_async()` to indicate that the Activity is waiting for an external completion.
- Use another Activity method to communicate the result of the asynchronous Activity back to the Workflow

Make your changes to the code in the `practice` subdirectory (look for `TODO` comments that will guide you to where you should make changes to the code). If you need a hint or want to verify your changes, look at the complete version in the `solution` subdirectory.

## Part A: Retrieving the Task Token

1. `workflow.py` is the only file in this Exercise — it contains a Worker, a Workflow, an Activity with two methods, and a Starter, all in one. This is intended to showcase how you can consolidate your Temporal logic using the Python SDK. Edit `workflow.py`.
2. Everything in this file is already complete outside of the Activity definition, which contains two different methods, `compose_greeting()` and `complete_greeting()`. Your Workflow calls `compose_greeting()`, which can then call `complete_greeting()` as a subtask. To do that, use `asyncio.create_task()`.
3. `complete_greeting()` requires a Task Token as an argument, so make sure to obtain it as `activity.info().task_token`.
4. Save the file.

## Part B: Set Your Activity to Return `ErrResultPending`

1. Continue editing the same Activity definition in the `workflow.py` file.
2. To indicate that it will be completing asynchronously, instead of returning, `compose_greeting()` should call `activity.raise_complete_async()`.
3. Save the file.

## Part C: Configure a Client to send CompleteActivity

1. Now, edit the `complete_greeting()` Activity method. The `heartbeat_timeout` configured in your call to `workflow.execute_activity_method()` is 2 seconds. Since an Activity that is completing asynchronously may run for a long time, it should send regular Heartbeats to indicate that it has not failed. With a Heartbeat timeout of 2 seconds, you should add a loop to send a Heartbeat every 1 second. To do this, use `handle.heartbeat()` and `asyncio.sleep(1)`.
2. After several Heartbeats, call `handle.complete()` to complete the Activity.
3. Save the file.

## Part D: Running the Workflow and Completing it Asynchronously

At this point, you can run your Workflow. Because it is all contained in `workflow.py`, you only need to run `python workflow.py`. You should receive the following output:

```
Running workflow.
Completing activity asynchronously
Waiting one second...
Waiting one second...
Waiting one second...
Activity complete!
```

You have successfully demonstrated asynchronous activity completion.

### This is the end of the exercise.


