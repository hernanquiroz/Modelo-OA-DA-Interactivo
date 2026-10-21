import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# ───────────────────────────────────────────────────────────────
# Configuración de la página
# ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Modelo OA-DA Interactivo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────────────────────
# Título y descripción
# ──────────────────────────────────────────────────────────────
st.title("📊 Oferta y Demanda Agregada (Interactivo)")
st.markdown("""
Desplaza las curvas de **Demanda Agregada (DA)** y **Oferta Agregada a Corto Plazo (OACP)** 
para analizar los efectos sobre el producto real y el nivel de precios.
""")

# ──────────────────────────────────────────────────────────────
# Parámetros base del modelo
# ──────────────────────────────────────────────────────────────
st.sidebar.header("️ Parámetros Base")

# Parámetros de la curva DA: P = a - b*Y
a_base = st.sidebar.number_input("Intercepto DA (a)", value=10.0, step=0.5)
b = st.sidebar.number_input("Pendiente DA (b)", value=0.7, step=0.1)

# Parámetros de la curva OA: P = c + d*Y
c_base = st.sidebar.number_input("Intercepto OA (c)", value=1.0, step=0.5)
d = st.sidebar.number_input("Pendiente OA (d)", value=0.7, step=0.1)

st.sidebar.markdown("---")

# ───────────────────────────────────────────────────────────────
# Sliders de desplazamiento
# ──────────────────────────────────────────────────────────────
st.sidebar.header(" Desplazamientos de Curvas")

