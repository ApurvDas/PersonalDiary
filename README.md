# Personal Diary Application

This is a Python-based GUI application for maintaining a personal diary. Users can create, save, view, and search diary entries with features like user authentication, theme customization, and export options.

---

## Features

1. **User Authentication**
   - Login and registration system with secure password hashing using `SHA-256`.
   - Separate diary file for each user.

2. **Diary Management**
   - Add new entries with timestamps.
   - View, search, and manage entries.

3. **Export Options**
   - Save entries to a `.txt` file.
   - Export entries to a `.pdf` file (requires `ReportLab` library).

4. **Theme Customization**
   - Switch between light and dark themes.

5. **Auto-Save**
   - Automatically saves entries to the user's diary file.

6. **Search Functionality**
   - Search for specific keywords in saved entries.

7. **Multi-User Support**
   - Each user maintains their own diary, stored in a separate file.

---

## Prerequisites

### Python Libraries
- **Required**: `tkinter`, `hashlib`, `datetime`
- **Optional (for PDF export)**: `reportlab`

Install `reportlab` using the command:

```bash
pip install reportlab
```

## Sample Screenshots
![python_KJfLAtsCJX](https://github.com/user-attachments/assets/12ab51ed-ef74-4f1b-8de9-37b397c92058)
![python_D6wF0WX7xz](https://github.com/user-attachments/assets/910407d2-0911-473a-bc18-97935d3bb17d)


 
