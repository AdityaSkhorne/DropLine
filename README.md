# 🚀 DropLine: AI-Driven Universal Link Understanding Assistant

DropLine is an asynchronous Retrieval-Augmented Generation (RAG) system designed to solve the **"Signpost vs. Destination"** link accessibility bottleneck. It resolves wrapper links, extracts clean semantic content from web pages and YouTube transcripts, and synthesizes it into structured educational insights.

---

## 🧠 The Problem: Signpost vs. Destination
Modern web content is often hidden behind "signposts"—wrapper links, redirects, or placeholder URLs (e.g., Google Maps internal links). Standard AI scrapers fail because they attempt to process the signpost code rather than the intended destination data. 

**DropLine** solves this by implementing a two-step "Universal Link Resolver" that mimics human browsing to follow redirects and recover direct media or text content.

---

## 🛠️ Prerequisites
Ensure your device has the following installed:
* **Python 3.9+**: For the FastAPI backend and AI processing.
* **VS Code**: Your primary IDE for development.
* **Google Gemini API Key**: Required for the reasoning engine (Obtain from Google AI Studio).
* **Git**: For version control and repository management.

---

## 📥 Installation & Setup

1. **Clone the Project**:
   ```powershell
   git clone [https://github.com/AdityaSkhorne/DropLine.git](https://github.com/AdityaSkhorne/DropLine.git)
   cd DropLine


2. Create a Virtual Environment:
   ```PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install Dependencies:
   ```PowerShell
   pip install -r requirements.txt

4. Configure API Key:
   Open models/ai_engine.py and replace "YOUR_GEMINI_API_KEY" with your secret key from Google AI Studio.


🏃 How to Run (Step-by-Step)
To run DropLine, you must have two separate terminals running at the same time.

Step 1: Start the Backend (VS Code Terminal)
The backend handles URL resolution, content extraction, and AI inference.

   1. Open the terminal inside VS Code.

   2. Run: python main.py

   3. The server is ready when you see: Uvicorn running on http://127.0.0.1:8000.


Step 2: Start the Frontend (PowerShell as Administrator)
The frontend provides the interactive UI and session management.

   1. Search for PowerShell in the Windows Start menu.

   2. Right-click and select "Run as Administrator".

   3. Navigate to the project: cd D:\DropLine.

   4. Activate the environment: .\.venv\Scripts\Activate.  ps1.

   5. Run:
       ```PowerShell
           streamlit run frontend/app_ui.py --browser.gatherUsageStats false


✨ Key Features & Outputs
Universal Resolver: Asynchronous logic to follow 301/302 redirects and resolve placeholder links.

High-Precision Extraction: Using Trafilatura, we achieve ~15% content retention, removing 85% of web boilerplate/junk.

5-Point Pedagogical Framework:
   1. Concise Summary (3 sentences).
   2. Key Concepts (Taxonomy of terms).
   3. Teaching Mode (Analogy-based learning).
   4. Real-World Applications.
   5. Automated Quiz (Multiple-choice assessment).

Stateful Chatbot: Persistent conversation history using st.session_state for multi-turn grounded tutoring.



📂 Project Structure
backend/: Core FastAPI router (app.py).

frontend/: Streamlit user interface (app_ui.py).

extractors/: Specialized logic for Web, YouTube, and Universal Resolution.

models/: Pydantic schemas and Gemini prompt engineering.

utils/: Redirect handling and URL validation helpers.


### 🚀 To Push to GitHub:
Once you have saved the `README.md`, run these commands in your VS Code terminal to update your repository:
1.  `git add README.md`
2.  `git commit -m "Update README with Universal Resolver and Setup Guide"`
3.  `git push origin main`

Would you like me to help you draft the **"Troubleshooting"** section if you encounter any issues during the `git push`?