from fastapi import APIRouter
import requests

router = APIRouter()

# ───────────── Geocode ─────────────
@router.get("/geocode")
def geocode_city(city: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "format": "json",
        "q": city,
        "limit": 1
    }
    headers = {
        "User-Agent": "naari-care-app"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        return {"error": "Geocoding failed"}

    data = response.json()
    if not data:
        return {"error": "City not found"}

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"])
    }


# ───────────── Nearby Doctors ─────────────
@router.get("/nearby-doctors")
def get_nearby_doctors(lat: float, lon: float, radius: int):
    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
    );
    out body;
    """

    response = requests.post(overpass_url, data=query)

    if response.status_code != 200:
        return []

    data = response.json()

    doctors = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})
        doctors.append({
            "id": element.get("id"),
            "name": tags.get("name"),
            "hospital": tags.get("name"),
            "address": tags.get("addr:full") or "",
            "lat": element.get("lat"),
            "lon": element.get("lon"),
            "phone": tags.get("phone")
        })

    return doctors
