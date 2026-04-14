import streamlit as st
import mysql.connector
from openai import OpenAI
import os
from dotenv import load_dotenv
from decimal import Decimal
import base64

# =========================
# LOAD ENV VARIABLES
# =========================
load_dotenv()

# =========================
# OPENAI CLIENT (SECURE)
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================
# MYSQL CONNECTION
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Acernitro@5",
        database="amazon_project"
    )

# =========================
# BACKGROUND IMAGE FUNCTION
# =========================
def get_base64_image(image_file):
    with open(image_file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = get_base64_image("background.jpg")

# =========================
# APPLY BACKGROUND
# =========================
st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{bg_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    background: rgba(0, 0, 0, 0.75);
    padding: 2rem;
    border-radius: 15px;
}}

h1, h2, h3, p, label {{
    color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# FORMAT RESULT FUNCTION
# =========================
def format_result(result):
    try:
        # If single value (like SUM)
        if isinstance(result, tuple) and len(result) == 1:
            value = float(result[0])
            return f"👉 ${round(value/1_000_000, 2)} Million"

        # If multiple rows (like GROUP BY)
        formatted = []
        for row in result:
            name = str(row[0])

            try:
                value = float(row[1])
                value = round(value/1_000_000, 2)
                formatted.append(f"👉 {name}: ${value} Million")
            except:
                formatted.append(f"👉 {name}: {row[1]}")

        return "\n".join(formatted)

    except Exception as e:
        return f"Error formatting result: {e}"

# =========================
# ASK QUESTION FUNCTION
# =========================
def ask_question(question):
    prompt = f"""
You are an SQL expert.

Convert the following question into a valid MySQL query.
Table name: amazon_data

Columns:
user_id, product_id, category, subcategory, brand, price,
discount, final_price, rating, review_count, stock,
seller_id, seller_rating, purchase_date, shipping_time_days,
location, device, payment_method, is_returned, delivery_status

IMPORTANT RULES:
- Only return SQL query
- No markdown
- No explanation
- Use correct column names

Question: {question}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip()

    # Remove accidental markdown if any
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()

        return format_result(result)

    except Exception as e:
        return f"❌ Error: {str(e)}"

# =========================
# UI DESIGN
# =========================
st.title("🟠 AI Data Assistant")
st.subheader("📊 Ask questions about your Amazon Sales & Customer Insights Dashboard")

question = st.text_input("💬 Enter your question:")

st.markdown("### 💡 Try asking:")
st.write("- Total revenue")
st.write("- Top 5 categories by revenue")
st.write("- Orders by payment method")
st.write("- Average rating")
st.write("- Return rate")

if st.button("🚀 Get Answer"):
    if question:
        answer = ask_question(question)
        st.success(f"📊 Result:\n\n{answer}")
    else:
        st.warning("Please enter a question")

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📌 About")
st.sidebar.write("AI-powered analytics system built using:")
st.sidebar.write("• Python 🐍")
st.sidebar.write("• MySQL 🗄️")
st.sidebar.write("• OpenAI 🤖")
st.sidebar.write("• Streamlit 🌐")

st.sidebar.markdown("---")
st.sidebar.write("👨‍💻 Built by Aswin Jayakumar S 🚀")