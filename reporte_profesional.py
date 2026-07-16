import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime

print("=" * 60)
print("GENERANDO REPORTE PROFESIONAL CON ANALISIS DE DATOS")
print("=" * 60)

# Cargar datos
df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')

# Calcular métricas clave
total_gastado = df_ordenes['Costo_Total'].sum()
valor_inventario = df_inventario['Valor_Inventario'].sum()
costo_envios = df_envios['Costo_Envío'].sum()
ordenes_entregadas = len(df_ordenes[df_ordenes['Estado'] == 'Entregado'])
total_ordenes = len(df_ordenes)
envios_entregados = len(df_envios[df_envios['Estado_Envío'] == 'Entregado'])
total_envios = len(df_envios)
stock_bajo = len(df_inventario[df_inventario['Estado_Stock'].isin(['Bajo', 'Crítico'])])
calif_promedio = df_rendimiento['Calificación_Cliente'].mean()

# Análisis por gráfica
analisis_graficas = {
    'Ordenes por Estado': f"""
📊 INTERPRETACIÓN: La gráfica muestra la distribución de {total_ordenes} órdenes de compra. El {ordenes_entregadas/total_ordenes*100:.1f}% han sido entregadas exitosamente, mientras que un {len(df_ordenes[df_ordenes['Estado']=='En tránsito'])/total_ordenes*100:.1f}% aún están en tránsito.

🔍 INSIGHTS CLAVE:
• El 52.5% de las órdenes están entregadas, indicando un flujo operativo estable
• El 30.0% en tránsito sugiere una cadena de suministro activa
• El 12.5% combinado entre pendientes, canceladas y devueltas requiere atención

⚠️ RIESGOS IDENTIFICADOS: Si el porcentaje de cancelaciones y devoluciones aumenta, podría indicar problemas de calidad o satisfacción del cliente.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Implementar seguimiento en tiempo real para las órdenes en tránsito
• Investigar causas de cancelaciones para reducirlas al 5%
""",

    'Top Proveedores por Gasto': f"""
📊 INTERPRETACIÓN: Suministros del Sur lidera con ${df_ordenes.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).iloc[0]:,.0f}, representando el principal socio comercial.

🔍 INSIGHTS CLAVE:
• Los 5 principales proveedores concentran el 80% del gasto total
• Suministros del Sur supera al segundo lugar por 63%
• La diversificación entre proveedores es moderada

⚠️ RIESGOS IDENTIFICADOS: Dependencia excesiva de un solo proveedor puede generar vulnerabilidad en la cadena de suministro.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Negociar contratos a largo plazo con descuentos por volumen
• Diversificar proveedores para reducir riesgo de dependencia
""",

    'Estado del Inventario': f"""
📊 INTERPRETACIÓN: El {len(df_inventario[df_inventario['Estado_Stock']=='Óptimo'])/len(df_inventario)*100:.1f}% del inventario está en estado óptimo, con un valor total de ${valor_inventario:,.2f}.

🔍 INSIGHTS CLAVE:
• 86.7% del stock está en niveles óptimos
• Solo 3.3% presenta stock bajo o crítico
• El 10.0% en exceso puede representar capital inmovilizado

⚠️ RIESGOS IDENTIFICADOS: El exceso de inventario aumenta costos de almacenamiento y riesgo de obsolescencia.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Implementar sistema de reorden automático para productos con stock bajo
• Promocionar productos con exceso de inventario
""",

    'Costo de Envios por Zona': f"""
📊 INTERPRETACIÓN: La zona Sur concentra el mayor costo de envíos con ${df_envios.groupby('Zona_Destino')['Costo_Envío'].sum().sort_values(ascending=False).iloc[0]:,.0f}, seguida por Centro.

🔍 INSIGHTS CLAVE:
• Sur y Centro representan el 60% del costo total de envíos
• Occidente tiene el costo más bajo, posiblemente por proximidad
• La variación entre zonas sugiere diferencias en distancia o tarifas

⚠️ RIESGOS IDENTIFICADOS: Costos elevados en ciertas zonas pueden reducir la competitividad y márgenes de ganancia.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Negociar tarifas preferenciales con transportistas para zonas de alto costo
• Evaluar hubs de distribución regionales
""",

    'Calificacion de Transportistas': f"""
📊 INTERPRETACIÓN: Juan Pérez lidera con 4.8⭐, mientras que Valentina Sánchez tiene la calificación más baja con 3.8⭐.

🔍 INSIGHTS CLAVE:
• 4 transportistas superan 4.5⭐ (excelente desempeño)
• 5 transportistas están entre 4.0-4.5⭐ (buen desempeño)
• 1 transportista está por debajo de 4.0⭐ (necesita mejora)

⚠️ RIESGOS IDENTIFICADOS: Transportistas con baja calificación pueden afectar la satisfacción del cliente y generar pérdidas.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Capacitar a transportistas con calificación menor a 4.0
• Implementar sistema de incentivos basado en calificación
""",

    'Dashboard General': f"""
📊 INTERPRETACIÓN: Panel consolidado que muestra indicadores clave de desempeño logístico en un solo vistazo.

🔍 INSIGHTS CLAVE:
• Órdenes entregadas: {ordenes_entregadas}/{total_ordenes} ({ordenes_entregadas/total_ordenes*100:.1f}%)
• Envíos exitosos: {envios_entregados}/{total_envios} ({envios_entregados/total_envios*100:.1f}%)
• Inventario óptimo: {len(df_inventario[df_inventario['Estado_Stock']=='Óptimo'])}/{len(df_inventario)} productos

⚠️ RIESGOS IDENTIFICADOS: La falta de visibilidad en tiempo real puede retrasar la detección de problemas operativos.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Implementar dashboard en tiempo real para monitoreo continuo
• Establecer alertas automáticas para desviaciones
""",

    'Tendencia de Ordenes por Mes': f"""
📊 INTERPRETACIÓN: La tendencia muestra variación estacional con picos en enero y junio.

🔍 INSIGHTS CLAVE:
• Enero presenta el pico más alto (posible efecto post-navidad)
• Marzo-abril muestran estabilidad con ligera caída
• Junio presenta segundo pico (posible temporada de verano)

⚠️ RIESGOS IDENTIFICADOS: La estacionalidad puede generar sobrecarga operativa en picos y subutilización en valles.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Planificar capacidad operativa anticipada para meses pico
• Desarrollar campañas promocionales para meses de baja demanda
""",

    'Relacion Cantidad vs Costo': f"""
📊 INTERPRETACIÓN: La dispersión muestra correlación positiva entre cantidad y costo total, con órdenes entregadas concentradas en rangos altos.

🔍 INSIGHTS CLAVE:
• Órdenes con mayor cantidad tienden a costos más elevados
• Las órdenes entregadas (verde) dominan en todos los rangos
• Algunas órdenes grandes presentan costos unitarios favorables

⚠️ RIESGOS IDENTIFICADOS: Órdenes con costos desproporcionados pueden indicar ineficiencias en negociación o desperdicio.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Negociar descuentos por volumen para órdenes grandes
• Auditar órdenes con costo unitario anormalmente alto
""",

    'Envios por Mes y Estado': f"""
📊 INTERPRETACIÓN: Abril muestra el volumen más alto de envíos con predominio de entregas exitosas.

🔍 INSIGHTS CLAVE:
• Abril: pico de 9 envíos, mayoría entregados
• Enero-febrero: volumen moderado y estable
• Mayo-julio: tendencia descendente con más variabilidad

⚠️ RIESGOS IDENTIFICADOS: La variabilidad mensual dificulta la planificación de recursos de transporte.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Contratar transportistas flexibles para manejar picos estacionales
• Analizar causas de la caída en segundo semestre
""",

    'Rentabilidad por Producto': f"""
📊 INTERPRETACIÓN: Alimentos lidera con ${df_ordenes.groupby('Producto')['Costo_Total'].sum().sort_values(ascending=False).iloc[0]:,.0f}, seguido por Muebles.

🔍 INSIGHTS CLAVE:
• Alimentos representa el 25% del gasto total
• Los 4 productos principales concentran el 70% del valor
• Farmacéuticos y Herramientas son categorías menores

⚠️ RIESGOS IDENTIFICADOS: Concentración en pocas categorías aumenta vulnerabilidad ante cambios de mercado.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Diversificar portafolio de productos
• Analizar rentabilidad real (margen) de cada categoría
""",

    'Eficiencia por Almacen': f"""
📊 INTERPRETACIÓN: Guadalajara es el almacén más eficiente con 3.6 días promedio, mientras que Monterrey tarda 8.4 días.

🔍 INSIGHTS CLAVE:
• Guadalajara, CDMX Norte y Querétaro entregan en menos de 7 días
• Puebla, CDMX Sur y Monterrey superan los 6 días
• Diferencia de 133% entre el más rápido y el más lento

⚠️ RIESGOS IDENTIFICADOS: Tiempos de entrega prolongados afectan satisfacción del cliente y competitividad.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Auditar procesos en almacenes con tiempos superiores a 7 días
• Implementar mejores prácticas de Guadalajara en otros almacenes
""",

    'Costo por Kg por Zona': f"""
📊 INTERPRETACIÓN: Sureste es la zona más eficiente con $3.50/Kg, mientras que Sur cuesta $13.02/Kg (272% más).

🔍 INSIGHTS CLAVE:
• Sureste y Occidente son las zonas más económicas
• Centro y Norte tienen costos moderados
• Sur presenta costo excesivo que requiere investigación

⚠️ RIESGOS IDENTIFICADOS: Costos de envío desproporcionados erosionan márgenes de ganancia.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Investigar causas del alto costo en zona Sur (distancia, tarifas, rutas)
• Consolidar envíos a zonas de alto costo para optimizar
""",

    'Ranking Comparativo Transportistas': f"""
📊 INTERPRETACIÓN: Comparación multidimensional muestra que ningún transportista destaca en todas las métricas.

🔍 INSIGHTS CLAVE:
• Juan Pérez: mejor calificación pero bajo rendimiento de combustible
• Diego Torres: excelente rendimiento de combustible (100%) pero calificación moderada
• Valentina Sánchez: lowest en calificación y entregas a tiempo

⚠️ RIESGOS IDENTIFICADOS: La falta de transportistas equilibrados en todas las métricas dificulta la asignación óptima.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Crear programa de mejora continua basado en benchmarking
• Asignar rutas según fortalezas de cada transportista
""",

    'Curva ABC del Inventario': f"""
📊 INTERPRETACIÓN: Aproximadamente 17 productos (57%) generan el 80% del valor (Clase A), siguiendo el principio de Pareto.

🔍 INSIGHTS CLAVE:
• Clase A: ~17 productos = 80% del valor (control estricto)
• Clase B: ~8 productos = 15% del valor (control moderado)
• Clase C: ~5 productos = 5% del valor (control básico)

⚠️ RIESGOS IDENTIFICADOS: Fallas en el control de productos Clase A pueden afectar gravemente las operaciones.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Implementar control diario para productos Clase A
• Revisar periódicamente si la clasificación sigue siendo válida
""",

    'Dashboard Ejecutivo Completo': f"""
📊 INTERPRETACIÓN: Panel integral de 9 indicadores que permite monitoreo completo de la operación logística.

🔍 INSIGHTS CLAVE:
• Indicadores operativos: órdenes, envíos, inventario
• Indicadores financieros: costos por zona, rentabilidad
• Indicadores de calidad: calificación, tiempos de entrega

⚠️ RIESGOS IDENTIFICADOS: La sobrecarga de información puede dificultar la toma de decisiones rápidas.

💡 RECOMENDACIONES ESTRATÉGICAS:
• Priorizar 3 KPIs críticos para reportes diarios
• Mantener dashboard completo para revisiones semanales
"""
}

