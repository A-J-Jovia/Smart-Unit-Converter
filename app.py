import streamlit as st
import sympy as sp
import pandas as pd
from math import log10

# ------------------ UNIT CONVERSION DICTIONARY ------------------ #
unit_conversions = {
    'Length': {
        'meter': 1,
        'kilometer': 1000,
        'centimeter': 0.01,
        'inch': 0.0254,
        'foot': 0.3048,
        'mile': 1609.34
    },
    'Mass': {
        'kilogram': 1,
        'gram': 0.001,
        'pound': 0.453592,
        'ounce': 0.0283495
    },
    'Temperature': {
        'Celsius': lambda x: x,
        'Fahrenheit': lambda x: (x - 32) * 5 / 9,
        'Kelvin': lambda x: x - 273.15,
        'to_Celsius': {
            'Celsius': lambda x: x,
            'Fahrenheit': lambda x: (x - 32) * 5 / 9,
            'Kelvin': lambda x: x - 273.15
        },
        'from_Celsius': {
            'Celsius': lambda x: x,
            'Fahrenheit': lambda x: (x * 9 / 5) + 32,
            'Kelvin': lambda x: x + 273.15
        }
    },
    'Speed': {
        'm/s': 1,
        'km/h': 1 / 3.6,
        'mph': 0.44704,
        'ft/s': 0.3048,
        'knot': 0.514444
    },
    'Area': {
        'm²': 1,
        'cm²': 0.0001,
        'ft²': 0.092903,
        'in²': 0.00064516,
        'acre': 4046.86,
        'hectare': 10000
    },
    'Volume': {
        'm³': 1,
        'liter': 0.001,
        'milliliter': 0.000001,
        'gallon': 0.00378541,
        'pint': 0.000473176,
        'cup': 0.000236588
    },
    'Pressure': {
        'Pa': 1,
        'bar': 100000,
        'atm': 101325,
        'mmHg': 133.322,
        'psi': 6894.76
    },
    'Energy': {
        'joule': 1,
        'kilojoule': 1000,
        'calorie': 4.184,
        'kilocalorie': 4184,
        'BTU': 1055.06
    },
    'Time': {
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800,
        'year': 31536000
    },
    'Data Storage': {
        'bit': 1,
        'byte': 8,
        'KB': 8 * 1024,
        'MB': 8 * 1024 ** 2,
        'GB': 8 * 1024 ** 3,
        'TB': 8 * 1024 ** 4
    }
}

# ------------------ UNIT CONVERSION FUNCTION ------------------ #
def convert_units(value, from_unit, to_unit, unit_type):
    if unit_type == 'Temperature':
        to_c = unit_conversions['Temperature']['to_Celsius'][from_unit](value)
        return unit_conversions['Temperature']['from_Celsius'][to_unit](to_c)
    else:
        base = value * unit_conversions[unit_type][from_unit]
        return base / unit_conversions[unit_type][to_unit]

# ------------------ FORMULA CALCULATION ------------------ #
def calculate_formula(formula, variables):
    expr = sp.sympify(formula)
    substituted = expr.subs(variables)
    return substituted.evalf()

# Initialize history
if "history" not in st.session_state:
    st.session_state["history"] = []

# ------------------ STREAMLIT APP ------------------ #
st.set_page_config(page_title="Smart Unit Converter & Calculator", page_icon="🔢")
st.title("🔢 Smart Unit Converter & Multi-Mode Calculator")

st.sidebar.header("Choose Mode")
mode = st.sidebar.radio("Select Mode", [
    "Unit Converter", "Formula Calculator",
    "Scientific Calculator", "Physics Formula Solver",
    "Engineering Converter", "Health & Fitness Tools",
    "Conversion History & Bookmarks"
])

# ------------------ UNIT CONVERTER UI ------------------ #
if mode == "Unit Converter":
    st.header("📏 Unit Converter")
    unit_types = list(unit_conversions.keys())
    unit_type = st.selectbox("Choose Unit Type", unit_types)

    if unit_type == 'Temperature':
        units = list(unit_conversions['Temperature']['to_Celsius'].keys())
    else:
        units = list(unit_conversions[unit_type].keys())

    value = st.number_input("Enter value to convert:", format="%.6f")
    from_unit = st.selectbox("From Unit", units)
    to_unit = st.selectbox("To Unit", units)

    if st.button("Convert"):
        try:
            result = convert_units(value, from_unit, to_unit, unit_type)
            st.success(f"{value} {from_unit} = {result:.6f} {to_unit}")
            st.session_state["history"].append(("Unit Converter", f"{value} {from_unit}", f"{result:.6f} {to_unit}"))
        except Exception as e:
            st.error(f"Conversion error: {e}")

