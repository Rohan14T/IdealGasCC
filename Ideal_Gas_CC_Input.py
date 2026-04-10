import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Carnot Cycle P–V Diagram (Helium)")

# Constants
R = 8.314  # J/(mol*K)
gamma = 5/3  # monatomic gas
n = 1.0

# Inputs (optional sliders so users can change system)
T_H = st.slider("Hot Reservoir Temperature (K)", 400, 1000, 600)
T_C = st.slider("Cold Reservoir Temperature (K)", 200, 500, 300)

V_A_L = st.slider("Initial Volume A (L)", 0.5, 5.0, 1.0)

# Convert L → m^3
V_A = V_A_L * 1e-3

# --- Step 1: Isothermal expansion (A→B, T_H)
V_B = 2 * V_A
V1 = np.linspace(V_A, V_B, 100)
P1 = n * R * T_H / V1

# --- Step 2: Adiabatic expansion (B→C)
V_C = V_B * (T_H / T_C) ** (1 / (gamma - 1))
V2 = np.linspace(V_B, V_C, 100)
P2 = P1[-1] * (V_B / V2) ** gamma

# --- Step 3: Isothermal compression (C→D)
V_D = V_A * (T_H / T_C) ** (1 / (gamma - 1))
V3 = np.linspace(V_C, V_D, 100)
P3 = n * R * T_C / V3

# --- Step 4: Adiabatic compression (D→A)
V4 = np.linspace(V_D, V_A, 100)
P4 = P3[-1] * (V_D / V4) ** gamma

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(V1 * 1e3, P1 / 1e3, label="Isothermal Expansion (Th)")
ax.plot(V2 * 1e3, P2 / 1e3, label="Adiabatic Expansion")
ax.plot(V3 * 1e3, P3 / 1e3, label="Isothermal Compression (Tc)")
ax.plot(V4 * 1e3, P4 / 1e3, label="Adiabatic Compression")

ax.set_xlabel("Volume (L)")
ax.set_ylabel("Pressure (kPa)")
ax.set_title("Carnot Cycle P–V Diagram (Helium)")
ax.grid(True)
ax.legend()

st.pyplot(fig)
