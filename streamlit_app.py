import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================
# CONFIGURAR PÁGINA
# ============================================
st.set_page_config(
    page_title="Dashboard Logística",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# TÍTULO PRINCIPAL
# ============================================
st.title("📦 Dashboard de Logística")
st.markdown("---")

# ============================================
# CARGAR DATOS
# ============================================
@st.cache_data
def cargar_datos():
    df_ordenes = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Órdenes_Compra')
    df_inventario = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Inventario_Almacén')
    df_envios = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Envíos_Entregas')
    df_rendimiento = pd.read_excel('Logistica_Datos.xlsx', sheet_name='Rendimiento_Transportistas')
    return df_ordenes, df_inventario, df_envios, df_rendimiento

df_ordenes, df_inventario, df_envios, df_rendimiento = cargar_datos()

# ============================================
# BARRA LATERAL - FILTROS
# ============================================
st.sidebar.header("🔍 Filtros")

# Filtro por estado
estados = st.sidebar.multiselect(
    "Estado de Orden:",
    options=df_ordenes['Estado'].unique(),
    default=df_ordenes['Estado'].unique()
)

# Filtro por producto
productos = st.sidebar.multiselect(
    "Producto:",
    options=df_ordenes['Producto'].unique(),
    default=df_ordenes['Producto'].unique()
)

# Filtro por almacén
almacenes = st.sidebar.multiselect(
    "Almacén:",
    options=df_ordenes['Almacén_Destino'].unique(),
    default=df_ordenes['Almacén_Destino'].unique()
)

# Aplicar filtros
df_filtrado = df_ordenes[
    (df_ordenes['Estado'].isin(estados)) &
    (df_ordenes['Producto'].isin(productos)) &
    (df_ordenes['Almacén_Destino'].isin(almacenes))
]

# ============================================
# KPIs EN LA PARTE SUPERIOR
# ============================================
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="💰 Total Gastado",
        value=f"${df_filtrado['Costo_Total'].sum():,.0f}"
    )

with col2:
    st.metric(
        label="📦 Total Órdenes",
        value=f"{len(df_filtrado)}"
    )

with col3:
    st.metric(
        label="✅ Entregadas",
        value=f"{len(df_filtrado[df_filtrado['Estado']=='Entregado'])}"
    )

with col4:
    st.metric(
        label="📊 Valor Inventario",
        value=f"${df_inventario['Valor_Inventario'].sum():,.0f}"
    )

with col5:
    st.metric(
        label="⭐ Calificación",
        value=f"{df_rendimiento['Calificación_Cliente'].mean():.2f}"
    )

st.markdown("---")

# ============================================
# GRÁFICAS EN DOS COLUMNAS
# ============================================
col_izq, col_der = st.columns(2)

# --- Gráfica 1: Órdenes por Estado ---
with col_izq:
    st.subheader("📊 Órdenes por Estado")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    estado_counts = df_filtrado['Estado'].value_counts()
    colores = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#9b59b6']
    ax.pie(estado_counts.values, labels=estado_counts.index, 
           autopct='%1.1f%%', colors=colores[:len(estado_counts)], 
           startangle=90)
    st.pyplot(fig)

# --- Gráfica 2: Top Proveedores ---
with col_der:
    st.subheader("🏢 Top Proveedores por Gasto")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    top_prov = df_filtrado.groupby('Proveedor')['Costo_Total'].sum().sort_values(ascending=False).head(5)
    ax.barh(range(len(top_prov)), top_prov.values, color='#3498db')
    ax.set_yticks(range(len(top_prov)))
    ax.set_yticklabels(top_prov.index, fontsize=9)
    ax.set_xlabel('Costo Total ($)')
    ax.grid(axis='x', alpha=0.3)
    st.pyplot(fig)

st.markdown("---")

# ============================================
# SEGUNDA FILA DE GRÁFICAS
# ============================================
col_izq2, col_der2 = st.columns(2)

# --- Gráfica 3: Estado del Inventario ---
with col_izq2:
    st.subheader("📦 Estado del Inventario")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    stock_counts = df_inventario['Estado_Stock'].value_counts()
    colores_stock = ['#2ecc71', '#f39c12', '#e74c3c']
    ax.pie(stock_counts.values, labels=stock_counts.index, 
           autopct='%1.1f%%', colors=colores_stock[:len(stock_counts)], 
           startangle=90)
    st.pyplot(fig)

# --- Gráfica 4: Costo de Envíos por Zona ---
with col_der2:
    st.subheader("🚚 Costo de Envíos por Zona")
    
    fig, ax = plt.subplots(figsize=(8, 5))
    env_zona = df_envios.groupby('Zona_Destino')['Costo_Envío'].sum().sort_values(ascending=False)
    ax.bar(env_zona.index, env_zona.values, 
           color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'])
    ax.set_ylabel('Costo Total ($)')
    ax.grid(axis='y', alpha=0.3)
    st.pyplot(fig)

st.markdown("---")

# ============================================
# TABLA DE DATOS FILTRADOS
# ============================================
st.subheader("📋 Órdenes Filtradas")
st.dataframe(df_filtrado[['ID_Orden', 'Producto', 'Proveedor', 'Cantidad', 
                          'Costo_Total', 'Estado', 'Almacén_Destino']], 
             use_container_width=True)

# ============================================
# DESCARGAR REPORTE
# ============================================
st.markdown("---")
st.subheader("📥 Descargar Reporte")

csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Descargar CSV de órdenes filtradas",
    data=csv,
    file_name='ordenes_filtradas.csv',
    mime='text/csv'
)

st.success("✅ Dashboard actualizado con los filtros seleccionados")