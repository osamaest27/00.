import streamlit as st
import os
import base64
from agent import run_agent, load_memory

# 1. إعداد الصفحة (يجب أن يكون أول أمر)
st.set_page_config(page_title="Sivar AI Pro", layout="wide")

# 2. تعريف المسار الأساسي
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 3. دالة تحميل ملف الـ CSS الخارجي
def load_css(file_name):
    file_path = os.path.join(BASE_DIR, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 4. دالة تطبيق الخلفية
def apply_background(image_name):
    image_path = os.path.join(BASE_DIR, image_name)
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# تنفيذ التنسيقات
load_css("style.css")
apply_background('background.jpg')

# 5. الواجهة البرمجية
st.title("est27 🗿")

valid_extensions = ('.py', '.txt', '.json', '.dart')
files_in_dir = [f for f in os.listdir(BASE_DIR) if f.endswith(valid_extensions)]

st.subheader("إعدادات السياق")
selected_file = st.selectbox("اختر ملفاً لتحليله:", ["لا يوجد"] + files_in_dir)

full_path = os.path.join(BASE_DIR, selected_file) if selected_file != "لا يوجد" else None

st.divider()
user_prompt = st.text_input("أدخل أمرك البرمجي هنا:")

if st.button("تنفيذ الأمر"):
    if not user_prompt:
        st.warning("يرجى كتابة أمر أولاً!")
    else:
        with st.spinner('المساعد الذكي يحلل الكود...'):
            try:
                result = run_agent(user_prompt, full_path)
                st.success("النتيجة:")
                st.markdown(result)
            except Exception as e:
                st.error(f"خطأ: {e}")

# 6. القائمة الجانبية
with st.sidebar:
    st.header("سجل الأوامر")
    memory = load_memory()
    for item in memory[-5:]:
        st.info(f"**س:** {item['user']}")