
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def scrape_nobroker_rentals(pincode, flat_type, pages=1):
    listings = []
    for page in range(1, pages + 1):
        url = f"https://www.nobroker.in/property/rent/{flat_type.lower().replace(' ', '-')}-in-{pincode}?page={page}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all("script", {"type": "application/json"})

        for script in scripts:
            try:
                data = json.loads(script.string)
                props = data.get("props", {}).get("pageProps", {}).get("properties", [])
                for prop in props:
                    listings.append({
                        "source": "nobroker",
                        "pincode": pincode,
                        "flat_type": flat_type,
                        "rent": prop.get("rent"),
                        "area": prop.get("builtUpArea"),
                        "locality": prop.get("locality", ""),
                        "posted_on": datetime.now().strftime('%Y-%m-%d'),
                        "furnishing": prop.get("furnishing", ""),
                        "amenities": ', '.join(prop.get("amenities", [])),
                        "latitude": prop.get("lat"),
                        "longitude": prop.get("lng")
                    })
            except:
                continue
    return listings

def scrape_magicbricks_mock(pincode, flat_type):
    return [{
        "source": "magicbricks",
        "pincode": pincode,
        "flat_type": flat_type,
        "rent": 24000,
        "area": 1100,
        "locality": "Example Nagar",
        "posted_on": datetime.now().strftime('%Y-%m-%d'),
        "furnishing": "Semi-Furnished",
        "amenities": "Lift, Parking",
        "latitude": None,
        "longitude": None
    }]

def scrape_99acres_mock(pincode, flat_type):
    return [{
        "source": "99acres",
        "pincode": pincode,
        "flat_type": flat_type,
        "rent": 26000,
        "area": 1050,
        "locality": "Sample Layout",
        "posted_on": datetime.now().strftime('%Y-%m-%d'),
        "furnishing": "Furnished",
        "amenities": "Gym, Balcony",
        "latitude": None,
        "longitude": None
    }]

if __name__ == "__main__":
    print("Scraping rental listings from multiple sources...")
    nobroker_data = scrape_nobroker_rentals("560076", "2 BHK", pages=1)
    magicbricks_data = scrape_magicbricks_mock("560076", "2 BHK")
    acres99_data = scrape_99acres_mock("560076", "2 BHK")

    all_data = nobroker_data + magicbricks_data + acres99_data
    df = pd.DataFrame(all_data)
    df.to_csv("data/rentals.csv", index=False)
    print(f"Saved {len(df)} combined listings to data/rentals.csv")
