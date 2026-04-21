import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(layout="wide")

# ---------- LOAD ----------
@st.cache_data
def load_data():
    return pd.read_csv("sample_skus.csv")

df = load_data()

# ---------- SESSION ----------
if "cart" not in st.session_state:
    st.session_state.cart = {}

# ---------- FUNCTIONS ----------
def add(oe, brand, price):
    if oe in st.session_state.cart:
        st.session_state.cart[oe]["qty"] += 1
    else:
        st.session_state.cart[oe] = {"brand": brand, "price": price, "qty": 1}

def inc(oe):
    st.session_state.cart[oe]["qty"] += 1

def dec(oe):
    st.session_state.cart[oe]["qty"] -= 1
    if st.session_state.cart[oe]["qty"] <= 0:
        del st.session_state.cart[oe]

# ---------- STYLE ----------
st.markdown("""
<style>
.block-container {padding-top:0.5rem;}

.header {
    background:#0b2c5f;
    color:white;
    padding:12px 20px;
    font-weight:600;
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
    padding:4px 10px;
    border-radius:4px;
    text-decoration:none;
    font-size:12px;
}

.qty {
    display:flex;
    align-items:center;
    gap:6px;
}

.qty span {
    padding:0 6px;
}

.green {color:green; font-weight:600;}

.card {
    background:white;
    padding:12px;
    border-radius:10px;
    box-shadow:0 2px 6px rgba(0,0,0,0.1);
    font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Dynatrade Automotive LLC</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3,1])
with c1:
    st.markdown('<div class="card"><b>Welcome Mohamed Ali</b><br>Customer Code: CUST1001</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><b>Last Updated</b><br>20 May 2025</div>', unsafe_allow_html=True)

left, right = st.columns([3,1])

# ---------- SEARCH ----------
with left:
    search = st.text_input("", placeholder="Search parts...")

    if search:
        data = df[df.astype(str).apply(lambda r: search.lower() in r.str.lower().to_string(), axis=1)]
    else:
        data = df.head(15)

    # ---------- TABLE ----------
    html = """
    <table class="table">
    <tr>
    <th>Brand</th><th>Vehicle</th><th>OE</th>
    <th>Description</th><th>MFG</th><th>Stock</th>
    <th>Price</th><th>Action</th>
    </tr>
    """

    for i, r in data.iterrows():
        html += f"""
        <tr>
        <td>{r['Brand']}</td>
        <td>{r['Vehicle']}</td>
        <td>{r['OE']}</td>
        <td>{r['Description']}</td>
        <td>{r['MFG']}</td>
        <td class='green'>{r['Stock']}</td>
        <td>{r['Price_AED']}</td>
        <td><a href='?add={r["OE"]}' class='btn'>Add</a></td>
        </tr>
        """

    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    # ---------- HANDLE ADD ----------
    params = st.query_params
    if "add" in params:
        oe = params["add"]
        row = df[df["OE"] == oe].iloc[0]
        add(oe, row["Brand"], row["Price_AED"])
        st.query_params.clear()

    # ---------- CART ----------
    st.markdown("### Cart")

    cart_html = """
    <table class="table">
    <tr>
    <th>Brand</th><th>OE</th><th>Qty</th>
    <th>Price</th><th>Total</th><th>Action</th>
    </tr>
    """

    total = 0

    for oe, item in st.session_state.cart.items():
        line = item["qty"] * item["price"]
        total += line

        cart_html += f"""
        <tr>
        <td>{item['brand']}</td>
        <td>{oe}</td>
        <td>
        <div class='qty'>
        <a href='?dec={oe}'>-</a>
        <span>{item['qty']}</span>
        <a href='?inc={oe}'>+</a>
        </div>
        </td>
        <td>{item['price']}</td>
        <td>{round(line,2)}</td>
        <td><a href='?del={oe}'>❌</a></td>
        </tr>
        """

    cart_html += "</table>"
    st.markdown(cart_html, unsafe_allow_html=True)

    # ---------- HANDLE CART ACTIONS ----------
    if "inc" in params:
        inc(params["inc"])
        st.query_params.clear()

    if "dec" in params:
        dec(params["dec"])
        st.query_params.clear()

    if "del" in params:
        del st.session_state.cart[params["del"]]
        st.query_params.clear()

    st.markdown(f"### Grand Total: {round(total,2)} AED")

    # ---------- ACTIONS ----------
    a,b,c = st.columns(3)

    with a:
        if st.session_state.cart:
            st.download_button("Excel", pd.DataFrame(st.session_state.cart).to_csv(), "cart.csv")

    with b:
        if st.session_state.cart:
            phone = "971501234567"
            msg = "Inquiry:%0A"
            for oe, item in st.session_state.cart.items():
                msg += f"{oe} Qty:{item['qty']}%0A"
            url = f"https://wa.me/{phone}?text={msg}"
            st.markdown(f"[WhatsApp]({url})")

    with c:
        if st.button("Clear"):
            st.session_state.cart = {}
            st.rerun()

# ---------- RIGHT ----------
with right:
    st.markdown("""
    <div class="card">
    🔴 Ramadan Offer 2025.pdf<br>
    🔴 Price Update - May.xlsx<br>
    🔵 Campaign
    </div>
    """, unsafe_allow_html=True)
