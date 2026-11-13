#!/usr/bin/env python3
"""Fetches your real contribution counts for the last year -> data/activity.json.
Needs env GITHUB_TOKEN (Actions provides one automatically). No fake data is ever written."""
import json, os, sys, urllib.request
from datetime import datetime, timedelta, timezone

USER = "absolutenoobtechie"
token = os.environ.get("GITHUB_TOKEN")
if not token:
    sys.exit("GITHUB_TOKEN not set; skipping (activity.svg keeps its last version).")

now = datetime.now(timezone.utc)
frm = (now - timedelta(days=364)).strftime("%Y-%m-%dT00:00:00Z")
q = """query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t){
contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": q, "variables": {"u": USER, "f": frm, "t": now.strftime("%Y-%m-%dT%H:%M:%SZ")}}).encode(),
    headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": USER},
)
data = json.load(urllib.request.urlopen(req, timeout=30))
if "errors" in data:
    sys.exit(f"GraphQL error: {data['errors']}")
weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
days = [{"date": d["date"], "count": d["contributionCount"]} for w in weeks for d in w["contributionDays"]]
days.sort(key=lambda d: d["date"])
with open(os.path.join(os.path.dirname(__file__), "..", "data", "activity.json"), "w") as f:
    json.dump({"synced": now.strftime("%Y-%m-%d"), "days": days}, f)
print(f"saved {len(days)} days")
