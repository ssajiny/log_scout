import re
import tkinter as tk
import os

from tkinter.scrolledtext import ScrolledText
from Observer import Observer

class ConsoleUI(Observer):
    def __init__(self, root, frame, variables):
        self.root = root
        self.frame = frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.variables = variables
        # 환경변수 초기값
        self.log_file_position = self.get_initial_file_position()
        self.auto_scroll = True
        self.highlight_word = []
        self.hide_word = []
        self.is_playing = True
        self.monitor_id = ""
        self.line_limit = self.variables.get_variable('line_limit')
        self.refresh_rate = self.variables.get_variable('refresh_rate')

        self.scrolled_text = ScrolledText(frame, wrap=tk.NONE, state='disabled')
        self.scrolled_text.grid(row=0, column=0, sticky="nsew")
        self.scrolled_text.configure(font=('TkFixedFont', 15))
        self.scrolled_text.tag_config('TRACE', foreground='white')
        self.scrolled_text.tag_config('DEBUG', foreground='green')
        self.scrolled_text.tag_config('INFO', foreground='skyblue')
        self.scrolled_text.tag_config('WARN', foreground='yellow')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('highlight', foreground='black', background='yellow')

        # Ctrl+C 단축키에 복사 기능 바인딩
        self.scrolled_text.bind("<Control-c>", self.copy_selection)
        self.scrolled_text.bind("<Command-c>", self.copy_selection)
    

    # Filters, FileMenu에서 옵션값이 변경 되었을 때
    def update(self, key, value):
        if(key == 'file_path'):
            self.clear_text()    
        if(key == 'refresh_rate'):
            self.refresh_rate = value
        if(key == 'line_limit'):
            self.line_limit = value        
        if(key == 'auto_scroll'):
            self.auto_scroll = value
        if(key == 'highlight_word'):
            self.highlight_word = value
        if(key == 'hide_word'):
            self.hide_word = value
        if(key == 'is_playing'):
            self.is_playing = value
            if self.is_playing:
                self.read_file()
            else:
                self.stop_display()
                

    # File 변경시 텍스트 모두 지우기
    def clear_text(self):
        # Set the state to 'normal' to enable editing
        self.scrolled_text.config(state='normal')
        # Clear the content
        self.scrolled_text.delete("1.0", tk.END)
        # Set the state back to 'disabled'
        self.scrolled_text.config(state='disabled')
        self.stop_display()
        self.read_file()


    # 파일을 읽을 위치 (맨 아래부터)
    def get_initial_file_position(self):
        file_path = self.variables.get_variable('file_path')
        with open(file_path, 'r') as f:
            f.seek(0, os.SEEK_END)  # Move to the end of the file
            return f.tell()


    # 파일을 읽는다.
    def read_file(self):
        file_path = self.variables.get_variable('file_path')
        if file_path is not None:
            try:
                # with open(file_path, 'r') as f:
                #     # Move to the last read position
                #     f.seek(self.log_file_position)
                #     # Read from the last read position
                #     new_lines = f.readlines()
                #     if new_lines:
                #         for line in new_lines:
                #             # Buffer에 저장
                #             # srid값이 변할 때 까지 Buffer = {srid='mysrid0001', logArr=[log1, log2, ...]} 저장
                #             # srid값이 변한다면, Filter 적용

                #             # Filter 적용
                #             # highlight_word 존재하면 self.display(line, 'highlight')
                #             # hide_word에 존재하면 self.display(line, 'hide')
                #             # 둘 다 아니라면 self.display(line, 'normal')

                #             self.display(line, 'normal')
                #         # Update the position
                #         self.log_file_position = f.tell()

                with open(file_path, 'r') as f:
                    f.seek(self.log_file_position)
                    new_lines = f.readlines()
                    if new_lines:
                        rid = ''
                        logArr = []
                        highlight_flag = False
                        hide_flag = False

                        for line in new_lines:                
                            match = re.search(r"srid=([a-zA-Z0-9]+)", line)
                            if match:
                                # srid값이 변할 때 까지 logArr=[log1, log2, ...] 저장
                                # srid값이 변한다면, Filter 적용
                                current_rid =  match.group(1).strip()
                                if rid != '' and rid != current_rid:
                                    # rid가 기존과 다름           
                                    # highlight_word 존재하면 self.display(line, 'highlight')
                                    # hide_word에 존재하면 self.display(line, 'hide')
                                    # 둘 다 아니라면 self.display(line, 'normal')
                                    for log in logArr:
                                        if highlight_flag:
                                            self.display(log, 'highlight')
                                        elif hide_flag:
                                            print('hide')
                                        else:
                                            self.display(log, 'normal')                    

                                    # 다음 값으로 변경
                                    highlight_flag = False
                                    hide_flag = False
                                    rid = current_rid
                                    logArr = []
                                    logArr.append(line)
                                else:
                                    # rid가 기존과 같음
                                    if any(word in line for word in self.highlight_word):
                                        highlight_flag = True
                                    elif any(word in line for word in self.hide_word):
                                        hide_flag = True         
                                    rid = current_rid
                                    logArr.append(line)
                            else:
                                pass
                        # line 반복이 끝나면 버퍼에 남아 있는 항목 출력
                        for log in logArr:
                            if highlight_flag:
                                self.display(log, 'highlight')
                            elif hide_flag:
                                print('hide')
                            else:
                                self.display(log, 'normal')

                        # Update the position
                        self.log_file_position = f.tell()




            except Exception as e:
                print(f"Error reading log file: {e}")
        # Schedule the next check
        self.monitor_id = self.root.after(self.refresh_rate, self.read_file)


    # Log에서 Log Level 값을 추출한다.
    def extract_between(self, text):
        match = re.search(r'\[.*?\]\s+(.*?)\s+\[srid=.*?\]', text)
        if match:
            return match.group(1).strip()
        else:
            return None
        

    # Start displaying messages in the Console UI
    def display(self, line, status):
        log_level = self.extract_between(line)
        self.scrolled_text.configure(state='normal')
        # Filter 적용
        if status == 'normal': # 일반 텍스트
            self.scrolled_text.insert(tk.END, line, log_level)
        elif status == 'highlight': # 강조 텍스트
            self.scrolled_text.insert(tk.END, line, 'highlight')
        elif status == 'hide': # 숨김 텍스트
            pass
        self.scrolled_text.configure(state='disabled')
        # 맨 아래 고정
        if self.auto_scroll:
            self.scrolled_text.yview_moveto(1.0)
        # limit 넘는 라인 제거
        self.remove_excess_lines()

    
    # Stop displaying messages in the Console UI
    def stop_display(self):
        if self.monitor_id is not None:
            self.root.after_cancel(self.monitor_id)


    # limit_line 을 넘는 행 삭제
    def remove_excess_lines(self):
        limit = int(self.line_limit)
        lines = self.scrolled_text.get("1.0", tk.END).split("\n")
        if len(lines) > limit:
            self.scrolled_text.configure(state='normal')
            self.scrolled_text.delete("1.0", f"{len(lines) - limit}.0")
            self.scrolled_text.configure(state='disabled')

    # 클립보드에 선택한 텍스트 복사
    def copy_selection(self, event=None):
        try:            
            selected_text = self.scrolled_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            # 선택된 텍스트가 없을 경우 예외 처리
            pass