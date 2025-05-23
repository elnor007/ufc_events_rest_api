import requests
import time
import json

api_key = "1234567890..."       # Enter your auto generated API key
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



def update_data():
	list_update = []
	output_file = "ufc_full_competitions.json"

	with open(output_file, "r") as f:
		ufc_full_competitions = json.load(f)
	print("Updating current data...")	

	comp_url = f"{base_url}/competitions.json?api_key={api_key}"
	comp_response = safe_get(comp_url)
	comps = comp_response.get("competitions", [])
	time.sleep(1)

	len_old = len(ufc_full_competitions)
	len_new = len(comps)
	if len_old == len_new:
		print("Data is already up to date!")
		return 0

	for index in range(len_old, len_new):
		comp_id = comps[index].get("id")

		season_url = f"{base_url}/competitions/{comp_id}/seasons.json?api_key={api_key}"
		season_data = safe_get(season_url)
		comps[index]["seasons"] = season_data.get("seasons", [])
		list_update.append(comps[index])
		time.sleep(1)
		print(f"Update at index {index} complete")

	ufc_full_competitions += list_update

	with open(output_file, "w") as f:
		json.dump(ufc_full_competitions, f, indent=2)
	print(f"{output_file} has been updated successfully!")

if __name__ == "__main__":
        update_data()
