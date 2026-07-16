import pandas as pd
import matplotlib.pyplot as plt

# Cargar el Excel
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

print("=" * 50)
print("📊 ANÁLISIS DE LOGÍSTICA")
print("=" * 50)

# 1. Total gastado en órdenes
total_gastado = df_ordenes['Costo_Total'].sum()
print(f"\n💰 Total gastado en órdenes: ${total_gastado:,.2f}")

# 2. Órdenes por estado
print(f"\n📦 Órdenes por estado:")
print(df_ordenes['Estado'].value_counts())

# 3. Top 5 proveedores por gasto
print(f"\n🏢 Top 5 proveedores por gasto:")
top_proveedores = df_ordenes.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).head()
print(top_proveedores)

# 4. Valor total del inventario
valor_inventario = df_inventario['Valor_Inventario'].sum()
print(f"\n📦 Valor total del inventario: ${valor_inventario:,.2f}")

# 5. Productos con stock crítico/bajo
stock_bajo = df_inventario[df_inventario['Estado_Stock'].isin(['Bajo', 'Crítico'])]
print(f"\n⚠️ Productos con stock bajo/crítico: {len(stock_bajo)}")

# 6. Envíos por estado
print(f"\n🚚 Envíos por estado:")
print(df_envios['Estado_Envío'].value_counts())

# 7. Costo total de envíos
total_envios = df_envios['Costo_Envío'].sum()
print(f"\n💸 Costo total de envíos: ${total_envios:,.2f}")

# 8. Mejor transportista por calificación
mejor_transportista = df_rendimiento.groupby('Transportista')['Calificación_Cliente'].mean().sort_values(ascending=False)
print(f"\n⭐ Mejores transportistas (promedio calificación):")
print(mejor_transportista)