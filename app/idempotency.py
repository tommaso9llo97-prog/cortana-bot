import hashlib
import json
import time

def generate_macrodroid_idempotency_key(telegram_id, event_type, payload):
    payload_str = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    ts_floor = int(time.time() / 60) * 60
    raw = f"{telegram_id}:{event_type}:{payload_str}:{ts_floor}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()