import requests
import time
import json

api_key = "SkioKWudCNSQcSiqDJ3qIepC8lHy2JnI5ebdNgdl"       # Enter your auto generated API key
base_url = "https://api.sportradar.com/mma/trial/v2/en"
output_file = "ufc_full_competitions.json"

def safe_get(url, retries=3, delay=2):
        for attempt in range(retries):
                try:
                        response = requests.get(url, timeout=10)
                        if response.status_code == 429:
                                print(f"[{attempt+1}] Rate limited, retrying in {delay}s...")
                                time.sleep(delay)
                                continue
                        return response.json()
                except Exception as e:
                        print(f"[{attempt+1}] Failed to fetch {url}: {e}")
                        time.sleep(delay)
        return {}

def download_all_data():
        print(" Fetching competitions...")
        comp_url = f"{base_url}/competitions.json?api_key={api_key}"
        comp_response = safe_get(comp_url)
        competitions = comp_response.get("competitions", [])

        if not competitions:
                print(" No competitions found. Check API key or rate limits.")
                return

        results = []
        for i, comp in enumerate(competitions):
                comp_id = comp.get("id")

                # Fetch seasons data
                season_url = f"{base_url}/competitions/{comp_id}/seasons.json?api_key={api_key}"
                season_data = safe_get(season_url)
                comp["seasons"] = season_data.get("seasons", [])

                results.append(comp)
                time.sleep(1)  # Respect 1 QPS limit

        # Save the results to file
        with open(output_file, "w") as f:
                json.dump(results, f, indent=2)

        print(f"\n Saved {len(results)} competitions to '{output_file}'")

if __name__ == "__main__":
        download_all_data()
