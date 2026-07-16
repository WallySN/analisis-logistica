import pandas as pd

# Cargar datos originales
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

print("=" * 60)
print("EXPORTANDO TABLAS DE ANALISIS A EXCEL")
print("=" * 60)

# ============================================
# HOJA 1: Resumen Ejecutivo
# ============================================
print("\n[1/6] Creando Resumen Ejecutivo...")
resumen = pd.DataFrame({
    'Indicador': [
        'Total Gastado en Ordenes',
        'Ordenes Entregadas',
        'Ordenes En Transito',
        'Ordenes Canceladas',
        'Ordenes Devueltas',
        'Ordenes Pendientes',
        'Costo Total de Envios',
        'Valor Total del Inventario',
        'Total de Productos en Inventario',
        'Productos con Stock Bajo/Critico',
        'Numero de Transportistas',
        'Promedio Calificacion Transportistas'
    ],
    'Valor': [
        f"${df_ordenes['Costo_Total'].sum():,.2f}",
        len(df_ordenes[df_ordenes['Estado'] == 'Entregado']),
        len(df_ordenes[df_ordenes['Estado'] == 'En tránsito']),
        len(df_ordenes[df_ordenes['Estado'] == 'Cancelado']),
        len(df_ordenes[df_ordenes['Estado'] == 'Devuelto']),
        len(df_ordenes[df_ordenes['Estado'] == 'Pendiente']),
        f"${df_envios['Costo_Envío'].sum():,.2f}",
        f"${df_inventario['Valor_Inventario'].sum():,.2f}",
        len(df_inventario),
        len(df_inventario[df_inventario['Estado_Stock'].isin(['Bajo', 'Crítico'])]),
        df_rendimiento['Transportista'].nunique(),
        f"{df_rendimiento['Calificación_Cliente'].mean():.2f}"
    ]
})

# ============================================
# HOJA 2: Rentabilidad por Producto
# ============================================
print("[2/6] Creando Rentabilidad por Producto...")
rentabilidad = df_ordenes.groupby('Producto').agg({
    'Costo_Total': 'sum',
    'Cantidad': 'sum',
    'ID_Orden': 'count'
}).rename(columns={'ID_Orden': 'Num_Ordenes'})
rentabilidad['Costo_Promedio_Unitario'] = (rentabilidad['Costo_Total'] / rentabilidad['Cantidad']).round(2)
rentabilidad['%_del_Total'] = ((rentabilidad['Costo_Total'] / rentabilidad['Costo_Total'].sum()) * 100).round(1)
rentabilidad = rentabilidad.sort_values('Costo_Total', ascending=False)

# ============================================
# HOJA 3: Eficiencia por Almacen
# ============================================
print("[3/6] Creando Eficiencia por Almacen...")
eficiencia_almacen = df_ordenes.groupby('Almacén_Destino').agg({
    'Tiempo_Entrega_Días': 'mean',
    'Costo_Total': 'sum',
    'ID_Orden': 'count'
})
eficiencia_almacen.columns = ['Tiempo_Promedio_Dias', 'Costo_Total', 'Total_Ordenes']
eficiencia_almacen['Tiempo_Promedio_Dias'] = eficiencia_almacen['Tiempo_Promedio_Dias'].round(1)
eficiencia_almacen['Eficiencia'] = eficiencia_almacen['Tiempo_Promedio_Dias'].apply(
    lambda x: 'Excelente' if x < 7 else 'Buena' if x < 10 else 'Regular' if x < 12 else 'Deficiente'
)
eficiencia_almacen = eficiencia_almacen.sort_values('Tiempo_Promedio_Dias')

# ============================================
# HOJA 4: Eficiencia de Envios por Zona
# ============================================
print("[4/6] Creando Eficiencia de Envios...")
df_envios['Costo_por_Kg'] = (df_envios['Costo_Envío'] / df_envios['Peso_kg']).round(2)
eficiencia_envio = df_envios.groupby('Zona_Destino').agg({
    'Costo_Envío': 'sum',
    'Peso_kg': 'sum',
    'Costo_por_Kg': 'mean',
    'ID_Envío': 'count'
})
eficiencia_envio.columns = ['Costo_Total_Envios', 'Peso_Total_Kg', 'Costo_Promedio_por_Kg', 'Total_Envios']
eficiencia_envio['Costo_Promedio_por_Kg'] = eficiencia_envio['Costo_Promedio_por_Kg'].round(2)
eficiencia_envio['Eficiencia_Costo'] = eficiencia_envio['Costo_Promedio_por_Kg'].apply(
    lambda x: 'Economica' if x < 5 else 'Moderada' if x < 10 else 'Cara'
)
eficiencia_envio = eficiencia_envio.sort_values('Costo_Promedio_por_Kg')

