import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

# ============================================
# GRÁFICA 1: Órdenes por Estado (Pastel)
# ============================================
plt.figure(figsize=(8, 6))
estados = df_ordenes['Estado'].value_counts()
colores = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
plt.pie(estados.values, labels=estados.index, autopct='%1.1f%%', colors=colores, startangle=90)
plt.title('📦 Órdenes por Estado', fontsize=14, fontweight='bold')
plt.savefig('grafica1_ordenes_estado.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 1 guardada: grafica1_ordenes_estado.png")
plt.close()

# ============================================
# GRÁFICA 2: Top 5 Proveedores por Gasto (Barras)
# ============================================
plt.figure(figsize=(10, 6))
top_prov = df_ordenes.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).head()
barras = plt.barh(top_prov.index[::-1], top_prov.values[::-1], color='#3498db')
plt.xlabel('Costo Total ($)', fontsize=12)
plt.title('🏢 Top 5 Proveedores por Gasto', fontsize=14, fontweight='bold')
plt.grid(axis='x', alpha=0.3)
# Agregar valores en las barras
for barra in barras:
    ancho = barra.get_width()
    plt.text(ancho + 5000, barra.get_y() + barra.get_height()/2, 
             f'${ancho:,.0f}', va='center', fontsize=10)
plt.savefig('grafica2_proveedores.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 2 guardada: grafica2_proveedores.png")
plt.close()

# ============================================
# GRÁFICA 3: Estado del Inventario (Pastel)
# ============================================
plt.figure(figsize=(8, 6))
stock_estado = df_inventario['Estado_Stock'].value_counts()
colores_stock = ['#2ecc71', '#f39c12', '#e74c3c']
plt.pie(stock_estado.values, labels=stock_estado.index, autopct='%1.1f%%', 
        colors=colores_stock, startangle=90)
plt.title('📦 Estado del Inventario', fontsize=14, fontweight='bold')
plt.savefig('grafica3_inventario.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 3 guardada: grafica3_inventario.png")
plt.close()

# ============================================
# GRÁFICA 4: Envíos por Zona (Barras)
# ============================================
plt.figure(figsize=(10, 6))
envios_zona = df_envios.groupby('Zona_Destino')['Costo_Envío'].sum().sort_values(ascending=False)
barras = plt.bar(envios_zona.index, envios_zona.values, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])
plt.ylabel('Costo Total de Envíos ($)', fontsize=12)
plt.title('🚚 Costo de Envíos por Zona', fontsize=14, fontweight='bold')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
# Agregar valores sobre las barras
for barra in barras:
    altura = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, altura + 200, 
             f'${altura:,.0f}', ha='center', fontsize=10)
plt.savefig('grafica4_envios_zona.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 4 guardada: grafica4_envios_zona.png")
plt.close()

# ============================================
# GRÁFICA 5: Calificación de Transportistas (Barras horizontales)
# ============================================
plt.figure(figsize=(10, 6))
calif = df_rendimiento.groupby('Transportista')['Calificación_Cliente'].mean().sort_values()
colores_calif = ['#e74c3c' if x < 4.0 else '#f39c12' if x < 4.5 else '#2ecc71' for x in calif.values]
barras = plt.barh(calif.index, calif.values, color=colores_calif)
plt.xlabel('Calificación Promedio (⭐)', fontsize=12)
plt.title('⭐ Calificación de Transportistas', fontsize=14, fontweight='bold')
plt.xlim(3, 5.5)
plt.grid(axis='x', alpha=0.3)
# Agregar valores
for barra in barras:
    ancho = barra.get_width()
    plt.text(ancho + 0.05, barra.get_y() + barra.get_height()/2, 
             f'{ancho:.1f} ⭐', va='center', fontsize=10)
plt.savefig('grafica5_transportistas.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 5 guardada: grafica5_transportistas.png")
plt.close()

# ============================================
# GRÁFICA 6: Dashboard resumen (varios en uno)
# ============================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Subplot 1: Órdenes por estado
estados = df_ordenes['Estado'].value_counts()
axes[0,0].pie(estados.values, labels=estados.index, autopct='%1.1f%%', colors=colores)
axes[0,0].set_title('Órdenes por Estado', fontweight='bold')

# Subplot 2: Top 5 proveedores
top5 = df_ordenes.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).head()
axes[0,1].barh(range(len(top5)), top5.values, color='#3498db')
axes[0,1].set_yticks(range(len(top5)))
axes[0,1].set_yticklabels(top5.index, fontsize=8)
axes[0,1].set_title('Top 5 Proveedores', fontweight='bold')
axes[0,1].grid(axis='x', alpha=0.3)

# Subplot 3: Envíos por estado
env_estados = df_envios['Estado_Envío'].value_counts()
axes[1,0].bar(env_estados.index, env_estados.values, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
axes[1,0].set_title('Envíos por Estado', fontweight='bold')
axes[1,0].tick_params(axis='x', rotation=15)

# Subplot 4: Stock crítico
stock_estado = df_inventario['Estado_Stock'].value_counts()
axes[1,1].pie(stock_estado.values, labels=stock_estado.index, autopct='%1.1f%%', colors=colores_stock)
axes[1,1].set_title('Estado del Inventario', fontweight='bold')

plt.suptitle('📊 DASHBOARD DE LOGÍSTICA', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('grafica6_dashboard.png', dpi=150, bbox_inches='tight')
print("✅ Gráfica 6 guardada: grafica6_dashboard.png")
plt.close()

print("\n" + "=" * 50)
print("🎉 ¡TODAS LAS GRÁFICAS CREADAS!")
print("=" * 50)
print("\nArchivos generados:")
print("   📊 grafica1_ordenes_estado.png")
print("   📊 grafica2_proveedores.png")
print("   📊 grafica3_inventario.png")
print("   📊 grafica4_envios_zona.png")
print("   📊 grafica5_transportistas.png")
print("   📊 grafica6_dashboard.png")