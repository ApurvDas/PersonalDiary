import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, simpledialog
from datetime import datetime
import os
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, entered_password):
    return stored_password == hash_password(entered_password)

class PersonalDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary")
        self.root.geometry("800x600")
        self.entries = []
        self.current_user = None
        self.theme = "light"
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Welcome to Personal Diary", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username:", font=("Arial", 14)).pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 14)).pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.root, text="Login", font=("Arial", 14), command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", font=("Arial", 14), command=self.register).pack(pady=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Login Failed", "Username and Password are required!")
            return
        user_file = f"{username}_diary.txt"
        if os.path.exists(user_file):
            with open(user_file, "r") as file:
                stored_password = file.readline().strip()
                if verify_password(stored_password, password):
                    self.current_user = username
                    self.entries = file.readlines()
                    self.create_main_screen()
                else:
                    messagebox.showerror("Login Failed", "Incorrect password!")
        else:
            messagebox.showerror("Login Failed", "User not found! Please register.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Registration Failed", "Username and Password are required!")
            return
        user_file = f"{username}_diary.txt"
        if os.path.exists(user_file):
            messagebox.showerror("Registration Failed", "User already exists! Please log in.")
        else:
            hashed_password = hash_password(password)
            with open(user_file, "w") as file:
                file.write(f"{hashed_password}\n")
            messagebox.showinfo("Registration Successful", "You can now log in!")

    def create_main_screen(self):
        self.clear_screen()
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save to File", command=self.save_to_file)
        file_menu.add_command(label="Export as PDF", command=self.export_as_pdf)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self.logout)
        menu_bar.add_cascade(label="File", menu=file_menu)
        theme_menu = tk.Menu(menu_bar, tearoff=0)
        theme_menu.add_command(label="Light Theme", command=lambda: self.set_theme("light"))
        theme_menu.add_command(label="Dark Theme", command=lambda: self.set_theme("dark"))
        menu_bar.add_cascade(label="Theme", menu=theme_menu)
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 20)).pack(pady=10)
        self.entry_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=10)
        self.entry_text.pack(pady=10)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        tk.Button(button_frame, text="Save Entry", command=self.save_entry, width=15).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="View Entries", command=self.view_entries, width=15).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Search", command=self.search_entries, width=15).grid(row=0, column=2, padx=5)
        self.display_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=10, state=tk.DISABLED)
        self.display_area.pack(pady=10)

    def save_entry(self):
        text = self.entry_text.get("1.0", tk.END).strip()
        if text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            entry = f"[{timestamp}]\n{text}\n"
            self.entries.append(entry)
            self.entry_text.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Entry saved!")
            self.auto_save()
        else:
            messagebox.showwarning("Warning", "No text entered!")

    def view_entries(self):
        self.display_area.config(state=tk.NORMAL)
        self.display_area.delete("1.0", tk.END)
        if self.entries:
            for entry in self.entries:
                self.display_area.insert(tk.END, entry + "\n")
        else:
            self.display_area.insert(tk.END, "No entries yet!")
        self.display_area.config(state=tk.DISABLED)

    def auto_save(self):
        if self.current_user:
            user_file = f"{self.current_user}_diary.txt"
            with open(user_file, "w") as file:
                file.write(hash_password(self.password_entry.get().strip()) + "\n")
                file.writelines(self.entries)

    def save_to_file(self):
        if self.entries:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as file:
                    file.writelines(self.entries)
                messagebox.showinfo("Success", "Entries saved to file!")
        else:
            messagebox.showwarning("Warning", "No entries to save!")

    def export_as_pdf(self):
        try:
            from reportlab.pdfgen import canvas
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                pdf = canvas.Canvas(file_path)
                pdf.setFont("Helvetica", 12)
                y = 800
                for entry in self.entries:
                    if y < 50:
                        pdf.showPage()
                        pdf.setFont("Helvetica", 12)
                        y = 800
                    pdf.drawString(50, y, entry.strip())
                    y -= 20
                pdf.save()
                messagebox.showinfo("Success", "Entries exported to PDF!")
        except ImportError:
            messagebox.showerror("Error", "ReportLab is not installed. Install it with 'pip install reportlab'.")

    def search_entries(self):
        search_term = simpledialog.askstring("Search", "Enter a keyword:")
        if search_term:
            results = [entry for entry in self.entries if search_term.lower() in entry.lower()]
            self.display_area.config(state=tk.NORMAL)
            self.display_area.delete("1.0", tk.END)
            if results:
                for result in results:
                    self.display_area.insert(tk.END, result + "\n")
            else:
                self.display_area.insert(tk.END, "No matching entries found!")
            self.display_area.config(state=tk.DISABLED)

    def logout(self):
        self.current_user = None
        self.entries = []
        self.create_login_screen()

    def set_theme(self, theme):
        self.theme = theme
        if theme == "dark":
            self.root.config(bg="black")
            for widget in self.root.winfo_children():
                widget.config(bg="black", fg="white")
        else:
            self.root.config(bg="white")
            for widget in self.root.winfo_children():
                widget.config(bg="white", fg="black")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalDiary(root)
    root.mainloop()
