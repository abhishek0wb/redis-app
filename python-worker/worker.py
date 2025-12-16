import redis
import json
import google.generativeai as genai
import os

API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost") 
r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
print("🚀 AI Worker started... Ready to summarize.")

while True:
    task = r.brpop('job_queue')

    if task:
        queue_name_bytes, data_bytes = task
        
        try:
            data = json.loads(data_bytes.decode('utf-8'))
            
            user_text = data.get('text', 'No text provided')
            print(f"Received Text: {user_text[:50]}...") 
            print(" Asking Gemini to summarize...")
            
            response = model.generate_content(f"Summarize this in one sentence: {user_text}")
            ai_summary = response.text
            
            print(f" AI Summary: {ai_summary}")

            response_payload = json.dumps({
                "original_text": user_text,
                "summary": ai_summary
            })
            r.publish('job_result', response_payload)
            
        except json.JSONDecodeError as e:
            print(f"JSON Decoding Error: {e} on data: {data_bytes}")
            
        except Exception as e:
            print(f" Gemini API Error: {e}")
            
        print("---------------------------------------")