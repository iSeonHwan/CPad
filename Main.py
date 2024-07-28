# 프로그램명: 바이트 계산 패드
# 설명: 바이트 계산 기능이 있는 간단한 메모 프로그램
# 날짜: 2024. 7. 28.

# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox, font

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cpad")
        self.geometry("600x400")

        # 기본 폰트 설정
        self.default_font = font.Font(family="Arial", size=12)
        
        # 메인 프레임 생성
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 텍스트 영역
        self.text_area = tk.Text(self.main_frame, undo=True, font=self.default_font)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 스크롤바 추가
        self.scrollbar = tk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        # 상태 표시줄 프레임
        self.status_frame = tk.Frame(self, height=25)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.status_frame.pack_propagate(False)  # 프레임 크기 고정

        # 상태 표시줄
        self.status_bar = tk.Label(self.status_frame, text="number of character: 0, byte: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X)

        # 텍스트 변경 이벤트 바인딩
        self.text_area.bind("<KeyRelease>", self.update_status_bar)

        # 메뉴바 설정
        self.setup_menu()

    def setup_menu(self):
        # 메뉴바의 폰트를 지정함.
        self.menu_bar = tk.Menu(self, font=("Arial", 12))
        self.config(menu=self.menu_bar)

        # 파일 메뉴바의 폰트를 지정함.
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0, font=("Arial", 12))
        self.menu_bar.add_cascade(label="file", menu=self.file_menu)
        self.file_menu.add_command(label="open", command=self.open_file)
        self.file_menu.add_command(label="save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="close", command=self.quit)

        # 문자 변환 메뉴 항목 추가
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Convert to Smart Quotes", command=self.auto_replace)

        # 폰트 메뉴 추가
        self.font_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Font", menu=self.font_menu)
        self.font_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        self.font_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.update_status_bar()

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension="txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                messagebox.showinfo("Finish to save", "The file has been saved")

    def update_status_bar(self, event=None):
        text_content = self.text_area.get(1.0, tk.END).strip()
        char_count = len(text_content)
        byte_count = len(text_content.encode('utf-8'))
        self.status_bar.config(text=f"number of character: {char_count}, byte: {byte_count}")

    def auto_replace(self, event=None):
        # 현재 커서 위치를 저장
        cursor_pos = self.text_area.index(tk.INSERT)

        # 텍스트 내용을 가져와서 변환
        text_content = self.text_area.get("1.0", tk.END)
        replacements = {
            "‘": "'", "’": "'", "“": '"', "”": '"',
            "\'": "'", '\"': '"'
        }
        for old, new in replacements.items():
            text_content = text_content.replace(old, new)

        # 변경된 텍스트를 다시 삽입
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text_content)

        # 커서 위치 복원
        self.text_area.mark_set(tk.INSERT, cursor_pos)

        # 상태 표시줄 업데이트
        self.update_status_bar()

    def increase_font_size(self):
        current_size = self.default_font['size']
        new_size = current_size + 2
        self.default_font.configure(size=new_size)
        self.text_area.configure(font=self.default_font)
        self.update_status_bar()

    def decrease_font_size(self):
        current_size = self.default_font['size']
        new_size = max(8, current_size - 2)  # 최소 크기를 8로 제한
        self.default_font.configure(size=new_size)
        self.text_area.configure(font=self.default_font)
        self.update_status_bar()

if __name__ == "__main__":
    app = Notepad()
    app.mainloop()
