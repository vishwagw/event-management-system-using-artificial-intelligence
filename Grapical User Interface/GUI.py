import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from services.qr_service import generate_qr_code, scan_qr_code
from services.report_service import generate_report
from models.attendee import Attendee
#from services.notification_service import send_email
from services.whatsapp_service import send_whatsapp_qr

# Global variable to prevent multiple Toplevel forms
current_popup = None

def generate_qr_ui(attendees_list_frame, attendee_to_edit=None):
    """Opens a form to generate or edit attendee QR code."""
    global current_popup
    if current_popup:
        current_popup.lift()
        return  # Avoid multiple instances of the form

    def clear_form():
        """Clears all form fields after submission or edit."""
        try:
            entry_name.delete(0, tk.END)
            entry_phone.delete(0, tk.END)
            entry_amount.delete(0, tk.END)
            entry_persons.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        except tk.TclError:
            pass #Widgets are already destroyed

    def clear_errors():
        """Clears all error labels."""
        error_name.config(text="")
        error_phone.config(text="")
        error_amount.config(text="")
        error_persons.config(text="")
        error_email.config(text="")

    def validate_form():
        """Validates the form and returns a boolean."""
        clear_errors()
        is_valid = True

        if not entry_name.get().strip():
            error_name.config(text="Name is required!")
            is_valid = False

        phone = entry_phone.get().strip()
        if not phone.isdigit() or len(phone) != 10:
            error_phone.config(text="Phone must be a 10-digit number!")
            is_valid = False

        try:
            amount = float(entry_amount.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            error_amount.config(text="Amount must be a positive number!")
            is_valid = False

        try:
            num_persons = int(entry_persons.get().strip())
            if num_persons <= 0:
                raise ValueError
        except ValueError:
            error_persons.config(text="Number of persons must be a positive integer!")
            is_valid = False

        email = entry_email.get().strip()
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            error_email.config(text="Enter a valid email address!")
            is_valid = False

        return is_valid

    def submit():
        """Handles form submission."""        
        if validate_form():
            """Submits attendee details for QR generation and DB storage with validations."""
            username = entry_name.get().strip()
            phone = entry_phone.get().strip()
            amount = float(entry_amount.get().strip())
            num_persons = int(entry_persons.get().strip())
            email = entry_email.get().strip()
            
            if username and phone and amount and num_persons and email:
                qr_code_path = generate_qr_code(f"{username},{phone},{email}", phone)
                existing_attendee = Attendee.get_attendee_by_phone(phone)
            
                if attendee_to_edit:
                    # Update existing attendee
                    attendee_id = attendee_to_edit[0]  # Get the ID from the pre-filled attendee
                    Attendee.update_attendee(username, phone, float(amount), int(num_persons), email, qr_code_path, attendee_id)
                    messagebox.showinfo("Success", "Attendee updated successfully!")
                elif not existing_attendee:
                    # Add new attendee
                    Attendee.add_attendee(username, phone, float(amount), int(num_persons), email, qr_code_path)
                    messagebox.showinfo("Success", "Attendee added successfully!")
                else:
                    messagebox.showerror("Error", "Phone number already exists!")
            
                update_attendees_list(attendees_list_frame)
                # Send QR code to email
                #send_email(email, qr_code_path)
                # Send QR via WhatsApp
                send_whatsapp_qr(phone, qr_code_path)
                messagebox.showinfo("Success", "Attendee added and QR sent via WhatsApp!")
                clear_form()
                close_popup()

            else:
                messagebox.showerror("Error", "All fields are required!")

    def close_popup():
        """Close the Toplevel form."""
        global current_popup
        if current_popup:
            current_popup.destroy()
            current_popup = None

    current_popup = tk.Toplevel()
    current_popup.title("Generate QR Code")
    current_popup.protocol("WM_DELETE_WINDOW", close_popup)

    # Form Fields
    tk.Label(current_popup, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_name = tk.Entry(current_popup)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(current_popup, text="Phone").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_phone = tk.Entry(current_popup)
    entry_phone.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(current_popup, text="Amount").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_amount = tk.Entry(current_popup)
    entry_amount.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(current_popup, text="Persons").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_persons = tk.Entry(current_popup)
    entry_persons.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(current_popup, text="Email").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    entry_email = tk.Entry(current_popup)
    entry_email.grid(row=4, column=1, padx=5, pady=5)

    # Error labels
    error_name = tk.Label(current_popup, text="", fg="red")
    error_name.grid(row=0, column=2, padx=5, sticky="w")

    error_phone = tk.Label(current_popup, text="", fg="red")
    error_phone.grid(row=1, column=2, padx=5, sticky="w")

    error_amount = tk.Label(current_popup, text="", fg="red")
    error_amount.grid(row=2, column=2, padx=5, sticky="w")

    error_persons = tk.Label(current_popup, text="", fg="red")
    error_persons.grid(row=3, column=2, padx=5, sticky="w")

    error_email = tk.Label(current_popup, text="", fg="red")
    error_email.grid(row=4, column=2, padx=5, sticky="w")

    # Pre-fill form fields if editing
    if attendee_to_edit:
        entry_name.insert(0, attendee_to_edit[1])
        entry_phone.insert(0, attendee_to_edit[2])
        entry_amount.insert(0, attendee_to_edit[3])
        entry_persons.insert(0, attendee_to_edit[4])
        entry_email.insert(0, attendee_to_edit[5])

    tk.Button(current_popup, text="Submit", command=submit).grid(row=5, column=0, columnspan=2, pady=10)

def update_attendees_list(frame):
    """Refreshes attendee list table with Edit/Delete buttons."""
    for widget in frame.winfo_children():
        widget.destroy()

    attendees = Attendee.get_all_attendees()
    if attendees:
        columns = ("ID", "Name", "Phone", "Amount", "Persons", "Email", 'QRCode Path', "Attended", "Created", "Updated")
        tree = ttk.Treeview(frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)

        for attendee in attendees:
            tree.insert("", "end", values=attendee)

        tree.pack(fill="both", expand=True)

        def delete_attendee():
            """Delete selected attendee after confirmation."""
            selected = tree.selection()
            if not selected:
                return

            attendee = tree.item(selected[0])['values']
            confirm = messagebox.askyesno("Confirm Delete", f"Delete {attendee[1]}?")
            if confirm:
                Attendee.delete_attendee(attendee[2])
                update_attendees_list(frame)

        def edit_attendee():
            """Edit selected attendee."""
            selected = tree.selection()
            if not selected:
                return
            attendee = tree.item(selected[0])['values']
            generate_qr_ui(frame, attendee_to_edit=attendee)

        # Buttons on Frame
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Edit", command=edit_attendee).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete", command=delete_attendee).pack(side=tk.RIGHT, padx=10)

    else:
        tk.Label(frame, text="No attendees yet.", font=("Arial", 12)).pack(pady=10)

def main_ui():
    """Main UI Entry for Application."""
    root = tk.Tk()
    root.title("Event Management System")

    tk.Button(root, text="Generate QR Code", command=lambda: generate_qr_ui(attendees_frame)).pack(pady=10)
    tk.Button(root, text="Generate Report", command=generate_report).pack(pady=10)

    attendees_frame = tk.Frame(root)
    attendees_frame.pack(fill="both", expand=True, padx=10, pady=10)

    update_attendees_list(attendees_frame)
    root.mainloop()
