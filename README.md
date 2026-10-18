# Your-Goth-Girl
A tiny pixel-art goth tamagotchi made with Python and Tkinter. Keep her fed, happy and full of dark energy, or she'll fade away under the bench.

FEATURES
Three stats (Hunger, Happiness, Energy) that slowly drop over time
Mood messages that change depending on how she's doing
Outfit switcher to cycle through her looks
A black cat companion 🐈‍⬛ (meow ^^)
Breathing animation so she feels alive
Name your goth girl in the input box
Pixel-art sprites with automatic background removal
Custom pastel/goth color palette

CONTROLS
Button	Effect
Feed	Hunger +20
Reassure	Happiness +15
Gothify	Energy +10
Change outfit	Switches to the next outfit
Every 5 seconds her stats go down a little, so don't leave her alone for too long.

REQUIREMENTS
Python 3.8+
Pillow
pip install pillow
Tkinter comes with Python on Windows and macOS. On Linux you may need to install it separately (for example sudo apt install python3-tk).

HOW TO RUN
git clone https://github.com/kkoket/your-goth-girl.git
cd your-goth-girl
python main.py
Project structure
your-goth-girl/
├── main.py
├── README.md
└── images/
    ├── goth1.png
    ├── goth2.png
    ├── goth3.png
    └── cat.png
Roadmap
 Game over when a stat reaches 0
 Day/night cycle
 Breathing animation: Done
 Blinking animation
 Clickable cat
 Event diary
 Save and load progress
Made with: Python, Tkinter, Pillow
