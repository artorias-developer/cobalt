#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

"""
Helpers for WebSocket tests.
"""

from typing import Any, Dict, List, Optional


WS_URL = "/api/v1/ws"
BARRIER_EVENT = "__barrier__"


def send_event(websocket, event: str, data: Optional[Dict[str, Any]] = None) -> None:
    message: Dict[str, Any] = {"event": event}

    if data is not None:
        message["data"] = data

    websocket.send_json(message)


def _is_barrier_reply(reply: Dict[str, Any]) -> bool:
    return reply.get("type") == "error" and BARRIER_EVENT in str(reply.get("data"))


def collect_replies(websocket) -> List[Dict[str, Any]]:
    """
    Returns every message the server sent in response to previously sent events.

    Events are processed sequentially, so the error reply to an unknown "barrier" event
    arrives only after all earlier events have finished. This never blocks forever when an
    event produces no reply: the barrier reply always comes.
    """
    send_event(websocket, BARRIER_EVENT)
    replies = []

    while not _is_barrier_reply(reply := websocket.receive_json()):
        replies.append(reply)

    return replies


def sync(websocket) -> None:
    """
    Waits until every previously sent event has been handled and asserts there were no replies.
    """
    replies = collect_replies(websocket)

    assert replies == [], f"Unexpected replies: {replies}"
