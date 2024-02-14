import tkinter as tk
from tkinter import Frame
from tkinter.font import Font
from PIL import Image, ImageTk

class AppGUI:
    
    def __init__(self, app):
        self.app = app
        self.labels = {}
        self.assets = {}
        self.widgets = {}
        self.tk = tk.Tk()
        
    def spawn_window(self):
        self.frame = tk.Frame(self.tk, height=300, width=300)
        self.frame.pack(side='top', fill='x')
        self.tk.title("LoL Quiz")
        self.tk.attributes("-topmost", True)
        self.tk.overrideredirect(True)
        self.tk.attributes("-alpha", 1.0)
        
        def on_mouse_enter(event):
            self.tk.attributes("-alpha", 1.0)

        def on_mouse_leave(event):
            self.tk.attributes("-alpha", 1.0)
        
        self.tk.bind("<Enter>", on_mouse_enter)
        self.tk.bind("<Leave>", on_mouse_leave)
        
        self.add_bg()
        self.add_top_bar()
        self.add_start_button()
        
    def add_bg(self, img_path="./assets/gui_bg.jpg"):
        bg_img = Image.open(img_path)
        self.assets['bg_image'] = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(self.frame, image=self.assets['bg_image'])
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
    def add_top_bar(self):
    
        def close_window():
            self.tk.destroy()
            exit()
    
        title_bar = Frame(self.frame, bg='white', relief='raised', bd=2)
        custom_font = Font(family="Helvetica", size=8, weight="bold")
        title_label = tk.Label(title_bar, font= custom_font, text="LoL Quiz Handicap", fg='black', bg="white")
        title_label.pack(side=tk.LEFT)
        close_button = tk.Button(title_bar, text="X", command=close_window)
        close_button.pack(side=tk.RIGHT)
        title_bar.pack(fill=tk.X)
            
    def add_start_button(self):
        
        def btn_action(btn):
            btn.destroy()
            self.app.start_game()
        
        play_img = Image.open("./assets/play.png")
        play_img = play_img.resize((50, 50), Image.Resampling.LANCZOS)
        self.assets['play_img'] = ImageTk.PhotoImage(play_img)
        
        btn = tk.Button(self.frame, image=self.assets['play_img'])
        btn.pack(side='left', padx=5, pady=5) 
        btn.config(command=lambda btn = btn: btn_action(btn))
        btn.pack()
        
    def update_label(self, text, id):
        if id in self.labels:
            self.labels[id].config(text=text)
        else:
            self.add_label(text, id)
            
    def add_label(self, text, id):
        
        if 'question' in id:
            custom_font = Font(family="Helvetica", size=10)
            label = tk.Label(self.frame, text=text, font=custom_font, wraplength=300)
            label.pack(side="right", padx=(8, 5))
            
        if 'handicaps' in id:
            custom_font = Font(family="Helvetica", size=10)
            label = tk.Label(self.frame, text=text, font=custom_font, wraplength=300)
            label.pack(side="right", padx=(8, 5))
            
        if 'difficulty' in id:
            custom_font = Font(family="Helvetica", size=10)
            label = tk.Label(self.frame, text=text, font=custom_font)
            label.pack(side="right")
            
        if 'topic' in id:
            custom_font = Font(family="Helvetica", size=10)
            label = tk.Label(self.frame, text=text, font=custom_font)
            label.pack(side="right")
            
        if 'timer' in id:
            custom_font = Font(family="Helvetica", size=10)
            label = tk.Label(self.frame, text=text, font=custom_font)
            label.pack(side="right", padx=(8, 5))
            
        if 'answers_right' in id:
            custom_font = Font(family="Helvetica", size=12)
            label = tk.Label(self.frame, text=text, font=custom_font, bg='green', fg='white')
            label.pack(side="left", padx=(5, 5))
            
        if 'answers_wrong' in id:
            custom_font = Font(family="Helvetica", size=12)
            label = tk.Label(self.frame, text=text, font=custom_font, bg='red', fg='white')
            label.pack(side="left", padx=(5, 5))
        
        self.labels[id] = label
        
    def remove_label(self, id):
        if id in self.labels:
            self.labels[id].destroy()
            del self.labels[id]