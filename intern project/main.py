import json
import os
import re
import shutil
import uuid
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

CONTACTS_FILE = "contacts.json"
BACKUP_FILE   = "contacts_backup.json"
APP_TITLE     = "Contact Management System"
WINDOW_SIZE   = "860x560"

BG_DARK    = "#1e1e2e"
BG_PANEL   = "#2a2a3e"
BG_CARD    = "#313145"
ACCENT     = "#7c6af7"
ACCENT_HOV = "#6a58e0"
TEXT_PRI   = "#e0e0f0"
TEXT_SEC   = "#9090b0"
DANGER     = "#e05a5a"
BORDER     = "#44445a"


class ContactStore:
    def __init__(self, filepath: str = CONTACTS_FILE):
        self.filepath = filepath
        self.contacts: list[dict] = []
        self.load()

    def load(self) -> None:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.contacts = data if isinstance(data, list) else data.get("contacts", [])
            except (json.JSONDecodeError, IOError) as exc:
                messagebox.showerror("Load Error", f"Could not read contacts file:\n{exc}")
                self.contacts = []
        else:
            self.contacts = []
            self._write()

    def save(self) -> None:
        self._backup()
        self._write()

    def _write(self) -> None:
        try:
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self.contacts, f, indent=2, ensure_ascii=False)
        except IOError as exc:
            messagebox.showerror("Save Error", f"Could not save contacts:\n{exc}")

    def _backup(self) -> None:
        if os.path.exists(self.filepath):
            try:
                shutil.copy2(self.filepath, BACKUP_FILE)
            except IOError:
                pass

    def add(self, name: str, phone: str, email: str) -> dict:
        self._check_duplicate(name, phone)
        contact = {
            "id":      str(uuid.uuid4()),
            "name":    name.strip(),
            "phone":   phone.strip(),
            "email":   email.strip(),
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        self.contacts.append(contact)
        self.save()
        return contact

    def update(self, contact_id: str, name: str, phone: str, email: str) -> dict:
        self._check_duplicate(name, phone, exclude_id=contact_id)
        for c in self.contacts:
            if c["id"] == contact_id:
                c["name"]    = name.strip()
                c["phone"]   = phone.strip()
                c["email"]   = email.strip()
                c["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save()
                return c
        raise LookupError(f"Contact with id {contact_id} not found.")

    def delete(self, contact_id: str) -> None:
        self.contacts = [c for c in self.contacts if c["id"] != contact_id]
        self.save()

    def search(self, query: str) -> list[dict]:
        q = query.lower().strip()
        if not q:
            return self.contacts
        return [
            c for c in self.contacts
            if q in c["name"].lower()
            or q in c.get("phone", "").lower()
            or q in c.get("email", "").lower()
        ]

    def get_by_id(self, contact_id: str) -> dict | None:
        return next((c for c in self.contacts if c["id"] == contact_id), None)

    def _check_duplicate(self, name: str, phone: str, exclude_id: str = None) -> None:
        for c in self.contacts:
            if c["id"] == exclude_id:
                continue
            if c["name"].lower() == name.strip().lower():
                raise ValueError(f"A contact named '{name}' already exists.")
            if phone.strip() and c.get("phone") == phone.strip():
                raise ValueError(f"Phone number '{phone}' is already in use.")


def validate_name(name: str) -> str:
    name = name.strip()
    if not name:
        raise ValueError("Name is required.")
    if len(name) < 2:
        raise ValueError("Name must be at least 2 characters.")
    if len(name) > 60:
        raise ValueError("Name must be under 60 characters.")
    return name

def validate_phone(phone: str) -> str:
    phone = phone.strip()
    if phone and not re.match(r"^[\d\s\+\-\(\)]{6,20}$", phone):
        raise ValueError("Phone must be 6-20 chars (digits, spaces, +, -, ( ) ).")
    return phone

def validate_email(email: str) -> str:
    email = email.strip()
    if email and not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        raise ValueError("Please enter a valid email address.")
    return email


def styled_button(parent, text, command, bg=ACCENT, fg=TEXT_PRI,
                  hover_bg=ACCENT_HOV, **kwargs) -> tk.Button:
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=hover_bg, activeforeground=fg,
        relief="flat", cursor="hand2", padx=14, pady=6,
        font=("Segoe UI", 10, "bold"), bd=0, **kwargs
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

def labeled_entry(parent, label_text: str, row: int,
                  show: str = "") -> tuple[tk.Label, tk.Entry]:
    lbl = tk.Label(parent, text=label_text, bg=BG_CARD,
                   fg=TEXT_SEC, font=("Segoe UI", 9))
    lbl.grid(row=row, column=0, sticky="w", padx=(20, 8), pady=(10, 0))
    var = tk.StringVar()
    ent = tk.Entry(parent, textvariable=var, show=show,
                   bg=BG_PANEL, fg=TEXT_PRI, insertbackground=TEXT_PRI,
                   relief="flat", font=("Segoe UI", 11),
                   highlightthickness=1, highlightcolor=ACCENT,
                   highlightbackground=BORDER)
    ent.grid(row=row + 1, column=0, sticky="ew", padx=20, pady=(2, 0), ipady=6)
    return lbl, ent


class ContactDialog(tk.Toplevel):
    def __init__(self, parent, title: str, contact: dict = None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.configure(bg=BG_CARD)
        self.grab_set()
        self.result: dict | None = None
        self._contact = contact
        self._build_ui()
        self._populate(contact)
        self._center(parent)

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        tk.Label(self, text=self.title(), bg=BG_CARD, fg=TEXT_PRI,
                 font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, sticky="w", padx=20, pady=(18, 4))

        tk.Frame(self, bg=ACCENT, height=2).grid(
            row=1, column=0, sticky="ew", padx=20, pady=(0, 6))

        _, self.ent_name  = labeled_entry(self, "Full Name *", row=2)
        _, self.ent_phone = labeled_entry(self, "Phone Number", row=4)
        _, self.ent_email = labeled_entry(self, "Email Address", row=6)

        self.lbl_err = tk.Label(self, text="", bg=BG_CARD, fg=DANGER,
                                font=("Segoe UI", 9), wraplength=280, justify="left")
        self.lbl_err.grid(row=8, column=0, sticky="w", padx=20, pady=(8, 0))

        btn_frame = tk.Frame(self, bg=BG_CARD)
        btn_frame.grid(row=9, column=0, sticky="ew", padx=20, pady=16)
        styled_button(btn_frame, "  Save  ", self._on_save).pack(side="right", padx=(6, 0))
        styled_button(btn_frame, "Cancel", self.destroy,
                      bg=BG_PANEL, hover_bg=BORDER).pack(side="right")

    def _populate(self, contact: dict | None) -> None:
        if contact:
            self.ent_name.insert(0, contact.get("name", ""))
            self.ent_phone.insert(0, contact.get("phone", ""))
            self.ent_email.insert(0, contact.get("email", ""))

    def _center(self, parent) -> None:
        self.update_idletasks()
        pw = parent.winfo_rootx() + parent.winfo_width() // 2
        ph = parent.winfo_rooty() + parent.winfo_height() // 2
        w, h = self.winfo_width(), self.winfo_height()
        self.geometry(f"+{pw - w // 2}+{ph - h // 2}")

    def _on_save(self) -> None:
        self.lbl_err.config(text="")
        try:
            name  = validate_name(self.ent_name.get())
            phone = validate_phone(self.ent_phone.get())
            email = validate_email(self.ent_email.get())
        except ValueError as exc:
            self.lbl_err.config(text=str(exc))
            return
        self.result = {"name": name, "phone": phone, "email": email}
        self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(720, 460)
        self.configure(bg=BG_DARK)
        self.store = ContactStore()
        self._selected_id: str | None = None
        self._apply_styles()
        self._build_ui()
        self._refresh_table()

    def _apply_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_PANEL, foreground=TEXT_PRI,
                        rowheight=32, fieldbackground=BG_PANEL,
                        bordercolor=BORDER, borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background=BG_DARK, foreground=ACCENT,
                        relief="flat", font=("Segoe UI", 10, "bold"))
        style.map("Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", "#ffffff")])

    def _build_ui(self) -> None:
        header = tk.Frame(self, bg=BG_PANEL, height=56)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="📋  " + APP_TITLE,
                 bg=BG_PANEL, fg=TEXT_PRI,
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=20, pady=12)

        self.lbl_count = tk.Label(header, text="0 contacts",
                                  bg=ACCENT, fg="#ffffff",
                                  font=("Segoe UI", 9, "bold"),
                                  padx=10, pady=4)
        self.lbl_count.pack(side="right", padx=20, pady=14)

        toolbar = tk.Frame(self, bg=BG_DARK)
        toolbar.pack(fill="x", padx=16, pady=(12, 6))

        search_frame = tk.Frame(toolbar, bg=BG_PANEL,
                                highlightthickness=1, highlightbackground=BORDER)
        search_frame.pack(side="left", fill="x", expand=True)

        tk.Label(search_frame, text="🔍", bg=BG_PANEL,
                 fg=TEXT_SEC, font=("Segoe UI", 11)).pack(side="left", padx=(8, 0))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search())
        tk.Entry(search_frame, textvariable=self.search_var,
                 bg=BG_PANEL, fg=TEXT_PRI, insertbackground=TEXT_PRI,
                 relief="flat", font=("Segoe UI", 11),
                 highlightthickness=0).pack(
            side="left", fill="x", expand=True, ipady=7, padx=6)

        btn_bar = tk.Frame(toolbar, bg=BG_DARK)
        btn_bar.pack(side="right", padx=(12, 0))
        styled_button(btn_bar, "+ Add",    self._on_add).pack(side="left", padx=3)
        styled_button(btn_bar, "✏  Edit",  self._on_edit,
                      bg=BG_CARD, hover_bg=BORDER).pack(side="left", padx=3)
        styled_button(btn_bar, "🗑 Delete", self._on_delete,
                      bg=DANGER, hover_bg="#c04040").pack(side="left", padx=3)

        table_frame = tk.Frame(self, bg=BG_DARK)
        table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        cols = ("Name", "Phone", "Email", "Created")
        self.tree = ttk.Treeview(table_frame, columns=cols,
                                 show="headings", selectmode="browse")

        widths = {"Name": 200, "Phone": 150, "Email": 240, "Created": 140}
        for col in cols:
            self.tree.heading(col, text=col,
                              command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=widths[col], anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda _: self._on_edit())

        self.lbl_status = tk.Label(self, text="Ready",
                                   bg=BG_PANEL, fg=TEXT_SEC,
                                   font=("Segoe UI", 9), anchor="w", padx=12)
        self.lbl_status.pack(fill="x", side="bottom")

    def _refresh_table(self, contacts: list = None) -> None:
        self.tree.delete(*self.tree.get_children())
        rows = contacts if contacts is not None else self.store.contacts

        self.tree.tag_configure("odd",  background=BG_PANEL)
        self.tree.tag_configure("even", background=BG_CARD)

        for i, c in enumerate(rows):
            tag = "odd" if i % 2 == 0 else "even"
            self.tree.insert("", "end", iid=c["id"],
                             values=(c["name"],
                                     c.get("phone", "—"),
                                     c.get("email", "—"),
                                     c.get("created", "—")),
                             tags=(tag,))

        count = len(rows)
        total = len(self.store.contacts)
        self.lbl_count.config(text=f"{count} contact{'s' if count != 1 else ''}")
        if count < total:
            self._set_status(f"Showing {count} of {total} contacts")
        else:
            self._set_status(f"{total} contact{'s' if total != 1 else ''} loaded")

        self._selected_id = None

    def _get_selected_contact(self) -> dict | None:
        sel = self.tree.selection()
        if not sel:
            return None
        return self.store.get_by_id(sel[0])

    def _sort_by(self, col: str) -> None:
        key_map = {"Name": "name", "Phone": "phone",
                   "Email": "email", "Created": "created"}
        key = key_map.get(col, "name")
        self.store.contacts.sort(
            key=lambda c: c.get(key, "").lower(),
            reverse=getattr(self, "_sort_asc", False)
        )
        self._sort_asc = not getattr(self, "_sort_asc", False)
        self._refresh_table()

    def _set_status(self, msg: str) -> None:
        self.lbl_status.config(text=msg)

    def _on_select(self, _event=None) -> None:
        sel = self.tree.selection()
        self._selected_id = sel[0] if sel else None

    def _on_search(self) -> None:
        results = self.store.search(self.search_var.get())
        self._refresh_table(results)

    def _on_add(self) -> None:
        dlg = ContactDialog(self, "Add New Contact")
        self.wait_window(dlg)
        if dlg.result:
            try:
                c = self.store.add(**dlg.result)
                self._refresh_table()
                self.tree.selection_set(c["id"])
                self.tree.see(c["id"])
                self._set_status(f"✔  Contact '{c['name']}' added.")
                messagebox.showinfo("Success", f"'{c['name']}' has been added!")
            except ValueError as exc:
                messagebox.showerror("Duplicate Contact", str(exc))

    def _on_edit(self) -> None:
        contact = self._get_selected_contact()
        if not contact:
            messagebox.showwarning("No Selection", "Please select a contact to edit.")
            return
        dlg = ContactDialog(self, "Edit Contact", contact)
        self.wait_window(dlg)
        if dlg.result:
            try:
                c = self.store.update(contact["id"], **dlg.result)
                self._refresh_table()
                self.tree.selection_set(c["id"])
                self._set_status(f"✔  Contact '{c['name']}' updated.")
                messagebox.showinfo("Updated", f"'{c['name']}' has been updated!")
            except (ValueError, LookupError) as exc:
                messagebox.showerror("Error", str(exc))

    def _on_delete(self) -> None:
        contact = self._get_selected_contact()
        if not contact:
            messagebox.showwarning("No Selection", "Please select a contact to delete.")
            return
        confirmed = messagebox.askyesno(
            "Confirm Delete",
            f"Delete '{contact['name']}'?\n\nThis action cannot be undone.",
            icon="warning"
        )
        if confirmed:
            self.store.delete(contact["id"])
            self._refresh_table()
            self._set_status(f"🗑  Contact '{contact['name']}' deleted.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
