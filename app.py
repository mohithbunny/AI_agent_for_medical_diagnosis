import streamlit as st
import json
from Main import run_agents   # ✅ Import function directly

st.set_page_config(page_title="Medical AI Agents", layout="centered")
st.title("🩺 AI Medical Diagnostic Agents")
st.write("Upload a medical report in plain text (or PDF), run the agents, and view combined analysis.")

uploaded_file = st.file_uploader("Medical report (.txt or .pdf)", type=["txt","pdf"])
if uploaded_file:
    content = uploaded_file.read()
    try:
        text = content.decode("utf-8")
    except:
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n\n".join(page.extract_text() for page in reader.pages)

    st.subheader("Report Preview")
    st.text_area("", text, height=200)

    if st.button("🧠 Run Diagnostic Agents"):
        with st.spinner("Analyzing report with agents..."):
            try:
                results = run_agents(text)   # ✅ Call directly
            except Exception as e:
                st.error(f"Agent execution failed: {e}")
            else:
                st.success("✅ Agents completed")

                st.header("🫀 Cardiologist Agent")
                st.write(results["cardiologist"])

                st.header("🫁 Pulmonologist Agent")
                st.write(results["pulmonologist"])

                st.header("🧠 Psychologist Agent")
                st.write(results["psychologist"])

                st.header("📝 Combined Summary")
                st.write(results["summary"])
