from PIL import Image
import os

print("=" * 50)
print("CREANDO PDF CON TODAS LAS GRAFICAS")
print("=" * 50)

# Lista de graficas en orden
graficas = [
    'grafica1_ordenes_estado.png',
    'grafica2_proveedores.png',
    'grafica3_inventario.png',
    'grafica4_envios_zona.png',
    'grafica5_transportistas.png',
    'grafica6_dashboard.png',
    'grafica7_tendencia_ordenes.png',
    'grafica8_cantidad_vs_costo.png',
    'grafica9_envios_mes_estado.png',
    'grafica10_rentabilidad_producto.png',
    'grafica11_eficiencia_almacen.png',
    'grafica12_costo_kg_zona.png',
    'grafica13_ranking_transportistas.png',
    'grafica14_curva_abc.png',
    'grafica15_dashboard_ejecutivo.png'
]

# Verificar que existen
imagenes = []
for g in graficas:
    if os.path.exists(g):
        imagenes.append(Image.open(g).convert('RGB'))
        print(f"✅ {g}")
    else:
        print(f"❌ {g} - no encontrado")

if len(imagenes) > 0:
    # Guardar como PDF
    primera = imagenes[0]
    resto = imagenes[1:]
    
    primera.save(
        'Reporte_Logistica_Graficas.pdf',
        save_all=True,
        append_images=resto,
        resolution=150
    )
    
    print("\n" + "=" * 50)
    print("PDF CREADO: Reporte_Logistica_Graficas.pdf")
    print(f"Total de paginas: {len(imagenes)}")
    print("=" * 50)
else:
    print("No se encontraron graficas para convertir.")