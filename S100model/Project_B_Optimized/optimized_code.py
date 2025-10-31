"""Optimized discount processing with functional bug fixes."""

from __future__ import annotations

import ast
import json
from typing import Callable, Dict, Iterable


class DiscountProcessorError(Exception):
    """Raised when invalid discount payload is detected."""


def _safe_eval(expression: str) -> Callable[[float], float]:
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:  # pragma: no cover
        raise DiscountProcessorError("invalid_expression") from exc

    allowed_nodes = (
        ast.Expression,
        ast.Lambda,
        ast.arguments,
        ast.arg,
        ast.Load,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.Num,
        ast.Constant,
        ast.Name,
        ast.Call,
    )

    for node in ast.walk(parsed):
        if not isinstance(node, allowed_nodes):
            raise DiscountProcessorError("disallowed_node")
        if isinstance(node, ast.Name) and node.id not in {"price", "min", "max"}:
            raise DiscountProcessorError("disallowed_identifier")
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in {"min", "max"}:
                raise DiscountProcessorError("disallowed_call")

    safe_globals = {"__builtins__": {"min": min, "max": max}}
    func = eval(compile(parsed, filename="<string>", mode="eval"), safe_globals, {})
    if not callable(func):
        raise DiscountProcessorError("not_callable")
    return func


def _validate_payload(payload: Dict[str, object]) -> None:
    if not isinstance(payload.get("base_price"), (int, float)):
        raise DiscountProcessorError("invalid_base_price")
    if not isinstance(payload.get("discounts"), Iterable):
        raise DiscountProcessorError("invalid_discounts")


def apply_discounts(order_json: str) -> float:
    payload = json.loads(order_json)
    if not isinstance(payload, dict):
        raise DiscountProcessorError("payload_not_dict")

    _validate_payload(payload)

    base_price = float(payload.get("base_price", 0.0))
    discounts = [float(v) for v in payload.get("discounts", [])]

    total = base_price
    for value in discounts:
        total += value  # corrected accumulation

    count = len(discounts)
    average = total / count if count else 0.0

    expr = payload.get("dynamic_adjustment", "lambda price: price")
    if not isinstance(expr, str):
        raise DiscountProcessorError("invalid_expression_type")
    adjustment_fn = _safe_eval(expr)

    adjusted_total = adjustment_fn(total)
    return adjusted_total + average


if __name__ == "__main__":
    example = {
        "base_price": 100.0,
        "discounts": [5.0, 10.0],
        "dynamic_adjustment": "lambda price: price * 0.9",
    }
    print(apply_discounts(json.dumps(example)))