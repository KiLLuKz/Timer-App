import os, sys
import webview
import threading
import time
from playsound import playsound

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def play_sound(file):
    threading.Thread(target=lambda: playsound(resource_path(file)), daemon=True).start()

class TimerAPI:
    def __init__(self):
        self.seconds = 0
        self.running = False
        self.countdown = False

    # --- Timer ปกติ ---
    def start_timer(self):
        if not self.running:
            self.running = True
            self.countdown = False
            threading.Thread(target=self.run_timer, daemon=True).start()
            play_sound("click.mp3")  # เล่นเสียงตอนกด Start
        return "Timer started"

    # --- Countdown ---
    def start_countdown(self, seconds):
        if not self.running:
            self.seconds = int(seconds)
            self.running = True
            self.countdown = True
            threading.Thread(target=self.run_timer, daemon=True).start()
            play_sound("click.mp3")  # เล่นเสียงตอนกด Start
        return "Countdown started"

    # --- หยุด ---
    def stop(self):
        self.running = False
        play_sound("click.mp3")  # เล่นเสียงตอนกด Stop
        return "Stopped"

    # --- รีเซ็ต ---
    def reset(self):
        self.running = False
        self.seconds = 0
        # อัปเดตเวลาในหน้าเว็บทันที
        if webview.windows:
            webview.windows[0].evaluate_js(
                f"document.getElementById('time').innerText = '{self.format_time()}'"
            )
        play_sound("click.mp3")  # เล่นเสียงตอนกด Reset
        return "Reset"

    # --- ลูปเวลา ---
    def run_timer(self):
        while self.running:
            time.sleep(1)
            if self.countdown:
                if self.seconds > 0:
                    self.seconds -= 1
                else:
                    self.running = False
                    play_sound("alarm.mp3")
            else:
                self.seconds += 1
            # อัปเดต HTML ผ่าน JS
            webview.windows[0].evaluate_js(
                f"document.getElementById('time').innerText = '{self.format_time()}'"
            )

    def format_time(self):
        h = self.seconds // 3600
        m = (self.seconds % 3600) // 60
        s = self.seconds % 60
        return f"{h:02d}:{m:02d}:{s:02d}"

# --- สร้างหน้าต่าง ---
api = TimerAPI()
webview.create_window("Timer App", resource_path("Timer.html"), js_api=api, width=800, height=600)
webview.start()
