import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Carnot Cycle P–V Diagram (Helium)")

# Constants
R = 8.314  # J/(mol*K)
gamma = 5/3  # monatomic gas
n = 1.0

# Inputs (optional sliders so users can change system)
T_H = st.number_input(
    "Hot Reservoir Temperature (K)",
    min_value=1.0,
    max_value=5000.0,
    value=800.0,
    step=10.0
)

T_C = st.number_input(
    "Cold Reservoir Temperature (K)",
    min_value=1.0,
    max_value=3000.0,
    value=300.0,
    step=10.0
)

V_A_L = st.number_input(
    "Initial Volume A (L)",
    min_value=0.001,
    max_value=100.0,
    value=1.0,
    step=0.1
)

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

import pandas as pd

# Ideal gas law: P = nRT / V
n = 1.0

# Define key state points
states = {
    "A (start)": {
        "T": T_H,
        "V": V_A,
    },
    "B (after isothermal expansion)": {
        "T": T_H,
        "V": V_B,
    },
    "C (after adiabatic expansion)": {
        "T": T_C,
        "V": V_C,
    },
    "D (after isothermal compression)": {
        "T": T_C,
        "V": V_D,
    }
}

# Compute pressures
for key in states:
    T = states[key]["T"]
    V = states[key]["V"]
    P = n * R * T / V
    states[key]["P"] = P

# Convert to DataFrame
df = pd.DataFrame(states).T
df = df[["T", "P", "V"]]

# Unit conversions for readability
df["P (kPa)"] = df["P"] / 1000
df["V (L)"] = df["V"] * 1000

# Drop raw SI columns if you want cleaner display
df = df[["T", "P (kPa)", "V (L)"]]

st.subheader("State Points (1 mol Ideal Gas)")
st.dataframe(df)
