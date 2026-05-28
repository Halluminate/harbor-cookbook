import asyncio
import json
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

PROBLEM_ID = "wyatt-test-problem-tagging-25"
MCP_URL = "http://halluminate:8000/mcp"


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


async def main() -> None:
    async with streamablehttp_client(MCP_URL) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "grade_problem",
                {
                    "problem_id": PROBLEM_ID,
                    "transcript": "",
                },
            )

    if result.isError:
        raise RuntimeError(f"grade_problem failed: {result.content}")
    if not result.content or result.content[0].type != "text":
        raise RuntimeError(f"grade_problem returned unexpected content: {result.content!r}")

    grade = json.loads(result.content[0].text)
    reward = extract_score(grade)
    Path("/logs/verifier/reward.json").write_text(
        json.dumps({"reward": reward, "grade": grade}, indent=2)
    )
    Path("/logs/verifier/reward.txt").write_text(f"{reward}\n")


asyncio.run(main())
