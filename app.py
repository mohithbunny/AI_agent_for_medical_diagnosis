import streamlit as st
import subprocess
import json
import os
st.set_page_config(page_title="Medical AI Agents", layout="centered")
st.title("🩺 AI Medical Diagnostic Agents")
st.write("Upload a medical report in plain text (or PDF), run the agents, and view combined analysis.")

# Upload
uploaded_file = st.file_uploader("Medical report (.txt or .pdf)", type=["txt","pdf"])
if uploaded_file:
    content = uploaded_file.read()
    try:
        text = content.decode("utf‑8")
    except:
        import PyPDF2
        reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n\n".join(page.extract_text() for page in reader.pages)
    
    st.subheader("Report Preview")
    st.text_area("", text, height=200)

    if st.button("🧠 Run Diagnostic Agents"):
        with st.spinner("Analyzing report with agents..."):
            proc = subprocess.run(
                ["python", "Main.py"], 
                env={**os.environ, "MEDICAL_REPORT": text}, 
                capture_output=True, text=True
            )
        if proc.returncode != 0:
            st.error("Agent execution failed:\n" + proc.stderr)
        else:
            try:
                print("printing")
                print(proc.stdout)
                print("parsing")
                print(json.loads(proc.stdout))
                results = json.loads(proc.stdout)
            except:
                st.error("Could not parse output, check Main.py structure.")
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
