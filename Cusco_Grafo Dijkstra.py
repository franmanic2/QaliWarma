import networkx as nx
import matplotlib.pyplot as plt
from pymongo import MongoClient

# Conectar a la base de datos
client = MongoClient('mongodb+srv://LuisAlfonso:Pelusa97@anemia.fjbkwgs.mongodb.net/')
db = client['Anemia']
collection = db['Colegios_Cusco_2023']

# Recopilar y procesar los datos
data = list(collection.find())

# Crear el grafo
G = nx.DiGraph()

# Agregar nodos y aristas
for item in data:
    if item['DEPARTAMENTO'] not in G.nodes:
        G.add_node(item['DEPARTAMENTO'])
    if item['PROVINCIA'] not in G.nodes:
        G.add_node(item['PROVINCIA'])
    if item['DISTRITO'] not in G.nodes:
        G.add_node(item['DISTRITO'])
    if item['UBIGEO'] not in G.nodes:
        G.add_node(item['UBIGEO'])
    if item['InstitucionEducativa'] not in G.nodes:
        G.add_node(item['InstitucionEducativa'])
    if item['NivelEducativo'] not in G.nodes:
        G.add_node(item['NivelEducativo'])
    G.add_edge(item['DEPARTAMENTO'], item['PROVINCIA'])
    G.add_edge(item['PROVINCIA'], item['DISTRITO'])
    G.add_edge(item['DISTRITO'], item['UBIGEO'])
    G.add_edge(item['UBIGEO'], item['InstitucionEducativa'])
    G.add_edge(item['InstitucionEducativa'], item['NivelEducativo'])

# Agregar información adicional a los nodos
for node in G.nodes:
    if 'PROVINCIA' in G.nodes[node]:
        G.nodes[node]['PROVINCIA'] = G.nodes[node]['PROVINCIA'].upper()

# Menu para seleccionar la provincia
print("Seleccione la provincia que desea visualizar:")
print("1. ACOMAYO")
print("2. ANTA")
print("3. CALCA")
print("4. CANAS")
print("5. CANCHIS")
print("6. CHUMBIVILCAS")
print("7. CUSCO")
print("8. ESPINAR")
print("9. LA CONVENCION")
print("10. PARURO")
print("11. PAUCARTAMBO")
print("12. QUISPICANCHI")
print("13. URUBAMBA")

provincia = int(input("Ingrese el número de la provincia: "))

# Menu para seleccionar el nivel educativo
print("Seleccione el nivel educativo que desea incluir:")
print("1. INICIAL")
print("2. PRIMARIA")


nivel_educativo = int(input("Ingrese el número del nivel educativo: "))

# Filtrar los datos según la provincia y el nivel educativo
provincia_seleccionada = None
nivel_educativo_seleccionado = None
if provincia == 1:
    provincia_seleccionada = "ACOMAYO"
elif provincia == 2:
    provincia_seleccionada = "ANTA"
elif provincia == 3:
    provincia_seleccionada = "CALCA"
elif provincia == 4:
    provincia_seleccionada = "CANAS"
elif provincia == 5:
    provincia_seleccionada = "CANCHIS"
elif provincia == 6:
    provincia_seleccionada = "CHUMBIVILCAS"
elif provincia == 7:
    provincia_seleccionada = "CUSCO"
elif provincia == 8:
    provincia_seleccionada = "ESPINAR"
elif provincia == 9:
    provincia_seleccionada = "LA CONVENCION"
elif provincia == 10:
    provincia_seleccionada = "PARURO"
elif provincia == 11:
    provincia_seleccionada = "PAUCARTAMBO"
elif provincia == 12:
    provincia_seleccionada = "QUISPICANCHI"
elif provincia == 13:
    provincia_seleccionada = "URUBAMBA"

if nivel_educativo == 1:
    nivel_educativo_seleccionado = "INICIAL"
elif nivel_educativo == 2:
    nivel_educativo_seleccionado = "PRIMARIA"

# Crear el grafo para la provincia seleccionada y el nivel educativo seleccionado
G_provincia = nx.DiGraph()

# Agregar nodos y aristas para la provincia seleccionada y el nivel educativo seleccionado
for item in data:
    if item['PROVINCIA'] == provincia_seleccionada and item['NivelEducativo'] == nivel_educativo_seleccionado:
        if item['DEPARTAMENTO'] not in G_provincia.nodes:
            G_provincia.add_node(item['DEPARTAMENTO'])
        if item['PROVINCIA'] not in G_provincia.nodes:
            G_provincia.add_node(item['PROVINCIA'])
        if item['DISTRITO'] not in G_provincia.nodes:
            G_provincia.add_node(item['DISTRITO'])
        if item['UBIGEO'] not in G_provincia.nodes:
            G_provincia.add_node(item['UBIGEO'])
        if item['InstitucionEducativa'] not in G_provincia.nodes:
            G_provincia.add_node(item['InstitucionEducativa'])
        G_provincia.add_edge(item['DEPARTAMENTO'], item['PROVINCIA'])
        G_provincia.add_edge(item['PROVINCIA'], item['DISTRITO'])
        G_provincia.add_edge(item['DISTRITO'], item['UBIGEO'])
        G_provincia.add_edge(item['UBIGEO'], item['InstitucionEducativa'])
        G_provincia.add_edge(item['InstitucionEducativa'], item['NivelEducativo'])

# Agregar información adicional a los nodos para la provincia seleccionada y el nivel educativo seleccionado
for node in G_provincia.nodes:
    if 'PROVINCIA' in G_provincia.nodes[node]:
        G_provincia.nodes[node]['PROVINCIA'] = G_provincia.nodes[node]['PROVINCIA'].upper()

# Visualizar el grafo para la provincia seleccionada y el nivel educativo seleccionado
pos = nx.spring_layout(G_provincia)
nx.draw_networkx_nodes(G_provincia, pos, node_size=500, node_color='lightblue')
nx.draw_networkx_edges(G_provincia, pos, width=1, edge_color='gray')
nx.draw_networkx_labels(G_provincia, pos, font_size=10, font_color='black')
plt.title('Grafo de Colegios en la Provincia de ' + provincia_seleccionada + ' con Nivel Educativo ' + nivel_educativo_seleccionado)
plt.show()

# Cerrar la conexión a la base de datos
client.close()