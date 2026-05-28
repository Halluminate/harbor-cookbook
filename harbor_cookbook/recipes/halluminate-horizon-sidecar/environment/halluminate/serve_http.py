#!/usr/bin/env python3
"""Serve the generated TAIGA FastMCP app over streamable HTTP."""

import os

from environment.server import mcp


def main() -> None:
    os.chdir("/workdir")
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = int(os.environ.get("MCP_PORT", "8000"))
    mcp.settings.transport_security.enable_dns_rebinding_protection = False
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
