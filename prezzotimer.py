import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

class PrezzotimerApp:
    """
    PrezzotimerApp is a Tkinter-based timer for pacing slide presentations.
    It helps presenters keep on track by showing the ideal slide number based on elapsed time.
    """
    def __init__(self, root):
        """
        Initialize the PrezzotimerApp with input and timer screens.
        """
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
        self.duration_var = tk.StringVar(value='10')  # Default for development
        tk.Entry(self.input_frame, textvariable=self.duration_var).grid(row=0, column=1)

        # Total slides
        tk.Label(self.input_frame, text='Total Slides:').grid(row=1, column=0, sticky='e')
        self.slides_var = tk.StringVar(value='100')  # Default for development
        tk.Entry(self.input_frame, textvariable=self.slides_var).grid(row=1, column=1)

        # Start time (default to next half hour or hour)
        tk.Label(self.input_frame, text='Start Time (HH:MM, 24h):').grid(row=2, column=0, sticky='e')
        self.start_time_var = tk.StringVar(value=default_start_str)
        tk.Entry(self.input_frame, textvariable=self.start_time_var).grid(row=2, column=1)

        # Buffer
        tk.Label(self.input_frame, text='Buffer (minutes, end early):').grid(row=3, column=0, sticky='e')
        self.buffer_var = tk.StringVar(value='10')  # Default buffer
        tk.Entry(self.input_frame, textvariable=self.buffer_var).grid(row=3, column=1)

        # Start button
        self.start_button = tk.Button(self.input_frame, text='Start Timer', command=self.start_timer)
        self.start_button.grid(row=4, column=0, columnspan=2, pady=10)

        # self.timer_frame is the timer/main screen
        self.timer_frame = tk.Frame(root)
        self.timer_label = tk.Label(self.timer_frame, text='Timer will appear here', font=('Arial', 24))
        self.timer_label.pack(pady=20)
        self.slide_label = tk.Label(self.timer_frame, text='Ideal Slide: --', font=('Arial', 18))
        self.slide_label.pack()

        self.elapsed_label = tk.Label(self.timer_frame, text='', font=('Arial', 14))
        self.elapsed_label.pack(pady=5)

        self.timer_running = False

    def parse_start_time(self, start_time_str):
        """
        Parse the start time string into a datetime object (24h or 12h format).
        Accepts '1400', '14:00', '2pm', '2:30pm', '2.20', etc.
        """
        s = start_time_str.strip().lower().replace(' ', '')
        # Handle '2.20' or '14.20' as '2:20' or '14:20'
        if '.' in s and s.replace('.', '').isdigit():
            parts = s.split('.')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                s = f'{int(parts[0])}:{int(parts[1]):02d}'
        if len(s) == 4 and s.isdigit():
            s = s[:2] + ':' + s[2:]
        elif 'am' in s or 'pm' in s:
            ampm = 'am' if 'am' in s else 'pm'
            time_part = s.replace('am', '').replace('pm', '')
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
            s = f'{hour:02d}:{minute:02d}'
        now = datetime.now()
        return datetime.strptime(s, '%H:%M').replace(year=now.year, month=now.month, day=now.day)

    def calculate_ideal_slide(self, elapsed_seconds, total_seconds, total_slides):
        """
        Calculate the ideal slide number based on elapsed time.
        """
        ideal_slide = int(round((elapsed_seconds / total_seconds) * total_slides))
        if ideal_slide < 1:
            ideal_slide = 1
        if ideal_slide > total_slides:
            ideal_slide = total_slides
        return ideal_slide

    def start_timer(self):
        """
        Start the timer using user input, switch to timer screen, and begin updates.
        """
        try:
            self.duration_minutes = float(self.duration_var.get())
            self.total_slides = int(self.slides_var.get())
            self.buffer_minutes = float(self.buffer_var.get())
            effective_duration = self.duration_minutes - self.buffer_minutes
            if effective_duration <= 0:
                raise ValueError('Buffer must be less than duration.')
            start_time_str = self.start_time_var.get()
            parsed_start_time = self.parse_start_time(start_time_str)
            now = datetime.now()
            # If start time is in the past or now, start from now and run for effective duration
            if parsed_start_time <= now:
                self.start_time = now
                self.end_time = now + timedelta(minutes=effective_duration)
            else:
                self.start_time = parsed_start_time
                self.end_time = parsed_start_time + timedelta(minutes=effective_duration)
            self.effective_duration = effective_duration
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
        """
        Update the timer display every second, showing elapsed time and ideal slide.
        If waiting for a future start time, show a waiting message.
        """
        if not self.timer_running:
            return
        now = datetime.now()
        if now < self.start_time:
            # Waiting for the scheduled start time
            start_str = self.start_time.strftime('%-I:%M%p').lower()
            now_str = now.strftime('%-I:%M%p').lower()
            self.timer_label.config(text=f'Waiting to start at {start_str}')
            self.slide_label.config(text='')
            self.elapsed_label.config(text='')
            # Show current time in a smaller font below
            if not hasattr(self, 'current_time_label'):
                self.current_time_label = tk.Label(self.timer_frame, text='', font=('Arial', 10))
                self.current_time_label.pack()
            self.current_time_label.config(text=f'(Current time: {now_str})')
            # Show 'preso to begin in' in small font
            minutes_to_start = int((self.start_time - now).total_seconds() // 60)
            seconds_to_start = int((self.start_time - now).total_seconds() % 60)
            if not hasattr(self, 'begin_in_label'):
                self.begin_in_label = tk.Label(self.timer_frame, text='', font=('Arial', 14))
                self.begin_in_label.pack()
            if minutes_to_start > 0:
                self.begin_in_label.config(text=f'preso to begin in {minutes_to_start} min')
            else:
                self.begin_in_label.config(text=f'preso to begin in {seconds_to_start} sec')
            self.root.after(1000, self.update_timer)
            return
        # Remove the current time and begin_in labels if they exist
        if hasattr(self, 'current_time_label'):
            self.current_time_label.destroy()
            del self.current_time_label
        if hasattr(self, 'begin_in_label'):
            self.begin_in_label.destroy()
            del self.begin_in_label
        elapsed = now - self.start_time
        total_seconds = self.effective_duration * 60
        elapsed_seconds = elapsed.total_seconds()
        if elapsed_seconds < 0:
            elapsed_seconds = 0
        if elapsed_seconds > total_seconds:
            elapsed_seconds = total_seconds
            self.timer_running = False
        elapsed_str = str(timedelta(seconds=int(elapsed_seconds)))
        self.elapsed_label.config(text=f'Elapsed: {elapsed_str}')
        ideal_slide = self.calculate_ideal_slide(elapsed_seconds, total_seconds, self.total_slides)
        self.timer_label.config(text=f'Ideal Slide: {ideal_slide}')
        self.slide_label.config(text=f'Time Remaining: {str(timedelta(seconds=int(total_seconds - elapsed_seconds)))}')
        if self.timer_running:
            self.root.after(1000, self.update_timer)

if __name__ == '__main__':
    root = tk.Tk()
    app = PrezzotimerApp(root)
    root.mainloop() 