# ============================================
# HOJA 5: Ranking Completo Transportistas
# ============================================
print("[5/6] Creando Ranking de Transportistas...")
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
ranking['%_Entrega_a_Tiempo'] = ((ranking['Envíos_Entregados_Tiempo'] / ranking['Envíos_Realizados']) * 100).round(1)
ranking['Rendimiento_Km_Litro'] = (ranking['Kilómetros_Recorridos'] / ranking['Combustible_Litros']).round(2)
ranking['Costo_por_Km'] = (ranking['Costo_Combustible'] / ranking['Kilómetros_Recorridos']).round(2)
ranking['Ranking'] = ranking['Calificación_Cliente'].apply(
    lambda x: '⭐⭐⭐⭐⭐' if x >= 4.8 else '⭐⭐⭐⭐' if x >= 4.5 else '⭐⭐⭐' if x >= 4.0 else '⭐⭐' if x >= 3.5 else '⭐'
)
ranking = ranking.sort_values('Calificación_Cliente', ascending=False)

# ============================================
# HOJA 6: Analisis ABC del Inventario
# ============================================
print("[6/6] Creando Analisis ABC...")
inventario_abc = df_inventario[['SKU', 'Nombre_Producto', 'Categoría', 'Stock_Actual', 'Precio_Unitario', 'Valor_Inventario']].copy()
inventario_abc = inventario_abc.sort_values('Valor_Inventario', ascending=False)
inventario_abc['%_del_Valor_Total'] = ((inventario_abc['Valor_Inventario'] / inventario_abc['Valor_Inventario'].sum()) * 100).round(2)
inventario_abc['%_Acumulado'] = (inventario_abc['%_del_Valor_Total'].cumsum()).round(1)

def clasificar_abc(porcentaje):
    if porcentaje <= 80:
        return 'A - Control Estricto'
    elif porcentaje <= 95:
        return 'B - Control Moderado'
    else:
        return 'C - Control Basico'

inventario_abc['Clasificacion_ABC'] = inventario_abc['%_Acumulado'].apply(clasificar_abc)

# ============================================
# HOJA 7: Indicadores Mensuales
# ============================================
print("[Bonus] Creando Indicadores Mensuales...")
mensual = df_rendimiento.groupby('Mes').agg({
    'Envíos_Realizados': 'sum',
    'Envíos_Entregados_Tiempo': 'sum',
    'Costo_Combustible': 'sum',
    'Incidentes_Reportados': 'sum',
    'Calificación_Cliente': 'mean'
}).round(2)
mensual['%_Entrega_a_Tiempo'] = ((mensual['Envíos_Entregados_Tiempo'] / mensual['Envíos_Realizados']) * 100).round(1)
mensual = mensual.sort_values('Envíos_Realizados', ascending=False)

# ============================================
# HOJA 8: Alertas de Stock (Bajo/Critico)
# ============================================
print("[Bonus] Creando Alertas de Stock...")
alertas = df_inventario[df_inventario['Estado_Stock'].isin(['Bajo', 'Crítico'])][
    ['SKU', 'Nombre_Producto', 'Categoría', 'Stock_Actual', 'Stock_Mínimo', 'Stock_Máximo', 'Estado_Stock', 'Ubicación_Almacén', 'Proveedor_Principal']
].copy()
alertas['Recomendacion'] = alertas['Estado_Stock'].apply(
    lambda x: 'REABASTECER URGENTE' if x == 'Crítico' else 'Programar reabastecimiento'
)

# ============================================
# GUARDAR TODO EN EXCEL
# ============================================
print("\n" + "=" * 60)
print("GUARDANDO EN EXCEL...")
print("=" * 60)

with pd.ExcelWriter('Logistica_Analisis_Completo.xlsx', engine='openpyxl') as writer:
    resumen.to_excel(writer, sheet_name='1_Resumen_Ejecutivo', index=False)
    rentabilidad.to_excel(writer, sheet_name='2_Rentabilidad_Producto')
    eficiencia_almacen.to_excel(writer, sheet_name='3_Eficiencia_Almacen')
    eficiencia_envio.to_excel(writer, sheet_name='4_Eficiencia_Envios')
    ranking.to_excel(writer, sheet_name='5_Ranking_Transportistas')
    inventario_abc.to_excel(writer, sheet_name='6_Analisis_ABC', index=False)
    mensual.to_excel(writer, sheet_name='7_Indicadores_Mensuales')
    alertas.to_excel(writer, sheet_name='8_Alertas_Stock', index=False)

print("\n" + "=" * 60)
print("ARCHIVO CREADO: Logistica_Analisis_Completo.xlsx")
print("=" * 60)
print("\nHojas generadas:")
print("   1. Resumen_Ejecutivo        - KPIs principales")
print("   2. Rentabilidad_Producto    - Ganancias por tipo de producto")
print("   3. Eficiencia_Almacen       - Tiempos de entrega por almacen")
print("   4. Eficiencia_Envios        - Costo por Kg por zona")
print("   5. Ranking_Transportistas   - Metricas completas con estrellas")
print("   6. Analisis_ABC             - Clasificacion del inventario")
print("   7. Indicadores_Mensuales    - Rendimiento mes a mes")
print("   8. Alertas_Stock            - Productos que necesitan atencion")
print("\nTOTAL: 8 hojas de analisis profesional!")