import streamlit as st
import pandas as pd
import duckdb
from io import BytesIO

st.set_page_config(layout="wide", page_title="Dynatrade Portal")

# --- CSS (simple example) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
<style>
body {font-family: 'Inter', sans-serif; background:#f5f7fa;}
.header {background:#0b3d91; color:white; padding:14px; border-radius:6px;}
.card {background:white; padding:12px; border-radius:6px; box-shadow:0 1px 4px rgba(0,0,0,0.08);}
.small {font-size:13px; color:#666;}
.btn-whatsapp {background:#25D366; color:white; padding:8px 12px; border-radius:6px;}
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header"><h2>Dynatrade Automotive LLC</h2></div>', unsafe_allow_html=True)
st.markdown("**Welcome, Mohamed Ali**  \n**Customer Code:** CUST1001  \n**Salesman:** Ahmed Khan | +971 50 123 4567", unsafe_allow_html=True)
st.write("")

# --- Load data (DuckDB over Parquet or CSV) ---
@st.cache_data
def load_data():
    # For demo we load a small CSV in repo; replace with Parquet for full dataset
    df = pd.read_csv("sample_skus.csv")
    return df

df = load_data()

# --- Search bar ---
q = st.text_input("Search by OE, MFG, Brand, Vehicle, Description", "")
if q:
    # simple server-side filter
    ql = q.lower()
    results = df[df.apply(lambda r: ql in str(r['OE']).lower() or ql in str(r['Brand']).lower() or ql in str(r['Description']).lower() or ql in str(r['Vehicle']).lower(), axis=1)]
else:
    results = df.head(50)

# --- Layout: results and cart ---
col1, col2 = st.columns([3,1])
with col1:
    st.markdown("### Search Parts")
    st.dataframe(results[['Brand','Vehicle','OE','Description','Stock','Price_AED']].rename(columns={'Price_AED':'Price (AED)'}), height=300)
with col2:
    st.markdown("### Cart")
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    # simple cart UI
    for i, item in enumerate(st.session_state.cart):
        st.write(f"{item['Brand']} | {item['OE']} | Qty: {item['Qty']} | Total: {item['Total']:.2f} AED")
    st.write("Grand Total: ", sum([it['Total'] for it in st.session_state.cart]))

# --- Add to cart (demo) ---
if st.button("Add first result to cart") and not results.empty:
    row = results.iloc[0]
    item = {'Brand':row['Brand'],'OE':row['OE'],'Qty':1,'Total':float(row['Price_AED'])}
    st.session_state.cart.append(item)
    st.experimental_rerun()

# --- Download cart as Excel ---
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Cart')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart)
    st.download_button("Download Cart (Excel)", data=to_excel(cart_df), file_name="cart.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# --- WhatsApp inquiry ---
if st.session_state.cart:
    msg = "Inquiry%20from%20Mohamed%20Ali%3A%0A"
    for it in st.session_state.cart:
        msg += f"{it['Brand']}%20OE%3A{it['OE']}%20Qty%3A{it['Qty']}%0A"
    wa_link = f"https://wa.me/971501234567?text={msg}"
    st.markdown(f'<a class="btn-whatsapp" href="{wa_link}" target="_blank">Send Inquiry on WhatsApp</a>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 Dynatrade Automotive LLC. WhatsApp: +971 50 123 4567 | Email: sales@dynatrade.ae")
