# app.py
import streamlit as st
import pandas as pd
from io import BytesIO
import urllib.parse

st.set_page_config(layout="wide", page_title="Dynatrade B2B Portal")

# -------------------------
# CSS / Theme (load early)
# -------------------------
st.markdown("""
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --navy:#0b3d91;
  --teal:#0fb3a6;
  --muted:#6b7280;
  --card-bg:#ffffff;
  --page-bg:#f5f7fa;
}
html,body {font-family: 'Inter', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; background:var(--page-bg); color:#111; margin:0; padding:0;}
.header {background:var(--navy); color:white; padding:16px 20px; border-radius:8px; display:flex; align-items:center; gap:14px;}
.logo {width:44px; height:44px; background:white; border-radius:6px; display:inline-block;}
.header h1 {margin:0; font-size:18px; font-weight:700;}
.top-meta {margin-top:10px; color:var(--muted); font-size:13px;}
.card {background:var(--card-bg); padding:14px; border-radius:8px; box-shadow:0 6px 18px rgba(11,61,145,0.06);}
.search-input {width:100%; padding:12px 14px; border-radius:10px; border:1px solid #e6e9ef; font-size:14px;}
.popular-chips {margin-top:8px; display:flex; gap:8px; flex-wrap:wrap;}
.chip {background:#eef6ff; color:var(--navy); padding:6px 10px; border-radius:999px; font-size:13px; cursor:pointer;}
.results-table {width:100%; border-collapse:collapse; margin-top:12px;}
.results-table th {background:var(--navy); color:white; padding:10px; text-align:left; font-weight:600; font-size:13px;}
.results-table td {padding:10px; border-bottom:1px solid #eef0f4; font-size:13px; vertical-align:middle;}
.results-table tr:hover td {background:#fbfdff;}
.cart-panel {position:relative;}
.cart-item {display:flex; justify-content:space-between; gap:8px; padding:10px 0; border-bottom:1px dashed #eef0f4;}
.qty-btn {background:#f3f4f6; border-radius:6px; padding:6px 8px; cursor:pointer; margin:0 4px;}
.btn {display:inline-block; padding:10px 14px; border-radius:8px; text-decoration:none; color:white; font-weight:600;}
.btn-excel {background:var(--navy);}
.btn-whatsapp {background:#25D366;}
.notifications {font-size:13px;}
.footer {margin-top:18px; color:var(--muted); font-size:13px; padding-top:12px; border-top:1px solid #eef0f4;}
.small {font-size:13px; color:var(--muted);}
.add-btn {background:#0b3d91; color:white; padding:6px 10px; border-radius:6px; text-decoration:none; font-weight:600;}
.qty-input {width:48px; text-align:center; padding:6px; border-radius:6px; border:1px solid #e6e9ef;}
</style>
""", unsafe_allow_html=True)

# -------------------------
# Utilities
# -------------------------
@st.cache_data
def load_data(path="sample_skus.csv"):
    df = pd.read_csv(path, dtype=str)
    if 'Stock' in df.columns:
        df['Stock'] = pd.to_numeric(df['Stock'], errors='coerce').fillna(0).astype(int)
    if 'Price_AED' in df.columns:
        df['Price_AED'] = pd.to_numeric(df['Price_AED'], errors='coerce').fillna(0.0)
    return df

def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Cart')
        writer.save()
    return output.getvalue()

def format_whatsapp_message(cart_items, customer_name="Mohamed Ali", cust_code="CUST1001"):
    lines = [f"Inquiry from {customer_name} ({cust_code}):"]
    for it in cart_items:
        lines.append(f"{it['Brand']} | OE:{it['OE']} | Qty:{it['Qty']} | Unit:{it['UnitPrice']:.2f} AED")
    return urllib.parse.quote("\n".join(lines))

# -------------------------
# Load data
# -------------------------
try:
    df = load_data()
except Exception:
    st.error("Failed to load sample_skus.csv. Check file exists and is valid CSV.")
    st.stop()

# -------------------------
# Header and meta
# -------------------------
st.markdown('<div class="header"><div class="logo"></div><h1>Dynatrade Automotive LLC</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="top-meta">Welcome, <strong>Mohamed Ali</strong> &nbsp;&nbsp;|&nbsp;&nbsp; Customer Code: <strong>CUST1001</strong> &nbsp;&nbsp;|&nbsp;&nbsp; Salesman: <strong>Ahmed Khan</strong> (+971 50 123 4567)</div>', unsafe_allow_html=True)
st.write("")

# -------------------------
# Search and layout
# -------------------------
q = st.text_input("Search by OE, MFG, Brand, Vehicle, Description", value="", key="search_input")
st.markdown('<div class="popular-chips"><span class="chip">M24 Bolt</span><span class="chip">Hex Bolt</span><span class="chip">000000005503 | Daimler</span></div>', unsafe_allow_html=True)

def filter_df(df, q):
    if not q or str(q).strip()=="":
        return df
    ql = str(q).lower()
    mask = df.apply(lambda r: ql in str(r.get('OE','')).lower() or ql in str(r.get('Brand','')).lower() or ql in str(r.get('Description','')).lower() or ql in str(r.get('Vehicle','')).lower(), axis=1)
    return df[mask]

results = filter_df(df, q)

col1, col2 = st.columns([3,1])

