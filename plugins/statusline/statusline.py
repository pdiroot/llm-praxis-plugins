#!/usr/bin/env -S uv run --quiet --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Prints the Claude Code status line of a project. Reads the status JSON on stdin."""

import contextlib
import json
import math
import os
import sys
import time
from pathlib import PurePath
from typing import Any

# Thresholds: a percent turns yellow at WARN and red at DANGER.
WARN = 50
DANGER = 80
COST_WARN = 20
COST_DANGER = 50
# A limit shows its reset time only from this percent used. Override with STATUSLINE_RESET_FROM.
RESET_FROM = 50
TTL_SECONDS = {"5m": 300, "1h": 3600}

# Only the directory, warnings and alerts have a color; everything else is the default color.
DEFAULT = ""
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"
SEP = " │ "
BAR_WIDTH = 8
BAR_FULL = "▰"
BAR_EMPTY = "▱"
CACHE_ICON = "◷"
RESET_ICON = "↻"


def level_color(pct: float) -> str:
    return RED if pct >= DANGER else YELLOW if pct >= WARN else DEFAULT


def paint(color: str, text: str) -> str:
    return f"{color}{text}{RESET}" if color else text


def number(value: Any) -> float | None:
    ok = isinstance(value, int | float) and not isinstance(value, bool)
    return float(value) if ok and math.isfinite(value) else None


def until(seconds: float) -> str:
    """3d 4h13m, 2h05m or 13m."""
    minutes = math.ceil(seconds / 60)
    days, rest = divmod(minutes, 1440)
    hours, minutes = divmod(rest, 60)
    if days:
        return f"{days}d {hours}h{minutes:02d}m"
    return f"{hours}h{minutes:02d}m" if hours else f"{minutes}m"


def cost_segment(cost: float) -> str:
    color = RED if cost > COST_DANGER else YELLOW if cost > COST_WARN else DEFAULT
    return paint(color, f"${cost:.2f}")


def cache_segment(cache: dict[str, Any], now: float) -> str | None:
    expires = number(cache.get("expires_at"))
    if cache.get("warm") and expires is not None and expires > now:
        left = expires - now
        ttl = TTL_SECONDS.get(str(cache.get("ttl")), 3600)
        used = 100 * (1 - left / ttl)
        return paint(level_color(used), f"{CACHE_ICON} cache {math.ceil(left / 60)}m")
    # Warm with no expiry means the expiry is unknown; a past expiry means the cache went cold.
    if cache.get("warm") and expires is None:
        return f"{CACHE_ICON} cache warm"
    return f"{CACHE_ICON} cache cold"


def context_segment(pct: float) -> str:
    pct = min(100.0, max(0.0, pct))
    filled = min(BAR_WIDTH, round(pct * BAR_WIDTH / 100))
    bar = BAR_FULL * filled + BAR_EMPTY * (BAR_WIDTH - filled)
    return paint(level_color(pct), f"{bar} {int(pct)}%")


def window_segment(label: str, window: dict[str, Any], now: float) -> str | None:
    pct = number(window.get("used_percentage"))
    resets = number(window.get("resets_at"))
    if pct is None or resets is None or resets <= now:
        return None
    text = f"{label} {int(pct)}%"
    if pct >= reset_from():
        text += f" {RESET_ICON} {until(resets - now)}"
    return paint(level_color(pct), text)


def reset_from() -> float:
    try:
        return float(os.environ["STATUSLINE_RESET_FROM"])
    except (KeyError, ValueError):
        return RESET_FROM


def section(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}


def segments(data: dict[str, Any], now: float) -> list[str | None]:
    out: list[str | None] = []
    workspace = section(data, "workspace")
    # The launch directory: current_dir follows each cd of the session.
    current = workspace.get("project_dir") or workspace.get("current_dir")
    name = PurePath(current).name if isinstance(current, str) else ""
    out.append(paint(CYAN, name) if name else None)
    for value in (
        section(data, "model").get("display_name"),
        section(data, "effort").get("level"),
    ):
        out.append(value if isinstance(value, str) and value else None)
    cost = number(section(data, "cost").get("total_cost_usd"))
    out.append(cost_segment(cost) if cost is not None else None)
    if isinstance(data.get("prompt_cache"), dict):
        out.append(cache_segment(data["prompt_cache"], now))
    pct = number(section(data, "context_window").get("used_percentage"))
    out.append(context_segment(pct) if pct is not None else None)
    limits = section(data, "rate_limits")
    out.append(window_segment("5h", section(limits, "five_hour"), now))
    out.append(window_segment("7d", section(limits, "seven_day"), now))
    return out


def main() -> None:
    line = ""
    # The status line must never fail: any error leaves the line empty.
    with contextlib.suppress(Exception):
        data = json.load(sys.stdin)
        # Test seam for the clock, not a setting.
        now = float(os.environ.get("STATUSLINE_NOW") or time.time())
        line = SEP.join(s for s in segments(data, now) if s)
    print(line)


if __name__ == "__main__":
    main()