# ------------------ FORMULA CALCULATOR UI ------------------ #
elif mode == "Formula Calculator":
    st.header("📐 Formula Calculator")
    formula = st.text_input("Enter formula (e.g., F = m * a)")

    if "=" in formula:
        lhs, rhs = formula.split("=")
        try:
            expr = sp.sympify(rhs)
            variables = expr.free_symbols
            user_inputs = {}
            for var in variables:
                user_inputs[var] = st.number_input(f"Enter value for {var}:", format="%.4f")
            if st.button("Calculate"):
                result = calculate_formula(expr, user_inputs)
                st.success(f"{lhs.strip()} = {result:.4f}")
                st.session_state["history"].append(("Formula Calculator", formula.strip(), f"{lhs.strip()} = {result:.4f}"))
        except Exception as e:
            st.error(f"Error parsing formula: {e}")
    elif formula != "":
        st.warning("⚠️ Please use '=' to separate left-hand side and right-hand side.")

# ------------------ SCIENTIFIC CALCULATOR ------------------ #
elif mode == "Scientific Calculator":
    st.header("🔬 Scientific Calculator")
    expr_input = st.text_input("Enter expression (e.g., sin(pi/2) + log(10))")

    if expr_input:
        try:
            expr_parsed = sp.sympify(expr_input, evaluate=True)
            result = expr_parsed.evalf()
            st.success(f"Result: {result}")
            st.session_state["history"].append(("Scientific Calculator", expr_input, str(result)))
        except Exception as e:
            st.error(f"Error: {e}")

    st.caption("✅ Supported: sin, cos, tan, log, ln, exp, sqrt, factorial, pi, E, etc.")

# ------------------ PHYSICS FORMULA SOLVER ------------------ #
elif mode == "Physics Formula Solver":
    st.header("⚛️ Physics Formula Solver")

    if "history" not in st.session_state:
        st.session_state["history"] = []

    physics_formulas = {
        "Newton’s Second Law": "F = m * a",
        "Ohm’s Law": "V = I * R",
        "Kinetic Energy": "KE = 0.5 * m * v**2",
        "Gravitational Potential Energy": "PE = m * g * h",
        "Pressure": "P = F / A",
        "Work Done": "W = F * d",
        "Power": "P = W / t",
        "Momentum": "p = m * v",
        "Hooke's Law": "F = k * x",
        "Charge": "Q = I * t",
        "Coulomb's Law": "F = k * q1 * q2 / r**2",
        "Wave Speed": "v = f * λ",
        "Refractive Index": "n = c / v",
        "Ideal Gas Law": "P * V = n * R * T",
        "Einstein's Mass-Energy": "E = m * c**2",
    }

    choice = st.selectbox("Choose a Formula", list(physics_formulas.keys()))
    formula = physics_formulas[choice]
    st.latex(formula)

    # Split formula and get symbolic variables
    lhs, rhs = formula.split("=")
    lhs = lhs.strip()
    rhs = rhs.strip()

    try:
        expr = sp.sympify(rhs, evaluate=False)
    except Exception as e:
        st.error(f"Could not parse formula: {e}")
        st.stop()

    variables = list(expr.free_symbols)
    inputs = {}

    # Ask user for input
    for var in variables:
        val = st.number_input(f"Enter value for {var}", format="%.4f")
        inputs[var] = val

    if st.button("Solve"):
        try:
            result = expr.subs(inputs).evalf()
            st.success(f"{lhs} = {result:.4f}")
            st.session_state["history"].append(("Physics Formula Solver", formula, f"{lhs} = {result:.4f}"))
        except Exception as e:
            st.error(f"Error in calculation: {e}")

# ------------------ ENGINEERING CONVERSIONS DICTIONARY ------------------ #
engineering_conversions = {
    "Mechanical": {
        "Force": {
            "N": 1,
            "kN": 1e3,
            "lbf": 4.44822
        },
        "Torque": {
            "Nm": 1,
            "kNm": 1e3,
            "lbf·ft": 1.35582
        },
        "Pressure": {
            "Pa": 1,
            "kPa": 1e3,
            "MPa": 1e6,
            "psi": 6894.76,
            "bar": 1e5
        }
    },
    "Electrical": {
        "Voltage": {
            "V": 1,
            "kV": 1e3
        },
        "Current": {
            "A": 1,
            "mA": 1e-3,
            "μA": 1e-6
        },
        "Resistance": {
            "Ω": 1,
            "kΩ": 1e3,
            "MΩ": 1e6
        },
        "Capacitance": {
            "F": 1,
            "μF": 1e-6,
            "nF": 1e-9,
            "pF": 1e-12
        }
    },
    "Thermal": {
        "Energy": {
            "J": 1,
            "kJ": 1e3,
            "cal": 4.184,
            "BTU": 1055.06
        },
        "Power": {
            "W": 1,
            "kW": 1e3,
            "HP": 745.7
        }
    },
    "Fluid Mechanics": {
        "Flow Rate": {
            "m³/s": 1,
            "L/min": 1/60000,
            "GPM": 6.309e-5
        },
        "Viscosity": {
            "Pa·s": 1,
            "cP": 0.001
        }
    },
    "Civil": {
        "Length": {
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "in": 0.0254,
            "ft": 0.3048
        },
        "Area": {
            "m²": 1,
            "cm²": 0.0001,
            "in²": 0.00064516,
            "ft²": 0.092903
        },
        "Volume": {
            "m³": 1,
            "L": 0.001,
            "ft³": 0.0283168
        }
    }
}

