# Exercise #3: Querying Workflows

During this exercise, you will:

- Define and handle a Query
- Create a handle on a Workflow to be queried
- Call the Query from the Client
- Send a Query from the Command line

Make your changes to the code in the `practice` subdirectory (look for
`TODO` comments that will guide you to where you should make changes to
the code). If you need a hint or want to verify your changes, look at
the complete version in the `solution` subdirectory.

## Part A: Defining a Query

In this part of the exercise, you will define your Query.

1. Edit the `workflow.py` file.

The Workflow runs a blocking `while True` loop that will cause it to wait for either the `exit()` Signal or a `submit_greeting()` Signal before doing anything. A variable called `self._current_state` that provides information about the Workflow Execution is also updated in several places. You will add a Query that returns the status of this variable.

2. Anywhere within the Workflow definition (for example, just before your Signal functions), add a Query function called `current_state_query()`. It should be annotated with `@workflow.query` and `return self._current_state`.
3. Save the file.

## Part B: Performing a Query from a Client

In this part of the exercise, you will create another Temporal client that sends a Query. `queryclient.py` currently contains a near-empty Temporal client. You will use this client to send a Query.

1. Edit the `queryclient.py` file. This time, the `handle` has been obtained for you. 
2. Immediately after the line that obtains the `handle`, use `handle.query()` to send a query. You can import the Query type from `workflow.py` — note that `from workflow import MyWorkflow` is included at the imports at the start of this file. Save the query result in a variable like `result`.
3. Immediately after that, log the Query result. For this exercise, a `print()` statement is fine.
4. Save the file.

## Part C: Running the Workflow and the Query

At this point, you can run your Workflow. Because it is the same Workflow from the last exercise with added Query support, it will wait to receive a Signal after starting.

1. In a terminal window, run `python workflow.py`. This file contains both a Temporal Worker and a Workflow definition that will execute immediately after starting the Worker. You will receive some logging output:

```
Running workflow.
```

2. You can now Query your Workflow. In another terminal, run `python queryclient.py`. It will send a Query to your Workflow, which will immediately return the Query result:

```
"waiting for signal"
```

You have now demonstrated sending a Query to a Workflow from a Temporal Client. Before moving on, you can send one from the CLI as well. 

## Part D: Sending a Query from the Command Line

To send a Query from the CLI, use `temporal workflow query` with the same parameters as your client:

```bash
temporal workflow query \
    --workflow-id="queries" \
    --type="current_state_query"
```

It will produce the same result:

```
Query result:
  QueryResult "waiting for signal"
```

Now you can send a Signal to your Workflow so it completes successfully, or just terminate it.

## Part E: Send Your Signal

In the terminal you ran your query in, run `python signalclient.py`. It will send a Signal to your Workflow. This should cause your Workflow to return with a result, containing the `User 1` argument from `signalclient.py`.

```
Result: ['Hello, User 1']
```

Notice that because `workflow.py` shuts down the Worker when
the Workflow finishes, you cannot Query the Workflow after you
have Signalled it to exit. In contrast, if you ran the Worker
in one file/terminal and the Workflow in another, the Workflow
would shut down and the Worker would keep running, and you could
Query it even after it has exited.

### This is the end of the exercise.
