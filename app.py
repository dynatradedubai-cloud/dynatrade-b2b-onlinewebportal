import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("sample_skus.csv")

df = load_data()

# ---------- SESSION CART ----------
if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------- ADD TO CART FUNCTION ----------
def add_to_cart(item):
    for cart_item in st.session_state.cart:
        if cart_item["OE"] == item["OE"]:
            cart_item["Qty"] += 1
            return
    item["Qty"] = 1
    st.session_state.cart.append(item)

# ---------- REMOVE ----------
def remove_item(index):
    st.session_state.cart.pop(index)

# ---------- CSS ----------
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

.table th {
    background-color: #f1e3c6;
    padding: 8px;
    text-align: left;
}

.table td {
    padding: 8px;
    border-top: 1px solid #ddd;
}

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
    st.markdown('<table class="table">', unsafe_allow_html=True)
    st.markdown("""
    <tr>
    <th>Brand</th>
    <th>Vehicle</th>
    <th>OE</th>
    <th>Description</th>
    <th>Stock</th>
    <th>Price</th>
    <th>Action</th>
    </tr>
    """, unsafe_allow_html=True)

    for i, row in filtered.iterrows():
        cols = st.columns([1,1,1,2,1,1,1])

        cols[0].write(row["Brand"])
        cols[1].write(row["Vehicle"])
        cols[2].write(row["OE"])
        cols[3].write(row["Description"])
        cols[4].markdown(f"<span class='green'>{row['Stock']}</span>", unsafe_allow_html=True)
        cols[5].write(row["Price_AED"])

        if cols[6].button("Add", key=f"add_{i}"):
            add_to_cart({
                "Brand": row["Brand"],
                "Vehicle": row["Vehicle"],
                "OE": row["OE"],
                "Description": row["Description"],
                "Price": row["Price_AED"]
            })

    # ---------- CART ----------
    st.markdown('<div class="section-title">Cart</div>', unsafe_allow_html=True)

    total = 0

    for idx, item in enumerate(st.session_state.cart):
        cols = st.columns([1,1,1,1,1,1])

        cols[0].write(item["Brand"])
        cols[1].write(item["OE"])
        cols[2].write(item["Qty"])
        cols[3].write(item["Price"])

        item_total = item["Qty"] * item["Price"]
        total += item_total

        cols[4].write(round(item_total,2))

        if cols[5].button("Remove", key=f"rm_{idx}"):
            remove_item(idx)
            st.rerun()

    st.markdown(f"### **Grand Total: {round(total,2)} AED**")

    colA, colB, colC = st.columns(3)

    with colA:
        st.button("Download Excel")

    with colB:
        st.button("Send WhatsApp")

    with colC:
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.rerun()

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
