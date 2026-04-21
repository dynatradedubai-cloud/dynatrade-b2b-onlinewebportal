import streamlit as st
import pandas as pd

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
    for c in st.session_state.cart:
        if c["OE"] == item["OE"]:
            c["Qty"] += 1
            return
    item["Qty"] = 1
    st.session_state.cart.append(item)

def update_qty(index, change):
    st.session_state.cart[index]["Qty"] += change
    if st.session_state.cart[index]["Qty"] <= 0:
        st.session_state.cart.pop(index)

# ---------- CSS ----------
st.markdown("""
<style>

/* REMOVE DEFAULT SPACE */
.block-container { padding-top: 0.5rem; }

/* TOP NAV */
.topnav {
    background:#0b2c5f;
    color:white;
    padding:10px 20px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}

.search-top input {
    width:400px;
    padding:6px;
    border-radius:5px;
    border:none;
}

/* CARD */
.card {
    background:white;
    padding:12px;
    border-radius:10px;
    box-shadow:0 2px 6px rgba(0,0,0,0.08);
    font-size:13px;
}

/* SECTION */
.title { font-weight:600; margin:10px 0; }

/* TABLE HEADER STRIP */
.header-strip {
    background:#f1e3c6;
    padding:8px;
    font-weight:600;
    font-size:13px;
}

/* ROW */
.row { padding:6px 0; border-bottom:1px solid #eee; font-size:13px; }

/* BUTTON */
.stButton button {
    background:#0b2c5f;
    color:white;
    border-radius:4px;
    height:30px;
    font-size:12px;
}

/* GREEN */
.green { color:green; font-weight:600; }

/* QTY BTN */
.qty-btn {
    background:#ddd;
    padding:2px 6px;
    margin:0 3px;
    cursor:pointer;
    border-radius:3px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TOP NAV ----------
st.markdown("""
<div class="topnav">
    <div><b>Dynatrade Automotive LLC</b></div>
    <div class="search-top">
        <input placeholder="Search by OE, Brand, Vehicle...">
    </div>
    <div>🔔 EN | 👤 Mohamed Ali</div>
</div>
""", unsafe_allow_html=True)

# ---------- CUSTOMER ----------
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

    search = st.text_input("", placeholder="Search parts...")

    if search:
        filtered = df[
            df.astype(str).apply(lambda r: search.lower() in r.str.lower().to_string(), axis=1)
        ]
    else:
        filtered = df.head(15)

    # HEADER STRIP
    cols = st.columns([1,1,1.2,2.5,1,1,1,1])
    headers = ["Brand","Vehicle","OE","Description","MFG","Stock","Price",""]
    for col, h in zip(cols, headers):
        col.markdown(f"<div class='header-strip'>{h}</div>", unsafe_allow_html=True)

    # ROWS
    for i, row in filtered.iterrows():
        cols = st.columns([1,1,1.2,2.5,1,1,1,1])

        cols[0].write(row["Brand"])
        cols[1].write(row["Vehicle"])
        cols[2].write(row["OE"])
        cols[3].write(row["Description"])
        cols[4].write(row["MFG"])
        cols[5].markdown(f"<span class='green'>{row['Stock']}</span>", unsafe_allow_html=True)
        cols[6].write(row["Price_AED"])

        if cols[7].button("Add", key=f"add_{i}"):
            add_to_cart({
                "Brand": row["Brand"],
                "OE": row["OE"],
                "Price": row["Price_AED"]
            })

    # ---------- CART ----------
    st.markdown('<div class="title">Cart</div>', unsafe_allow_html=True)

    total = 0

    cols = st.columns([1,1,1,1,1,1])
    headers = ["Brand","OE","Qty","Price","Total",""]
    for col, h in zip(cols, headers):
        col.markdown(f"<div class='header-strip'>{h}</div>", unsafe_allow_html=True)

    for idx, item in enumerate(st.session_state.cart):
        cols = st.columns([1,1,1,1,1,1])

        cols[0].write(item["Brand"])
        cols[1].write(item["OE"])

        qty_col = cols[2]
        if qty_col.button("-", key=f"dec_{idx}"):
            update_qty(idx, -1)
            st.rerun()

        qty_col.write(item["Qty"])

        if qty_col.button("+", key=f"inc_{idx}"):
            update_qty(idx, 1)
            st.rerun()

        cols[3].write(item["Price"])

        item_total = item["Qty"] * item["Price"]
        total += item_total

        cols[4].write(round(item_total,2))

        if cols[5].button("❌", key=f"rm_{idx}"):
            st.session_state.cart.pop(idx)
            st.rerun()

    st.markdown(f"### **Grand Total: {round(total,2)} AED**")

    a,b,c = st.columns(3)

    with a:
        if st.session_state.cart:
            st.download_button("⬇ Excel", pd.DataFrame(st.session_state.cart).to_csv(index=False), "cart.csv")

    with b:
        if st.session_state.cart:
            phone = "971501234567"
            msg = "Inquiry:%0A"
            for item in st.session_state.cart:
                msg += f"OE:{item['OE']} Qty:{item['Qty']}%0A"
            url = f"https://wa.me/{phone}?text={msg}"
            st.markdown(f"[💬 WhatsApp]({url})")

    with c:
        if st.button("🗑 Clear"):
            st.session_state.cart = []
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
