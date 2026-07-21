import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Configuración de la página
# --------------------------------------------------

st.set_page_config(
    page_title="Vehicle Sales Dashboard",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------------------------
# Cargar datos
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("data/vehicles_us.csv")
    return df


df = load_data()

# --------------------------------------------------
# Título
# --------------------------------------------------

st.title("🚗 Used Vehicle Sales Dashboard")

st.markdown("""
Explora anuncios de vehículos usados en Estados Unidos mediante gráficos interactivos.
Utiliza los filtros del panel lateral para actualizar toda la información del dashboard.
""")

st.divider()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Filtros")

model = st.sidebar.multiselect(
    "Modelo",
    sorted(df["model"].dropna().unique()),
    default=sorted(df["model"].dropna().unique())
)

vehicle_type = st.sidebar.multiselect(
    "Tipo de vehículo",
    sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

fuel = st.sidebar.multiselect(
    "Combustible",
    sorted(df["fuel"].dropna().unique()),
    default=sorted(df["fuel"].dropna().unique())
)

filtered_df = df[
    (df["manufacturer"].isin(manufacturer)) &
    (df["type"].isin(vehicle_type)) &
    (df["fuel"].isin(fuel))
]

# Si los filtros no devuelven datos
if filtered_df.empty:
    st.warning("No existen vehículos con esos filtros.")
    st.stop()

# --------------------------------------------------
# KPIs
# --------------------------------------------------

st.subheader("📊 General Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Vehicles",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "Average Price",
        f"${filtered_df['price'].mean():,.0f}"
    )

with col3:
    st.metric(
        "Average Mileage",
        f"{filtered_df['odometer'].mean():,.0f} mi"
    )

st.divider()

# --------------------------------------------------
# Mostrar datos
# --------------------------------------------------

if st.checkbox("Show filtered dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# Histograma de precios
# --------------------------------------------------

st.subheader("💰 Vehicle Price Distribution")

bins = st.slider(
    "Number of bins",
    min_value=10,
    max_value=80,
    value=30
)

fig = px.histogram(
    filtered_df,
    x="price",
    nbins=bins,
    color_discrete_sequence=["royalblue"],
    marginal="box",
    opacity=0.85
)

fig.update_layout(
    title="Distribution of Vehicle Prices",
    xaxis_title="Price ($)",
    yaxis_title="Number of Vehicles",
    template="plotly_white"
)

st.plotly_chart(
    fig,
    use_container_width=True
)