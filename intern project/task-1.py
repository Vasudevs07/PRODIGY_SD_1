import json
import os
import re

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

def validate_email(email):
    return re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email) is not None

def validate_phone(phone):
    return re.match(r"^[\d\s\+\-\(\)]{6,20}$", phone) is not None

def add_contact(contacts):
    print("\n--- Add New Contact ---")
    name = input("Name (required): ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    phone = input("Phone (optional): ").strip()
    if phone and not validate_phone(phone):
        print("Error: Invalid phone number format.")
        return

    email = input("Email (optional): ").strip()
    if email and not validate_email(email):
        print("Error: Invalid email format.")
        return

    contact = {
        "id": str(len(contacts) + 1),
        "name": name,
        "phone": phone,
        "email": email
    }
    contacts.append(contact)
    save_contacts(contacts)
    print(f"\nContact '{name}' added successfully!")

def view_contacts(contacts):
    print("\n--- Contact List ---")
    if not contacts:
        print("No contacts found.")
        return
    for i, c in enumerate(contacts, 1):
        print(f"\n[{i}] {c['name']}")
        if c.get("phone"):
            print(f"    Phone: {c['phone']}")
        if c.get("email"):
            print(f"    Email: {c['email']}")

def search_contacts(contacts):
    print("\n--- Search Contacts ---")
    query = input("Enter name, phone, or email to search: ").strip().lower()
    results = [
        c for c in contacts
        if query in c["name"].lower()
        or query in c.get("phone", "").lower()
        or query in c.get("email", "").lower()
    ]
    if not results:
        print("No contacts found matching your search.")
    else:
        for c in results:
            print(f"\n  Name : {c['name']}")
            if c.get("phone"):
                print(f"  Phone: {c['phone']}")
            if c.get("email"):
                print(f"  Email: {c['email']}")

def edit_contact(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        idx = int(input("\nEnter contact number to edit: ")) - 1
        if idx < 0 or idx >= len(contacts):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    c = contacts[idx]
    print(f"\nEditing: {c['name']} (press Enter to keep current value)")

    new_name = input(f"Name [{c['name']}]: ").strip()
    if new_name:
        c["name"] = new_name

    new_phone = input(f"Phone [{c.get('phone','')}]: ").strip()
    if new_phone:
        if not validate_phone(new_phone):
            print("Error: Invalid phone number. Edit cancelled.")
            return
        c["phone"] = new_phone

    new_email = input(f"Email [{c.get('email','')}]: ").strip()
    if new_email:
        if not validate_email(new_email):
            print("Error: Invalid email address. Edit cancelled.")
            return
        c["email"] = new_email

    save_contacts(contacts)
    print(f"\nContact '{c['name']}' updated successfully!")

def delete_contact(contacts):
    view_contacts(contacts)
    if not contacts:
        return
    try:
        idx = int(input("\nEnter contact number to delete: ")) - 1
        if idx < 0 or idx >= len(contacts):
            print("Invalid selection.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    name = contacts[idx]["name"]
    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").strip().lower()
    if confirm == "y":
        contacts.pop(idx)
        save_contacts(contacts)
        print(f"Contact '{name}' deleted.")
    else:
        print("Deletion cancelled.")

def main():
    contacts = load_contacts()
    print("=============================")
    print("  Contact Management System  ")
    print("=============================")

    while True:
        print("\n--- Main Menu ---")
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contacts")
        print("4. Edit Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contacts(contacts)
        elif choice == "4":
            edit_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()