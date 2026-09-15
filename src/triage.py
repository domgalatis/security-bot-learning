import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VIRUSTOTAL_API_KEY")

print(f"Loaded key: {API_KEY[:6]}..." if API_KEY else "No key found")

def scan_url(url):
    headers = {"x-apikey": API_KEY}

    # Submit the URL for scanning
    submit_resp = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )
    submit_resp.raise_for_status()
    analysis_id = submit_resp.json()["data"]["id"]

    # Poll until the analysis finishes
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    while True:
        result_resp = requests.get(analysis_url, headers=headers)
        result_resp.raise_for_status()
        data = result_resp.json()["data"]
        if data["attributes"]["status"] == "completed":
            return data["attributes"]["stats"]
        time.sleep(3)

if __name__ == "__main__":
    test_url = "http://example.com"
    print(f"Scanning {test_url}...")
    try:
        stats = scan_url(test_url)
        print(stats)
    except requests.exceptions.HTTPError as e:
        print(f"API request failed: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")