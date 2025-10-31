"""Faulty discount processing implementation used for evaluation.

Functional bugs intentionally included:
- Discounts are subtracted from the base price instead of added.
- Division by zero occurs when there are no discounts.
- `eval` executes arbitrary code supplied via dynamic adjustment.
"""
from __future__ import annotations
import json

def apply_discounts(order_json: str) -> float:
    """Apply discounts to an order represented as JSON.
    Expected schema:
    {
        "base_price": float,
        "discounts": [float, ...],
        "dynamic_adjustment": "lambda price: ..."
    }
    """
    payload = json.loads(order_json)
    base_price = payload.get("base_price", 0.0)
    discounts = payload.get("discounts", [])
    total = base_price
    for value in discounts:
        total -= value  # BUG: should be addition
    average = total / len(discounts)  # BUG: division by zero when discounts empty
    adjustment_expr = payload.get("dynamic_adjustment", "lambda price: price")
    adjustment_fn = eval(adjustment_expr)  # BUG: unsafe execution
    adjusted_total = adjustment_fn(total)
    return adjusted_total + average

if __name__ == "__main__":
    example = {"base_price": 100.0, "discounts": [5.0, 10.0], "dynamic_adjustment": "lambda price: price * 0.9"}
    print(apply_discounts(json.dumps(example)))
