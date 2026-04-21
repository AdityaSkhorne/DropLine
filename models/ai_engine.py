from google import genai
import time

# IMPORTANT: Put your actual Google AI Studio API key here
client = genai.Client(api_key="YOUR_GEMINI_API_KEY")

def generate_teaching_insights(text: str, max_retries=3):
    if not text or len(text) < 100:
        return None

    # --- THIS IS THE PROMPT ---
    # Whatever you write here controls exactly what the AI outputs on your website.
    prompt = f"""
    You are an expert teacher. Based on the following extracted webpage content, provide a beautifully formatted response with these exact 5 sections:

    ### 1. Concise Summary
    Provide a short, 3-sentence summary of the content.

    ### 2. Key Concepts
    List the most important vocabulary words or ideas mentioned in the text using bullet points.

    ### 3. 'Teaching Mode' Explanation
    Explain the main topic simply, using an analogy, as if I am a beginner.

    ### 4. Real-World Applications
    Give 2 or 3 practical examples of how the information in this link is used in real life or industry.

    ### 5. Test Your Knowledge (Quick Quiz)
    Provide 3 multiple-choice questions based on the text to test my understanding. Put the correct answers at the very bottom.
    
    Content: {text[:15000]} 
    """
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            
            return {
                "ai_teaching_mode": response.text
            }
            
        except Exception as e:
            error_message = str(e)
            if "503" in error_message or "429" in error_message or "UNAVAILABLE" in error_message:
                print(f"⚠️ Google server busy. Retrying in 3 seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(3)
            else:
                return {"error": error_message}
    
    return {"error": "Google Gemini servers are currently overloaded. Please try again in a few minutes."}



# ... (keep your existing generate_teaching_insights function)

def chat_with_document(text: str, question: str, max_retries=3):
    if not text:
        return {"error": "No document context available."}

    prompt = f"""
    You are a helpful AI tutor. Use the following document context to answer the student's question.
    If the answer is not in the document, politely say "I cannot find the answer to that in the provided link."
    
    Document Context: {text[:15000]}
    
    Student's Question: {question}
    """
    
    for attempt in range(max_retries):
        try:
            # Using the chat model to answer the specific question
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            return {"answer": response.text}
        except Exception as e:
            error_message = str(e)
            if "503" in error_message or "429" in error_message or "UNAVAILABLE" in error_message:
                time.sleep(3)
            else:
                return {"error": error_message}
                
    return {"error": "Google Gemini servers are overloaded. Please try again."}    