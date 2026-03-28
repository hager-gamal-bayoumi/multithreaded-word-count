Install Gradio

!pip install gradio

import gradio as gr
import time
from concurrent.futures import ThreadPoolExecutor

🔹 Function to count words in a chunk

def count_words(chunk):
return len(chunk.split())

🔹 Split text into chunks (by words - correct way)

def split_text(text, num_threads):
words = text.split()
chunk_size = len(words) // num_threads

chunks = []  
for i in range(num_threads):  
    start = i * chunk_size  
    if i == num_threads - 1:  
        end = len(words)  
    else:  
        end = (i + 1) * chunk_size  

    chunk = " ".join(words[start:end])  
    chunks.append(chunk)  

return chunks

🔹 Single-threaded word count

def single_thread(text):
start = time.time()
count = len(text.split())
end = time.time()
return count, end - start

🔹 Multi-threaded word count

def multi_thread(text, num_threads=4):
chunks = split_text(text, num_threads)

start = time.time()  
with ThreadPoolExecutor(max_workers=num_threads) as executor:  
    results = executor.map(count_words, chunks)  

total = sum(results)  
end = time.time()  

return total, end - start

🔥 Main function for Gradio

def process_file(file):
if file is None:
return "❌ Please upload a file"

try:  
    # 📌 If Gradio returns a file path  
    if isinstance(file, str):  
        with open(file, "r", encoding="utf-8") as f:  
            text = f.read()  
    else:  
        # 📌 If it's a file object  
        text = file.read().decode("utf-8")  

    # Single-thread result  
    single_count, single_time = single_thread(text)  

    # Multi-thread result  
    multi_count, multi_time = multi_thread(text)  

    return f"""

📊 Results:

🔹 Single Thread:
Word Count: {single_count}
Time: {single_time:.4f} seconds

🔹 Multi Thread:
Word Count: {multi_count}
Time: {multi_time:.4f} seconds
"""

except Exception as e:  
    return f"❌ Error occurred: {str(e)}"

🎨 Gradio Interface

interface = gr.Interface(
fn=process_file,
inputs=gr.File(label="📂 Upload TXT File"),
outputs="text",
title="🔥 Multithreaded Word Count",
description="Upload a text file to count words and compare performance"
)

Launch (important for Colab)

interface.launch(share=True)
