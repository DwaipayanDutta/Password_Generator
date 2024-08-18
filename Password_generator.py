import os
import json
import secrets
import string
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from cryptography.fernet import Fernet

# Helper Functions
def generate_key():
    return Fernet.generate_key()

def save_key(key, key_file):
    with open(key_file, 'wb') as file:
        file.write(key)

def load_key(key_file):
    with open(key_file, 'rb') as file:
        return file.read()

def generate_password(length, characters):
    if length < 8:
        raise ValueError("Password length should be at least 8 characters")
    return ''.join(secrets.choice(characters) for _ in range(length))

def encrypt_data(data, fernet):
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data, fernet):
    return fernet.decrypt(encrypted_data).decode()

class PasswordManager:
    def __init__(self, key_file='key.key', data_file='passwords.json'):
        self.key_file = key_file
        self.data_file = data_file
        if not os.path.exists(self.key_file):
            self.key = generate_key()
            save_key(self.key, self.key_file)
        else:
            self.key = load_key(self.key_file)
        self.fernet = Fernet(self.key)
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    content = file.read()
                    if content.strip() == '':
                        self.data = {}
                    else:
                        encrypted_data = json.loads(content)
                        self.data = {k: decrypt_data(v.encode(), self.fernet) for k, v in encrypted_data.items()}
            except (json.JSONDecodeError, ValueError) as e:
                messagebox.showwarning("Warning", f"Error loading passwords: {e}")
                self.data = {}
        else:
            self.data = {}

    def save_data(self):
        with open(self.data_file, 'w') as file:
            encrypted_data = {k: encrypt_data(v, self.fernet).decode() for k, v in self.data.items()}
            json.dump(encrypted_data, file)

    def add_password(self, site, password):
        self.data[site] = password
        self.save_data()

    def get_password(self, site):
        return self.data.get(site, "No password found for this site")

    def get_all_passwords(self):
        return self.data

    def export_to_txt(self, output_file='passwords.txt'):
        with open(output_file, 'w') as file:
            for site, password in self.data.items():
                file.write(f"{site}: {password}\n")
        return os.path.abspath(output_file)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Password Manager")
        self.root.geometry("600x400")  # Adjusted size for better fit
        self.pm = PasswordManager()
        self.master_password = "Donotdisturb!01"  # Set your master password here

        self.create_master_password_prompt()
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Change theme here

    def create_master_password_prompt(self):
        self.master_password_entry = tk.Toplevel(self.root)
        self.master_password_entry.title("Enter Master Password")
        self.master_password_entry.geometry("300x150")  
        self.master_password_entry.attributes('-topmost', True) 

        frame = tk.Frame(self.master_password_entry, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Master Password:", font=("Calibri", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.master_password_input = tk.Entry(frame, show='*', font=("Calibri", 12))
        self.master_password_input.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(frame, text="Submit", command=self.check_master_password, font=("Calibri", 12)).grid(row=1, column=0, columnspan=2, pady=10)

    def check_master_password(self):
        entered_password = self.master_password_input.get()
        if entered_password == self.master_password:
            self.master_password_entry.destroy()
            self.create_widgets()
        else:
            messagebox.showerror("Error", "Incorrect master password. Try again.")

    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(main_frame, text="Site:", font=("Calibri", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.site_entry = tk.Entry(main_frame, width=40, font=("Calibri", 12))
        self.site_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(main_frame, text="Password:", font=("Calibri", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.password_entry = tk.Entry(main_frame, width=40, show='*', font=("Calibri", 12))
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(main_frame, text="Add Password", command=self.add_password, font=("Calibri", 12)).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Retrieve Password", command=self.retrieve_password, font=("Calibri", 12)).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Generate Password", command=self.show_password_preset_dialog, font=("Calibri", 12)).grid(row=4, column=0, padx=10, pady=10)
        
        self.copy_button = tk.Button(main_frame, text="Copy Generated Password", command=self.copy_password, font=("Calibri", 12))
        self.copy_button.grid(row=4, column=1, padx=10, pady=10)
        self.copy_button.config(state=tk.DISABLED)

        tk.Button(main_frame, text="Show All Passwords", command=self.show_all_passwords, font=("Calibri", 12)).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Clear Fields", command=self.clear_fields, font=("Calibri", 12)).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(main_frame, text="Export to TXT", command=self.export_to_txt, font=("Calibri", 12)).grid(row=7, column=0, columnspan=2, pady=10)

    def show_password_preset_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Password Generation Options")
        dialog.geometry("400x350")

        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Password Length:", font=("Calibri", 12)).pack(pady=5)
        length_entry = tk.Entry(frame, font=("Calibri", 12))
        length_entry.pack(pady=10)

        tk.Label(frame, text="Select Character Sets:", font=("Calibri", 12)).pack(pady=5)
        charsets = {
            'Uppercase Letters (A-Z)': tk.BooleanVar(value=True),
            'Lowercase Letters (a-z)': tk.BooleanVar(value=True),
            'Digits (0-9)': tk.BooleanVar(value=True),
            'Special Characters': tk.BooleanVar(value=True)
        }

        charsets_frame = tk.Frame(frame)
        charsets_frame.pack(pady=10)

        for label, var in charsets.items():
            tk.Checkbutton(charsets_frame, text=label, variable=var, font=("Calibri", 12)).pack(anchor='w')

        tk.Label(frame, text="Special Characters:", font=("Calibri", 12)).pack(pady=5)
        self.special_chars = tk.StringVar(value="~!@#$%^&*+-/.,\\{}[]();:?<>\",'_")
        special_chars_entry = tk.Entry(frame, textvariable=self.special_chars, font=("Calibri", 12))
        special_chars_entry.pack(pady=10)

        def on_generate():
            try:
                length = int(length_entry.get())
                if length < 8:
                    messagebox.showwarning("Input Error", "Password length should be at least 8 characters.")
                    return

                characters = ""
                if charsets['Uppercase Letters (A-Z)'].get():
                    characters += string.ascii_uppercase
                if charsets['Lowercase Letters (a-z)'].get():
                    characters += string.ascii_lowercase
                if charsets['Digits (0-9)'].get():
                    characters += string.digits
                if charsets['Special Characters'].get():
                    special_chars = self.special_chars.get()
                    characters += ''.join(c for c in special_chars if c not in characters)

                if not characters:
                    messagebox.showwarning("Input Error", "No character sets selected.")
                    return

                password = generate_password(length, characters)
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, password)
                self.copy_button.config(state=tk.NORMAL)
                messagebox.showinfo("Generated Password", f"Generated password: {password}")
                dialog.destroy()

            except ValueError:
                messagebox.showwarning("Input Error", "Please enter a valid number for password length.")

        tk.Button(frame, text="Generate", command=on_generate, font=("Calibri", 12)).pack(pady=20)

    def add_password(self):
        site = self.site_entry.get()
        password = self.password_entry.get()
        if not site or not password:
            messagebox.showwarning("Input Error", "Please provide both site and password.")
            return
        self.pm.add_password(site, password)
        messagebox.showinfo("Success", f"Password for {site} added.")
        self.clear_fields()

    def retrieve_password(self):
        site = self.site_entry.get()
        if not site:
            messagebox.showwarning("Input Error", "Please provide a site.")
            return
        password = self.pm.get_password(site)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def copy_password(self):
        password = self.password_entry.get()
        if password:
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            self.root.update()  # keep the clipboard updated
            messagebox.showinfo("Copied", "Password copied to clipboard.")

    def clear_fields(self):
        self.site_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.copy_button.config(state=tk.DISABLED)

    def show_all_passwords(self):
        table_window = tk.Toplevel(self.root)
        table_window.title("Stored Passwords")
        table_window.geometry("600x400")  # Adjusted size for better fit

        frame = tk.Frame(table_window, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)

        columns = ('site', 'password')
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        tree.heading('site', text='Site', font=("Calibri", 12))
        tree.heading('password', text='Password', font=("Calibri", 12))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=scrollbar.set)

        for site, password in self.pm.get_all_passwords().items():
            tree.insert('', tk.END, values=(site, password))

    def export_to_txt(self):
        output_file = self.pm.export_to_txt()
        messagebox.showinfo("Export Complete", f"Passwords exported to: {output_file}")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
