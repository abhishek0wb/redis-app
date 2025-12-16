import redis
import json
import google.generativeai as genai
import os

# CONFIGURATION
# Best practice: Use environment variables, but for now paste it here# 1. READ API KEY FROM ENVIRONMENT VARIABLE
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    # Fail fast if key is missing (good practice)
    print("🚨 ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost") 
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
print("🚀 AI Worker started... Ready to summarize.")

while True:
    # BRPOP returns a tuple: (queue_name_bytes, data_bytes)
    task = r.brpop('job_queue')

    if task:
        # Extract the data element (the second element of the tuple)
        queue_name_bytes, data_bytes = task
        
        try:
            # Decode the bytes to a string, then parse the JSON
            # This is the line that caused the original error, now inside a try/except block
            data = json.loads(data_bytes.decode('utf-8'))
            
            user_text = data.get('text', 'No text provided')
            print(f"📥 Received Text: {user_text[:50]}...") # Print first 50 chars safely
            
            # 1. CALL REAL AI
            print("🧠 Asking Gemini to summarize...")
            
            # Ensure the full text is sent to the model for summarization
            response = model.generate_content(f"Summarize this in one sentence: {user_text}")
            ai_summary = response.text
            
            print(f"✅ AI Summary: {ai_summary}")

            # 2. SEND BACK TO NESTJS
            response_payload = json.dumps({
                "original_text": user_text,
                "summary": ai_summary
            })
            r.publish('job_result', response_payload)
            
        except json.JSONDecodeError as e:
            # Log the specific error and continue waiting for the next job
            print(f"🚨 JSON Decoding Error: {e} on data: {data_bytes}")
            
        except Exception as e:
            # Handle API errors, network issues, etc.
            print(f"❌ Gemini API Error: {e}")
            
        print("---------------------------------------")