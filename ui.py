import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import threading
import os
import sys
import time
from automation_core import get_driver, send_messages
from urllib.parse import quote


def app_dir():
    """Always returns the folder where the exe (or script) lives."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


MESSAGE_FILE = os.path.join(app_dir(), "message.txt")
NUMBERS_FILE = os.path.join(app_dir(), "numbers.txt")

# ── Palette ──────────────────────────────────────────────
BG          = "#1a1a2e"   # deep navy background
CARD        = "#16213e"   # card surface
ACCENT      = "#25D366"   # WhatsApp green
ACCENT2     = "#128C7E"   # darker teal for header
BTN_SAVE    = "#0d6efd"   # blue
BTN_EXIT    = "#dc3545"   # red
BTN_SEND    = "#25D366"   # green
BTN_READY   = "#10b981"   # emerald
BORDER      = "#0f3460"   # card border
FG          = "#e2e8f0"   # primary text
FG_DIM      = "#94a3b8"   # muted text
FG_GREEN    = "#4ade80"   # status green
FONT_MAIN   = ("Segoe UI", 9)
FONT_LABEL  = ("Segoe UI", 9, "bold")
FONT_TITLE  = ("Segoe UI", 14, "bold")
FONT_SMALL  = ("Segoe UI", 8)


def make_button(parent, text, command, bg, hover_bg, fg="white", width=None):
    """Flat modern button with hover effect."""
    cfg = dict(text=text, command=command, bg=bg, fg=fg,
               font=("Segoe UI", 9, "bold"), relief=tk.FLAT,
               cursor="hand2", padx=12, pady=6, bd=0,
               activebackground=hover_bg, activeforeground=fg)
    if width:
        cfg["width"] = width
    btn = tk.Button(parent, **cfg)
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn


def make_small_button(parent, text, command):
    """Compact inline button."""
    btn = tk.Button(parent, text=text, command=command,
                    font=FONT_SMALL, bg=BORDER, fg=FG_DIM,
                    relief=tk.FLAT, cursor="hand2", padx=8, pady=2, bd=0,
                    activebackground="#1e3a5f", activeforeground=FG)
    btn.bind("<Enter>", lambda e: btn.config(bg="#1e3a5f", fg=FG))
    btn.bind("<Leave>", lambda e: btn.config(bg=BORDER, fg=FG_DIM))
    return btn


class WhatsAppBulkMessengerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WA Bulk Messenger")
        self.root.geometry("730x1")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.is_running   = False
        self.driver       = None
        self.proceed_send = False
        self.status_text  = tk.StringVar(value="Ready")

        self._build()
        # Auto-fit window height to content
        self.root.update_idletasks()
        self.root.geometry(f"730x{self.root.winfo_reqheight()}")

    # ──────────────────────────────────────────────────────
    def _build(self):
        self._build_header()
        self._build_panels()
        self._build_statusbar()
        self._build_footer()
        self.load_default_message()
        self.load_default_numbers()
        self.update_info()

    # ── Header ────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=ACCENT2, height=52)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)

        # WhatsApp circle logo
        canvas = tk.Canvas(hdr, width=32, height=32, bg=ACCENT2,
                           highlightthickness=0)
        canvas.create_oval(2, 2, 30, 30, fill=ACCENT, outline="")
        canvas.create_text(16, 16, text="W", fill="white",
                           font=("Segoe UI", 13, "bold"))
        canvas.pack(side=tk.LEFT, padx=(14, 8), pady=10)

        tk.Label(hdr, text="WhatsApp Bulk Messenger",
                 font=FONT_TITLE, bg=ACCENT2, fg="white").pack(side=tk.LEFT, pady=10)

        tk.Label(hdr, text="Made by Harsh Gupta",
                 font=FONT_SMALL, bg=ACCENT2, fg="#a7f3d0").pack(side=tk.RIGHT, padx=16)

    # ── Two-column panels ─────────────────────────────────
    def _build_panels(self):
        row = tk.Frame(self.root, bg=BG)
        row.pack(fill=tk.X, expand=False, padx=14, pady=(12, 6))
        row.columnconfigure(0, weight=1)
        row.columnconfigure(1, weight=1)

        self.message_text = self._build_card(row, "✉  Message", 0,
                                             self.load_message_file,
                                             lambda: self.message_text.delete("1.0", tk.END))

        self.numbers_text = self._build_card(row, "📞  Phone Numbers", 1,
                                             self.load_numbers_file,
                                             lambda: self.numbers_text.delete("1.0", tk.END))

    def _build_card(self, parent, title, col, load_cmd, clear_cmd):
        # Outer card frame
        card = tk.Frame(parent, bg=CARD, bd=0, highlightthickness=1,
                        highlightbackground=BORDER)
        card.grid(row=0, column=col, sticky="nsew",
                  padx=(0, 7) if col == 0 else (7, 0))
        # Card header row
        top = tk.Frame(card, bg=CARD)
        top.pack(fill=tk.X, padx=10, pady=(8, 4))

        tk.Label(top, text=title, font=FONT_LABEL,
                 bg=CARD, fg=ACCENT).pack(side=tk.LEFT)

        make_small_button(top, "✕ Clear", clear_cmd).pack(side=tk.RIGHT, padx=(4, 0))
        make_small_button(top, "📂 Load", load_cmd).pack(side=tk.RIGHT)

        # Separator line
        tk.Frame(card, bg=BORDER, height=1).pack(fill=tk.X, padx=10)

        # Text area
        txt = scrolledtext.ScrolledText(
            card, height=8, wrap=tk.WORD,
            font=("Consolas", 9),
            bg="#0d1b2a", fg=FG,
            insertbackground=ACCENT,
            selectbackground=ACCENT2,
            relief=tk.FLAT, bd=8,
        )
        txt.pack(fill=tk.X, expand=False, padx=2, pady=2)
        txt.bind("<KeyRelease>", lambda e: self.update_info())
        return txt

    # ── Status bar ────────────────────────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self.root, bg=CARD, height=30,
                       highlightthickness=1, highlightbackground=BORDER)
        bar.pack(fill=tk.X, padx=14, pady=(0, 6))
        bar.pack_propagate(False)

        # Pulsing dot
        self.dot_canvas = tk.Canvas(bar, width=10, height=10,
                                    bg=CARD, highlightthickness=0)
        self.dot_canvas.pack(side=tk.LEFT, padx=(10, 4), pady=10)
        self._dot = self.dot_canvas.create_oval(1, 1, 9, 9, fill=FG_GREEN, outline="")

        self.status_lbl = tk.Label(bar, textvariable=self.status_text,
                                   font=FONT_SMALL, bg=CARD, fg=FG_GREEN, anchor="w")
        self.status_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Char / number counts
        self.chars_lbl = tk.Label(bar, text="0 chars", font=FONT_SMALL,
                                  bg=CARD, fg=FG_DIM)
        self.chars_lbl.pack(side=tk.RIGHT, padx=(0, 10))

        tk.Label(bar, text="│", bg=CARD, fg=BORDER).pack(side=tk.RIGHT)

        self.nums_lbl = tk.Label(bar, text="0 numbers", font=FONT_SMALL,
                                 bg=CARD, fg=FG_DIM)
        self.nums_lbl.pack(side=tk.RIGHT, padx=(0, 6))

    # ── Footer buttons ────────────────────────────────────
    def _build_footer(self):
        foot = tk.Frame(self.root, bg=BG)
        foot.pack(fill=tk.X, padx=14, pady=(0, 12))

        self.start_btn = make_button(foot, "🚀  Send Messages",
                                     self.start_sending, BTN_SEND, "#1DB954")
        self.start_btn.pack(side=tk.LEFT, padx=(0, 6))

        self.proceed_btn = make_button(foot, "✅  I'm Logged In – Go!",
                                       self.proceed_after_login, BTN_READY, "#059669")
        # hidden by default

        make_button(foot, "💾  Save",  self.save_to_files,
                    BTN_SAVE, "#0b5ed7").pack(side=tk.LEFT, padx=(0, 6))

        make_button(foot, "✕  Exit",   self.root.quit,
                    BTN_EXIT, "#b02a37").pack(side=tk.LEFT)

    # ──────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────
    def set_status(self, msg, color=FG_GREEN):
        self.status_text.set(msg)
        self.status_lbl.config(fg=color)
        self.dot_canvas.itemconfig(self._dot, fill=color)

    def update_info(self):
        msg  = self.message_text.get("1.0", tk.END).strip()
        nums = [n for n in self.numbers_text.get("1.0", tk.END).splitlines() if n.strip()]
        self.chars_lbl.config(text=f"{len(msg)} chars")
        self.nums_lbl.config(text=f"{len(nums)} numbers")

    def load_default_message(self):
        try:
            if os.path.exists(MESSAGE_FILE):
                self.message_text.insert("1.0", open(MESSAGE_FILE, encoding="utf8").read())
        except Exception as e:
            print(e)

    def load_default_numbers(self):
        try:
            if os.path.exists(NUMBERS_FILE):
                self.numbers_text.insert("1.0", open(NUMBERS_FILE).read())
        except Exception as e:
            print(e)

    def load_message_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            try:
                self.message_text.delete("1.0", tk.END)
                self.message_text.insert("1.0", open(path, encoding="utf8").read())
                self.set_status(f"Loaded {os.path.basename(path)}")
                self.update_info()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_numbers_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("CSV", "*.csv"), ("All", "*.*")])
        if path:
            try:
                self.numbers_text.delete("1.0", tk.END)
                self.numbers_text.insert("1.0", open(path).read())
                self.set_status(f"Loaded {os.path.basename(path)}")
                self.update_info()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_to_files(self):
        msg  = self.message_text.get("1.0", tk.END).strip()
        nums = self.numbers_text.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("Empty", "Message is empty!"); return
        if not nums:
            messagebox.showwarning("Empty", "No phone numbers!"); return
        open(MESSAGE_FILE, "w", encoding="utf8").write(msg)
        open(NUMBERS_FILE, "w").write(nums)
        self.set_status("Files saved ✓")

    # ──────────────────────────────────────────────────────
    # Sending logic
    # ──────────────────────────────────────────────────────
    def proceed_after_login(self):
        self.proceed_send = True
        self.proceed_btn.pack_forget()
        self.start_btn.config(state=tk.NORMAL)

    def start_sending(self):
        msg  = self.message_text.get("1.0", tk.END).strip()
        nums = [n.strip() for n in self.numbers_text.get("1.0", tk.END).splitlines() if n.strip()]
        if not msg:
            messagebox.showwarning("Missing", "Enter a message first!"); return
        if not nums:
            messagebox.showwarning("Missing", "Enter at least one number!"); return

        if not messagebox.askyesno("Confirm",
                f"Send to {len(nums)} numbers?\n\nChrome will open for WhatsApp Web login."):
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.set_status("Initializing Chrome…", "#facc15")
        threading.Thread(target=self._send_thread,
                         args=(quote(msg), nums), daemon=True).start()

    def _send_thread(self, message, numbers):
        try:
            self.set_status("Opening WhatsApp Web…", "#facc15")
            driver = get_driver()
            self.driver = driver
            driver.get("https://web.whatsapp.com")

            self.set_status("⏳ Waiting for login — click the button when ready!", "#facc15")
            self.proceed_send = False
            self.proceed_btn.pack(side=tk.LEFT, padx=(0, 6), before=self.start_btn)

            t = 0
            while not self.proceed_send and t < 6000:
                self.root.update()
                time.sleep(0.1)
                t += 1

            if not self.proceed_send:
                raise Exception("Login timeout (10 min). Please restart and try again.")

            self.set_status(f"Sending… 0 / {len(numbers)}", "#facc15")
            send_messages(driver, numbers, message)

            driver.close()
            self.set_status(f"✅ Done! Sent to {len(numbers)} numbers.", FG_GREEN)
            messagebox.showinfo("Done", f"Messages sent to {len(numbers)} numbers!")

        except Exception as e:
            self.set_status("❌ Error", "#f87171")
            messagebox.showerror("Error", str(e))
        finally:
            self.is_running    = False
            self.proceed_send  = False
            self.proceed_btn.pack_forget()
            self.start_btn.config(state=tk.NORMAL)
            if self.driver:
                try: self.driver.close()
                except: pass


def main():
    root = tk.Tk()
    app = WhatsAppBulkMessengerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

