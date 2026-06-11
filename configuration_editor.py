import configparser
import json
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


CONFIG_PATH = Path("configuration.ini")


class ConfigurationEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Rom-Linker Configuration")
        self.geometry("720x600")
        self.minsize(640, 540)

        self.scan_disks = tk.StringVar()
        self.ignore_disks = tk.StringVar()
        self.ignore_consoles = tk.StringVar()
        self.ignore_local_disk = tk.BooleanVar()
        self.internal_roms_path = tk.StringVar()
        self.external_roms_path = tk.StringVar()
        self.dry_run = tk.BooleanVar()
        self.auto_close = tk.BooleanVar()
        self.auto_close_seconds = tk.IntVar()
        self.status = tk.StringVar(value="Ready")

        self.configure(background="#f5f7fb")
        self.create_style()
        self.create_widgets()
        self.load_configuration()

    def create_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#f5f7fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f5f7fb", foreground="#1f2937")
        style.configure("Card.TLabel", background="#ffffff", foreground="#1f2937")
        style.configure("Hint.TLabel", background="#ffffff", foreground="#6b7280", font=("Segoe UI", 9))
        style.configure("Title.TLabel", background="#f5f7fb", foreground="#111827", font=("Segoe UI", 18, "bold"))
        style.configure("Section.TLabel", background="#ffffff", foreground="#111827", font=("Segoe UI", 11, "bold"))
        style.configure("TButton", padding=(12, 6))
        style.configure("Accent.TButton", background="#2563eb", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("TCheckbutton", background="#ffffff", foreground="#1f2937")

    def create_widgets(self):
        root = ttk.Frame(self, padding=20)
        root.pack(fill="both", expand=True)

        header = ttk.Frame(root)
        header.pack(fill="x", pady=(0, 16))
        ttk.Label(header, text="Rom-Linker Configuration", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Edit configuration.ini without touching the file by hand.",
        ).pack(anchor="w", pady=(4, 0))

        canvas = tk.Canvas(root, borderwidth=0, background="#f5f7fb", highlightthickness=0)
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
        self.form = ttk.Frame(canvas)
        self.form.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.form, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.create_scan_card()
        self.create_ignore_card()
        self.create_path_card()
        self.create_options_card()

        footer = ttk.Frame(root)
        footer.pack(fill="x", pady=(14, 0))
        ttk.Label(footer, textvariable=self.status).pack(side="left")
        ttk.Button(footer, text="Reload", command=self.load_configuration).pack(side="right", padx=(8, 0))
        ttk.Button(footer, text="Save", style="Accent.TButton", command=self.save_configuration).pack(side="right")

    def create_card(self, title):
        card = ttk.Frame(self.form, style="Card.TFrame", padding=16)
        card.pack(fill="x", pady=(0, 12))
        ttk.Label(card, text=title, style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        return card

    def add_text_field(self, parent, label, variable, hint):
        ttk.Label(parent, text=label, style="Card.TLabel").pack(anchor="w")
        ttk.Entry(parent, textvariable=variable).pack(fill="x", pady=(4, 2))
        ttk.Label(parent, text=hint, style="Hint.TLabel").pack(anchor="w", pady=(0, 10))

    def create_scan_card(self):
        card = self.create_card("Scan")
        self.add_text_field(card, "scan_disks", self.scan_disks, 'JSON list. Example: ["D", "H"]. Empty [] scans all drives.')

    def create_ignore_card(self):
        card = self.create_card("Ignore")
        self.add_text_field(card, "ignore_disks", self.ignore_disks, 'JSON list. Example: ["C"].')
        self.add_text_field(card, "ignore_consoles", self.ignore_consoles, 'JSON list. Example: ["n64", "megadrive"].')
        ttk.Checkbutton(card, text="Ignore local disk", variable=self.ignore_local_disk).pack(anchor="w")

    def create_path_card(self):
        card = self.create_card("Paths")
        ttk.Label(card, text="internal_roms_path", style="Card.TLabel").pack(anchor="w")
        internal_row = ttk.Frame(card, style="Card.TFrame")
        internal_row.pack(fill="x", pady=(4, 2))
        ttk.Entry(internal_row, textvariable=self.internal_roms_path).pack(side="left", fill="x", expand=True)
        ttk.Button(internal_row, text="Browse", command=self.browse_internal_path).pack(side="left", padx=(8, 0))
        ttk.Label(card, text="Local roms folder. Must end with /.", style="Hint.TLabel").pack(anchor="w", pady=(0, 10))
        self.add_text_field(card, "external_roms_path", self.external_roms_path, "Roms folder inside each external drive. Must end with /.")

    def create_options_card(self):
        card = self.create_card("Options")
        ttk.Checkbutton(card, text="Dry run", variable=self.dry_run).pack(anchor="w")
        ttk.Label(
            card,
            text="Shows what would happen without creating links, deleting links, or renaming folders.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(0, 10))
        ttk.Checkbutton(card, text="Auto close", variable=self.auto_close).pack(anchor="w")
        ttk.Label(card, text="auto_close_seconds", style="Card.TLabel").pack(anchor="w", pady=(10, 0))
        ttk.Spinbox(card, from_=0, to=3600, textvariable=self.auto_close_seconds, width=10).pack(anchor="w", pady=(4, 0))

    def browse_internal_path(self):
        selected = filedialog.askdirectory(title="Select internal roms folder")
        if selected:
            path_value = selected.replace("\\", "/")
            if not path_value.endswith("/"):
                path_value += "/"
            self.internal_roms_path.set(path_value)

    def load_configuration(self):
        if not CONFIG_PATH.exists():
            messagebox.showerror("Missing file", "configuration.ini was not found.")
            return

        config = configparser.ConfigParser()
        config.read(CONFIG_PATH)

        self.scan_disks.set(config.get("SCAN", "scan_disks", fallback="[]"))
        self.ignore_disks.set(config.get("IGNORE", "ignore_disks", fallback="[]"))
        self.ignore_consoles.set(config.get("IGNORE", "ignore_consoles", fallback="[]"))
        self.ignore_local_disk.set(read_bool(config, "IGNORE", "ignore_local_disk", True))
        self.internal_roms_path.set(config.get("PATH", "internal_roms_path", fallback="./roms/"))
        self.external_roms_path.set(config.get("PATH", "external_roms_path", fallback="/roms/"))
        self.dry_run.set(read_bool(config, "OPTIONS", "dry_run", False))
        self.auto_close.set(read_bool(config, "OPTIONS", "auto_close", True))
        self.auto_close_seconds.set(config.getint("OPTIONS", "auto_close_seconds", fallback=10))
        self.status.set("Loaded configuration.ini")

    def save_configuration(self):
        try:
            scan_disks = parse_json_list("scan_disks", self.scan_disks.get())
            ignore_disks = parse_json_list("ignore_disks", self.ignore_disks.get())
            ignore_consoles = parse_json_list("ignore_consoles", self.ignore_consoles.get())
            internal_path = validate_path("internal_roms_path", self.internal_roms_path.get())
            external_path = validate_path("external_roms_path", self.external_roms_path.get())
            auto_close_seconds = int(self.auto_close_seconds.get())
            if auto_close_seconds < 0:
                raise ValueError("auto_close_seconds must be zero or greater.")
        except ValueError as error:
            messagebox.showerror("Invalid configuration", str(error))
            return

        CONFIG_PATH.write_text(
            build_configuration_text(
                scan_disks,
                ignore_disks,
                ignore_consoles,
                self.ignore_local_disk.get(),
                internal_path,
                external_path,
                self.dry_run.get(),
                self.auto_close.get(),
                auto_close_seconds,
            ),
            encoding="utf-8",
        )
        self.status.set("Saved configuration.ini")
        messagebox.showinfo("Saved", "configuration.ini was saved successfully.")


def parse_json_list(name, value):
    parsed = json.loads(value)
    if not isinstance(parsed, list):
        raise ValueError(f"{name} must be a JSON list.")
    for entry in parsed:
        if not isinstance(entry, str):
            raise ValueError(f"{name} must contain only strings.")
    return parsed


def validate_path(name, value):
    if not value.endswith("/"):
        raise ValueError(f"{name} must end with /.")
    return value


def read_bool(config, section, option, fallback):
    if not config.has_option(section, option):
        return fallback
    return config.get(section, option).strip().lower() in ["1", "true", "yes", "on"]


def bool_to_ini(value):
    return "1" if value else "0"


def build_configuration_text(
    scan_disks,
    ignore_disks,
    ignore_consoles,
    ignore_local_disk,
    internal_roms_path,
    external_roms_path,
    dry_run,
    auto_close,
    auto_close_seconds,
):
    return f"""; REMOVE THE SEMICOLON AT THE BEGINNING OF THE LINE IF YOU WANT TO USE IT

; IF YOU INCLUDE A "X:" DISK TO "scan_disks" AND ADD IT TO "ignore_disks"
; OR if it is the local disk and "ignore_local_disk=true" IT WILL IGNORE IT
; IN OTHER WORDS: ROM-LINKER GIVES PRIORITY TO THE [IGNORE] SECTION

[SCAN]
; Empty [] means all disks will be scanned
scan_disks={json.dumps(scan_disks)}

[IGNORE]
; Empty [] means no disk will be ignored
ignore_disks={json.dumps(ignore_disks)}

; Empty [] means no console will be ignored
ignore_consoles={json.dumps(ignore_consoles)}

; Value 1 is ON, anything else is OFF
ignore_local_disk={bool_to_ini(ignore_local_disk)}

[PATH]
; It needs to end with /
internal_roms_path={internal_roms_path}

; It needs to end with /
external_roms_path={external_roms_path}

[OPTIONS]
; Shows what would be changed without creating links, deleting links, or renaming folders
; Value 1 is ON, anything else is OFF
dry_run={bool_to_ini(dry_run)}

; Closes the script after it finishes running
auto_close={bool_to_ini(auto_close)}

; Configures how many seconds the script will wait before closing
auto_close_seconds={auto_close_seconds}
"""


if __name__ == "__main__":
    app = ConfigurationEditor()
    app.mainloop()
