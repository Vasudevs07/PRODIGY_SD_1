# 📋 Contact Management System

> **Prodigy Infotech Internship — Software Development Track | Task 03**
> Repository: `PRODIGY_SD_03`

A professional desktop application to **add, view, search, edit, and delete contacts** — built with Python and Tkinter, featuring a modern dark-themed GUI and persistent JSON storage with automatic backups.

---

 

| Feature | Description |
|---|---|
| **Add Contact** | Enter name (required), phone, and email with real-time validation |
| **View Contacts** | Sortable table with alternating row colours for easy scanning |
| **Search** | Instant live search across name, phone, and email |
| **Edit Contact** | Double-click a row or click Edit to update any field |
| **Delete Contact** | Confirmation dialog before deletion to prevent accidents |
| **Duplicate Prevention** | Blocks duplicate names and phone numbers |
| **UUID IDs** | Every contact gets a universally unique identifier |
| **JSON Storage** | Contacts persisted in `contacts.json` in the project folder |
| **Auto Backup** | `contacts_backup.json` created before every write |
| **Sort by Column** | Click any column header to sort ascending / descending |
| **Status Bar** | Live feedback on all actions |
| **Dark Modern UI** | Professional purple-accented dark theme |

---

## 🗂 Project Structure

```
PRODIGY_SD_03/
│
├── main.py              # Application source code (OOP, GUI, data layer)
├── contacts.json        # Live contacts database (auto-created)
├── contacts_backup.json # Automatic backup (auto-created on first save)
├── requirements.txt     # Dependency notes (stdlib only – no pip install needed)
└── README.md            # This file
```

---

## 🚀 Installation & Running

### Prerequisites
- Python **3.10 or higher**
- Tkinter (bundled with standard Python on Windows and macOS)

#### Linux (if Tkinter is missing)
```bash
sudo apt-get install python3-tk
```

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/PRODIGY_SD_03.git
cd PRODIGY_SD_03

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. No pip installs needed – all stdlib!

# 4. Run the application
python main.py
```

---

## 🖥 Usage

| Action | How |
|---|---|
| Add a contact | Click **+ Add**, fill in the form, click **Save** |
| Edit a contact | Select a row → click **✏ Edit** (or double-click the row) |
| Delete a contact | Select a row → click **🗑 Delete** → confirm the dialog |
| Search | Type in the search bar — table filters instantly |
| Sort | Click any column header (Name / Phone / Email / Created) |

---

## 📸 Screenshots

> _Run the app and take a screenshot to add here._

```
[ Add a screenshot of the main window here ]
[ Add a screenshot of the Add Contact dialog here ]
```

---

## 🏗 Architecture

The code follows a clean **two-layer OOP architecture**:

```
App  (tkinter.Tk)
 ├── ContactStore          ← Data layer: file I/O, CRUD, validation
 ├── ContactDialog         ← Modal form for Add / Edit
 └── Treeview + toolbar    ← Presentation layer
```

- **`ContactStore`** — handles all JSON read/write, UUID generation, duplicate checks, and backup logic. Completely independent of the GUI.
- **`App`** — root window, owns the store, renders the table and toolbar.
- **`ContactDialog`** — reusable modal that works for both Add and Edit.
- **Helper functions** — `validate_name`, `validate_phone`, `validate_email` keep validation logic separate and testable.

---

## 🔒 Data & Backup

- Contacts are stored in `contacts.json` (human-readable JSON).
- Before every write, the current file is automatically copied to `contacts_backup.json`.
- If `contacts.json` is corrupted, rename `contacts_backup.json` to restore.

---

## 🛠 Technologies

- **Python 3.10+**
- **Tkinter** — built-in GUI framework
- **ttk.Treeview** — sortable contact table
- **json / uuid / shutil / re / datetime** — standard library

---

## 📄 License

This project is submitted as part of the **Prodigy Infotech Software Development Internship**.
Free to use for educational purposes.

---

## 🙋 Author

**Vasudev Sivakumar**
Software Development Intern — Prodigy Infotech
GitHub: [@vasudevsivakum](https://github.com/vasudevsivakum)
LinkedIn: [linkedin.com/in/vasudevsivakumar](https://linkedin.com/in/vasudevsivakumar)
