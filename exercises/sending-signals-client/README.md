## Exercise #2: Sending a Signal from a Client

During this exercise, you will:

- Define and handle a Signal
- Retrieve a handle on the Workflow to Signal
- Use a Temporal Client to send the Signal

Make your changes to the code in the `practice` subdirectory (look for
`TODO` comments that will guide you to where you should make changes to
the code). If you need a hint or want to verify your changes, look at
the complete version in the `solution` subdirectory.

## Part A: Defining a Signal

In this part of the exercise, you will define a Signal named `submit_greeting`, and let the Workflow know what to do when it encounters the Signal.

1. Edit the `workflow.py` file.
2. `workflow.py` currently contains a Workflow definition that includes one Signal function, `exit()`. The Workflow runs a blocking `while True` loop that will cause it to wait for either the `exit()` Signal or another `submit_greeting()` Signal before doing anything. Within the Workflow definition, just above the `exit()` Signal function, add a Signal function for `submit_greeting()`. It should take an additional string argument called `name`. When the signal is received, it should call `await self._pending_greetings.put(name)`. You can use the `exit()` Signal function below as a reference.
3. Save the file.

## Part B: Getting a Handle on your Workflow

In this part of the exercise, you will create another Temporal client that sends a Signal. `signalclient.py` currently contains a near-empty Temporal client -- it looks like a Starter or a Worker, but it does not register any Workflows or do anything. You will use this client to send a Signal.

1. Edit the `signalclient.py` file.
2. Within the `main()` function, directly after the `Client.connect()` call, call `client.get_workflow_handle()` using the Workflow ID from `workflow.py` to get a Handle on this Workflow. Return it to a variable like `handle`. 
3. Save the file.

## Part C: Signaling Your Workflow

Now you will add the `handle.signal()` call itself.

1. Continue editing the `signalclient.py` file.
2. After the line where you obtain your Workflow `handle` by running `get_workflow_handle()`, add another line with a call to `handle.signal()`. It should call the `submit_greeting` signal with an additional username argument like `User 1`. Don't forget to call `handle.signal()` with `await` because it is an asychronous function.
3. On the next line, add a call to `time.sleep(1)` to make this client wait before sending another signal.
4. Finally, add a call to `await handle.signal("exit")`. This will send the other Signal type handled by this Workflow — `exit` — and cause it to return.

## Part D: Start Your Workflow

At this point, you can run your Workflow. It should run normally but wait to receive a Signal.

1. In a terminal window, run `python workflow.py`. This file contains both a Temporal Worker and a Workflow definition that will execute immediately after starting the Worker. You will receive some logging output:

```
Running workflow.
```

2. Your Workflow will not return as you added a blocking Signal call. In the next step, you will Signal your workflow.

## Part E: Send Your Signal

1. In a second terminal, run `python signalclient.py`. It will send a Signal to your Workflow. This should cause your Workflow to return with a result, containing the `User 1` argument from `signalclient.py`.

```
Result: ['Hello, User 1']
```

2. You have successfully sent a Signal from a Temporal Client to a running Workflow.

### This is the end of the exercise.
