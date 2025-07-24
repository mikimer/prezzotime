# PREZZOTIMER ⏰ 🤔
# 

This project is for people who give presentations with lots of slides and want to avoid running overtime.

## My problem:
I believe in the concept of [one-idea-per-slide](https://www.youtube.com/shorts/qKDvUO-hK5s). I run a [workshop](https://lu.ma/nascent) where I present ~250 slides over 2 hours, interspersed with lots of audience participation. So it's easy for the workshop to run long, but I want to respect my audience's time and keep to the planned 2 hours. So far, I've been [keeping time by manually](IMG_0532.jpeg) writing out a table of time on the clock and target slide number, which I then compare to the current slide. This is tedious and distracts from the preso. 

I wanna build "an app for that".


## Solution: Prezzotimer app 
Input values: 
  - Presentation duration (e.g., 2 hours)
  - Total slides (e.g., 250) 
  - Start time (e.g., 2.30pm) since I'll launch this app 10 to 20 mins before I begin presenting.
 
Output: 
  - A timer that counts 1->250 over 2 hours so I can compare the slide timer with the current slide.
  - The timer should be large (full screen) when I'm giving an in-person workshop and small (ideally in the Menu Bar) for on-line webinars. 

Future development: I use Google Presentations so I could try to link this app to gPreso so it would automatically see which slide I'm on and provide more useful feedback.


Assume: [screen extension, not display mirroring](Mac-External-Displays-Arrangment.jpg) during in-person workshops.


## Details

- Smart time input: Accepts start times in many formats, including '2pm', '2:30pm', '14:00', '1400', '2.20', and '14.20'.
- Defaults for rapid setup: During development, the slides and duration fields autopopulate with 100 and 10, respectively.
- Buffer field: Specify a buffer (default 10 minutes) to end the timer early and leave time for Q&A or wrap-up.
- Waiting screen: If the start time is in the future, the app displays a clear waiting message, current time, and a countdown until the presentation begins.
- User-friendly time display: All times are shown in 12-hour am/pm format for clarity.
- Input validation: The app checks for valid numbers and ensures the buffer is less than the total duration.
- Modular, refactored code: Timer logic and time parsing are separated for easier maintenance and future improvements.



