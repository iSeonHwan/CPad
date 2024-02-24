# 프로그램명: 바이트 계산 패드
# 설명: 바이트 계산 기능이 있는 간단한 메모 프로그램
# 날짜: 2024. 2. 24.

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Notepad(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cpad")
        self.geometry("600x400")

        self.text_area = tk.Text(self)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        # 텍스트 변경 이벤트 바인딩
        self.text_area.bind("<KeyRelease>", self.update_status_bar)
        
        self.status_bar = tk.Label(self, text="number of character: 0, byte: 0", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)


        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="file", menu=self.file_menu)
        self.file_menu.add_command(label="open", command=self.open_file)
        self.file_menu.add_command(label="save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="close", command=self.quit)

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.update_status_bar() #추가된 부분.

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension="txt")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
                messagebox.showinfo("Finish to save", "The file has been saved")

    def update_status_bar(self, event=None):
        text_content = self.text_area.get(1.0, tk.END)
        char_count = len(text_content) - 1  # 텍스트 끝의 '\n' 제외
        byte_count = len(text_content.encode('utf-8')) - 1  # UTF-8 인코딩 사용, 텍스트 끝의 '\n' 제외
        self.status_bar.config(text=f"number of character: {char_count}, byte: {byte_count}")
    



if __name__ == "__main__":
    app = Notepad()
    app.mainloop()

