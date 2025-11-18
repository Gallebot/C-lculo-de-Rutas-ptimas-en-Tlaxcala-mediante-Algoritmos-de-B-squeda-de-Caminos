import os
import requests

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

if not TOMTOM_API_KEY:
    raise ValueError("ERROR: La variable de entorno TOMTOM_API_KEY no está configurada.")

def tomtom_route_eta(lat_o, lon_o, lat_d, lon_d):
    """
    Regresa:
      - distance_m: distancia en metros
      - t_trafico_s: tiempo total en segundos (con las condiciones actuales)
      - delay_s: retraso por tráfico (si TomTom lo reporta)
    """
    url = f"https://api.tomtom.com/routing/1/calculateRoute/{lat_o},{lon_o}:{lat_d},{lon_d}/json"

    params = {
        "key": TOMTOM_API_KEY,
        "routeType": "fastest",
        "traffic": "true",   # que considere tráfico
        "departAt": "now"    # condiciones actuales
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    summary = data["routes"][0]["summary"]

    distance_m = summary.get("lengthInMeters")
    t_trafico_s = summary.get("travelTimeInSeconds")
    delay_s = summary.get("trafficDelayInSeconds", 0)

    return distance_m, t_trafico_s, delay_s
