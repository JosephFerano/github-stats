#!/usr/bin/env python3

import os
import urllib.request
import json
import datetime

api_key = ""
with open("./api-key") as f:
    api_key = f.readlines()[0]

def make_request():
    headers = {}
    headers['User-Agent'] = "curl/7.54"
    headers['Authorization'] = f"bearer {api_key}"
    headers['Content-Type'] = "application/json"
    now = datetime.datetime.now()
    year_ago = now - datetime.timedelta(days=365, seconds=1)
    now = now.isoformat(timespec="seconds")
    year_ago = year_ago.isoformat(timespec="seconds")
    data = {
        "query": "query {viewer {contributionsCollection(from: " + f"\"{year_ago}\"" + ", to: " + f"\"{now}Z\"" + ") {contributionCalendar {weeks {contributionDays {contributionCount date}}}}}}"
    }
    url = "https://api.github.com/graphql"
    encoded = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, headers=headers, data=encoded, method="POST")
    res = urllib.request.urlopen(req)
    decoded = res.read().decode('utf-8')
    return json.loads(decoded)

blob = make_request()
weeks = blob["data"]["viewer"]["contributionsCollection"]["contributionCalendar"]["weeks"]

dates = []
for week in weeks:
    for date in week["contributionDays"]:
        d = datetime.datetime.strptime(date["date"], "%Y-%m-%d")
        if date["contributionCount"] > 0:
            dates.append(d)

streaks = [1]
for i, date in enumerate(dates[1:], 1):
    delta = date - dates[i - 1]
    if delta.days == 1:
        streaks[-1] += 1
    elif streaks[-1] > 0:
        streaks.append(1)

streaks.sort(reverse=True)

print(f"Longest Daily Github Contribution Streak In Past 365 days:\n{streaks[0]}")
