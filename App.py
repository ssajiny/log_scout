import signal
from tkinter import ttk, VERTICAL, HORIZONTAL

from Variables import Variables
from FileMenu import FileMenu
from ConsoleUI import ConsoleUI
from Filters import Filters

class App:
    def __init__(self, root):
        self.root = root
        root.title('Sangjin\'s LogScout')
        root.geometry('1280x800+50+50')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # 환경설정
        variables = Variables()
        FileMenu(root, variables)        

        # Create Vertical Frame
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew") # self.root의 0,0 격자

        # Create Horizontal Frame
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)

        # Filter Frame
        filters_frame = ttk.Labelframe(horizontal_pane, text="Filters")
        horizontal_pane.add(filters_frame, weight=1)    

        # Console Frame
        console_frame = ttk.Labelframe(vertical_pane, text="Console")
        vertical_pane.add(console_frame, weight=1)

        # Initialize ConsoleUI
        self.console = ConsoleUI(self.root, console_frame, variables)
        self.filters = Filters(filters_frame, variables)
        self.console.read_file()

        # 옵저버에 등록
        variables.register_observer(self.console)

        # Terminate Program
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)
        

    def quit(self):
        self.root.destroy()