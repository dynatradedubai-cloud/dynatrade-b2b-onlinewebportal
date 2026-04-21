import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
body {
    background-color: #f5f7fb;
}

.header {
    background-color: #0b2c5f;
    padding: 15px;
    color: white;
    font-size: 22px;
    font-weight: bold;
}

.sub-header {
    font-size: 18px;
    font-weight: bold;
    margin-top: 10px;
}

.card {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}

.gold-header {
    background-color: #f1e3c6;
    padding: 10px;
    font-weight: bold;
}

.btn {
    background-color: #0b2c5f;
    color: white;
    padding: 6px 12px;
    border-radius: 5px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Dynatrade Automotive LLC</div>', unsafe_allow_html=True)

# ---------- CUSTOMER INFO ----------
col1, col2 = st.columns([3,1])

with col1:
    st.markdown("""
    <div class="card">
    <b>Welcome, Mohamed Ali</b><br>
    Customer Code: CUST1001 | Salesman: Ahmed Khan<br>
    📞 +971 50 123 4567 | ✉️ ahmed.khan@dynatrade.ae
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
    <b>Last Updated</b><br>
    20 May 2025<br>10:30 AM
    </div>
    """, unsafe_allow_html=True)

# ---------- MAIN LAYOUT ----------
left, right = st.columns([3,1])

# ---------- LEFT SIDE ----------
with left:

    st.markdown("### Search Parts")

    search = st.text_input("Search by OE, Brand, Vehicle...")

    st.markdown("**Popular Search:** M24 Bolt | Hex Bolt | Daimler")

    # SAMPLE TABLE (will replace with Excel later)
    data = pd.DataFrame({
        "Brand": ["Sampa", "OEM"],
        "Vehicle": ["DAIMLER AG", "DAIMLER AG"],
        "OE": ["000000005503", "000000005503"],
        "Description": ["HEXAGON HEAD BOLT", "HEXAGON HEAD BOLT"],
        "Stock": [11, 12],
        "Price (AED)": [13.72, 32.28]
    })

    st.dataframe(data, use_container_width=True)

    # ---------- CART ----------
    st.markdown("### Cart")

    cart = pd.DataFrame({
        "Brand": ["Sampa"],
        "OE": ["000000005503"],
        "Qty": [1],
        "Price": [13.72],
        "Total": [13.72]
    })

    st.dataframe(cart, use_container_width=True)

    st.markdown("### Grand Total: 13.72 AED")

    colA, colB, colC = st.columns(3)

    with colA:
        st.button("Download Cart (Excel)")

    with colB:
        st.button("Send via WhatsApp")

    with colC:
        st.button("Clear Cart")

# ---------- RIGHT SIDE (NOTIFICATIONS) ----------
with right:

    st.markdown("### Notifications")

    st.markdown("""
    <div class="card">
    🔴 Ramadan Offer 2025.pdf<br><br>
    🔴 Price Update - May.xlsx<br><br>
    🔵 New Campaign Available
    </div>
    """, unsafe_allow_html=True)
