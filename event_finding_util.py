from flask import Flask, jsonify, render_template, request
from datetime import datetime, date
import requests
import json

with open("ufc_full_competitions.json") as  f:
        competitions = json.load(f)

api_key = '1234567890...' # Input the generated API key

app = Flask(__name__)

def get_all_competitions_sorted():
        comps_with_dates = []

        for comp in competitions:

                try:
                        comp_date = datetime.strptime(comp["seasons"][0]["start_date"], "%Y-%m-%d").date()
                        comps_with_dates.append({"comp": comp, "date": comp_date})
                except ValueError:
                        continue

        sorted_comps = sorted(comps_with_dates, key=lambda x: x["date"])
        return sorted_comps

def findLastEvent():
        today = date.today()
        sorted_comps = get_all_competitions_sorted()

        for i, comp_bundle in enumerate(sorted_comps):
                if comp_bundle["date"] > today:
                        return i-1, [c["comp"] for c in sorted_comps]

        return len(sorted_comps) - 1, [c["comp"] for c in sorted_comps]


def findNext(num):
        index, competitionsSorted = findLastEvent()
        start = index+1
        end = start + num
        slicedEvents = competitionsSorted[start : end]
        print(f"finding next {num} events!")
        return slicedEvents


def findPrev(num):
        index, competitionsSorted = findLastEvent()
        start = index
        end = start - num
        slicedEvents = competitionsSorted[start : end : -1]
        print(f"Finding last {num} events!")
        return slicedEvents
