from typing import Any, Dict, List, Tuple

OPS = {
    "eq": lambda a, b: a == b,
    "neq": lambda a, b: a != b,
    "lt": lambda a, b: (a is not None and b is not None and a < b),
    "lte": lambda a, b: (a is not None and b is not None and a <= b),
    "gt": lambda a, b: (a is not None and b is not None and a > b),
    "gte": lambda a, b: (a is not None and b is not None and a >= b),
    "in": lambda a, b: (a in b) if isinstance(b, (list, set, tuple)) else False,
    "exists": lambda a, b: (a is not None) if b else (a is None)
}

def evaluate_condition(user: Dict[str, Any], cond: Dict[str, Any]) -> bool:
    field = cond.get("field")
    op = cond.get("op")
    value = cond.get("value", None)
    user_val = user.get(field, None)
    fn = OPS.get(op)
    if fn is None:
        return False
    try:
        return fn(user_val, value)
    except Exception:
        return False

def match_scheme(user: Dict[str, Any], scheme: Dict[str, Any]) -> Tuple[bool, List[str]]:
    reasons = []
    for cond in scheme.get("eligibility_conditions", []):
        ok = evaluate_condition(user, cond)
        reasons.append(f"{cond['field']} {cond['op']} {cond.get('value')} => {'OK' if ok else 'NO'}")
        if not ok:
            return False, reasons
    return True, reasons

def rank_schemes(matches: List[Tuple[Dict[str, Any], List[str]]]) -> List[Dict[str, Any]]:
    ranked = sorted(matches, key=lambda t: len(t[0].get("eligibility_conditions", [])), reverse=True)
    return [{"scheme": s, "reasons": r, "score": len(s.get("eligibility_conditions", []))} for s, r in ranked]

def find_matches(user: Dict[str, Any], schemes: List[Dict[str, Any]], user_state: str="ALL") -> List[Dict[str, Any]]:
    valid = []
    for s in schemes:
        states = s.get("states_applicable", ["ALL"])
        if "ALL" not in states and user_state not in states:
            continue
        ok, reasons = match_scheme(user, s)
        if ok:
            valid.append((s, reasons))
    return rank_schemes(valid)