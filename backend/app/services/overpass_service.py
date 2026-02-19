import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def get_nearby_doctors(lat: float, lon: float, radius: int):
    query = f"""
    [out:json];
    (
      node["healthcare"="doctor"](around:{radius},{lat},{lon});
      way["healthcare"="doctor"](around:{radius},{lat},{lon});
      relation["healthcare"="doctor"](around:{radius},{lat},{lon});
    );
    out center;
    """

    response = requests.post(OVERPASS_URL, data={"data": query})

    if response.status_code != 200:
        return {"error": "Overpass API failed"}

    data = response.json()
    results = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})

        results.append({
            "id": element.get("id"),
            "name": tags.get("name", "Doctor"),
            "lat": element.get("lat") or element.get("center", {}).get("lat"),
            "lon": element.get("lon") or element.get("center", {}).get("lon"),
            "speciality": tags.get("healthcare:speciality", "General"),
            "phone": tags.get("phone") or tags.get("contact:phone"),
            "address": tags.get("addr:full")
        })

    return results
