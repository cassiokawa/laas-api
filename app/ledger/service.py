import time
import uuid
from collections import defaultdict

class LedgerService:
    def __init__(self):
        self.available = defaultdict(int)
        self.held = defaultdict(int)
        self.holds = {}

    def earn(self, user_id: str, base_points: int, reason: str) -> str:
        # MVP: just credit. Next step is double-entry + db.
        self.available[user_id] += base_points
        return f"txn_{uuid.uuid4().hex}"

    def reserve(self, user_id: str, points: int):
        if self.available[user_id] < points:
            return False, None
        self.available[user_id] -= points
        self.held[user_id] += points

        hold_id = f"hold_{uuid.uuid4().hex}"
        self.holds[hold_id] = {"user_id": user_id, "points": points, "ts": int(time.time()), "status": "RESERVED"}
        return True, hold_id

    def balance(self, user_id: str):
        return {"user_id": user_id, "available": self.available[user_id], "held": self.held[user_id]}

    def liability(self):
        total = sum(self.available.values()) + sum(self.held.values())
        return {"total_points_liability": total}
