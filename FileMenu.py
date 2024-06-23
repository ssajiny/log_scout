import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class FileMenu():
    def __init__(self, root, variables):
        self.root = root
        self.variables = variables

        # Menu 생성
        menubar=tk.Menu(self.root)
        menu_file=tk.Menu(menubar, tearoff=0)
        menu_file.add_command(label="Open File", command=self.select_file)
        menu_file.add_command(label="Settings", command=self.open_settings)
        menubar.add_cascade(label="File", menu=menu_file)

        # Line Limit 값
        self.lines = ['100', '200', '300', '400', '500', '600', '700', '800', '900', '1000']
        # Refresh Rate 값
        self.rates = ['100', '500', '1000']
        self.root.config(menu=menubar)


    # Menu 생성
    def open_settings(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")        
        self.settings_window.geometry("+50+50")
        self.settings_window.resizable(False, False)

        # Option List 생성
        ## Refresh Rate
        ttk.Label(self.settings_window, text="Refresh Rate(Sec):").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        refresh_rate_option = ttk.Combobox(self.settings_window, values=self.rates, state='readonly')
        refresh_rate = self.variables.get_variable('refresh_rate')
        refresh_rate_option.set(refresh_rate)
        refresh_rate_option.grid(row=1, column=1, padx=10, pady=5)
        ## Line Limit
        ttk.Label(self.settings_window, text="Line Limitaion(Lines):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        line_limit_option = ttk.Combobox(self.settings_window, values=self.lines, state='readonly')
        line_limit = self.variables.get_variable('line_limit')
        line_limit_option.set(line_limit)
        line_limit_option.grid(row=2, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = ttk.Frame(self.settings_window)
        button_frame.grid(row=3, column=1, pady=10)
        ## Save Button
        ## 버튼이 생성되는 시점에 실행되지 않도록 Lambda 사용
        save_button = ttk.Button(button_frame, text="Save", 
                                 command=lambda: self.save_settings(
                                     refresh_rate=refresh_rate_option.get(),
                                     line_limit=line_limit_option.get()
                                     )) 
        save_button.grid(row=1, column=1)
        ## Cancel Button
        cancel_button = ttk.Button(button_frame, text="Cancel",
                                   command=lambda: self.settings_window.destroy())
        cancel_button.grid(row=1, column=2)


    # variables값 저장
    def save_settings(self, **kwargs): 
        for key, value in kwargs.items():
            self.variables.set_variable(key, value)

        # config.json 파일 변경
        self.variables.save_variables()
        self.settings_window.destroy()
    
    
    # 관찰할 파일 지정
    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.variables.set_variable('file_path', file_path)

            # config.json 파일 변경
            self.variables.save_variables()
        else:
            print("No file selected")