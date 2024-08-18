# 🛡️ Password Generator

## 🎯 Overview

Welcome to the **Password Generator** – your go-to tool for creating and managing strong, secure passwords effortlessly. This Python application is designed to generate random passwords, store them securely, and provide an intuitive graphical interface for managing your credentials.

## 🌟 Features

- 🔐 **Generate Strong Passwords:** Create robust, random passwords with customizable lengths and character sets.
- 📂 **Add and Retrieve Passwords:** Securely store and retrieve passwords for your favorite sites.
- 📜 **Export Passwords:** Export all stored passwords to a text file for backup or sharing.
- 🔒 **Encryption:** Keep your passwords safe with encryption.
- 🖥️ **User-Friendly GUI:** A graphical user interface built with Tkinter for a seamless experience.

## 🚀 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/DwaipayanDutta/Password_Generator.git
   cd Password_Generator
   ```
2. **Install Dependencies:** 
Ensure you have the required Python libraries:
    - cryptography
    - tkinter
    
3. **Run the Application:**\
 Start the application with:

   ```bash
   python Password_generator.py
   ```
3. **Master Password:**\
   Currently the master password is set to - Donotdisturb!01 change if required in the code before the code run by navigating to :
      ```bash
    self.master_password = "Donotdisturb!01"
     ``` 
## 🌟 Features
- 🔐 **Generate Strong Passwords**: Create robust, random passwords with customizable lengths and character sets.
- 📂 **Add and Retrieve Passwords**: Securely store and retrieve passwords for your favorite sites.
- 📜 **Export Passwords**: Export all stored passwords to a text file for backup or sharing.
- 🔒 **Encryption**: Keep your passwords safe with encryption.
- 🖥️ **User-Friendly GUI**: A graphical user interface built with Tkinter for a seamless experience.
## 🔧 Password Management
- 🆕 **Add Password**: Enter the site and password, then click "Add Password."
- 🔍 **Retrieve Password**: Enter the site name to get the stored password.
- 🔄 **Generate Password**: Click "Generate Password" and configure the options to create a new password.
- 📊 **Show All Passwords**: View all stored passwords in a neatly organized table.
- 📥 **Export to TXT**: Export all passwords to a text file.

## 🔧PasswordManager Class
-  __init__(key_file='key.key', data_file='passwords.json') 🛠: Initializes the password manager, handling key management and data loading.
- load_data() 📥: Loads and decrypts password data.
- save_data() 💾: Encrypts and saves password data.
- add_password(site, password) 🆕: Adds a new password entry.
- get_password(site) 🔍: Retrieves a password for a specific site.
- get_all_passwords() 📜: Returns all stored passwords.
- export_to_txt(output_file='passwords.txt') 📤: Exports passwords to a text file.
