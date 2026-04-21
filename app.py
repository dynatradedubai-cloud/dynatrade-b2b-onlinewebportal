import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("sample_skus.csv")

df = load_data()

# ---------- CUSTOM UI ----------
st.markdown("""
<style>
body { background-color: #f5f7fb; font-family: Arial; }

.header {
    background-color: #0b2c5f;
    color: white;
    padding: 14px;
    font-size: 22px;
    font-weight: bold;
}

.card {
    background: white;
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
}

.section-title {
    font-size: 18px;
    font-weight: bold;
    margin-top: 15px;
}

.table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.table th {
    background-color: #f1e3c6;
    padding: 10px;
    text-align: left;
}

.table td {
    padding: 10px;
    border-top: 1px solid #ddd;
}

.btn {
    background-color: #0b2c5f;
    color: white;
    padding: 6px 12px;
    border-radius: 5px;
    border: none;
}

.qty {
    width: 50px;
}

.search {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

.red {color:red;}
.green {color:green;}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Dynatrade Automotive LLC</div>', unsafe_allow_html=True)

# ---------- CUSTOMER ----------
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

# ---------- LAYOUT ----------
left, right = st.columns([3,1])

# ---------- SEARCH ----------
with left:
    st.markdown('<div class="section-title">Search Parts</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="Search by OE, Brand, Vehicle, Description")

    if search:
        filtered = df[
            df.astype(str).apply(lambda row: search.lower() in row.str.lower().to_string(), axis=1)
        ]
    else:
        filtered = df.head(20)

    # ---------- TABLE ----------
    table_html = """
    <table class="table">
    <tr>
    <th>Brand</th>
    <th>Vehicle</th>
    <th>OE</th>
    <th>Description</th>
    <th>Stock</th>
    <th>Price (AED)</th>
    </tr>
    """

    for _, row in filtered.iterrows():
        table_html += f"""
        <tr>
        <td>{row['Brand']}</td>
        <td>{row['Vehicle']}</td>
        <td>{row['OE']}</td>
        <td>{row['Description']}</td>
        <td class='green'>{row['Stock']}</td>
        <td>{row['Price_AED']}</td>
        </tr>
        """

    table_html += "</table>"

    st.markdown(table_html, unsafe_allow_html=True)

    # ---------- CART (STATIC FOR NOW) ----------
    st.markdown('<div class="section-title">Cart</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="table">
    <tr>
    <th>Brand</th>
    <th>OE</th>
    <th>Qty</th>
    <th>Price</th>
    <th>Total</th>
    </tr>
    <tr>
    <td>Sampa</td>
    <td>000000005503</td>
    <td>1</td>
    <td>13.72</td>
    <td>13.72</td>
    </tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("### **Grand Total: 13.72 AED**")

    colA, colB, colC = st.columns(3)

    with colA:
        st.button("Download Excel")

    with colB:
        st.button("Send WhatsApp")

    with colC:
        st.button("Clear Cart")

# ---------- NOTIFICATIONS ----------
with right:
    st.markdown('<div class="section-title">Notifications</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    🔴 Ramadan Offer 2025.pdf<br><br>
    🔴 Price Update - May.xlsx<br><br>
    🔵 New Campaign Available
    </div>
    """, unsafe_allow_html=True)
