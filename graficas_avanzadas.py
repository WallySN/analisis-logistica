import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

# ============================================
# GRAFICA 10: Rentabilidad por Producto (barras horizontales)
# ============================================
plt.figure(figsize=(10, 6))
rentabilidad = df_ordenes.groupby('Producto')['Costo_Total'].sum().sort_values()
colores = ['#e74c3c' if x < 800000 else '#f39c12' if x < 1500000 else '#2ecc71' for x in rentabilidad.values]
barras = plt.barh(rentabilidad.index, rentabilidad.values, color=colores)
plt.xlabel('Costo Total ($)', fontsize=12)
plt.title('Rentabilidad por Tipo de Producto', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
for barra in barras:
    ancho = barra.get_width()
    plt.text(ancho + 20000, barra.get_y() + barra.get_height()/2, 
             f'${ancho:,.0f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('grafica10_rentabilidad_producto.png', dpi=150, bbox_inches='tight')
print("Grafica 10 guardada: grafica10_rentabilidad_producto.png")
plt.close()

# ============================================
# GRAFICA 11: Eficiencia de Entrega por Almacen
# ============================================
plt.figure(figsize=(10, 6))
eficiencia = df_ordenes.groupby('Almacén_Destino')['Tiempo_Entrega_Días'].mean().sort_values()
colores = ['#2ecc71' if x < 7 else '#f39c12' if x < 10 else '#e74c3c' for x in eficiencia.values]
barras = plt.bar(eficiencia.index, eficiencia.values, color=colores)
plt.ylabel('Dias Promedio de Entrega', fontsize=12)
plt.title('Eficiencia de Entrega por Almacen', fontsize=14, fontweight='bold')
plt.xticks(rotation=15)
plt.grid(axis='y', alpha=0.3)
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 0.2, 
             f'{altura:.1f} d', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('grafica11_eficiencia_almacen.png', dpi=150, bbox_inches='tight')
print("Grafica 11 guardada: grafica11_eficiencia_almacen.png")
plt.close()

# ============================================
# GRAFICA 12: Costo por Kg por Zona
# ============================================
plt.figure(figsize=(10, 6))
df_envios['Costo_por_Kg'] = df_envios['Costo_Envío'] / df_envios['Peso_kg']
costo_kg = df_envios.groupby('Zona_Destino')['Costo_por_Kg'].mean().sort_values()
colores = ['#2ecc71' if x < 5 else '#f39c12' if x < 10 else '#e74c3c' for x in costo_kg.values]
barras = plt.bar(costo_kg.index, costo_kg.values, color=colores)
plt.ylabel('Costo por Kg ($)', fontsize=12)
plt.title('Costo de Envio por Kg - Eficiencia por Zona', fontsize=14, fontweight='bold')
plt.grid(axis='y', alpha=0.3)
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 0.3, 
             f'${altura:.2f}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('grafica12_costo_kg_zona.png', dpi=150, bbox_inches='tight')
print("Grafica 12 guardada: grafica12_costo_kg_zona.png")
plt.close()

# ============================================
# GRAFICA 13: Ranking Transportistas (Radar de metricas)
# ============================================
plt.figure(figsize=(12, 8))
ranking = df_rendimiento.groupby('Transportista').agg({
    'Calificación_Cliente': 'mean',
    '%_Entregas_a_Tiempo': 'mean',
    'Rendimiento_Km_Litro': 'mean'
}).round(2)

# Normalizar para comparar (0-100)
ranking_norm = ranking.copy()
ranking_norm['Calificación_Cliente'] = (ranking_norm['Calificación_Cliente'] / 5) * 100
ranking_norm['%_Entregas_a_Tiempo'] = ranking_norm['%_Entregas_a_Tiempo'].clip(0, 100)
ranking_norm['Rendimiento_Km_Litro'] = (ranking_norm['Rendimiento_Km_Litro'] / ranking_norm['Rendimiento_Km_Litro'].max()) * 100

x = range(len(ranking_norm))
ancho = 0.25
plt.bar([i - ancho for i in x], ranking_norm['Calificación_Cliente'], width=ancho, label='Calificación (%)', color='#3498db')
plt.bar(x, ranking_norm['%_Entregas_a_Tiempo'], width=ancho, label='Entregas a Tiempo (%)', color='#2ecc71')
plt.bar([i + ancho for i in x], ranking_norm['Rendimiento_Km_Litro'], width=ancho, label='Rendimiento Combustible (%)', color='#f39c12')

plt.xlabel('Transportista', fontsize=12)
plt.ylabel('Puntuación Normalizada (0-100)', fontsize=12)
plt.title('Ranking Comparativo de Transportistas', fontsize=14, fontweight='bold')
plt.xticks(x, ranking_norm.index, rotation=45, ha='right')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('grafica13_ranking_transportistas.png', dpi=150, bbox_inches='tight')
print("Grafica 13 guardada: grafica13_ranking_transportistas.png")
plt.close()

# ============================================
# GRAFICA 14: Analisis ABC del Inventario
# ============================================
plt.figure(figsize=(10, 6))
inventario_abc = df_inventario[['SKU', 'Nombre_Producto', 'Valor_Inventario']].copy()
inventario_abc = inventario_abc.sort_values('Valor_Inventario', ascending=False)
inventario_abc['%_Acumulado'] = (inventario_abc['Valor_Inventario'].cumsum() / inventario_abc['Valor_Inventario'].sum() * 100)

# Curva ABC
plt.plot(range(1, len(inventario_abc)+1), inventario_abc['%_Acumulado'], 
         marker='o', linewidth=2, markersize=4, color='#3498db')
plt.axhline(y=80, color='#e74c3c', linestyle='--', label='80% (Clase A)')
plt.axhline(y=95, color='#f39c12', linestyle='--', label='95% (Clase B)')
plt.fill_between(range(1, len(inventario_abc)+1), 0, inventario_abc['%_Acumulado'], 
                 alpha=0.3, color='#3498db')
plt.xlabel('Productos (ordenados por valor)', fontsize=12)
plt.ylabel('% Valor Acumulado', fontsize=12)
plt.title('Curva ABC del Inventario', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('grafica14_curva_abc.png', dpi=150, bbox_inches='tight')
print("Grafica 14 guardada: grafica14_curva_abc.png")
plt.close()

# ============================================
# GRAFICA 15: Dashboard Ejecutivo Final
# ============================================
fig = plt.figure(figsize=(16, 12))

# Subplot 1
ax1 = plt.subplot(3, 3, 1)
estados = df_ordenes['Estado'].value_counts()
ax1.pie(estados.values, labels=estados.index, autopct='%1.1f%%', 
        colors=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6'])
ax1.set_title('Ordenes por Estado', fontweight='bold', fontsize=10)

# Subplot 2
ax2 = plt.subplot(3, 3, 2)
top5 = df_ordenes.groupby('Producto')['Costo_Total'].sum().sort_values(ascending=False).head()
ax2.barh(top5.index[::-1], top5.values[::-1], color='#3498db')
ax2.set_title('Top 5 Productos', fontweight='bold', fontsize=10)

# Subplot 3
ax3 = plt.subplot(3, 3, 3)
stock = df_inventario['Estado_Stock'].value_counts()
ax3.pie(stock.values, labels=stock.index, autopct='%1.1f%%', 
        colors=['#2ecc71', '#f39c12', '#e74c3c'])
ax3.set_title('Estado Inventario', fontweight='bold', fontsize=10)

# Subplot 4
ax4 = plt.subplot(3, 3, 4)
env_zona = df_envios.groupby('Zona_Destino')['Costo_Envío'].sum().sort_values(ascending=False)
ax4.bar(env_zona.index, env_zona.values, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])
ax4.set_title('Envios por Zona ($)', fontweight='bold', fontsize=10)
ax4.tick_params(axis='x', rotation=15)

# Subplot 5
ax5 = plt.subplot(3, 3, 5)
calif = df_rendimiento.groupby('Transportista')['Calificación_Cliente'].mean().sort_values()
colores_calif = ['#e74c3c' if x < 4.0 else '#f39c12' if x < 4.5 else '#2ecc71' for x in calif.values]
ax5.barh(calif.index, calif.values, color=colores_calif)
ax5.set_title('Calificacion Transportistas', fontweight='bold', fontsize=10)
ax5.set_xlim(3, 5.5)

# Subplot 6
ax6 = plt.subplot(3, 3, 6)
efic = df_ordenes.groupby('Almacén_Destino')['Tiempo_Entrega_Días'].mean().sort_values()
colores_ef = ['#2ecc71' if x < 7 else '#f39c12' if x < 10 else '#e74c3c' for x in efic.values]
ax6.bar(efic.index, efic.values, color=colores_ef)
ax6.set_title('Tiempo Entrega por Almacen', fontweight='bold', fontsize=10)
ax6.tick_params(axis='x', rotation=15)

# Subplot 7
ax7 = plt.subplot(3, 3, 7)
rent = df_ordenes.groupby('Producto')['Costo_Total'].sum().sort_values()
ax7.barh(rent.index, rent.values, color='#9b59b6')
ax7.set_title('Rentabilidad Productos', fontweight='bold', fontsize=10)

# Subplot 8
ax8 = plt.subplot(3, 3, 8)
df_envios['CostoKg'] = df_envios['Costo_Envío'] / df_envios['Peso_kg']
ck = df_envios.groupby('Zona_Destino')['CostoKg'].mean().sort_values()
ax8.bar(ck.index, ck.values, color='#1abc9c')
ax8.set_title('Costo por Kg por Zona', fontweight='bold', fontsize=10)
ax8.tick_params(axis='x', rotation=15)

# Subplot 9
ax9 = plt.subplot(3, 3, 9)
mensual = df_rendimiento.groupby('Mes')['Envíos_Realizados'].sum().reindex(
    ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio'], fill_value=0)
ax9.plot(mensual.index, mensual.values, marker='o', color='#e67e22', linewidth=2, markersize=6)
ax9.fill_between(range(len(mensual)), mensual.values, alpha=0.3, color='#e67e22')
ax9.set_title('Envios por Mes', fontweight='bold', fontsize=10)
ax9.tick_params(axis='x', rotation=45)

plt.suptitle('DASHBOARD EJECUTIVO - LOGISTICA', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('grafica15_dashboard_ejecutivo.png', dpi=150, bbox_inches='tight')
print("Grafica 15 guardada: grafica15_dashboard_ejecutivo.png")
plt.close()

print("\n" + "=" * 50)
print("TODAS LAS GRAFICAS AVANZADAS CREADAS!")
print("=" * 50)
print("\nNuevas graficas:")
print("   10. grafica10_rentabilidad_producto.png")
print("   11. grafica11_eficiencia_almacen.png")
print("   12. grafica12_costo_kg_zona.png")
print("   13. grafica13_ranking_transportistas.png")
print("   14. grafica14_curva_abc.png")
print("   15. grafica15_dashboard_ejecutivo.png (9 en 1)")
print("\nTOTAL: 15 graficas en tu proyecto!")