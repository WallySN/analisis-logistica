import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

print("=" * 60)
print("CREANDO 5 GRAFICAS FINALES")
print("=" * 60)

# ============================================
# GRAFICA 16: Mapa de calor de correlaciones
# ============================================
print("\n📊 Grafica 16: Mapa de calor de correlaciones...")
plt.figure(figsize=(10, 8))

# Seleccionar variables numericas
corr_data = df_ordenes[['Cantidad', 'Costo_Unitario', 'Costo_Total', 'Tiempo_Entrega_Días']].corr()

# Crear mapa de calor
sns.heatmap(corr_data, 
            annot=True, 
            cmap='RdYlBu_r', 
            center=0,
            square=True,
            fmt='.3f',
            cbar_kws={'label': 'Correlacion'},
            annot_kws={'size': 12})

plt.title('Mapa de Calor - Correlaciones entre Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('grafica16_mapa_calor.png', dpi=150, bbox_inches='tight')
print("✅ Grafica 16 guardada: grafica16_mapa_calor.png")
plt.close()

# ============================================
# GRAFICA 17: Boxplot de costos por categoria
# ============================================
print("\n📊 Grafica 17: Boxplot de costos por categoria...")
plt.figure(figsize=(12, 7))

# Crear boxplot
productos = df_ordenes['Producto'].unique()
datos_box = [df_ordenes[df_ordenes['Producto']==p]['Costo_Total'].values for p in productos]

box_plot = plt.boxplot(datos_box, patch_artist=True)

plt.xticks(range(1, len(productos)+1), productos, rotation=45, ha='right')

# Colores para cada caja
colores = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c', '#e67e22', '#34495e']
for patch, color in zip(box_plot['boxes'], colores):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

plt.ylabel('Costo Total ($)', fontsize=12)
plt.title('Distribucion de Costos por Categoria de Producto', fontsize=14, fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('grafica17_boxplot_costos.png', dpi=150, bbox_inches='tight')
print("✅ Grafica 17 guardada: grafica17_boxplot_costos.png")
plt.close()

# ============================================
# GRAFICA 18: Area apilada de envios por zona
# ============================================
print("\n📊 Grafica 18: Area apilada de envios por zona...")
plt.figure(figsize=(12, 7))

# Convertir fechas
df_envios['Fecha_Envio'] = pd.to_datetime(df_envios['Fecha_Envío'], format='%d/%m/%Y')
df_envios['Mes'] = df_envios['Fecha_Envio'].dt.to_period('M').astype(str)

# Pivot table para area apilada
envios_pivot = df_envios.pivot_table(index='Mes', 
                                      columns='Zona_Destino', 
                                      values='ID_Envío', 
                                      aggfunc='count',
                                      fill_value=0)

# Ordenar meses
meses_orden = ['2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07']
envios_pivot = envios_pivot.reindex([m for m in meses_orden if m in envios_pivot.index])

# Crear area apilada
envios_pivot.plot(kind='area', 
                  stacked=True, 
                  figsize=(12, 7),
                  alpha=0.7,
                  color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])

plt.title('Evolucion de Envios por Zona (Area Apilada)', fontsize=14, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Cantidad de Envios', fontsize=12)
plt.legend(title='Zona', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('grafica18_area_apilada.png', dpi=150, bbox_inches='tight')
print("✅ Grafica 18 guardada: grafica18_area_apilada.png")
plt.close()

# ============================================
# GRAFICA 19: Grafico de burbujas
# ============================================
print("\n📊 Grafica 19: Grafico de burbujas...")
plt.figure(figsize=(12, 8))

# Datos para burbujas
x = df_ordenes['Cantidad']
y = df_ordenes['Costo_Total']
z = df_ordenes['Tiempo_Entrega_Días']  # Tamaño de burbuja
colores_estado = df_ordenes['Estado'].map({
    'Entregado': '#2ecc71',
    'En tránsito': '#3498db',
    'Pendiente': '#f39c12',
    'Cancelado': '#e74c3c',
    'Devuelto': '#9b59b6'
})

scatter = plt.scatter(x, y, 
                     s=z*30,  # Tamaño proporcional a dias de entrega
                     c=colores_estado,
                     alpha=0.6,
                     edgecolors='black',
                     linewidth=0.5)

plt.xlabel('Cantidad', fontsize=12)
plt.ylabel('Costo Total ($)', fontsize=12)
plt.title('Relacion Cantidad vs Costo vs Tiempo de Entrega', fontsize=14, fontweight='bold')

# Leyenda manual
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#2ecc71', label='Entregado'),
                   Patch(facecolor='#3498db', label='En transito'),
                   Patch(facecolor='#f39c12', label='Pendiente'),
                   Patch(facecolor='#e74c3c', label='Cancelado'),
                   Patch(facecolor='#9b59b6', label='Devuelto')]
plt.legend(handles=legend_elements, loc='upper left', title='Estado')

# Nota sobre tamaño
plt.figtext(0.15, 0.02, 'Nota: Tamano de burbuja = Dias de entrega', 
            fontsize=9, style='italic')

plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('grafica19_burbujas.png', dpi=150, bbox_inches='tight')
print("✅ Grafica 19 guardada: grafica19_burbujas.png")
plt.close()

# ============================================
# GRAFICA 20: Radar/Spider de almacenes
# ============================================
print("\n📊 Grafica 20: Radar de almacenes...")
plt.figure(figsize=(10, 10))

# Calcular metricas por almacen
almacen_metrics = df_ordenes.groupby('Almacén_Destino').agg({
    'Tiempo_Entrega_Días': 'mean',
    'Costo_Total': 'sum',
    'ID_Orden': 'count'
}).reset_index()

# Normalizar metricas (0-100)
almacen_metrics['Tiempo_Norm'] = (1 - (almacen_metrics['Tiempo_Entrega_Días'] / almacen_metrics['Tiempo_Entrega_Días'].max())) * 100
almacen_metrics['Costo_Norm'] = (almacen_metrics['Costo_Total'] / almacen_metrics['Costo_Total'].max()) * 100
almacen_metrics['Ordenes_Norm'] = (almacen_metrics['ID_Orden'] / almacen_metrics['ID_Orden'].max()) * 100

# Crear radar
categorias = ['Velocidad\nEntrega', 'Volumen\nNegocio', 'Cantidad\nOrdenes']
N = len(categorias)

# Angulos para cada eje
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Crear subplot polar
ax = plt.subplot(111, projection='polar')

# Colores para cada almacen
colores_alm = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6', '#1abc9c']

for idx, row in almacen_metrics.iterrows():
    valores = [row['Tiempo_Norm'], row['Costo_Norm'], row['Ordenes_Norm']]
    valores += valores[:1]
    
    ax.plot(angles, valores, 'o-', linewidth=2, 
            label=row['Almacén_Destino'], color=colores_alm[idx % len(colores_alm)])
    ax.fill(angles, valores, alpha=0.15, color=colores_alm[idx % len(colores_alm)])

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categorias, fontsize=11)
ax.set_ylim(0, 100)
ax.set_title('Perfil Comparativo de Almacenes (Radar)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
ax.grid(True)

plt.tight_layout()
plt.savefig('grafica20_radar_almacenes.png', dpi=150, bbox_inches='tight')
print("✅ Grafica 20 guardada: grafica20_radar_almacenes.png")
plt.close()

print("\n" + "=" * 60)
print("🎉 TODAS LAS GRAFICAS FINALES CREADAS!")
print("=" * 60)
print("\nNuevas graficas:")
print("   16. grafica16_mapa_calor.png")
print("   17. grafica17_boxplot_costos.png")
print("   18. grafica18_area_apilada.png")
print("   19. grafica19_burbujas.png")
print("   20. grafica20_radar_almacenes.png")
print("\nTOTAL ACUMULADO: 20 graficas!")