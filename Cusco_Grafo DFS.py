import pymongo
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Conectar a la base de datos
client = pymongo.MongoClient("mongodb+srv://LuisAlfonso:Pelusa97@anemia.fjbkwgs.mongodb.net/")
db = client["Anemia"]
collection = db["Tamizaje_Atendido_2023"]

# Seleccionar el código de UBIGEO
print("CODIGO UBIGEO DEL DEPARATAMENTO CUSCO")
print( "80201")  
print( "80202")
print( "80203")
print( "80204")
print( "80205")
print( "80206")
print( "80207")
print( "80301")
print( "80302")
print( "80304")
ubigeo_code = int(input("Ingrese el código de UBIGEO que desea visualizar:"))

# Procesar los datos
departamentos = {}
for document in collection.find():
    departamento = document["DEPARTAMENTO"]
    ubigeo = document["UBIGEO"]
    dni = document["DNI"]
    edad = document["EDAD"]
    sexo = document["SEXO"]
    diagnostico = document["DIAGNOSTICO"]
    
    if ubigeo == ubigeo_code:
        if departamento not in departamentos:
            departamentos[departamento] = {}
        if ubigeo not in departamentos[departamento]:
            departamentos[departamento][ubigeo] = []
        departamentos[departamento][ubigeo].append({
            "DNI": dni,
            "EDAD": edad,
            "SEXO": sexo,
            "DIAGNOSTICO": diagnostico
        })

# Crear el grafo
G = nx.DiGraph()
for departamento, ubigeos in departamentos.items():
    for ubigeo, casos in ubigeos.items():
        G.add_node(departamento, label=departamento)
        G.add_node(ubigeo, label=ubigeo)
        for caso in casos:
            G.add_node(caso["DNI"], label=caso["DNI"])
            G.add_node(caso["EDAD"], label=caso["EDAD"])
            G.add_node(caso["SEXO"], label=caso["SEXO"])
            G.add_node(caso["DIAGNOSTICO"], label=caso["DIAGNOSTICO"])
            G.add_edge(departamento, ubigeo)
            G.add_edge(ubigeo, caso["DNI"])
            G.add_edge(caso["DNI"], caso["EDAD"])
            G.add_edge(caso["DNI"], caso["SEXO"])
            G.add_edge(caso["DNI"], caso["DIAGNOSTICO"])

# Posicionar los nodos en un orden circular
pos = nx.circular_layout(G)

# Crear la lista de colores
colors = ['lightblue', 'green', 'red', 'green', 'yellow']

# Visualizar el grafo
nx.draw_networkx(G, pos, with_labels=True, node_color=[
    colors[0] if node not in [caso["DNI"] for caso in departamentos[departamento][ubigeo] for departamento, ubigeos in departamentos.items() for ubigeo, casos in ubigeos.items()] else
    colors[1] if node in [caso["DNI"] for caso in departamentos[departamento][ubigeo] for departamento, ubigeos in departamentos.items() for ubigeo, casos in ubigeos.items()] else
    colors[2] if caso["DIAGNOSTICO"] == "D" else
    colors[3] if caso["DIAGNOSTICO"] == "P" else
    colors[4] if caso["DIAGNOSTICO"] == "R" else
    'gray' for node in G.nodes()
], node_size=5000, edge_color='gray', arrowsize=20)
plt.show()

# Crear una tabla con los datos
df = pd.DataFrame()
for departamento, ubigeos in departamentos.items():
    for ubigeo, casos in ubigeos.items():
        for caso in casos:
            df = pd.concat([df, pd.DataFrame({
                "Departamento": [departamento],
                "UBIGEO": [ubigeo],
                "DNI": [caso["DNI"]],
                "EDAD": [caso["EDAD"]],
                "SEXO": [caso["SEXO"]],
                "DIAGNOSTICO": [caso["DIAGNOSTICO"]]
            })])

# Mostrar la tabla
plt.figure(figsize=(10, 5))
plt.table(cellText=df.values[:, 1:], colLabels=df.columns[1:], loc='center')
plt.show()
# Cerrar la conexión a la base de datos
client.close()