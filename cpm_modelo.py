#cpm.py
import networkx as nx

def calcular_camino_critico(actividades):
    G = nx.DiGraph()
    for actividad in actividades:
        G.add_edge(actividad['inicio'], actividad['fin'], duracion=actividad['duracion'])
    
    camino_critico = nx.dag_longest_path(G, weight='duracion')
    duracion_total = nx.dag_longest_path_length(G, weight='duracion')
    
    return camino_critico, duracion_total