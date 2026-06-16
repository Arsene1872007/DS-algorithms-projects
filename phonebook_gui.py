import customtkinter as ctk
from tkinter import messagebox
from hashtable import HashTable
from Contactlogic import add_contact, delete_contact, update_contact
from validation import strip_non_digits

# ── Color Palette ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")

BG_MAIN      = "#080808"
BG_CARD      = "#121212"
BG_INPUT     = "#1C1C1C"
ACCENT       = "#E53935"
ACCENT_HOVER = "#FF4D4D"
DANGER       = "#9A0007"
TEXT_MAIN    = "#FFFFFF"
TEXT_MUTED   = "#757575"


class PhonebookApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.phonebook = HashTable()
        self.editing_contact = None   # (name, phone_no) of the contact being edited
        self._toast_job = None

        self.title("PHONEBOOK | Dashboard")
        self.geometry("1000x650")
        self.minsize(900, 600)
        self.configure(fg_color=BG_MAIN)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()
        self._refresh_list()

    # ── Sidebar ───────────────────────────────────────────────────────────────
    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, fg_color=BG_CARD, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        ctk.CTkLabel(self.sidebar, text="P H O N E B O O K",
                     font=("Arial Black", 24), text_color=ACCENT).pack(pady=(40, 5), anchor="w", padx=30)
        ctk.CTkLabel(self.sidebar, text="SECURE COMPACT STORAGE",
                     font=("Arial Bold", 10), text_color=TEXT_MUTED).pack(anchor="w", padx=30, pady=(0, 40))

        self.form_title = ctk.CTkLabel(self.sidebar, text="Add New Contact",
                                       font=("Arial Bold", 18), text_color=TEXT_MAIN)
        self.form_title.pack(anchor="w", padx=30, pady=(0, 15))

        self.entry_name = ctk.CTkEntry(self.sidebar, placeholder_text="Full Name",
                                       height=45, fg_color=BG_INPUT, border_width=0, font=("Arial", 14))
        self.entry_name.pack(fill="x", padx=30, pady=10)

        self.entry_phone = ctk.CTkEntry(self.sidebar, placeholder_text="Phone Number (digits only)",
                                        height=45, fg_color=BG_INPUT, border_width=0, font=("Arial", 14))
        self.entry_phone.pack(fill="x", padx=30, pady=10)
        self.entry_phone.bind("<KeyRelease>", self._enforce_digits_only)

        self.btn_save = ctk.CTkButton(self.sidebar, text="Save Contact", height=45,
                                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                                      text_color=TEXT_MAIN, font=("Arial Bold", 14),
                                      command=self._handle_save)
        self.btn_save.pack(fill="x", padx=30, pady=(20, 10))

        self.btn_cancel = ctk.CTkButton(self.sidebar, text="Cancel Edit", height=45,
                                        fg_color="transparent", hover_color=BG_INPUT,
                                        text_color=TEXT_MUTED, font=("Arial Bold", 14),
                                        command=self._reset_form)

        ctk.CTkLabel(self.sidebar, text="").pack(expand=True)

        self.lbl_stats = ctk.CTkLabel(self.sidebar, text="",
                                      font=("Arial", 12), text_color=TEXT_MUTED)
        self.lbl_stats.pack(pady=20)

    # ── Main Area ─────────────────────────────────────────────────────────────
    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        search_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        ctk.CTkLabel(search_frame, text="Index Directory",
                     font=("Arial Black", 24), text_color=TEXT_MAIN).pack(side="left")

        self.entry_search = ctk.CTkEntry(
            search_frame, placeholder_text="🔍 Filter registry instantly...",
            width=300, height=40, fg_color=BG_INPUT,
            border_color=ACCENT, border_width=1, corner_radius=20)
        self.entry_search.pack(side="right")
        self.entry_search.bind("<KeyRelease>", self._handle_search)

        self.list_frame = ctk.CTkScrollableFrame(self.main_area, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, sticky="nsew")

    # ── Phone digit enforcement ───────────────────────────────────────────────
    def _enforce_digits_only(self, event=None):
        text = self.entry_phone.get()
        clean = strip_non_digits(text)
        if text != clean:
            self._show_toast("Digits only — no letters or symbols.", "error")
            cursor = self.entry_phone.index("insert")
            self.entry_phone.delete(0, "end")
            self.entry_phone.insert(0, clean)
            self.entry_phone.icursor(min(cursor, len(clean)))

    # ── Save handler ──────────────────────────────────────────────────────────
    def _handle_save(self):
        name  = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()

        if self.editing_contact:
            old_name, old_phone = self.editing_contact
            if old_name.lower() != name.lower():
                # Name changed — delete old entry then add as new contact
                del_result = delete_contact(self.phonebook, old_name, old_phone)
                if "deleted" not in del_result.lower():
                    self._show_toast(del_result, "error")
                    return
                result = add_contact(self.phonebook, name, phone)
            else:
                result = update_contact(self.phonebook, old_name, old_phone, phone)
        else:
            result = add_contact(self.phonebook, name, phone)

        success = "successfully" in result.lower()
        self._show_toast(result, "success" if success else "error")
        if success:
            self._reset_form()
            self._refresh_list()

    # ── Edit / Delete ─────────────────────────────────────────────────────────
    def _prepare_edit(self, name, phone_no):
        self.editing_contact = (name, phone_no)
        self.form_title.configure(text="Modify Registry", text_color=ACCENT)

        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, name)

        self.entry_phone.delete(0, "end")
        self.entry_phone.insert(0, phone_no)

        self.btn_save.configure(text="Commit Changes")
        self.btn_cancel.pack(fill="x", padx=30, pady=5, after=self.btn_save)

    def _delete_contact(self, name, phone_no):
        if messagebox.askyesno("Confirm Wipe", f"Permanently wipe '{name}' from storage?"):
            result = delete_contact(self.phonebook, name, phone_no)
            if "deleted" in result.lower():
                self._show_toast(result, "success")
                if self.editing_contact == (name, phone_no):
                    self._reset_form()
                self._refresh_list()
            else:
                self._show_toast(result, "error")

    # ── Reset form ────────────────────────────────────────────────────────────
    def _reset_form(self):
        self.editing_contact = None
        self.form_title.configure(text="Add New Contact", text_color=TEXT_MAIN)
        self.entry_name.delete(0, "end")
        self.entry_phone.delete(0, "end")
        self.btn_save.configure(text="Save Contact")
        self.btn_cancel.pack_forget()

    # ── Search ────────────────────────────────────────────────────────────────
    def _handle_search(self, event=None):
        query = self.entry_search.get().lower()
        filtered = [c for c in self._get_all_contacts()
                    if query in c.name.lower() or query in c.phone_no]
        self._populate_list(filtered)

    # ── List helpers ──────────────────────────────────────────────────────────
    def _get_all_contacts(self):
        contacts = []
        for i in range(self.phonebook.size):
            cur = self.phonebook.buckets[i]
            while cur:
                contacts.append(cur)
                cur = cur.next
        return sorted(contacts, key=lambda c: c.name.lower())

    def _refresh_list(self):
        self._update_stats()
        self.entry_search.delete(0, "end")
        self._populate_list(self._get_all_contacts())

    def _update_stats(self):
        count = 0
        for i in range(self.phonebook.size):
            cur = self.phonebook.buckets[i]
            while cur:
                count += 1
                cur = cur.next
        self.lbl_stats.configure(text=f"Total Registry Entries: {count}")

    def _populate_list(self, contacts):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not contacts:
            ctk.CTkLabel(self.list_frame, text="Memory array empty.",
                         font=("Arial", 14), text_color=TEXT_MUTED).pack(pady=40)
            return

        for contact in contacts:
            card = ctk.CTkFrame(self.list_frame, fg_color=BG_CARD, corner_radius=12)
            card.pack(fill="x", pady=6, padx=5)

            avatar_frame = ctk.CTkFrame(card, width=45, height=45, corner_radius=22, fg_color=BG_INPUT)
            avatar_frame.pack(side="left", padx=15, pady=15)
            avatar_frame.pack_propagate(False)
            ctk.CTkLabel(avatar_frame, text=contact.name[0].upper(),
                         font=("Arial Bold", 18), text_color=ACCENT).place(relx=0.5, rely=0.5, anchor="center")

            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, pady=10)
            ctk.CTkLabel(info_frame, text=contact.name,
                         font=("Arial Bold", 16), text_color=TEXT_MAIN).pack(anchor="w", pady=(2, 0))
            ctk.CTkLabel(info_frame, text=contact.phone_no,
                         font=("Arial", 13), text_color=TEXT_MUTED).pack(anchor="w")

            btn_edit = ctk.CTkButton(card, text="✏️", width=40, fg_color="transparent",
                                     hover_color=BG_INPUT, text_color=ACCENT, font=("Arial", 16),
                                     command=lambda c=contact: self._prepare_edit(c.name, c.phone_no))
            btn_edit.pack(side="right", padx=(0, 15))

            btn_del = ctk.CTkButton(card, text="🗑️", width=40, fg_color="transparent",
                                    hover_color=DANGER, text_color=TEXT_MUTED, font=("Arial", 16),
                                    command=lambda c=contact: self._delete_contact(c.name, c.phone_no))
            btn_del.pack(side="right", padx=(0, 5))

    # ── Toast notifications ───────────────────────────────────────────────────
    def _show_toast(self, message, m_type="success"):
        if getattr(self, "toast_frame", None):
            try:
                self.toast_frame.destroy()
            except Exception:
                pass
        if self._toast_job:
            self.after_cancel(self._toast_job)

        color = ACCENT if m_type == "success" else DANGER
        self.toast_frame = ctk.CTkFrame(self.main_area, fg_color=color, corner_radius=20)
        self.toast_frame.place(relx=0.5, rely=0.95, anchor="s")
        ctk.CTkLabel(self.toast_frame, text=message,
                     font=("Arial Bold", 13), text_color=TEXT_MAIN).pack(padx=25, pady=10)
        self._toast_job = self.after(3000, self.toast_frame.destroy)


if __name__ == "__main__":
    app = PhonebookApp()
    app.mainloop()
