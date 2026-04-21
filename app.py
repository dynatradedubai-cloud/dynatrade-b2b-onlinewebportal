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
    st.session_state.cart = []

# ---------- FUNCTIONS ----------
def add_to_cart(item):
    for cart_item in st.session_state.cart:
        if cart_item["OE"] == item["OE"]:
            cart_item["Qty"] += 1
            return
    item["Qty"] = 1
    st.session_state.cart.append(item)

def remove_item(index):
    st.session_state.cart.pop(index)

def generate_whatsapp_text(cart):
    msg = "Hello, I would like to inquire:%0A%0A"
    for item in cart:
        msg += f"OE: {item['OE']} | Qty: {item['Qty']}%0A"
    return msg

# ---------- CSS (HIGH QUALITY UI) ----------
st.markdown("""
<style>

/* REMOVE STREAMLIT DEFAULT SPACE */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* HEADER */
.header {
    background: #0b2c5f;
    color: white;
    padding: 14px 20px;
    font-size: 20px;
    font-weight: 600;
}

/* CARDS */
.card {
    background: white;
    padding: 14px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    font-size: 14px;
}

/* SECTION TITLE */
.title {
    font-size: 16px;
    font-weight: 600;
    margin: 12px 0 6px 0;
}

/* SEARCH */
.search input {
    width: 100%;
    padding: 10px;
    border-radius: 6px;
    border: 1px solid #ccc;
}

/* TABLE HEADER */
.table-header {
    background: #f1e3c6;
    padding: 8px;
    font-weight: 600;
    border-radius: 5px;
}

/* ROW */
.row {
    padding: 6px 0;
    border-bottom: 1px solid #eee;
    font-size: 13px;
}

/* BUTTON */
.stButton button {
    background-color: #0b2c5f;
    color: white;
    border-radius: 5px;
    height: 32px;
    padding: 0 12px;
    font-size: 12px;
}

/* GREEN STOCK */
.green {
    color: green;
    font-weight: 600;
}

/* NOTIFICATIONS */
.notify {
    font-size: 13px;
    line-height: 22px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="header">Dynatrade Automotive LLC</div>', unsafe_allow_html=True)

# ---------- TOP INFO ----------
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

# ---------- LAYOUT ----------
left, right = st.columns([3,1])

# ---------- LEFT ----------
with left:

    st.markdown('<div class="title">Search Parts</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="Search by OE / Brand / Vehicle / Description")

    if search:
        filtered = df[
            df.astype(str).apply(lambda r: search.lower() in r.str.lower().to_string(), axis=1)
        ]
    else:
        filtered = df.head(15)

    # HEADER
    cols = st.columns([1,1,1.2,2.5,1,1,1])
    headers = ["Brand","Vehicle","OE","Description","Stock","Price",""]
    for col, h in zip(cols, headers):
        col.markdown(f"<div class='table-header'>{h}</div>", unsafe_allow_html=True)

    # ROWS
    for i, row in filtered.iterrows():
        cols = st.columns([1,1,1.2,2.5,1,1,1])

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
    st.markdown('<div class="title">Cart</div>', unsafe_allow_html=True)

    total = 0

    # CART HEADER
    cols = st.columns([1,1,1,1,1,1])
    headers = ["Brand","OE","Qty","Price","Total",""]
    for col, h in zip(cols, headers):
        col.markdown(f"<div class='table-header'>{h}</div>", unsafe_allow_html=True)

    for idx, item in enumerate(st.session_state.cart):
        cols = st.columns([1,1,1,1,1,1])

        cols[0].write(item["Brand"])
        cols[1].write(item["OE"])
        cols[2].write(item["Qty"])
        cols[3].write(item["Price"])

        item_total = item["Qty"] * item["Price"]
        total += item_total

        cols[4].write(round(item_total,2))

        if cols[5].button("❌", key=f"rm_{idx}"):
            remove_item(idx)
            st.rerun()

    st.markdown(f"### **Grand Total: {round(total,2)} AED**")

    # ACTION BUTTONS
    a,b,c = st.columns(3)

    with a:
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.download_button("⬇ Download Excel", df_cart.to_csv(index=False), "cart.csv")

    with b:
        if st.session_state.cart:
            phone = "971501234567"
            text = generate_whatsapp_text(st.session_state.cart)
            url = f"https://wa.me/{phone}?text={text}"
            st.markdown(f"[💬 WhatsApp]({url})")

    with c:
        if st.button("🗑 Clear"):
            st.session_state.cart = []
            st.rerun()

# ---------- RIGHT ----------
with right:

    st.markdown('<div class="title">Notifications</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card notify">
    🔴 Ramadan Offer 2025.pdf<br>
    🔴 Price Update - May.xlsx<br>
    🔵 New Campaign Available
    </div>
    """, unsafe_allow_html=True)
