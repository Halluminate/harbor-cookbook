# halluminate-horizon-sidecar

Runs a generated Halluminate/Horizon problem image as a Harbor sidecar.

This is a small integration POC for the shape we discussed:

- `main` is Harbor's normal agent runtime.
- `halluminate` is the generated Horizon desktop/world image.
- The sidecar starts the generated desktop entrypoint, then serves the generated TAIGA MCP server over `streamable-http` on port `8000`.
- noVNC is still available on port `6080` when using the dev compose overlay.

## Prerequisite

Build the Horizon problem image locally first:

```bash
cd /Users/wyatt/coding/GIT/halluminate-taiga/horizon
bun run build:local-problem-image -- \
  "https://horizon.halluminate.ai/editor?problemId=e1ee7b24-1e8d-438d-8dbc-14305bd418ff" \
  --tag halluminate-horizon-e1ee7b24 \
  --json
```

The default recipe expects:

```text
horizon-local-wyatt-test-problem-tagging:halluminate-horizon-e1ee7b24
```

Override it with `HALLUMINATE_IMAGE` if needed.

## Run

```bash
HALLUMINATE_IMAGE=horizon-local-wyatt-test-problem-tagging:halluminate-horizon-e1ee7b24 \
harbor run -p harbor_cookbook/recipes/halluminate-horizon-sidecar \
  --agent claude-code \
  --model anthropic/claude-sonnet-4-6
```

## Interactive Dev Run

```bash
RECIPE=/Users/wyatt/coding/GIT/harbor-cookbook/harbor_cookbook/recipes/halluminate-horizon-sidecar
ENV_DIR="$RECIPE/environment"
HARBOR=/Users/wyatt/coding/GIT/harbor

HALLUMINATE_IMAGE=horizon-local-wyatt-test-problem-tagging:halluminate-horizon-e1ee7b24 \
CONTEXT_DIR="$ENV_DIR" docker compose --project-name harbor-halluminate-dev \
  --project-directory "$ENV_DIR" \
  -f "$HARBOR/src/harbor/environments/docker/docker-compose-build.yaml" \
  -f "$ENV_DIR/docker-compose.yaml" \
  -f "$ENV_DIR/docker-compose.dev.yaml" \
  up -d --build
```

Open:

```text
http://127.0.0.1:6081/vnc.html?autoconnect=true&resize=scale
```

Stop:

```bash
HALLUMINATE_IMAGE=horizon-local-wyatt-test-problem-tagging:halluminate-horizon-e1ee7b24 \
CONTEXT_DIR="$ENV_DIR" docker compose --project-name harbor-halluminate-dev \
  --project-directory "$ENV_DIR" \
  -f "$HARBOR/src/harbor/environments/docker/docker-compose-build.yaml" \
  -f "$ENV_DIR/docker-compose.yaml" \
  -f "$ENV_DIR/docker-compose.dev.yaml" \
  down
```

## Notes

This recipe intentionally uses an HTTP wrapper around the generated image's stdio MCP server so Harbor agents do not need Docker socket access from `main`.

The verifier calls `grade_problem` with an empty transcript and writes Harbor's reward from the returned score. Transcript mapping is still future work.
