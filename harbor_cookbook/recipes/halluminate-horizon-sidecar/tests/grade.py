import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

PROBLEM_ID = "wyatt-test-problem-tagging-25"
MCP_URL = "http://halluminate:8000/mcp"
GRADING_ENV_EXTRA_FIELD = "_taigaGradingEnv"
GRADING_ENV_ALLOWLIST = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_API_AUXILIARY_MODEL_NAME",
)


def extract_score(grade: dict) -> float:
    for key in ("score", "reward"):
        value = grade.get(key)
        if isinstance(value, int | float):
            return float(value)
    subscores = grade.get("subscores")
    if isinstance(subscores, dict):
        overall = subscores.get("overall")
        if isinstance(overall, int | float):
            return float(overall)
    return 0.0


def grading_extra_fields() -> dict | None:
    grading_env = {
        key: value for key in GRADING_ENV_ALLOWLIST if (value := os.environ.get(key))
    }
    if not grading_env:
        return None
    return {GRADING_ENV_EXTRA_FIELD: grading_env}


async def main() -> None:
    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_args = {
                "problem_id": PROBLEM_ID,
                "transcript": "",
            }
            extra_fields = grading_extra_fields()
            if extra_fields is not None:
                tool_args["extra_fields"] = extra_fields
            result = await session.call_tool(
                "grade_problem",
                tool_args,
            )

    if result.isError:
        raise RuntimeError(f"grade_problem failed: {result.content}")
    if not result.content or result.content[0].type != "text":
        raise RuntimeError(f"grade_problem returned unexpected content: {result.content!r}")

    grade = json.loads(result.content[0].text)
    reward = extract_score(grade)
    Path("/logs/verifier/grade.json").write_text(json.dumps(grade, indent=2))
    Path("/logs/verifier/reward.json").write_text(json.dumps({"reward": reward}, indent=2))
    Path("/logs/verifier/reward.txt").write_text(f"{reward}\n")


asyncio.run(main())
