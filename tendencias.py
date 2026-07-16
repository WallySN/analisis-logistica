import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')

# Ver nombres de columnas (para debug)
print("Columnas en df_envios:", df_envios.columns.tolist())

# Convertir fechas - usando los nombres EXACTOS del Excel
df_ordenes['Fecha_Orden'] = pd.to_datetime(df_ordenes['Fecha_Orden'], format='%d/%m/%Y')
df_envios['Fecha_Envío'] = pd.to_datetime(df_envios['Fecha_Envío'], format='%d/%m/%Y')

# ============================================
# GRAFICA 7: Tendencia de ordenes por mes
# ============================================
plt.figure(figsize=(12, 6))
ordenes_mes = df_ordenes.groupby(df_ordenes['Fecha_Orden'].dt.to_period('M')).size()
ordenes_mes.index = ordenes_mes.index.astype(str)
plt.plot(range(len(ordenes_mes)), ordenes_mes.values, marker='o', linewidth=2, markersize=8, color='#3498db')
plt.fill_between(range(len(ordenes_mes)), ordenes_mes.values, alpha=0.3, color='#3498db')
plt.title('Tendencia de Ordenes por Mes', fontsize=14, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Numero de Ordenes', fontsize=12)
plt.xticks(range(len(ordenes_mes)), ordenes_mes.index, rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('grafica7_tendencia_ordenes.png', dpi=150, bbox_inches='tight')
print("Grafica 7 guardada: grafica7_tendencia_ordenes.png")
plt.close()

# ============================================
# GRAFICA 8: Comparacion costo vs cantidad
# ============================================
plt.figure(figsize=(10, 6))
colores_estado = {'Entregado':'#2ecc71', 'En tránsito':'#3498db', 
                  'Pendiente':'#f39c12', 'Cancelado':'#e74c3c', 'Devuelto':'#9b59b6'}
plt.scatter(df_ordenes['Cantidad'], df_ordenes['Costo_Total'], 
           c=df_ordenes['Estado'].map(colores_estado),
           alpha=0.6, s=100)
plt.xlabel('Cantidad', fontsize=12)
plt.ylabel('Costo Total ($)', fontsize=12)
plt.title('Relacion Cantidad vs Costo Total', fontsize=14, fontweight='bold')
plt.grid(alpha=0.3)

legend_elements = [Patch(facecolor='#2ecc71', label='Entregado'),
                   Patch(facecolor='#3498db', label='En transito'),
                   Patch(facecolor='#f39c12', label='Pendiente'),
                   Patch(facecolor='#e74c3c', label='Cancelado'),
                   Patch(facecolor='#9b59b6', label='Devuelto')]
plt.legend(handles=legend_elements, loc='upper left')
plt.tight_layout()
plt.savefig('grafica8_cantidad_vs_costo.png', dpi=150, bbox_inches='tight')
print("Grafica 8 guardada: grafica8_cantidad_vs_costo.png")
plt.close()

# ============================================
# GRAFICA 9: Envios por mes y estado
# ============================================
plt.figure(figsize=(12, 6))
df_envios['Mes'] = df_envios['Fecha_Envío'].dt.to_period('M').astype(str)
envios_pivot = df_envios.pivot_table(index='Mes', columns='Estado_Envío', aggfunc='size', fill_value=0)
envios_pivot.plot(kind='bar', stacked=True, figsize=(12, 6), 
                  color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
plt.title('Envios por Mes y Estado', fontsize=14, fontweight='bold')
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Cantidad de Envios', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Estado')
plt.tight_layout()
plt.savefig('grafica9_envios_mes_estado.png', dpi=150, bbox_inches='tight')
print("Grafica 9 guardada: grafica9_envios_mes_estado.png")
plt.close()

print("\nGraficas de tendencias creadas!")