# Desplazamiento de DA
delta_DA = st.sidebar.slider(
    "Desplazamiento DA (Δ)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

# Desplazamiento de OA
delta_OA = st.sidebar.slider(
    "Desplazamiento OA (Δ)",
    min_value=-5.0,
    max_value=5.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Leyenda:**")
st.sidebar.info("Δ positivo = desplazamiento derecha/arriba\n\nΔ negativo = desplazamiento izquierda/abajo")

# ───────────────────────────────────────────────────────────────
# Calcular curvas con desplazamientos
# ──────────────────────────────────────────────────────────────
Y = np.linspace(0, 10, 100)

# Curva DA: P = (a + delta_DA) - b*Y
# Un delta positivo desplaza DA hacia la derecha
P_DA = (a_base + delta_DA) - b * Y

# Curva OA: P = (c + delta_OA) + d*Y
# Un delta positivo desplaza OA hacia arriba/izquierda
P_OA = (c_base + delta_OA) + d * Y

# ───────────────────────────────────────────────────────────────
# Calcular punto de equilibrio
# ──────────────────────────────────────────────────────────────
# En equilibrio: DA = OA
# (a + delta_DA) - b*Y = (c + delta_OA) + d*Y
# Y* = [(a + delta_DA) - (c + delta_OA)] / (b + d)

a_actual = a_base + delta_DA
c_actual = c_base + delta_OA

Y_eq = (a_actual - c_actual) / (b + d)
P_eq = a_actual - b * Y_eq  # o también: P_eq = c_actual + d * Y_eq

# Calcular equilibrio original para comparación
Y_original = (a_base - c_base) / (b + d)
P_original = a_base - b * Y_original

# ──────────────────────────────────────────────────────────────
# Mostrar métricas de equilibrio
# ──────────────────────────────────────────────────────────────
st.markdown("###  Punto de Equilibrio Actual")
col1, col2 = st.columns(2)

with col1:
    delta_Y = Y_eq - Y_original
    st.metric(
        label="Producto Real de Equilibrio (Y*)",
        value=f"{Y_eq:.2f}",
        delta=f"{delta_Y:+.2f} {'↑' if delta_Y > 0.01 else '↓' if delta_Y < -0.01 else '→'}"
    )

with col2:
    delta_P = P_eq - P_original
    st.metric(
        label="Nivel de Precios de Equilibrio (P*)",
        value=f"{P_eq:.2f}",
        delta=f"{delta_P:+.2f} {'↑' if delta_P > 0.01 else '↓' if delta_P < -0.01 else '→'}"
    )

# ───────────────────────────────────────────────────────────────
# Crear la gráfica
# ─────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 7))

# Grid
ax.grid(True, linestyle='--', alpha=0.7)
ax.set_axisbelow(True)

# Curva DA
color_DA = 'blue'
ax.plot(Y, P_DA, color=color_DA, linewidth=2.5, 
        label=f'Demanda Agregada (DA) [Δ={delta_DA:+.1f}]')

# Curva OA
color_OA = 'red'
ax.plot(Y, P_OA, color=color_OA, linewidth=2.5, 
        label=f'Oferta Agregada (OACP) [Δ={delta_OA:+.1f}]')

# Punto de equilibrio
ax.plot(Y_eq, P_eq, 'ko', markersize=10, markeredgecolor='black', 
        markerfacecolor='gold', markeredgewidth=2, zorder=5)

# Etiquetas del punto de equilibrio
ax.annotate(f'Equilibrio\n(Y={Y_eq:.1f}, P={P_eq:.1f})', 
            xy=(Y_eq, P_eq), 
            xytext=(Y_eq + 0.8, P_eq + 0.5),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# Configuración de ejes
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('Producto Real (Y)', fontsize=12, fontweight='bold')
ax.set_ylabel('Nivel de Precios (P)', fontsize=12, fontweight='bold')
ax.set_title('Oferta y Demanda Agregada (Interactivo)', 
             fontsize=14, fontweight='bold', pad=20)

# Leyenda
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

# Líneas punteadas desde el equilibrio
ax.axhline(y=P_eq, color='gray', linestyle=':', alpha=0.5)
ax.axvline(x=Y_eq, color='gray', linestyle=':', alpha=0.5)

plt.tight_layout()

# ───────────────────────────────────────────────────────────────
# Mostrar gráfica en Streamlit
# ──────────────────────────────────────────────────────────────
st.pyplot(fig)

# ───────────────────────────────────────────────────────────────
# Análisis de políticas
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🔍 Análisis de Políticas Económicas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Demanda Agregada (DA)**")
    if delta_DA > 0:
        st.success(f"""
        **✅ Expansión de DA** ({delta_DA:+.1f})
        
        **Causas:**
        - ↑ Gasto público
        - ↓ Impuestos
        - ↑ Consumo
        - ↑ Inversión
        - ↑ Exportaciones netas
        
        **Efectos:**
        - ↑ Producto Real (Y)
        - ↑ Nivel de Precios (P)
        """)
    elif delta_DA < 0:
        st.error(f"""
        **⬇️ Contracción de DA** ({delta_DA:+.1f})
        
        **Causas:**
        - ↓ Gasto público
        - ↑ Impuestos
        - ↓ Consumo
        - ↓ Inversión
        
        **Efectos:**
        - ↓ Producto Real (Y)
        - ↓ Nivel de Precios (P)
        """)
    else:
        st.info("➡️ DA en posición original")

with col2:
    st.markdown("**Oferta Agregada (OACP)**")
    if delta_OA > 0:
        st.error(f"""
        **️ Shock negativo de oferta** ({delta_OA:+.1f})
        
        **Causas:**
        - ↑ Precios de materias primas
        - ↑ Salarios
        - Desastres naturales
        - ↑ Impuestos indirectos
        
        **Efectos:**
        - ↓ Producto Real (Y)
        - ↑ Nivel de Precios (P)
        - **Estanflación**
        """)
    elif delta_OA < 0:
        st.success(f"""
        **✅ Shock positivo de oferta** ({delta_OA:+.1f})
        
        **Causas:**
        - ↓ Precios de petróleo
        - Avance tecnológico
        - ↓ Costos de producción
        - Mejora en productividad
        
        **Efectos:**
        - ↑ Producto Real (Y)
        - ↓ Nivel de Precios (P)
        """)
    else:
        st.info("➡️ OA en posición original")

# ───────────────────────────────────────────────────────────────
# Escenarios predefinidos
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎯 Escenarios Económicos Predefinidos")

scenario = st.selectbox(
    "Selecciona un escenario para analizar:",
    ["Selecciona...",
     "1. Expansión Fiscal",
     "2. Contracción Monetaria",
     "3. Shock Positivo de Oferta",
     "4. Shock Negativo de Oferta (Estanflación)",
     "5. Política Mixta Expansiva",
     "6. Recesión por Demanda"]
)

if scenario == "1. Expansión Fiscal":
    st.info("📈 **Expansión Fiscal:** Aumento del gasto público o reducción de impuestos")
    st.markdown("- DA se desplaza a la **derecha** (Δ = +2.0)")
    st.markdown("- OA permanece constante")
    st.markdown("- **Resultado:** ↑Y, ↑P")
    delta_DA_demo, delta_OA_demo = 2.0, 0.0
    
elif scenario == "2. Contracción Monetaria":
    st.warning("📉 **Contracción Monetaria:** Reducción de la oferta monetaria")
    st.markdown("- DA se desplaza a la **izquierda** (Δ = -2.0)")
    st.markdown("- OA permanece constante")
    st.markdown("- **Resultado:** ↓Y, ↓P")
    delta_DA_demo, delta_OA_demo = -2.0, 0.0
    
elif scenario == "3. Shock Positivo de Oferta":
    st.success("✅ **Shock Positivo:** Avance tecnológico o ↓ costos")
    st.markdown("- OA se desplaza hacia **abajo/derecha** (Δ = -2.0)")
    st.markdown("- DA permanece constante")
    st.markdown("- **Resultado:** ↑Y, ↓P (¡El mejor escenario!)")
    delta_DA_demo, delta_OA_demo = 0.0, -2.0
    
elif scenario == "4. Shock Negativo de Oferta (Estanflación)":
    st.error("⚠️ **Shock Negativo:** ↑ petróleo o desastre natural")
    st.markdown("- OA se desplaza hacia **arriba/izquierda** (Δ = +2.0)")
    st.markdown("- DA permanece constante")
    st.markdown("- **Resultado:** ↓Y, ↑P (**Estanflación**)")
    delta_DA_demo, delta_OA_demo = 0.0, 2.0
    
elif scenario == "5. Política Mixta Expansiva":
    st.success(" **Política Mixta:** Fiscal + Monetaria expansiva")
    st.markdown("- DA se desplaza a la **derecha** (Δ = +2.5)")
    st.markdown("- OA se desplaza **ligeramente abajo** (Δ = -0.5)")
    st.markdown("- **Resultado:** ↑↑Y, P estable")
    delta_DA_demo, delta_OA_demo = 2.5, -0.5
    
elif scenario == "6. Recesión por Demanda":
    st.error("📉 **Recesión:** Caída del consumo e inversión")
    st.markdown("- DA se desplaza fuertemente a la **izquierda** (Δ = -3.0)")
    st.markdown("- OA permanece constante")
    st.markdown("- **Resultado:** ↓↓Y, ↓P (Deflación)")
    delta_DA_demo, delta_OA_demo = -3.0, 0.0
    
else:
    delta_DA_demo, delta_OA_demo = None, None

if delta_DA_demo is not None:
    st.markdown(f"""
    **Aplica este escenario:** Usa los sliders con los valores:
    - Desplazamiento DA: **{delta_DA_demo:+.1f}**
    - Desplazamiento OA: **{delta_OA_demo:+.1f}**
    """)

# ───────────────────────────────────────────────────────────────
# Ecuaciones
# ──────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 📐 Ecuaciones del Modelo")

col1, col2 = st.columns(2)

with col1:
    st.latex(rf"\text{{DA: }} P = {a_actual:.1f} - {b}Y")

with col2:
    st.latex(rf"\text{{OA: }} P = {c_actual:.1f} + {d}Y")

st.markdown(f"""
**Punto de equilibrio actual:**
- Y* = {Y_eq:.2f}
- P* = {P_eq:.2f}

**Variación respecto al equilibrio original:**
- ΔY = {Y_eq - Y_original:+.2f}
- ΔP = {P_eq - P_original:+.2f}
""")
