import pandas as pd
import numpy as np

print("=" * 60)
print("ACTUALIZANDO EXCEL CON TABLAS DE ANALISIS AVANZADO")
print("=" * 60)

# Cargar datos originales del Excel
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

# Calcular métricas base
total_ordenes = len(df_ordenes)
ordenes_entregadas = len(df_ordenes[df_ordenes['Estado'] == 'Entregado'])
total_gastado = df_ordenes['Costo_Total'].sum()
valor_inventario = df_inventario['Valor_Inventario'].sum()
costo_envios = df_envios['Costo_Envío'].sum()
total_envios = len(df_envios)

print("✅ Datos cargados correctamente")
print(f"   Órdenes: {total_ordenes}")
print(f"   Productos: {len(df_inventario)}")
print(f"   Envíos: {total_envios}")
print(f"   Transportistas: {df_rendimiento['Transportista'].nunique()}")

# Cargar Excel existente para preservar las 8 hojas que ya tenemos
print("\nCargando hojas existentes...")
with pd.ExcelFile('Logistica_Analisis_Completo.xlsx') as xls:
    hojas_existentes = {sheet: pd.read_excel(xls, sheet_name=sheet) 
                        for sheet in xls.sheet_names}

print(f"   Hojas existentes: {list(hojas_existentes.keys())}")

# ============================================
# HOJA 9: Matriz de Correlaciones
# ============================================
print("\n[1/5] Creando Matriz de Correlaciones...")

# Seleccionar variables numéricas
variables = ['Cantidad', 'Costo_Unitario', 'Costo_Total', 'Tiempo_Entrega_Días']
corr_data = df_ordenes[variables].corr()

# Redondear y formatear
corr_df = corr_data.round(3).reset_index()
corr_df.columns = ['Variable'] + list(corr_data.columns)

print(f"   Variables analizadas: {variables}")
print(f"   Correlación más alta: {corr_data.abs().unstack().sort_values(ascending=False).iloc[1]:.3f}")

# ============================================
# HOJA 10: Estadísticas Descriptivas por Producto
# ============================================
print("\n[2/5] Creando Estadísticas Descriptivas...")

estadisticas = df_ordenes.groupby('Producto').agg({
    'Cantidad': ['count', 'mean', 'std', 'min', 'max'],
    'Costo_Unitario': ['mean', 'std'],
    'Costo_Total': ['sum', 'mean', 'std'],
    'Tiempo_Entrega_Días': ['mean', 'std']
}).round(2)

# Aplanar nombres de columnas
estadisticas.columns = ['Cant_N', 'Cant_Media', 'Cant_Std', 'Cant_Min', 'Cant_Max',
                        'CostoUnit_Media', 'CostoUnit_Std',
                        'CostoTotal_Suma', 'CostoTotal_Media', 'CostoTotal_Std',
                        'Tiempo_Media', 'Tiempo_Std']

print(f"   Productos analizados: {len(estadisticas)}")

# ============================================
# HOJA 11: Análisis de Varianza por Estado
# ============================================
print("\n[3/5] Creando Análisis de Varianza...")

varianza = df_ordenes.groupby('Estado').agg({
    'Costo_Total': ['count', 'sum', 'mean', 'std', 'min', 'max']
}).round(2)

varianza.columns = ['N', 'Suma_Total', 'Media', 'Desv_Estandar', 'Minimo', 'Maximo']

print(f"   Estados analizados: {len(varianza)}")

# ============================================
# HOJA 12: Análisis Pareto (Regla 80/20)
# ============================================
print("\n[4/5] Creando Análisis Pareto...")

pareto = df_ordenes.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).reset_index()
pareto['%_del_Total'] = (pareto['Costo_Total'] / pareto['Costo_Total'].sum() * 100).round(2)
pareto['%_Acumulado'] = pareto['%_del_Total'].cumsum().round(2)

# Clasificación ABC
def clasificar_pareto(porcentaje):
    if porcentaje <= 80:
        return 'A - Vital (80% del valor)'
    elif porcentaje <= 95:
        return 'B - Importante (15% del valor)'
    else:
        return 'C - Complementario (5% del valor)'

pareto['Clasificacion'] = pareto['%_Acumulado'].apply(clasificar_pareto)

print(f"   Proveedores Clase A: {len(pareto[pareto['Clasificacion'].str.contains('A')])}")
print(f"   Proveedores Clase B: {len(pareto[pareto['Clasificacion'].str.contains('B')])}")
print(f"   Proveedores Clase C: {len(pareto[pareto['Clasificacion'].str.contains('C')])}")

