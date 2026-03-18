"""Prism Scanner MCP Server — expose scan/grade/clean as MCP tools."""
import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from .models import ScanTarget
from .scanner import PrismScanner
from .scoring import GRADE_INFO
from .fetcher import fetch_target, cleanup_temp
from .cleaner import generate_plan
from .engines.residue_engine import ResidueEngine

logger = logging.getLogger("prism.mcp")

app = Server("prism-scanner")


def _format_scan_summary(result_dict: dict) -> str:
    """Format a human-readable scan summary."""
    grade = result_dict["grade"]
    info = GRADE_INFO.get(grade, {})
    findings = result_dict["findings"]
    active = [f for f in findings if not f.get("suppressed")]

    lines = [
        f"# Prism Scan Report",
        f"**Grade: {grade}** — {info.get('label', '')}",
        f"**Recommendation:** {info.get('recommendation', '')}",
        f"",
        f"**Target:** {result_dict['target']['path']}",
        f"**Platform:** {result_dict['target'].get('platform') or 'auto-detected'}",
        f"**Scan time:** {result_dict['scan_duration_ms']}ms",
        f"**Findings:** {len(active)} active ({len(findings)} total)",
    ]

    if result_dict.get("behavior_tags"):
        lines.append(f"**Behaviors:** {', '.join(result_dict['behavior_tags'])}")

    if result_dict.get("key_risks"):
        lines.append(f"\n## Key Risks")
        for risk in result_dict["key_risks"]:
            lines.append(f"- {risk}")

    if active:
        lines.append(f"\n## Findings Detail")
        for f in sorted(active, key=lambda x: _sev_order(x["severity"])):
            loc = ""
            if f.get("file_path"):
                loc = f" at `{f['file_path']}"
                if f.get("line"):
                    loc += f":{f['line']}"
                loc += "`"
            lines.append(f"- **{f['severity'].upper()}** [{f['rule_id']}] {f['title']}{loc}")
            if f.get("description"):
                lines.append(f"  {f['description']}")
            if f.get("remediation"):
                lines.append(f"  *Fix:* {f['remediation']}")

    return "\n".join(lines)


def _sev_order(sev: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}.get(sev, 5)


