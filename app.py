import streamlit as st
import math
import datetime

# Conversion functions (basic sample)
def convert_units(value, from_unit, to_unit):
    conversion_factors = {
        ("meters", "kilometers"): 0.001,
        ("kilometers", "meters"): 1000,
        ("grams", "kilograms"): 0.001,
        ("kilograms", "grams"): 1000,
        ("celsius", "fahrenheit"): lambda c: (c * 9 / 5) + 32,
        ("fahrenheit", "celsius"): lambda f: (f - 32) * 5 / 9,
    }
    key = (from_unit, to_unit)
    factor = conversion_factors.get(key)
    if callable(factor):
        return factor(value)
    elif factor:
        return value * factor
    else:
        return "Conversion not supported."

# Scientific Calculator
def scientific_calculator():
    st.subheader("Scientific Calculator")
    expression = st.text_input("Enter expression (e.g. 2+3*sqrt(4))")
    if expression:
        try:
            result = eval(expression, {"__builtins__": None, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan, "pi": math.pi, "log": math.log, "exp": math.exp})
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Formula Calculator
def formula_calculator():
    st.subheader("Formula Calculator")
    st.markdown("**Area of a Circle**: πr²")
    radius = st.number_input("Enter radius", min_value=0.0)
    if radius:
        st.success(f"Area: {math.pi * radius**2:.2f}")

# Physics Formula Solver
def physics_formula_solver():
    st.subheader("Physics Formula Solver")
    st.markdown("**Newton’s Second Law**: F = m × a")
    m = st.number_input("Enter mass (kg)")
    a = st.number_input("Enter acceleration (m/s²)")
    if m and a:
        st.success(f"Force: {m * a} N")

# Engineering Converter
def engineering_converter():
    st.subheader("Engineering Converter")
    st.markdown("**Power Conversion**: Watts ↔ Horsepower")
    power = st.number_input("Enter power")
    option = st.selectbox("Convert from", ["Watts to HP", "HP to Watts"])
    if option == "Watts to HP":
        st.success(f"{power} W = {power / 745.7:.4f} HP")
    else:
        st.success(f"{power} HP = {power * 745.7:.2f} W")

# Health & Fitness Tools
def health_fitness_tools():
    st.subheader("Health & Fitness Tools")
    st.markdown("**BMI Calculator**")
    height = st.number_input("Height (in meters)", min_value=0.0)
    weight = st.number_input("Weight (in kilograms)", min_value=0.0)
    if height > 0 and weight > 0:
        bmi = weight / (height ** 2)
        st.success(f"BMI: {bmi:.2f}")

# Conversion History & Bookmarks
def history_bookmarks():
    st.subheader("Conversion History & Bookmarks")
    st.markdown("📌 Feature coming soon — will include saved conversions and usage history.")

# Sidebar
st.sidebar.title("Choose Mode")
mode = st.sidebar.radio("Select Mode", [
    "Unit Converter", 
    "Formula Calculator",
    "Scientific Calculator", 
    "Physics Formula Solver",
    "Engineering Converter", 
    "Health & Fitness Tools",
    "Conversion History & Bookmarks"
])

# Main logic
st.title("🔬 Smart Unit Converter & Formula Calculator")

if mode == "Unit Converter":
    st.subheader("Unit Converter")
    value = st.number_input("Enter value to convert")
    from_unit = st.selectbox("From Unit", ["meters", "kilometers", "grams", "kilograms", "celsius", "fahrenheit"])
    to_unit = st.selectbox("To Unit", ["meters", "kilometers", "grams", "kilograms", "celsius", "fahrenheit"])
    if st.button("Convert"):
        result = convert_units(value, from_unit, to_unit)
        st.success(f"Converted Value: {result}")

elif mode == "Formula Calculator":
    formula_calculator()

elif mode == "Scientific Calculator":
    scientific_calculator()

elif mode == "Physics Formula Solver":
    physics_formula_solver()

elif mode == "Engineering Converter":
    engineering_converter()

elif mode == "Health & Fitness Tools":
    health_fitness_tools()

elif mode == "Conversion History & Bookmarks":
    history_bookmarks()
