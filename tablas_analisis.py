import pandas as pd

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

print("=" * 60)
print("TABLAS DE ANALISIS AVANZADO")
print("=" * 60)

# ============================================
# TABLA 1: Rentabilidad por Producto
# ============================================
print("\n" + "-" * 60)
print("1. RENTABILIDAD POR TIPO DE PRODUCTO")
print("-" * 60)
rentabilidad = df_ordenes.groupby('Producto').agg({
    'Costo_Total': 'sum',
    'Cantidad': 'sum',
    'ID_Orden': 'count'
}).rename(columns={'ID_Orden': 'Num_Ordenes'})
rentabilidad['Costo_Promedio_Unitario'] = (rentabilidad['Costo_Total'] / rentabilidad['Cantidad']).round(2)
rentabilidad = rentabilidad.sort_values('Costo_Total', ascending=False)
print(rentabilidad.to_string())

# ============================================
# TABLA 2: Eficiencia de Entrega por Almacen
# ============================================
print("\n" + "-" * 60)
print("2. EFICIENCIA DE ENTREGA POR ALMACEN")
print("-" * 60)
eficiencia_almacen = df_ordenes.groupby('Almacén_Destino').agg({
    'Tiempo_Entrega_Días': 'mean',
    'Costo_Total': 'sum',
    'ID_Orden': 'count'
})
eficiencia_almacen.columns = ['Tiempo_Promedio_Dias', 'Costo_Total', 'Total_Ordenes']
eficiencia_almacen['Tiempo_Promedio_Dias'] = eficiencia_almacen['Tiempo_Promedio_Dias'].round(1)
eficiencia_almacen = eficiencia_almacen.sort_values('Tiempo_Promedio_Dias')
print(eficiencia_almacen.to_string())

# ============================================
# TABLA 3: Costo por Kg de Envio
# ============================================
print("\n" + "-" * 60)
print("3. EFICIENCIA DE COSTO DE ENVIO (Costo por Kg)")
print("-" * 60)
df_envios['Costo_por_Kg'] = (df_envios['Costo_Envío'] / df_envios['Peso_kg']).round(2)
eficiencia_envio = df_envios.groupby('Zona_Destino').agg({
    'Costo_Envío': 'sum',
    'Peso_kg': 'sum',
    'Costo_por_Kg': 'mean',
    'ID_Envío': 'count'
})
eficiencia_envio.columns = ['Costo_Envío', 'Peso_kg', 'Costo_por_Kg_Promedio', 'Total_Envíos']
eficiencia_envio['Costo_por_Kg_Promedio'] = eficiencia_envio['Costo_por_Kg_Promedio'].round(2)
eficiencia_envio = eficiencia_envio.sort_values('Costo_por_Kg_Promedio')
print(eficiencia_envio.to_string())

# ============================================
# TABLA 4: Ranking Completo de Transportistas
# ============================================
print("\n" + "-" * 60)
print("4. RANKING COMPLETO DE TRANSPORTISTAS")
print("-" * 60)
ranking = df_rendimiento.groupby('Transportista').agg({
    'Envíos_Realizados': 'sum',
    'Envíos_Entregados_Tiempo': 'sum',
    'Envíos_Retrasados': 'sum',
    'Kilómetros_Recorridos': 'sum',
    'Combustible_Litros': 'sum',
    'Costo_Combustible': 'sum',
    'Incidentes_Reportados': 'sum',
    'Calificación_Cliente': 'mean'
}).round(2)
ranking['%_Entrega_Tiempo'] = ((ranking['Envíos_Entregados_Tiempo'] / ranking['Envíos_Realizados']) * 100).round(1)
ranking['Rendimiento_Km_L'] = (ranking['Kilómetros_Recorridos'] / ranking['Combustible_Litros']).round(2)
ranking['Costo_por_Km'] = (ranking['Costo_Combustible'] / ranking['Kilómetros_Recorridos']).round(2)
ranking = ranking.sort_values('Calificación_Cliente', ascending=False)
print(ranking.to_string())

# ============================================
# TABLA 5: Analisis ABC de Inventario
# ============================================
print("\n" + "-" * 60)
print("5. ANALISIS ABC DEL INVENTARIO")
print("-" * 60)
inventario_abc = df_inventario[['SKU', 'Nombre_Producto', 'Valor_Inventario']].copy()
inventario_abc = inventario_abc.sort_values('Valor_Inventario', ascending=False)
inventario_abc['%_Acumulado'] = (inventario_abc['Valor_Inventario'].cumsum() / inventario_abc['Valor_Inventario'].sum() * 100).round(1)

def clasificar_abc(porcentaje):
    if porcentaje <= 80:
        return 'A (80% valor)'
    elif porcentaje <= 95:
        return 'B (15% valor)'
    else:
        return 'C (5% valor)'

inventario_abc['Clasificacion_ABC'] = inventario_abc['%_Acumulado'].apply(clasificar_abc)
print(inventario_abc[['SKU', 'Nombre_Producto', 'Valor_Inventario', '%_Acumulado', 'Clasificacion_ABC']].head(15).to_string())

abc_resumen = inventario_abc['Clasificacion_ABC'].value_counts()
print(f"\nResumen ABC:\n{abc_resumen.to_string()}")

# ============================================
# TABLA 6: Indicadores Mensuales
# ============================================
print("\n" + "-" * 60)
print("6. INDICADORES MENSUALES DE RENDIMIENTO")
print("-" * 60)
mensual = df_rendimiento.groupby('Mes').agg({
    'Envíos_Realizados': 'sum',
    'Envíos_Entregados_Tiempo': 'sum',
    'Costo_Combustible': 'sum',
    'Incidentes_Reportados': 'sum',
    'Calificación_Cliente': 'mean'
}).round(2)
mensual['%_Entrega_Tiempo'] = ((mensual['Envíos_Entregados_Tiempo'] / mensual['Envíos_Realizados']) * 100).round(1)
mensual = mensual.sort_values('Envíos_Realizados', ascending=False)
print(mensual.to_string())

print("\n" + "=" * 60)
print("FIN DEL ANALISIS")
print("=" * 60)