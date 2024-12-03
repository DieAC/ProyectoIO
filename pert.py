#pert.py
import networkx as nx

def calcular_pert(actividades):
    G = nx.DiGraph()
    for actividad in actividades:
        G.add_edge(actividad['inicio'], actividad['fin'], 
                   duracion_optima=actividad['optimista'],
                   duracion_mas_probable=actividad['probable'],
                   duracion_pesimista=actividad['pesimista'])
    
    # Calcular la duración 
    for u, v, data in G.edges(data=True):
        data['duracion_esperada'] = (data['duracion_optima'] + 4 * data['duracion_mas_probable'] + data['duracion_pesimista']) / 6
    
    # Camino critico
    camino_critico = nx.dag_longest_path(G, weight='duracion_esperada')
    duracion_total = nx.dag_longest_path_length(G, weight='duracion_esperada')
    
    return camino_critico, duracion_total
