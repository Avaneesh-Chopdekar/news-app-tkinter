import io
import webbrowser
import requests
import pyttsx3
import tkinter as tk
import threading
from urllib.request import urlopen
from PIL import ImageTk, Image
from constants import TOP_HEADLINES_URL


class NewsApp:
    def __init__(self):
        r = requests.get(TOP_HEADLINES_URL)
        self.data = r.json()
        # print(self.data)

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)
        self.load_gui()
        self.load_news_items(0)

    def load_gui(self):
        self.root = tk.Tk()
        self.root.title("Breaking News")
        self.root.geometry("350x600+50-50")
        self.root.resizable(0, 0)
        self.root.configure(background="black")

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def open_link(self, index):
        webbrowser.open(self.data["articles"][index]["url"])

    def prev_command(self, index):
        if index != 0:
            self.load_news_items(index - 1)
        else:
            self.load_news_items(len(self.data["articles"]) - 1)

    def next_command(self, index):
        if index != len(self.data["articles"]) - 1:
            self.load_news_items(index + 1)
        else:
            self.load_news_items(0)

    def speak_news(self, text1, text2):
        self.engine.say(text1)
        self.engine.runAndWait()
        self.engine.say(text2)
        self.engine.runAndWait()

    def load_news_items(self, index):
        self.clear()

        try:
            img_url = self.data["articles"][index]["urlToImage"]
            raw_img = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_img)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = (
                "https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg"
            )
            raw_img = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_img)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = tk.Label(self.root, image=photo)
        label.pack()

        heading = tk.Label(
            self.root,
            text=self.data["articles"][index]["title"],
            bg="black",
            fg="white",
            wraplength=350,
            justify="center",
        )
        heading.pack(pady=(10, 20))
        heading.config(font=("Roboto", 15))

        desc = tk.Label(
            self.root,
            text=self.data["articles"][index]["description"],
            bg="black",
            fg="white",
            wraplength=350,
            justify="center",
        )
        desc.pack(pady=(2, 20))
        desc.config(font=("Roboto", 12))

        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True, fill="both")

        prevBtn = tk.Button(
            frame,
            text="Prev",
            width=11,
            height=3,
            command=lambda: self.prev_command(index),
        )
        prevBtn.pack(side="left")

        readBtn = tk.Button(
            frame,
            text="Read More",
            width=11,
            height=3,
            command=lambda: self.open_link(index),
        )
        readBtn.pack(side="left")

        speakBtn = tk.Button(
            frame,
            text="Speak",
            width=11,
            height=3,
            command=lambda: threading.Thread(
                target=self.speak_news,
                args=(
                    self.data["articles"][index]["title"],
                    self.data["articles"][index]["description"],
                ),
            ).start(),
        )
        speakBtn.pack(side="left")

        nextBtn = tk.Button(
            frame,
            text="Next",
            width=11,
            height=3,
            command=lambda: self.next_command(index),
        )
        nextBtn.pack(side="left")

        self.root.mainloop()

NewsApp()