@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="prism_scan",
            description=(
                "Scan an AI agent skill, plugin, or MCP server for security risks. "
                "Accepts a local path or GitHub URL. Returns an A-F grade with "
                "detailed findings including malicious code detection, data "
                "exfiltration, persistence mechanisms, and supply chain risks."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Local path or GitHub URL to scan",
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["clawhub", "mcp", "npm", "pip"],
                        "description": "Force platform type (auto-detected if omitted)",
                    },
                    "include_residue": {
                        "type": "boolean",
                        "description": "Also scan system for leftover files from uninstalled skills",
                        "default": False,
                    },
                },
                "required": ["target"],
            },
        ),
        Tool(
            name="prism_grade",
            description=(
                "Quick security grade check for an agent skill, plugin, or MCP server. "
                "Returns only the letter grade (A-F) and recommendation, "
                "without full finding details. Fast for CI/CD gating."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "description": "Local path or GitHub URL to scan",
                    },
                    "platform": {
                        "type": "string",
                        "enum": ["clawhub", "mcp", "npm", "pip"],
                        "description": "Force platform type (auto-detected if omitted)",
                    },
                },
                "required": ["target"],
            },
        ),
        Tool(
            name="prism_clean_scan",
            description=(
                "Scan the local system for residue left behind by uninstalled "
                "agent skills — LaunchAgents, crontab entries, shell config "
                "modifications, orphaned credentials, and more."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="prism_clean_plan",
            description=(
                "Generate a cleanup plan for system residue found by prism_clean_scan. "
                "Shows what would be removed/fixed without making changes."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "prism_scan":
            return await _handle_scan(arguments)
        elif name == "prism_grade":
            return await _handle_grade(arguments)
        elif name == "prism_clean_scan":
            return await _handle_clean_scan()
        elif name == "prism_clean_plan":
            return await _handle_clean_plan()
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        logger.exception(f"Error in tool {name}")
        return [TextContent(type="text", text=f"Error: {e}")]


async def _handle_scan(arguments: dict) -> list[TextContent]:
    target_str = arguments["target"]
    platform = arguments.get("platform")
    include_residue = arguments.get("include_residue", False)

    # Fetch target (handles git URLs, local paths)
    fetch_result = fetch_target(target_str)
    try:
        scan_target = ScanTarget(
            path=fetch_result.local_path,
            platform=platform or fetch_result.platform,
            url=fetch_result.url,
        )
        scanner = PrismScanner()
        result = scanner.scan(scan_target, include_residue=include_residue)
        result_dict = result.to_dict()

        summary = _format_scan_summary(result_dict)
        # Append raw JSON for programmatic consumption
        summary += f"\n\n<details><summary>Raw JSON</summary>\n\n```json\n{json.dumps(result_dict, indent=2)}\n```\n</details>"

        return [TextContent(type="text", text=summary)]
    finally:
        cleanup_temp(fetch_result)


async def _handle_grade(arguments: dict) -> list[TextContent]:
    target_str = arguments["target"]
    platform = arguments.get("platform")

    fetch_result = fetch_target(target_str)
    try:
        scan_target = ScanTarget(
            path=fetch_result.local_path,
            platform=platform or fetch_result.platform,
            url=fetch_result.url,
        )
        scanner = PrismScanner()
        result = scanner.scan(scan_target)

        grade = result.grade
        info = GRADE_INFO[grade]
        active = result.active_findings
        sev_counts = {}
        for f in active:
            sev_counts[f.severity.value] = sev_counts.get(f.severity.value, 0) + 1

        text = (
            f"**Grade: {grade}** — {info['label']}\n"
            f"{info['recommendation']}\n\n"
            f"Findings: {len(active)} "
            f"({', '.join(f'{v} {k}' for k, v in sorted(sev_counts.items(), key=lambda x: _sev_order(x[0])))})\n"
            f"Scan time: {result.scan_duration_ms}ms"
        )
        return [TextContent(type="text", text=text)]
    finally:
        cleanup_temp(fetch_result)


async def _handle_clean_scan() -> list[TextContent]:
    engine = ResidueEngine()
    findings = engine.scan_system()

    if not findings:
        return [TextContent(type="text", text="No system residue found. Your system is clean.")]

    lines = [f"# System Residue Scan", f"Found **{len(findings)}** residue items:\n"]
    for f in findings:
        loc = f" at `{f.file_path}`" if f.file_path else ""
        lines.append(f"- **{f.severity.value.upper()}** [{f.rule_id}] {f.title}{loc}")
        if f.description:
            lines.append(f"  {f.description}")

    lines.append(f"\nUse `prism_clean_plan` to generate a cleanup plan.")
    return [TextContent(type="text", text="\n".join(lines))]


async def _handle_clean_plan() -> list[TextContent]:
    engine = ResidueEngine()
    findings = engine.scan_system()

    if not findings:
        return [TextContent(type="text", text="No system residue found. Nothing to clean.")]

    plan = generate_plan(findings)
    if not plan.actions:
        return [TextContent(
            type="text",
            text=f"Found {len(findings)} residue items, but none are auto-fixable. Manual review recommended.",
        )]

    lines = [f"# Cleanup Plan", f"**{len(plan.actions)}** actions to execute:\n"]
    for i, action in enumerate(plan.actions, 1):
        atype = action["type"]
        lines.append(f"**{i}. {action['title']}** ({action['rule_id']})")
        if atype == "remove_file":
            lines.append(f"   Action: DELETE `{action['path']}`")
        elif atype == "remove_line":
            lines.append(f"   Action: REMOVE line {action['line']} from `{action['path']}`")
        elif atype == "fix_permissions":
            lines.append(f"   Action: `chmod {action['target_mode']} {action['path']}`")
        elif atype == "remove_crontab":
            lines.append(f"   Action: Remove crontab entry")
        lines.append("")

    lines.append("To execute, run: `prism clean --apply`")
    return [TextContent(type="text", text="\n".join(lines))]


async def _async_main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def main():
    import asyncio
    asyncio.run(_async_main())
