import streamlit as st

st.title("Simple Calculator")

num1 = st.number_input("Enter your first number", value=0.0, format="%.2f")
operator = st.selectbox("Select operation", ["+", "-", "*", "/"])
num2 = st.number_input("Enter your second number", value=0.0, format="%.2f")

result = None
error = None

if st.button("Calculate"):
    try:
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                error = "Cannot divide by zero."
            else:
                result = num1 / num2
    except Exception as exc:
        error = f"Calculation error: {exc}"

if error:
    st.error(error)
elif result is not None:
    st.success(f"Result: {result}")