# ------------------ ENGINEERING CONVERTER ------------------ #
mode = st.radio("Choose Mode", ["Engineering Converter", "Physics Formula Solver"], key="main_mode")

if "history" not in st.session_state:
    st.session_state["history"] = []

if mode == "Engineering Converter":
    st.header("🏗️ Engineering Converter")
    category = st.selectbox("Select Category", list(engineering_conversions.keys()), key="eng_cat")
    conversion_type = st.selectbox("Select Conversion Type", list(engineering_conversions[category].keys()), key="eng_type")
    unit_dict = engineering_conversions[category][conversion_type]
    units = list(unit_dict.keys())

    val = st.number_input("Enter value", key="eng_value")
    from_unit = st.selectbox("From Unit", units, key="eng_from_unit")
    to_unit = st.selectbox("To Unit", units, key="eng_to_unit")

    if st.button("Convert", key="eng_convert"):
        try:
            base_value = val * unit_dict[from_unit]
            result = base_value / unit_dict[to_unit]
            st.success(f"{val} {from_unit} = {result:.4f} {to_unit}")
            st.session_state["history"].append(("Engineering Converter", f"{val} {from_unit}", f"{result:.4f} {to_unit}"))
        except Exception as e:
            st.error(f"Conversion error: {e}")

# ------------------ HEALTH & FITNESS TOOLS ------------------ #
elif mode == "Health & Fitness Tools":
    st.header("🧘 Health & Fitness Tools")
    option = st.selectbox("Choose Tool", ["BMI", "BMR", "TDEE", "Ideal Weight"])

    if option == "BMI":
        weight = st.number_input("Weight (kg)")
        height = st.number_input("Height (m)")
        if st.button("Calculate BMI"):
            if height > 0:
                bmi = weight / (height ** 2)
                st.success(f"BMI = {bmi:.2f}")
                st.session_state["history"].append(("BMI", f"Weight={weight}kg, Height={height}m", f"BMI={bmi:.2f}"))
            else:
                st.error("Height must be greater than 0")

    elif option == "BMR":
        gender = st.selectbox("Gender", ["Male", "Female"])
        age = st.number_input("Age", min_value=0, step=1)
        weight = st.number_input("Weight (kg)")
        height_cm = st.number_input("Height (cm)")
        if st.button("Calculate BMR"):
            if height_cm > 0 and age > 0:
                if gender == "Male":
                    bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
                else:
                    bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
                st.success(f"BMR = {bmr:.2f} kcal/day")
                st.session_state["history"].append(("BMR", f"Gender={gender}, Age={age}, Weight={weight}kg, Height={height_cm}cm", f"BMR={bmr:.2f}"))
            else:
                st.error("Age and Height must be positive")

    elif option == "TDEE":
        bmr = st.number_input("Enter BMR")
        activity = st.selectbox("Activity Level", [
            "Sedentary", "Light", "Moderate", "Active", "Very Active"])
        factor = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9
        }
        if st.button("Calculate TDEE"):
            tdee = bmr * factor[activity]
            st.success(f"TDEE = {tdee:.2f} kcal/day")
            st.session_state["history"].append(("TDEE", f"BMR={bmr}, Activity={activity}", f"TDEE={tdee:.2f}"))

    elif option == "Ideal Weight":
        height_cm = st.number_input("Height (cm)")
        if st.button("Calculate Ideal Weight"):
            if height_cm > 0:
                male = 50 + 0.91 * (height_cm - 152.4)
                female = 45.5 + 0.91 * (height_cm - 152.4)
                st.success(f"Ideal Weight:\nMale = {male:.2f} kg\nFemale = {female:.2f} kg")
                st.session_state["history"].append(("Ideal Weight", f"Height={height_cm}cm", f"Male={male:.2f}kg, Female={female:.2f}kg"))
            else:
                st.error("Height must be greater than 0")

# ------------------ CONVERSION HISTORY & BOOKMARKS ------------------ #
elif mode == "Conversion History & Bookmarks":
    st.header("📜 Conversion History & Bookmarks")
    if st.session_state["history"]:
        df = pd.DataFrame(st.session_state["history"], columns=["Type", "Input", "Output"])
        st.dataframe(df)
        csv = df.to_csv(index=False).encode()
        st.download_button("Download History CSV", data=csv, file_name="conversion_history.csv", mime="text/csv")
    else:
        st.info("No conversions or calculations performed yet.")