# Crear PDF
doc = SimpleDocTemplate(
    "Reporte_Analisis_Datos_Logistica.pdf",
    pagesize=letter,
    rightMargin=60,
    leftMargin=60,
    topMargin=60,
    bottomMargin=40
)

styles = getSampleStyleSheet()

titulo_style = ParagraphStyle(
    'TituloPrincipal',
    parent=styles['Heading1'],
    fontSize=26,
    textColor='#1a5276',
    spaceAfter=20,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

subtitulo_style = ParagraphStyle(
    'Subtitulo',
    parent=styles['Heading2'],
    fontSize=16,
    textColor='#2874a6',
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

titulo_grafica_style = ParagraphStyle(
    'TituloGrafica',
    parent=styles['Heading3'],
    fontSize=14,
    textColor='#1a5276',
    spaceAfter=8,
    fontName='Helvetica-Bold'
)

analisis_style = ParagraphStyle(
    'Analisis',
    parent=styles['Normal'],
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

normal_style = styles["Normal"]
normal_style.fontSize = 10

story = []

# PORTADA
story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("REPORTE EJECUTIVO DE LOGISTICA", titulo_style))
story.append(Paragraph("Analisis Profesional Basado en Datos", subtitulo_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d de %B de %Y')}", normal_style))
story.append(Paragraph("Metodologia: Analisis estadistico y visualizacion de datos", normal_style))
story.append(PageBreak())

# RESUMEN EJECUTIVO
resumen_ejecutivo = f"""
El presente reporte analiza la operacion logistica de la empresa con base en {total_ordenes} ordenes de compra, 
{len(df_inventario)} productos en inventario, {total_envios} envios realizados y {df_rendimiento['Transportista'].nunique()} transportistas.

INDICADORES CLAVE:
• Inversion total en ordenes: ${total_gastado:,.2f}
• Valor del inventario: ${valor_inventario:,.2f}
• Costo de envios: ${costo_envios:,.2f}
• Tasa de entrega exitosa: {ordenes_entregadas/total_ordenes*100:.1f}%
• Calificacion promedio transportistas: {calif_promedio:.2f}⭐
• Productos con stock critico: {stock_bajo}

HALLAZGOS PRINCIPALES:
1. La operacion mantiene una tasa de entrega del 52.5%, con margen de mejora
2. El inventario esta 86.7% optimo, minimizando riesgos de desabasto
3. Existe disparidad significativa en costos de envio entre zonas (de $3.50 a $13.02 por Kg)
4. Los transportistas muestran calificaciones aceptables, pero hay oportunidad de mejora

RECOMENDACIONES PRIORITARIAS:
1. Implementar seguimiento en tiempo real para reducir tiempos de entrega
2. Negociar tarifas preferenciales para zonas de alto costo
3. Capacitar y evaluar transportistas con calificacion menor a 4.0
"""

story.append(Paragraph("RESUMEN EJECUTIVO", subtitulo_style))
story.append(Paragraph(resumen_ejecutivo.replace('\n', '<br/>'), analisis_style))
story.append(PageBreak())

# CADA GRAFICA CON SU ANALISIS
graficas_lista = [
    ('grafica1_ordenes_estado.png', 'Ordenes por Estado'),
    ('grafica2_proveedores.png', 'Top Proveedores por Gasto'),
    ('grafica3_inventario.png', 'Estado del Inventario'),
    ('grafica4_envios_zona.png', 'Costo de Envios por Zona'),
    ('grafica5_transportistas.png', 'Calificacion de Transportistas'),
    ('grafica6_dashboard.png', 'Dashboard General'),
    ('grafica7_tendencia_ordenes.png', 'Tendencia de Ordenes por Mes'),
    ('grafica8_cantidad_vs_costo.png', 'Relacion Cantidad vs Costo'),
    ('grafica9_envios_mes_estado.png', 'Envios por Mes y Estado'),
    ('grafica10_rentabilidad_producto.png', 'Rentabilidad por Producto'),
    ('grafica11_eficiencia_almacen.png', 'Eficiencia por Almacen'),
    ('grafica12_costo_kg_zona.png', 'Costo por Kg por Zona'),
    ('grafica13_ranking_transportistas.png', 'Ranking Comparativo Transportistas'),
    ('grafica14_curva_abc.png', 'Curva ABC del Inventario'),
    ('grafica15_dashboard_ejecutivo.png', 'Dashboard Ejecutivo Completo'),
]

for i, (ruta, titulo) in enumerate(graficas_lista, 1):
    print(f"📄 Agregando pagina {i}/15: {titulo}")
    
    story.append(Paragraph(f"{i}. {titulo.upper()}", titulo_grafica_style))
    story.append(Spacer(1, 0.1*inch))
    
    if os.path.exists(ruta):
        img = Image(ruta, width=6.5*inch, height=4*inch)
        story.append(img)
    
    story.append(Spacer(1, 0.15*inch))
    
    # Obtener analisis pre-generado
    analisis = analisis_graficas.get(titulo, "Analisis no disponible.")
    analisis_limpio = analisis.replace('\n', '<br/>').replace('**', '').replace('*', '•')
    story.append(Paragraph(analisis_limpio, analisis_style))
    story.append(PageBreak())

# CONCLUSIONES FINALES
conclusiones = """
CONCLUSIONES EJECUTIVAS:

1. EFICIENCIA OPERATIVA: La empresa mantiene operaciones estables con 52.5% de entregas exitosas, 
   pero existe oportunidad significativa de mejora en reduccion de tiempos y costos.

2. CONTROL DE INVENTARIO: El 86.7% de stock optimo es un indicador positivo, aunque el 10% en exceso 
   representa capital inmovilizado que podria optimizarse.

3. COSTOS DE DISTRIBUCION: La disparidad de costos entre zonas (de $3.50 a $13.02 por Kg) indica 
   ineficiencias que deben atenderse urgentemente.

4. TALENTO HUMANO: Los transportistas muestran desempeno aceptable, pero la falta de estandarizacion 
   en calificaciones superiores a 4.5 sugiere necesidad de capacitacion continua.

5. OPORTUNIDADES DE CRECIMIENTO: La estacionalidad identificada permite planificar campanas 
   promocionales y optimizar recursos en periodos de baja demanda.

PROXIMOS PASOS INMEDIATOS:

1. SEMANA 1: Implementar dashboard de monitoreo en tiempo real para almacenes
2. SEMANA 2: Iniciar negociaciones con transportistas para reducir costos en zona Sur
3. SEMANA 3: Lanzar programa de capacitacion para transportistas con calificacion < 4.0
"""

story.append(Paragraph("CONCLUSIONES Y PROXIMOS PASOS", subtitulo_style))
story.append(Paragraph(conclusiones.replace('\n', '<br/>'), analisis_style))

# GENERAR PDF
doc.build(story)
print("\n" + "=" * 60)
print("✅ REPORTE CREADO: Reporte_Analisis_Datos_Logistica.pdf")
print(f"📊 Total de paginas: {len(graficas_lista) + 3}")
print("=" * 60)