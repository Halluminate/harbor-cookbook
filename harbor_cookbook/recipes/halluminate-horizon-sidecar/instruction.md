# Halluminate Horizon Sidecar

There is a Halluminate/Horizon problem environment available through the `halluminate` MCP server.

Problem id:

```text
wyatt-test-problem-tagging-25
```

First call `setup_problem` with that problem id to initialize the environment and receive the actual task statement. Then solve the task using the returned instructions and the available MCP tools.

Do not call `grade_problem`; Harbor's verifier calls it after your run.
