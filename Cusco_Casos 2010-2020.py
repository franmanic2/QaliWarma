import pymongo
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la conexión a MongoDB
client = pymongo.MongoClient('mongodb+srv://LuisAlfonso:Pelusa97@anemia.fjbkwgs.mongodb.net/')
db = client['Anemia']
collection = db['Cusco_2010_2020']

# Carga los datos de la colección
data = collection.find()

# Convertir los datos a un DataFrame de pandas
df = pd.DataFrame(list(data))

# Menú para seleccionar el año
print("Seleccione el año para ver la gráfica:")
print("1. 2010")
print("2. 2011")
print("3. 2012")
print("4. 2013")
print("5. 2014")
print("6. 2015")
print("7. 2016")
print("8. 2017")
print("9. 2018")
print("10. 2019")
print("11. 2020")
print("12. Resumen total")

year_choice = int(input("Elija una opción: "))

# Filtra los datos para el año seleccionado
if year_choice == 1:
    year = 2010
elif year_choice == 2:
    year = 2011
elif year_choice == 3:
    year = 2012
elif year_choice == 4:
    year = 2013
elif year_choice == 5:
    year = 2014
elif year_choice == 6:
    year = 2015
elif year_choice == 7:
    year = 2016
elif year_choice == 8:
    year = 2017
elif year_choice == 9:
    year = 2018
elif year_choice == 10:
    year = 2019
elif year_choice == 11:
    year = 2020
elif year_choice == 12:
    # Resumen total
    df_year_grouped = df.groupby(['PROVINCIA', 'DISTRITO']).agg({'CASOS': 'sum'}).reset_index()
    df_year_grouped.columns = ['PROVINCIA', 'DISTRITO', 'CASOS']
    plt.figure(figsize=(10, 6))
    plt.barh(df_year_grouped['PROVINCIA'], df_year_grouped['CASOS'], color='skyblue')
    plt.xlabel('Casos totales de Anemia')
    plt.ylabel('Provincia')
    plt.title('Casos totales de Anemia de las provincias de la Region de Cusco en todos los años 2010-2020')
    plt.show()
else:
    print("Opción no válida. Por favor, elija una opción entre 1 y 12.")
    exit()

# Filtra los datos para el año seleccionado
df_year = df[df['ANIO'] == year]

# Agrupa los datos por provincia y distrito
df_year_grouped = df_year.groupby(['PROVINCIA', 'DISTRITO']).agg({'CASOS': 'sum'}).reset_index()

# Renombra las columnas
df_year_grouped.columns = ['PROVINCIA', 'DISTRITO', 'CASOS']

# Gráfica de barras horizontales
plt.figure(figsize=(10, 6))
plt.barh(df_year_grouped['PROVINCIA'], df_year_grouped['CASOS'], color='skyblue')

# Etiquetas y título
plt.xlabel('Casos totales')
plt.ylabel('Provincia')
plt.title(f'Casos totales de Anemia por provincia en el año del {year}')

# Mostrar la gráfica
plt.show()

# Cierre de conexión a MongoDB
client.close()
