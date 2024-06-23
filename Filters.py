import tkinter as tk

class Filters:
    def __init__(self, frame, variables):        
        self.frame = frame
        self.variables = variables
        self.frame.columnconfigure(0, weight=1)
                
        # Filter Text Input
        self.search_text = tk.Text(self.frame, height=1)
        self.search_text.grid(row=0, column=0, sticky="ew")

        # Create Label and Toggle Button (Checkbutton)
        # Auto-Scroll Label
        self.toggle_var = tk.BooleanVar(value=True)
        self.toggle_button = tk.Checkbutton(self.frame, variable=self.toggle_var, command=self.toggle_scroll)
        self.toggle_button.grid(row=0, column=1, sticky="e")
        # Auto-Scroll Button
        self.label = tk.Label(self.frame, text="Auto-Scroll")
        self.label.grid(row=0, column=2, sticky="e")
       
        # Create buttons
        ## Resume Button
        self.resume_button = tk.Button(self.frame, text='Resume',
                                         state="disabled",
                                         disabledforeground="red",
                                         command=self.on_resume_button)
        self.resume_button.grid(row=0, column=3, sticky="e")
        ## Pause Button
        self.pause_button = tk.Button(self.frame, text='Pause', 
                                        state="normal",
                                        disabledforeground="red",
                                        command=self.on_pause_button)
        self.pause_button.grid(row=0, column=4, sticky="e")


    # Resume Button 함수
    def on_resume_button(self):
        text = self.search_text.get("1.0", "end-1c").replace(" ", "") # 공백 제거
        self.classify_words(text)
        self.variables.set_variable("is_playing", True)
        self.resume_button.config(state="disabled")
        self.pause_button.config(state="normal")


    # Pause Button 함수
    def on_pause_button(self):
        self.variables.set_variable("is_playing", False)
        self.resume_button.config(state="normal")
        self.pause_button.config(state="disabled")


    # Scroll Button 함수
    def toggle_scroll(self):
        self.variables.set_variable("auto_scroll", self.toggle_var.get())

    # 문자열을 '&'와 '!'를 기준으로 분리
    def classify_words(self, text):
        highlight_word = []
        hide_word = []
        elements = text.replace('!', '&!').split('&')
        for element in elements:
            if element.startswith('!'):
                hide_word.append(element[1:])
            elif element:
                highlight_word.append(element)
        self.variables.set_variable("highlight_word", highlight_word)
        self.variables.set_variable("hide_word", hide_word)