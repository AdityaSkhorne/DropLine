import streamlit as st
import requests

st.set_page_config(page_title="DropLine AI", page_icon="🚀", layout="centered")

# --- Initialize Memory (Session State) ---
if "context_text" not in st.session_state:
    st.session_state.context_text = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

st.title("🚀 DropLine: Interactive Link Tutor")
st.markdown("Paste a link, get the insights, and then chat with the AI about it!")

# --- Top Section: Analyze the Link ---
url_input = st.text_input("Enter Web or YouTube Link:")

if st.button("Analyze Link"):
    if url_input:
        # Clear old memory when a new link is analyzed
        st.session_state.chat_history = []
        st.session_state.context_text = ""
        st.session_state.analysis_data = None
        
        with st.spinner("DropLine AI is reading the web..."):
            try:
                response = requests.post("http://127.0.0.1:8000/analyze", json={"url": url_input})
                if response.status_code == 200:
                    data = response.json()
                    
                    # Save the data into Memory!
                    st.session_state.analysis_data = data
                    st.session_state.context_text = data.get("full_text", "")
                    
                    st.success("Analysis Complete! You can now chat with this document below.")
                else:
                    st.error(f"Server Error: {response.status_code}")
            except Exception as e:
                st.error(f"Failed to connect to backend. Error: {e}")

# --- Middle Section: Display the Report ---
if st.session_state.analysis_data:
    data = st.session_state.analysis_data
    st.subheader(f"📄 {data.get('title', 'Unknown Title')}")
    st.caption(f"Platform: {data.get('platform', '').upper()} | Content Type: {data.get('content_type', '').upper()}")
    
    with st.expander("Show AI Teacher Insights", expanded=True):
        analysis = data.get("analysis", {})
        if analysis and "ai_teaching_mode" in analysis:
            st.markdown(analysis["ai_teaching_mode"])
        elif analysis and "error" in analysis:
            st.error(f"AI Error: {analysis['error']}")

    st.divider()

    # --- Bottom Section: The Continuous Chatbot ---
    st.subheader("💬 Ask Follow-up Questions")
    
    # Draw all previous chat messages
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input Box
    user_question = st.chat_input("Ask anything about this link...")
    
    if user_question:
        # 1. Add user question to UI
        with st.chat_message("user"):
            st.markdown(user_question)
        st.session_state.chat_history.append({"role": "user", "content": user_question})

        # 2. Ask the Backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_payload = {
                    "context_text": st.session_state.context_text,
                    "question": user_question
                }
                chat_res = requests.post("http://127.0.0.1:8000/chat", json=chat_payload)
                
                if chat_res.status_code == 200:
                    answer_data = chat_res.json()
                    if answer_data.get("error"):
                        st.error(answer_data["error"])
                    else:
                        st.markdown(answer_data["answer"])
                        st.session_state.chat_history.append({"role": "assistant", "content": answer_data["answer"]})
                else:
                    st.error("Failed to get a response from the server.")