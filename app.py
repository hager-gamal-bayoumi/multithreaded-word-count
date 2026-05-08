# =====================================================
# IMPORTS
# =====================================================
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread, Lock
from queue import Queue
import multiprocessing
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =====================================================
# MODEL
# =====================================================
class WordCounterModel:
    def __init__(self):
        self.queue = Queue()
        self.lock = Lock()

    def read_file(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def split_text(self, text, n):
        words = text.split()
        if n <= 0: n = 1
        n = min(n, len(words))
        chunk_size = len(words) // n
        chunks = []
        for i in range(n):
            start = i * chunk_size
            end = len(words) if i == n - 1 else (i + 1) * chunk_size
            chunks.append(words[start:end])
        return chunks

    def producer(self, chunks):
        for chunk in chunks:
            self.queue.put(chunk)
        for _ in range(len(chunks)):
            self.queue.put(None)

    def consumer(self, result):
        while True:
            chunk = self.queue.get()
            if chunk is None:
                self.queue.task_done()
                break
            count = len(chunk)
            with self.lock:
                result.append(count)
            self.queue.task_done()

# =====================================================
# STRATEGY PATTERN
# =====================================================
class ThreadStrategy:
    def get_threads(self): pass

class ManualThreadStrategy(ThreadStrategy):
    def __init__(self, value): self.value = value
    def get_threads(self): return int(self.value)

class AutoThreadStrategy(ThreadStrategy):
    def get_threads(self): return multiprocessing.cpu_count()

# =====================================================
# VIEW
# =====================================================
class AppView:
    def __init__(self, root):
        self.root = root
        self.root.title("Multithreaded Word Count 🔥")
        self.root.geometry("1300x820") # زيادة طفيفة في الحجم الكلي
        self.root.configure(bg="#0f172a")
        self.build_ui()

    def build_ui(self):
        # 1. تقليل المسافة العلوية (العنوان)
        title = tk.Label(
            self.root,
            text="Multithreaded Word Count 🔥",
            font=("Segoe UI", 24, "bold"),
            fg="#38bdf8",
            bg="#0f172a"
        )
        title.pack(pady=(15, 5))

        # ================= TOP FRAME (إعدادات مضغوطة) =================
        self.top_frame = tk.Frame(self.root, bg="#172554")
        self.top_frame.pack(fill="x", padx=30, pady=5)

        # ملف (تصغير الارتفاع)
        self.file_frame = tk.Frame(self.top_frame, bg="#1e293b", height=70, highlightbackground="#38bdf8", highlightthickness=2, cursor="hand2")
        self.file_frame.pack(fill="x", padx=20, pady=10)
        self.file_frame.pack_propagate(False)

        self.file_label = tk.Label(self.file_frame, text="📂 Click To Select TXT File", font=("Segoe UI", 13), fg="white", bg="#1e293b", cursor="hand2")
        self.file_label.place(relx=0.5, rely=0.5, anchor="center")

        # خيارات (Options)
        self.options_frame = tk.Frame(self.top_frame, bg="#172554")
        self.options_frame.pack(fill="x", padx=20, pady=5)

        self.mode_var = tk.StringVar(value="manual")
        self.manual_radio = tk.Radiobutton(self.options_frame, text="Manual Threads", variable=self.mode_var, value="manual", command=self.toggle_thread_mode, font=("Segoe UI", 10), bg="#172554", fg="white", selectcolor="#1e293b", activebackground="#172554")
        self.manual_radio.pack(side="left", padx=10)

        self.auto_radio = tk.Radiobutton(self.options_frame, text="Auto Threads", variable=self.mode_var, value="auto", command=self.toggle_thread_mode, font=("Segoe UI", 10), bg="#172554", fg="white", selectcolor="#1e293b", activebackground="#172554")
        self.auto_radio.pack(side="left", padx=10)

        self.thread_label = tk.Label(self.options_frame, text="Workers: 5", font=("Segoe UI", 11, "bold"), bg="#172554", fg="white")
        self.thread_label.pack(side="right", padx=10)

        # سلايدر (تصغير المسافات)
        self.slider = tk.Scale(self.top_frame, from_=1, to=32, orient="horizontal", bg="#172554", fg="white", troughcolor="#334155", activebackground="#38bdf8", highlightthickness=0, command=self.update_slider)
        self.slider.set(5)
        self.slider.pack(fill="x", padx=20, pady=5)

        # زر البداية والبروجرس بار (دمجهم في سطر واحد لتوفير مساحة)
        action_frame = tk.Frame(self.top_frame, bg="#172554")
        action_frame.pack(fill="x", padx=20, pady=10)

        self.progress = ttk.Progressbar(action_frame, mode="indeterminate")
        self.progress.pack(side="left", fill="x", expand=True, padx=(0, 20))

        self.start_btn = tk.Button(action_frame, text="🚀 START", font=("Segoe UI", 11, "bold"), bg="#38bdf8", fg="black", padx=40, pady=5, cursor="hand2", relief="flat")
        self.start_btn.pack(side="right")

        # ================= CONTENT AREA (تكبير النتائج) =================
        self.content_frame = tk.Frame(self.root, bg="#0f172a")
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        # Chart
        self.chart_frame = tk.Frame(self.content_frame, bg="#172554")
        self.chart_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Result Frame (توسيع العرض لـ 480 لضمان ظهور الكلام)
        self.result_frame = tk.Frame(self.content_frame, bg="#172554", width=480)
        self.result_frame.pack(side="right", fill="both", expand=False)
        self.result_frame.pack_propagate(False)

        result_title = tk.Label(self.result_frame, text="📊 Results", font=("Segoe UI", 20, "bold"), fg="white", bg="#172554")
        result_title.pack(pady=15)

        # مستطيل النتائج (تكبيره ليكون واضحاً)
        self.result_box = tk.Frame(self.result_frame, bg="#020617")
        self.result_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.result_text = tk.Label(
            self.result_box,
            text="No Analysis Done Yet",
            justify="left",
            font=("Consolas", 13), # خط مريح للبيانات
            fg="#e2e8f0",
            bg="#020617",
            wraplength=420 # لضمان عدم خروج النص عن المستطيل
        )
        self.result_text.pack(anchor="nw", padx=20, pady=25)

    def update_slider(self, value):
        if self.mode_var.get() == "manual":
            self.thread_label.config(text=f"Workers: {value}")

    def toggle_thread_mode(self):
        mode = self.mode_var.get()
        if mode == "auto":
            self.slider.config(state="disabled")
            self.thread_label.config(text=f"Workers: AUTO ({multiprocessing.cpu_count()})")
        else:
            self.slider.config(state="normal")
            self.thread_label.config(text=f"Workers: {self.slider.get()}")

# =====================================================
# CONTROLLER
# =====================================================
class Controller:
    def __init__(self, root):
        self.model = WordCounterModel()
        self.view = AppView(root)
        self.file_path = None

        self.view.file_frame.bind("<Button-1>", self.choose_file)
        self.view.file_label.bind("<Button-1>", self.choose_file)
        self.view.start_btn.config(command=self.start_processing)

    def choose_file(self, event=None):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if path:
            self.file_path = path
            filename = path.split("/")[-1]
            self.view.file_label.config(text=f"✅ {filename}")

    def start_processing(self):
        if not self.file_path:
            messagebox.showerror("Error", "Please select a file first")
            return
        self.view.progress.start()
        Thread(target=self.process, daemon=True).start()

    def process(self):
        mode = self.view.mode_var.get()
        strategy = ManualThreadStrategy(self.view.slider.get()) if mode == "manual" else AutoThreadStrategy()
        threads_count = strategy.get_threads()

        text = self.model.read_file(self.file_path)

        # Single Thread
        start_single = time.time()
        single_count = len(text.split())
        single_time = (time.time() - start_single) * 1000

        # Multi Thread
        chunks = self.model.split_text(text, threads_count)
        results = []
        start_multi = time.time()
        self.model.producer(chunks)
        
        workers = []
        for _ in range(len(chunks)):
            t = Thread(target=self.model.consumer, args=(results,))
            t.start()
            workers.append(t)

        self.model.queue.join()
        for worker in workers: worker.join()
        
        multi_time = (time.time() - start_multi) * 1000
        multi_count = sum(results)
        speedup = single_time / multi_time if multi_time > 0 else 0

        self.view.root.after(0, lambda: self.update_ui(threads_count, single_count, multi_count, single_time, multi_time, speedup))

    def update_ui(self, threads, s_count, m_count, s_time, m_time, speedup):
        self.view.progress.stop()
        res = (
            #f"=========== RESULTS ===========\n\n"
            f"Threads Used       : {threads}\n\n"
            f"Single Word Count  : {s_count:,}\n"
            f"Multi Word Count   : {m_count:,}\n\n"
            f"Single Thread Time : {s_time:.3f} ms\n"
            f"Multi Thread Time  : {m_time:.3f} ms\n\n"
            f"Time Difference    : {abs(s_time-m_time):.3f} ms\n"
            f"Speed Performance  : {speedup:.2f}x ⚡\n\n"
            #f"================================"
        )
        self.view.result_text.config(text=res)
        self.draw_chart(s_time, m_time)

    def draw_chart(self, single, multi):
        for widget in self.view.chart_frame.winfo_children(): widget.destroy()
        fig, ax = plt.subplots(figsize=(5, 4), dpi=100)
        bars = ax.bar(["Single Thread", "Multi Thread"], [single, multi], color=['#334155', '#38bdf8'])
        ax.set_title("Time Comparison (ms)", color="white", pad=15)
        fig.patch.set_facecolor("#172554")
        ax.set_facecolor("#172554")
        ax.tick_params(colors='white')
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{height:.1f}ms', ha='center', va='bottom', color='white')
        canvas = FigureCanvasTkAgg(fig, master=self.view.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# =====================================================
# EXECUTION
# =====================================================
if __name__ == "__main__":
    root = tk.Tk()
    Controller(root)
    root.mainloop()
