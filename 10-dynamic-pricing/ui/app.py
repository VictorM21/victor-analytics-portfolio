import streamlit as st
import pandas as pd
import requests
import io
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Dynamic Pricing Engine", layout="wide")
st.title("📊 Dynamic Pricing Engine")
st.markdown("Get optimal price recommendations with uncertainty.")

st.sidebar.header("About")
st.sidebar.info("This demo uses a placeholder model. The real Bayesian model is being trained.")

st.header("Single Product Prediction")

with st.form("single_form"):
    col1, col2 = st.columns(2)
    with col1:
        product_id = st.text_input("Product ID", value="P001")
        current_price = st.number_input("Current Price ($)", min_value=0.01, value=100.0)
    with col2:
        competitor_price = st.number_input("Competitor Price ($)", min_value=0.0, value=95.0, help="Leave 0 if unknown")
        inventory_level = st.number_input("Inventory Level", min_value=0, value=100)

    submitted = st.form_submit_button("Get Recommendation")

if submitted:
    payload = {
        "product_id": product_id,
        "current_price": current_price,
        "competitor_price": competitor_price if competitor_price > 0 else None,
        "inventory_level": inventory_level
    }
    try:
        response = requests.post(f"{API_URL}/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success("Recommendation ready!")

            col1, col2, col3 = st.columns(3)
            col1.metric("Recommended Price", f"${result['recommended_price']:.2f}")
            col2.metric("Expected Profit", f"${result['expected_profit']:.2f}")
            col3.metric("Risk of Loss", f"{result['risk_of_loss']*100:.0f}%")

            st.subheader("Confidence Interval")
            ci = result['confidence_interval']
            st.write(f"90% Credible Interval: **${ci[0]:.2f} – ${ci[1]:.2f}**")

            fig, ax = plt.subplots()
            ax.barh(['Recommended Price'], [result['recommended_price']], color='skyblue')
            ax.errorbar(result['recommended_price'], 0,
                        xerr=[[result['recommended_price']-ci[0]], [ci[1]-result['recommended_price']]],
                        fmt='o', color='red', capsize=5)
            ax.set_xlabel('Price ($)')
            ax.set_title('Recommended Price with 90% CI')
            st.pyplot(fig)

        else:
            st.error(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")

st.header("Batch Prediction")
uploaded_file = st.file_uploader("Upload a CSV file with columns: product_id, current_price, competitor_price (optional)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded data:")
    st.dataframe(df.head())

    if st.button("Run Batch Prediction"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        try:
            response = requests.post(f"{API_URL}/batch", files=files)
            if response.status_code == 200:
                st.download_button(
                    label="Download Results",
                    data=response.content,
                    file_name="pricing_results.csv",
                    mime="text/csv"
                )
                result_df = pd.read_csv(io.BytesIO(response.content))
                st.success("Batch processed!")
                st.dataframe(result_df.head())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")
