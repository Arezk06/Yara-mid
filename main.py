import streamlit as st
import requests

# ڕێکخستنی شێوەی وێبسایتەکە
st.set_page_config(page_title="YARA Cosmetics", page_icon="✨", layout="centered")

FIREBASE_URL = "https://yara-mid-default-rtdb.firebaseio.com"

st.title("✨ YARA Cosmetics")
st.markdown("---")

# وەرگرتنی لیستی براندەکان لە فایەربەیسەکەت
try:
    brands_data = requests.get(f"{FIREBASE_URL}/brands.json").json()
    if brands_data:
        brand_names = list(brands_data.keys())
        selected_brand = st.selectbox("براندێک هەڵبژێرە", brand_names)

        # وەرگرتنی بەرهەمەکانی ئەو براندە
        products = requests.get(f"{FIREBASE_URL}/products/{selected_brand}.json").json()
        
        if products:
            st.subheader(f"بەرهەمەکانی {selected_brand}")
            cols = st.columns(2) # نیشاندان بە دوو ستوون وەک ناو ئەپەکە
            
            for idx, (p_id, p_info) in enumerate(products.items()):
                with cols[idx % 2]:
                    st.image(p_info['image'], use_container_width=True)
                    st.write(f"**{p_info['name']}**")
                    st.write(f"Price: {p_info['price']} IQD")
                    if st.button(f"کڕین - {p_info['name']}", key=p_id):
                        st.success(f"{p_info['name']} زیادکرا بۆ سەبەتە")
    else:
        st.warning("هیچ براندێک نەدۆزرایەوە.")
except Exception as e:
    st.error("ناتوانرێت داتا لە داتابەیس وەرگیرێت.")
