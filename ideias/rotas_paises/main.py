from geopy.geocoders import Nominatim
from scipy.spatial import distance
from itertools import permutations
import numpy as np

# 1. Inicializar geocodificador OSM
geolocator = Nominatim(user_agent="tsp_osm_app")

# 2. Função para obter lat/lon
def get_coords(location_name):
    location = geolocator.geocode(location_name)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"Local não encontrado: {location_name}")

# 3. Lista de cidades
places = [
    "Macapá, Brazil",
    "United States",
    "United Kingdom",
    "Russia",
    "South Africa",
    "Japan"
]

# Coordenadas
coords = [get_coords(p) for p in places]

# 4. Matriz de distâncias euclidianas
n = len(coords)
dist_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        dist_matrix[i][j] = distance.euclidean(coords[i], coords[j])

# 5. Resolver TSP
best_route = None
best_dist = float('inf')

for perm in permutations(range(1, n)):  # ignora o ponto inicial
    route = (0,) + perm + (0,)  # volta para o início
    total_dist = sum(dist_matrix[route[i], route[i + 1]] for i in range(len(route) - 1))
    if total_dist < best_dist:
        best_dist = total_dist
        best_route = route

# 6. Exibir resultado
print("Melhor rota (índices):", best_route)
print("Rota legível:", [places[i] for i in best_route])
print(f"Distância total (em graus lat/lon): {best_dist:.4f}")

# Se quiser converter de graus para km (aproximação usando 111 km por grau):
km_dist = best_dist * 111
print(f"Distância aproximada: {km_dist:.2f} km")
