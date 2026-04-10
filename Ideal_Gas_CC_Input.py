# save as app_ideal.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Ideal Gas Carnot Cycle", layout="wide")
st.title("Ideal Gas Carnot Cycle Simulator")

# --- User inputs ---
st.sidebar.header("Gas Properties")
gas = st.sidebar.text_input("Gas name", "Ideal Gas")

st.sidebar.header("Cycle Temperatures")
Th = st.sidebar.number_input("Hot temperature (K)", min_value=0.1, value=500.0)
Tcold = st.sidebar.number_input("Cold temperature (K)", min_value=0.1, max_value=Th-0.1, value=300.0)

st.sidebar.header("Cycle Volumes")
V1_L = st.sidebar.number_input("Initial volume (L/mol)", min_value=0.001, value=1.0)
V2_L = st.sidebar.number_input("End hot isothermal volume (L/mol)", min_value=V1_L*1.01, value=3.0)

st.sidebar.header("Degrees of Freedom")
mol_type = st.sidebar.selectbox("Molecule type", ["monatomic", "linear", "nonlinear"])

# --- Convert units ---
V1 = V1_L * 1e-3
V2 = V2_L * 1e-3

# --- Constants ---
R = 8.314

if mol_type == "monatomic":
    f = 3
elif mol_type == "linear":
    f = 5
else:
    f = 6

Cv = (f/2) * R
Cp = Cv + R
gamma = Cp / Cv

# --- Ideal gas pressure ---
def pressure(T, V):
    return (R * T) / V

points = 300

# --- Hot isothermal expansion ---
V_hot = np.linspace(V1, V2, points)
P_hot = pressure(Th, V_hot)

# --- Adiabatic expansion ---
# TV^(gamma-1) = const
const1 = Th * (V2**(gamma - 1))
V_adiab1 = np.linspace(V2, V2*3, points)
T_adiab1 = const1 / (V_adiab1**(gamma - 1))

# find V3 where T = Tcold
V3 = (const1 / Tcold)**(1/(gamma - 1))
V_adiab1 = np.linspace(V2, V3, points)
T_adiab1 = const1 / (V_adiab1**(gamma - 1))
P_adiab1 = pressure(T_adiab1, V_adiab1)

# --- Cold isothermal compression ---
# find V4 using second adiabat
const2 = Tcold * (V3**(gamma - 1))
V4 = (const2 / Th)**(1/(gamma - 1))

V_cold = np.linspace(V3, V4, points)
P_cold = pressure(Tcold, V_cold)

# --- Adiabatic compression ---
V_adiab2 = np.linspace(V4, V1, points)
T_adiab2 = const2 / (V_adiab2**(gamma - 1))
P_adiab2 = pressure(T_adiab2, V_adiab2)

# --- Work calculations ---
W_hot    = np.trapezoid(P_hot, V_hot)
W_adiab1 = np.trapezoid(P_adiab1, V_adiab1)
W_cold   = np.trapezoid(P_cold, V_cold)
W_adiab2 = np.trapezoid(P_adiab2, V_adiab2)

W_net = W_hot + W_adiab1 + W_cold + W_adiab2

# Ideal Carnot efficiency (exact)
efficiency = 1 - (Tcold / Th)

# --- Plot ---
fig, ax = plt.subplots(figsize=(8,6))

ax.plot(V_hot*1e3, P_hot/1e3, 'r', label="Isothermal Expansion (Th)")
ax.plot(V_adiab1*1e3, P_adiab1/1e3, 'orange', label="Adiabatic Expansion")
ax.plot(V_cold*1e3, P_cold/1e3, 'b', label="Isothermal Compression (Tcold)")
ax.plot(V_adiab2*1e3, P_adiab2/1e3, 'g', label="Adiabatic Compression")

ax.set_xlabel("Volume (L/mol)")
ax.set_ylabel("Pressure (kPa)")
ax.set_title(f"Ideal Gas Carnot Cycle: {gas}")
ax.grid(True)
ax.legend()

st.pyplot(fig)
plt.close(fig)

# --- Summary ---
st.subheader("Cycle Summary")
st.write(f"Net Work = {W_net:.2f} J/mol")
st.write(f"Efficiency (numerical) ≈ {W_net/W_hot*100:.2f}%")
st.write(f"Efficiency (Carnot exact) = {efficiency*100:.2f}%")