import pandas as pd
import matplotlib.pyplot as plot
import matplotlib.markers as markers
from math import floor, sqrt

# 1. Cargar el archivo de datos de la actividad 2
df = pd.read_csv('gaiadr3_IC_2391.csv')
print(df.dtypes)

# print(df.isnull().sum())

paralelaje = df['parallax']
paralelaje.plot.hist(color= '#ADD8E6', bins=60, edgecolor='black')
plot.ylabel('Cantidad de estrellas')
plot.xlabel('Paralelaje (mas)')
plot.title('Histograma de paralelajes')

plot.show()
minimum_parallax = paralelaje.min()
maximum_parallax = paralelaje.max()
print("Minimum parallax: ", minimum_parallax)
print("Maximum parallax: ", maximum_parallax)

# 2. Calcular la distancia máxima y mínima.
def dist_parallax(row):
    return 1/(row['parallax']/1000)

df['distance'] = df.apply(lambda row: dist_parallax(row), axis=1)
print(f"Minimum distance: {df['distance'].min()}")
print(f"Maximum distance: {df['distance'].max()}")

Q1 = df['pmra'].quantile(0.25)
Q3 = df['pmra'].quantile(0.75)
IQR = Q3 - Q1
limites1 = [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]

Q1 = df['pmdec'].quantile(0.25)
Q3 = df['pmdec'].quantile(0.75)
IQR = Q3 - Q1
limites2 = [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]

df_reduced = df[(df['pmra'] >= limites1[0]) & (df['pmra'] <= limites1[1]) & (df['pmdec'] >= limites2[0]) & (df['pmdec'] <= limites2[1])]

x_scatter = df_reduced['pmra']
y_scatter = df_reduced['pmdec']
plot.xlabel('pmra')
plot.ylabel('pmdec')
plot.scatter(x_scatter, y_scatter, color='#2E5984', marker=markers.MarkerStyle('.', fillstyle='full').scaled(0.05))
plot.show()

centro_de_cumulo = [-26.0,23.0]

df_reduced["distance_to_center"] = df_reduced.apply(lambda row: sqrt((row['pmra'] - centro_de_cumulo[0])**2 + (row['pmdec'] - centro_de_cumulo[1])**2), axis=1) 
first_cut = df_reduced.loc[df_reduced['distance_to_center']<=4]
print("First cut : ")
print(first_cut)

second_cut = first_cut[first_cut['distance'].between(138.465, 169.235)]
print("Second cut : ")
print(second_cut)