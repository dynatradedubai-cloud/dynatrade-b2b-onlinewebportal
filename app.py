import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(layout="wide")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    return pd.read_csv("sample_skus.csv")

df = load_data()

# ---------- SESSION ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------- FUNCTIONS ----------
def add_to_cart(oe, brand, price):
    if oe in st.session_state.cart:
        st.session_state.cart[oe]["qty"] += 1
    else:
        st.session_state.cart[oe] = {
            "brand": brand,
            "price": price,
            "qty": 1
        }

def update_qty(oe, change):
    st.session_state.cart[oe]["qty"] += change
    if st.session_state.cart[oe]["qty"] <= 0:
        del st.session_state.cart[oe]

# ---------- CSS ----------
st.markdown("""
<style>

.block-container {padding-top:0.5rem;}

.topbar {
    background:#0b2c5f;
    color:white;
    padding:10px 20px;
    font-weight:600;
}

.searchbox {
    width:100%;
    padding:10px;
    border-radius:6px;
    border:1px solid #ccc;
}

.table {
    width:100%;
    border-collapse:collapse;
    font-size:13px;
}

.table th {
    background:#f1e3c6;
    padding:8px;
    text-align:left;
}

.table td {
    padding:8px;
    border-bottom:1px solid #eee;
}

.btn {
    background:#0b2c5f;
    color:white;
    border:none;
    padding:5px 10px;
    border-radius:4px;
    cursor:pointer;
}

.qty {
    display:flex;
    gap:5px;
    align-items:center;
}

.qty button {
    padding:2px 6px;
    border:none;
    background:#ddd;
    cursor:pointer;
    border-radius:3px;
}

.green {color:green; font-weight:600;}

.card {
    background:white;
    padding:12px;
    border-radius:10px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
    font-size:13px;
}

.title {margin-top:10px; font-weight:600;}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="topbar">Dynatrade Automotive LLC</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3,1])

with c1:
    st.markdown("""
    <div class="card">
    <b>Welcome, Mohamed Ali</b><br>
    Customer Code: CUST1001 | Salesman: Ahmed Khan<br>
    📞 +971 50 123 4567 | ✉️ ahmed.khan@dynatrade.ae
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="card">
    <b>Last Updated</b><br>
    20 May 2025<br>10:30 AM
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([3,1])

# ---------- LEFT ----------
with left:

    st.markdown('<div class="title">Search Parts</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="Search parts...")

    if search:
        filtered = df[
            df.astype(str).apply(lambda r: search.lower() in r.str.lower().to_string(), axis=1)
        ]
    else:
        filtered = df.head(15)

    # ---------- TABLE ----------
    html = """
    <table class="table">
    <tr>
    <th>Brand</th>
    <th>Vehicle</th>
    <th>OE</th>
    <th>Description</th>
    <th>MFG</th>
    <th>Stock</th>
    <th>Price</th>
    <th></th>
    </tr>
    """

    for i, row in filtered.iterrows():
        html += f"""
        <tr>
        <td>{row['Brand']}</td>
        <td>{row['Vehicle']}</td>
        <td>{row['OE']}</td>
        <td>{row['Description']}</td>
        <td>{row['MFG']}</td>
        <td class="green">{row['Stock']}</td>
        <td>{row['Price_AED']}</td>
        <td></td>
        </tr>
        """

    html += "</table>"

    st.markdown(html, unsafe_allow_html=True)

    # ACTION BUTTONS BELOW TABLE (logic fix)
    for i, row in filtered.iterrows():
        if st.button(f"Add {row['OE']}", key=f"add_{i}"):
            add_to_cart(row["OE"], row["Brand"], row["Price_AED"])

    # ---------- CART ----------
    st.markdown('<div class="title">Cart</div>', unsafe_allow_html=True)

    cart_html = """
    <table class="table">
    <tr>
    <th>Brand</th>
    <th>OE</th>
    <th>Qty</th>
    <th>Price</th>
    <th>Total</th>
    <th></th>
    </tr>
    """

    total = 0

    for oe, item in st.session_state.cart.items():
        line_total = item["qty"] * item["price"]
        total += line_total

        cart_html += f"""
        <tr>
        <td>{item['brand']}</td>
        <td>{oe}</td>
        <td>{item['qty']}</td>
        <td>{item['price']}</td>
        <td>{round(line_total,2)}</td>
        <td></td>
        </tr>
        """

    cart_html += "</table>"

    st.markdown(cart_html, unsafe_allow_html=True)

    # QTY CONTROLS (aligned)
    for oe, item in st.session_state.cart.items():
        c1, c2, c3 = st.columns([1,1,1])
        if c1.button("-", key=f"dec_{oe}"):
            update_qty(oe, -1)
            st.rerun()
        c2.write(item["qty"])
        if c3.button("+", key=f"inc_{oe}"):
            update_qty(oe, 1)
            st.rerun()

    st.markdown(f"### Grand Total: {round(total,2)} AED")

    # ACTIONS
    a, b, c = st.columns(3)

    with a:
        if st.session_state.cart:
            st.download_button(
                "⬇ Excel",
                pd.DataFrame(st.session_state.cart).to_csv(),
                "cart.csv"
            )

    with b:
        if st.session_state.cart:
            phone = "971501234567"
            msg = "Inquiry:%0A"
            for oe, item in st.session_state.cart.items():
                msg += f"OE:{oe} Qty:{item['qty']}%0A"
            url = f"https://wa.me/{phone}?text={msg}"
            st.markdown(f"[💬 WhatsApp]({url})")

    with c:
        if st.button("Clear Cart"):
            st.session_state.cart = {}
            st.rerun()

# ---------- RIGHT ----------
with right:
    st.markdown('<div class="title">Notifications</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    🔴 Ramadan Offer 2025.pdf<br>
    🔴 Price Update - May.xlsx<br>
    🔵 New Campaign Available
    </div>
    """, unsafe_allow_html=True)
