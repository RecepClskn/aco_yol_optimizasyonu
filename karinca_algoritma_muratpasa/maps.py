#Ad: Recep
#Soyad: Çalışkan
#Numara: 2312721004
#Github Repo: https://github.com/RecepClskn/aco_yol_optimizasyonu.git

import googlemaps
import time

class Location:
    def __init__(self, name, address, lat, lng):
        self.name = name
        self.address = address
        self.lat = lat
        self.lng = lng


def make_gmaps_client(api_key: str):
    return googlemaps.Client(key=api_key)


def geocode_addresses(gmaps, names, addresses):
    locs = []
    for name, address in zip(names, addresses):
        res = gmaps.geocode(address)
        if not res:
            raise ValueError(f"Adres bulunamadı: {address}")

        loc = res[0]["geometry"]["location"]
        locs.append(Location(name, address, loc["lat"], loc["lng"]))
        time.sleep(0.1)
    return locs


def build_distance_matrix_km(gmaps, locs):
    n = len(locs)
    D = [[0.0] * n for _ in range(n)]

    coords = [(l.lat, l.lng) for l in locs]

    BATCH = 5  # 5 x 20 = 100 (API LIMITE TAM UYUM)

    for i in range(0, n, BATCH):
        origins = coords[i:i + BATCH]

        response = gmaps.distance_matrix(
            origins=origins,
            destinations=coords,
            mode="driving",
            units="metric"
        )

        for oi, row in enumerate(response["rows"]):
            for j, element in enumerate(row["elements"]):
                if element["status"] == "OK":
                    D[i + oi][j] = element["distance"]["value"] / 1000
                else:
                    D[i + oi][j] = float("inf")

    return D
