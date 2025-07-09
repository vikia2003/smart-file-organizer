import os
import shutil
import json
from datetime import datetime
from tkinter import Tk, Button, filedialog, messagebox, font, Label, Frame

organizer = None

class FileOrganizer:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.classified_files = {}
        
    def get_files(self):
        if os.path.isdir(self.folder_path):
            try:
                folder_item = os.listdir(self.folder_path)
                files_list = []
                for file in folder_item:
                    file_path = os.path.join(self.folder_path, file)
                    if os.path.isfile(file_path):
                        files_list.append(file)
                return files_list
            except PermissionError as er:
                print("Error accessing folder: ", er)
        elif os.path.isfile(self.folder_path):
            print("This is a file, not a folder.")
            return []
        else:
            print("Folder doesn't exist! :(")
            return []
        
    def classify_files(self):
        files = self.get_files()
        self.classified_files = {}
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in self.classified_files:
                self.classified_files[ext].append(file)
            else:
                self.classified_files[ext] = [file]

    def get_unique_filename(self, folder, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_name = filename
        while os.path.exists(os.path.join(folder, new_name)):
            new_name = f"{base}_{counter}{ext}"
            counter += 1
        return new_name
        
    def create_folders_and_move_files(self):
        try:
            log_entries = []
            for ext, files in self.classified_files.items():
                folder_name = ext[1:] if ext else "no_extension"
                dest_folder_path = os.path.join(self.folder_path, folder_name)
                if not os.path.exists(dest_folder_path):
                    os.makedirs(dest_folder_path)
                for file in files:
                    src_path = os.path.join(self.folder_path, file)
                    unique_name = self.get_unique_filename(dest_folder_path, file)
                    dest_path = os.path.join(dest_folder_path, unique_name)
                    shutil.move(src_path, dest_path)
                    log_entries.append({
                        "original_path": src_path,
                        "new_path": dest_path,
                        "time": datetime.now().isoformat()
                    })
            log_path = os.path.join(self.folder_path, "file_log.json")
            self.log_moved_files(log_entries, log_path)
            return True
        except Exception as e:
            print(f"Error during organizing files: {e}")
            return False


    def log_moved_files(self, log_entries, log_path):
        batch_id = datetime.now().isoformat()
        new_batch = {
            "batch_id": batch_id,
            "entries": log_entries
        }

        all_batches = []
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r') as f:
                    all_batches = json.load(f)
            except json.JSONDecodeError:
                all_batches = []

        all_batches.append(new_batch)

        with open(log_path, 'w') as f:
            json.dump(all_batches, f, indent=2)



    def undo_last_operation(self, log_path=None):
        if log_path is None:
            log_path = os.path.join(self.folder_path, "file_log.json")

        if not os.path.exists(log_path):
            return "No log file found. Nothing to undo.", None

        try:
            with open(log_path, 'r') as f:
                all_batches = json.load(f)

            if not all_batches:
                return "No move operations found to undo.", None

            last_batch = all_batches.pop()

            errors = []
            for entry in last_batch["entries"]:
                try:
                    if os.path.exists(entry['new_path']):
                        shutil.move(entry['new_path'], entry['original_path'])
                    else:
                        errors.append(f"File missing: {entry['new_path']}")
                except Exception as e:
                    errors.append(f"Failed to move {entry['new_path']}: {e}")

            with open(log_path, 'w') as f:
                json.dump(all_batches, f, indent=2)

            if errors:
                return "Undo completed with errors", errors
            else:
                return "Undo completed successfully.", None

        except Exception as e:
            return f"Failed to undo: {e}", None


    
    def cli_menu(self):
        log_path = os.path.join(self.folder_path, "file_log.json")
        while True:
            print("\nChoose an option:")
            print("1. Organize files")
            print("2. Undo last operation")
            print("3. Exit")
            choice = input("Enter your choice (1/2/3): ")
            if choice == "1":
                self.classify_files()
                self.create_folders_and_move_files()
            elif choice == "2":
                self.undo_last_operation(log_path)
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, try again.")

# GUI PART:
def on_enter(e):
    e.widget['bg'] = '#ffdef2' 

def on_leave(e):
    e.widget['bg'] = '#dca5c3' 

def choose_folder():
    global organizer
    folder = filedialog.askdirectory()
    if folder:
        folder_label.config(text=f"Selected folder:\n{folder}")
        status_label.config(text="Status: Organizing...")
        organize_btn.config(state="disabled")
        undo_btn.config(state="disabled")

        organizer = FileOrganizer(folder)
        organizer.classify_files()
        success = organizer.create_folders_and_move_files()

        if success:
            messagebox.showinfo("Success", "Files organized successfully!")
        else:
            messagebox.showerror("Error", "Failed to organize files. :( Check console for details.")

        status_label.config(text="Status: Idle")
        organize_btn.config(state="normal")
        undo_btn.config(state="normal")


def undo_last():
    global organizer
    if not organizer:
        messagebox.showwarning("Undo", "No folder selected yet!")
        return

    status_label.config(text="Status: Undoing...")
    organize_btn.config(state="disabled")
    undo_btn.config(state="disabled")

    try:
        organizer.undo_last_operation()
        messagebox.showinfo("Undo", "Undo completed successfully. :)")
    except Exception as e:
        messagebox.showerror("Error", f"Undo failed: {e}")

    status_label.config(text="Status: Idle")
    organize_btn.config(state="normal")
    undo_btn.config(state="normal")


window = Tk()
window.geometry("400x350")
window.title("Viki's File Organizer")
window.configure(bg="#f2e2ff")

frame = Frame(window, bg="#f2e2ff")
frame.pack(padx=30, pady=30)


title = Label(frame, text="Viki's file organizer", font=("Helvetica", 16, "bold"), bg="#f2e2ff", fg="#dca5c3")
title.pack(pady=(0, 20))

folder_label = Label(frame, text="No folder selected", font=("Helvetica", 10), bg="#ffdef2", fg="#9396d5")
folder_label.pack(pady=(0, 10))

status_label = Label(frame, text="Status: Idle", font=("Helvetica", 10, "italic"), bg="#ffdef2", fg="#9396d5")
status_label.pack(pady=(0, 20))


organize_btn = Button(frame, text="Pick a folder to organize :)", cursor="hand2", bg="#dca5c3", fg="#9e4a9e", relief="groove", font=("Helvetica", 11), command=choose_folder)
organize_btn.pack(pady=10)
organize_btn.bind("<Enter>", on_enter)
organize_btn.bind("<Leave>", on_leave)

undo_btn = Button(frame, text="Undo last operation", cursor="hand2", bg="#dca5c3", fg="#9e4a9e", relief="groove", font=("Helvetica", 11), command=undo_last)
undo_btn.pack(pady=10)
undo_btn.bind("<Enter>", on_enter)
undo_btn.bind("<Leave>", on_leave)

window.mainloop()


