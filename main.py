import streamlit as st
import requests
import webbrowser

# ڕێکخستنی سەرەتایی لاپەڕەکە
st.set_page_config(page_title="YARA Cosmetics", page_icon="✨", layout="wide")

FIREBASE_URL = "https://yara-mid-default-rtdb.firebaseio.com"
MY_PHONE = "07765123882"

# ستایلکردنی وێبسایتەکە بۆ ئەوەی لە ئەپ بچێت
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #008080; color: white; }
    .product-card { 
        background-color: white; 
        padding: 15px; 
        border-radius: 15px; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# دروستکردنی سەبەتەی کڕین لە میمۆریدا
if 'cart' not in st.session_state:
    st.session_state.cart = []

# نازناو (Header)
st.title("✨ YARA Cosmetics")
st.write("بەخێربێیت بۆ فرۆشگای یارا")

# بەشی براندەکان و بەرهەمەکان
tabs = st.tabs(["🏠 دوکان", "🛒 سەبەتەی کڕین"])

with tabs[0]:
    # وەرگرتنی براندەکان لە فایەربەیس
    try:
        brands = requests.get(f"{FIREBASE_URL}/brands.json").json()
        if brands:
            brand_list = list(brands.keys())
            selected_brand = st.selectbox("براندێک هەڵبژێرە:", ["هەمووی"] + brand_list)
            
            if selected_brand != "هەمووی":
                # نیشاندانی بەرهەمەکانی ئەو براندە
                prods = requests.get(f"{FIREBASE_URL}/products/{selected_brand}.json").json()
                if prods:
                    cols = st.columns(2) # دوو ستوون وەک ناو ئەپەکە
                    for idx, (id, p) in enumerate(prods.items()):
                        with cols[idx % 2]:
                            st.markdown(f"""
                                <div class="product-card">
                                    <img src="{p['image']}" width="100%">
                                    <h4>{p['name']}</h4>
                                    <p style="color: #008080; font-weight: bold;">{p['price']} IQD</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            qty = st.number_input(f"دانە ({p['name']})", min_value=1, value=1, key=f"qty_{id}")
                            if st.button(f"زیادکردن بۆ سەبەتە", key=f"btn_{id}"):
                                st.session_state.cart.append({"name": p['name'], "price": p['price'], "qty": qty})
                                st.success(f"{p['name']} زیادکرا!")
    except:
        st.error("پەیوەندی لەگەڵ داتابەیس نییە")

with tabs[1]:
    st.subheader("سەبەتەی کڕین")
    total = 0
    if st.session_state.cart:
        for item in st.session_state.cart:
            p_val = int(''.join(filter(str.isdigit, str(item['price']))))
            subtotal = p_val * item['qty']
            total += subtotal
            st.write(f"🛍️ **{item['name']}** - {item['qty']} دانە : {subtotal:,} IQD")
        
        st.divider()
        st.subheader(f"کۆی گشتی: {total:,} IQD")
        
        if st.button("پەیوەندی بکە بۆ داواکردن"):
            webbrowser.open(f"https://wa.me/{MY_PHONE.replace('0', '964', 1)}")
    else:
        st.write("سەبەتەکەت خاڵییە")
