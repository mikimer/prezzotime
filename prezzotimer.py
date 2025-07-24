import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class PrezzotimerApp:
    def __init__(self, root):
        self.root = root
        root.title('Prezzotimer')
        root.geometry('400x300')

        # Set default start time to next half hour or hour
        now = datetime.now()
        if now.minute < 30:
            default_start = now.replace(minute=30, second=0, microsecond=0)
        else:
            default_start = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        default_start_str = default_start.strftime('%H:%M')

        # self.input_frame is the input/setup screen
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(expand=True)

        # Duration
        tk.Label(self.input_frame, text='Presentation Duration (minutes):').grid(row=0, column=0, sticky='e')
        self.duration_var = tk.StringVar()
        tk.Entry(self.input_frame, textvariable=self.duration_var).grid(row=0, column=1)

        # Total slides
        tk.Label(self.input_frame, text='Total Slides:').grid(row=1, column=0, sticky='e')
        self.slides_var = tk.StringVar()
        tk.Entry(self.input_frame, textvariable=self.slides_var).grid(row=1, column=1)

        # Start time (default to next half hour or hour)
        tk.Label(self.input_frame, text='Start Time (HH:MM, 24h):').grid(row=2, column=0, sticky='e')
        self.start_time_var = tk.StringVar(value=default_start_str)
        tk.Entry(self.input_frame, textvariable=self.start_time_var).grid(row=2, column=1)

        # Start button
        self.start_button = tk.Button(self.input_frame, text='Start Timer', command=self.start_timer)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        # self.timer_frame is the timer/main screen
        self.timer_frame = tk.Frame(root)
        self.timer_label = tk.Label(self.timer_frame, text='Timer will appear here', font=('Arial', 24))
        self.timer_label.pack(pady=20)
        self.slide_label = tk.Label(self.timer_frame, text='Ideal Slide: --', font=('Arial', 18))
        self.slide_label.pack()

        self.elapsed_label = tk.Label(self.timer_frame, text='', font=('Arial', 14))
        self.elapsed_label.pack(pady=5)

        self.timer_running = False

    def start_timer(self):
        try:
            self.duration_minutes = float(self.duration_var.get())
            self.total_slides = int(self.slides_var.get())
            start_time_str = self.start_time_var.get().strip().lower().replace(' ', '')
            # Accept 4-digit times like '1400' and convert to '14:00'
            if len(start_time_str) == 4 and start_time_str.isdigit():
                start_time_str = start_time_str[:2] + ':' + start_time_str[2:]
            # Accept times like '2pm', '2:30pm', '2pm', '2:30pm', etc.
            elif 'am' in start_time_str or 'pm' in start_time_str:
                # Remove am/pm for parsing
                ampm = 'am' if 'am' in start_time_str else 'pm'
                time_part = start_time_str.replace('am', '').replace('pm', '')
                if ':' in time_part:
                    hour, minute = time_part.split(':')
                else:
                    hour, minute = time_part, '00'
                hour = int(hour)
                minute = int(minute)
                if ampm == 'pm' and hour != 12:
                    hour += 12
                if ampm == 'am' and hour == 12:
                    hour = 0
                start_time_str = f'{hour:02d}:{minute:02d}'
            now = datetime.now()
            start_time = datetime.strptime(start_time_str, '%H:%M').replace(year=now.year, month=now.month, day=now.day)
            # If start time is in the past, use now
            if start_time < now:
                self.start_time = now
            else:
                self.start_time = start_time
            self.end_time = self.start_time + timedelta(minutes=self.duration_minutes)
        except Exception as e:
            self.timer_label.config(text=f'Input error: {e}')
            self.input_frame.pack_forget()
            self.timer_frame.pack(expand=True)
            return

        self.input_frame.pack_forget()
        self.timer_frame.pack(expand=True)
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        now = datetime.now()
        elapsed = now - self.start_time
        total_seconds = self.duration_minutes * 60
        elapsed_seconds = elapsed.total_seconds()
        if elapsed_seconds < 0:
            elapsed_seconds = 0
        if elapsed_seconds > total_seconds:
            elapsed_seconds = total_seconds
            self.timer_running = False
        # Format elapsed time
        elapsed_str = str(timedelta(seconds=int(elapsed_seconds)))
        self.elapsed_label.config(text=f'Elapsed: {elapsed_str}')
        # Calculate ideal slide
        ideal_slide = int(round((elapsed_seconds / total_seconds) * self.total_slides))
        if ideal_slide < 1:
            ideal_slide = 1
        if ideal_slide > self.total_slides:
            ideal_slide = self.total_slides
        self.timer_label.config(text=f'Ideal Slide: {ideal_slide}')
        self.slide_label.config(text=f'Time Remaining: {str(timedelta(seconds=int(total_seconds - elapsed_seconds)))}')
        if self.timer_running:
            self.root.after(1000, self.update_timer)

if __name__ == '__main__':
    root = tk.Tk()
    app = PrezzotimerApp(root)
    root.mainloop() 