# ============================================
# HOJA 13: Indicadores KPI
# ============================================
print("\n[5/5] Creando Indicadores KPI...")

# Calcular métricas
tasa_entrega = ordenes_entregadas / total_ordenes * 100
costo_por_orden = total_gastado / total_ordenes
envios_por_transportista = total_envios / df_rendimiento['Transportista'].nunique()
tiempo_promedio = df_ordenes['Tiempo_Entrega_Días'].mean()
satisfaccion = df_rendimiento['Calificación_Cliente'].mean()

kpis = pd.DataFrame({
    'Indicador': [
        'OTIF (On Time In Full)',
        'Costo por Orden Promedio',
        'Costo Envio por Orden',
        'Productividad Transportista',
        'Tiempo Promedio Entrega',
        'Satisfaccion Cliente',
        'Tasa Entrega Exitosa',
        'Total Ordenes',
        'Total Envios',
        'Valor Inventario'
    ],
    'Valor_Actual': [
        f"{tasa_entrega:.1f}%",
        f"${costo_por_orden:,.2f}",
        f"${costo_envios/total_envios:,.2f}",
        f"{envios_por_transportista:.1f} envios/transp",
        f"{tiempo_promedio:.1f} dias",
        f"{satisfaccion:.2f}/5.0",
        f"{tasa_entrega:.1f}%",
        f"{total_ordenes}",
        f"{total_envios}",
        f"${valor_inventario:,.2f}"
    ],
    'Meta': [
        '≥ 85%',
        '≤ $150,000',
        '≤ $1,000',
        '≥ 15 envios',
        '≤ 7 dias',
        '≥ 4.5',
        '≥ 80%',
        '-',
        '-',
        '-'
    ],
    'Estado': [
        '⚠️ Alerta' if tasa_entrega < 85 else '✅ OK',
        '⚠️ Alerta' if costo_por_orden > 150000 else '✅ OK',
        '⚠️ Alerta' if costo_envios/total_envios > 1000 else '✅ OK',
        '⚠️ Alerta' if envios_por_transportista < 15 else '✅ OK',
        '⚠️ Alerta' if tiempo_promedio > 7 else '✅ OK',
        '⚠️ Alerta' if satisfaccion < 4.5 else '✅ OK',
        '⚠️ Alerta' if tasa_entrega < 80 else '✅ OK',
        '-',
        '-',
        '-'
    ]
})

print(f"   KPIs en alerta: {len(kpis[kpis['Estado'].str.contains('Alerta')])}")
print(f"   KPIs OK: {len(kpis[kpis['Estado'].str.contains('OK')])}")

# ============================================
# GUARDAR TODAS LAS HOJAS (existentes + nuevas)
# ============================================
print("\n" + "=" * 60)
print("GUARDANDO EN EXCEL...")
print("=" * 60)

with pd.ExcelWriter('Logistica_Analisis_Completo.xlsx', engine='openpyxl') as writer:
    
    # PRIMERO: Guardar las 8 hojas existentes
    print("\nGuardando hojas existentes...")
    for nombre, df in hojas_existentes.items():
        df.to_excel(writer, sheet_name=nombre, index=False)
        print(f"   ✅ {nombre}")
    
    # DESPUÉS: Guardar las 5 hojas nuevas
    print("\nGuardando hojas nuevas...")
    corr_df.to_excel(writer, sheet_name='9_Correlaciones', index=False)
    print("   ✅ 9_Correlaciones")
    
    estadisticas.to_excel(writer, sheet_name='10_Estadisticas')
    print("   ✅ 10_Estadisticas")
    
    varianza.to_excel(writer, sheet_name='11_Varianza')
    print("   ✅ 11_Varianza")
    
    pareto.to_excel(writer, sheet_name='12_Pareto_Proveedores', index=False)
    print("   ✅ 12_Pareto_Proveedores")
    
    kpis.to_excel(writer, sheet_name='13_KPIs', index=False)
    print("   ✅ 13_KPIs")

print("\n" + "=" * 60)
print("✅ EXCEL ACTUALIZADO: Logistica_Analisis_Completo.xlsx")
print("=" * 60)
print("\nHojas totales: 13")
print("   1-8: Hojas originales (Resumen, Rentabilidad, etc.)")
print("   9: Correlaciones")
print("   10: Estadísticas Descriptivas")
print("   11: Varianza por Estado")
print("   12: Pareto de Proveedores")
print("   13: KPIs con metas")