# -------------------------
# Results table (HTML) and Add buttons (Python)
# -------------------------
with col1:
    st.markdown('<div class="card"><h3>Search Parts</h3>', unsafe_allow_html=True)

    def render_results_table(df_results):
        rows_html = ""
        for idx, r in df_results.head(200).iterrows():
            price = float(r.get('Price_AED', 0.0))
            rows_html += f"""
            <tr>
              <td>{r.get('Brand','')}</td>
              <td>{r.get('Vehicle','')}</td>
              <td>{r.get('OE','')}</td>
              <td>{r.get('Description','')}</td>
              <td style="width:80px;">{r.get('Stock',0)}</td>
              <td style="width:110px;">{price:.2f}</td>
            </tr>
            """
        html = f"""
        <table class="results-table" role="table">
          <thead><tr>
            <th>Brand</th><th>Vehicle</th><th>OE</th><th>Description</th><th>Stock</th><th>Price (AED)</th>
          </tr></thead>
          <tbody>{rows_html}</tbody>
        </table>
        """
        st.markdown(html, unsafe_allow_html=True)

    render_results_table(results)

    visible = results.head(10)
    for i, row in visible.iterrows():
        cols = st.columns([3,2,1])
        with cols[0]:
            st.markdown(f"**{row.get('Brand','')}** — {row.get('Description','')}")
            st.markdown(f"<div class='small'>{row.get('Vehicle','')} | OE: {row.get('OE','')}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"Stock: {row.get('Stock',0)}  •  Price: {float(row.get('Price_AED',0.0)):.2f} AED")
        with cols[2]:
            if st.button("Add", key=f"add_{i}"):
                unit = float(row.get('Price_AED',0.0))
                item = {
                    "Brand": row.get('Brand',''),
                    "Vehicle": row.get('Vehicle',''),
                    "OE": row.get('OE',''),
                    "MFG": row.get('MFG','') if 'MFG' in row else '',
                    "Description": row.get('Description',''),
                    "Stock": int(row.get('Stock',0)),
                    "UnitPrice": unit,
                    "Qty": 1,
                    "Total": unit * 1
                }
                if 'cart' not in st.session_state:
                    st.session_state.cart = []
                st.session_state.cart.append(item)
                # Streamlit will rerun automatically after button click

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Cart panel and notifications
# -------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3>Cart</h3>', unsafe_allow_html=True)

    if 'cart' not in st.session_state:
        st.session_state.cart = []

    if not st.session_state.cart:
        st.markdown('<div class="small">Your cart is empty</div>', unsafe_allow_html=True)
    else:
        for idx, it in enumerate(st.session_state.cart):
            st.markdown(f'''
            <div class="cart-item">
              <div style="flex:1;">
                <div style="font-weight:600;">{it['Brand']} — {it['OE']}</div>
                <div class="small">{it['Description']}</div>
              </div>
              <div style="text-align:right; min-width:140px;">
                <div>Unit: {it['UnitPrice']:.2f} AED</div>
                <div style="margin-top:6px;">
                  <form action="#" method="post" style="display:inline;">
                    <input class="qty-input" value="{it['Qty']}" readonly>
                  </form>
                </div>
                <div style="margin-top:8px; font-weight:700;">{it['Total']:.2f} AED</div>
              </div>
            </div>
            ''', unsafe_allow_html=True)

        grand = sum([x['Total'] for x in st.session_state.cart])
        st.markdown(f'<div style="padding:12px 0; font-weight:700;">Grand Total: {grand:.2f} AED</div>', unsafe_allow_html=True)

        cart_df = pd.DataFrame(st.session_state.cart)
        excel_bytes = to_excel_bytes(cart_df)
        st.download_button("Download Cart (Excel)", data=excel_bytes, file_name="cart.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl")

        wa_msg = format_whatsapp_message(st.session_state.cart, customer_name="Mohamed Ali", cust_code="CUST1001")
        wa_link = f"https://wa.me/971501234567?text={wa_msg}"
        st.markdown(f'<a class="btn btn-whatsapp" href="{wa_link}" target="_blank" style="margin-right:8px;">Send Inquiry on WhatsApp</a>', unsafe_allow_html=True)

        mail_body = urllib.parse.quote("Please find my inquiry attached.\n\nRegards,\nMohamed Ali")
        mailto = f"mailto:sales@dynatrade.ae?subject=Parts Inquiry&body={mail_body}"
        st.markdown(f'<a class="btn btn-excel" href="{mailto}" style="background:#0b3d91; margin-left:6px;">Send Inquiry by Email</a>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="margin-top:12px;" class="card"><h4>Notifications</h4><div class="notifications"><div><strong>NEW</strong> Ramadan Offer 2025.pdf <span class="small">20 May 2025</span></div><div style="margin-top:6px;"><strong>NEW</strong> Price Update – May.xlsx <span class="small">19 May 2025</span></div><div style="margin-top:6px;"><strong>INFO</strong> New Campaign Available <span class="small">18 May 2025</span></div></div></div>', unsafe_allow_html=True)

# -------------------------
# Footer
# -------------------------
st.markdown('<div class="footer">© 2025 Dynatrade Automotive LLC. Need help? WhatsApp: +971 50 123 4567 | Email: sales@dynatrade.ae</div>', unsafe_allow_html=True)
