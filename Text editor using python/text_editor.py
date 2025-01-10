import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox

# Define themes
themes = {
    "light": {"bg": "white", "fg": "black"},
    "dark": {"bg": "black", "fg": "white"}
}

current_theme = "light"  # Default theme

def apply_theme():
    """Apply the current theme to all text areas."""
    theme = themes[current_theme]
    for child in notebook.winfo_children():
        text_area = child.winfo_children()[0]
        text_area.config(bg=theme["bg"], fg=theme["fg"], insertbackground=theme["fg"])

def toggle_theme():
    """Switch between light and dark themes."""
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme()
    update_theme_label()

def update_theme_label():
    """Update the theme menu label based on the current theme."""
    theme_menu.entryconfig(0, label="Dark Theme" if current_theme == "light" else "Light Theme")

def new_tab():
    """Create a new tab with a text area."""
    tab_count = len(notebook.tabs()) + 1
    new_frame = ttk.Frame(notebook)
    text_area = tk.Text(new_frame, wrap="word", undo=True)
    text_area.pack(fill="both", expand=True)
    notebook.add(new_frame, text=f"Tab {tab_count}")
    notebook.select(new_frame)
    apply_theme()
    configure_text_tags(text_area)

def close_tab():
    """Close the currently selected tab."""
    if len(notebook.tabs()) > 1:  # Ensure at least one tab remains
        current_tab = notebook.select()
        notebook.forget(current_tab)
    else:
        messagebox.showwarning("Warning", "At least one tab must remain open.")

def rename_tab():
    """Rename the currently selected tab."""
    current_tab_index = notebook.index(notebook.select())
    current_tab_name = notebook.tab(current_tab_index, "text")
    new_name = simpledialog.askstring("Rename Tab", f"Enter a new name for '{current_tab_name}':")
    if new_name:
        notebook.tab(current_tab_index, text=new_name)

def open_file():
    """Open a file in the current tab."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            current_tab = notebook.select()
            text_area = notebook.nametowidget(current_tab).winfo_children()[0]
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file.read())

def save_file():
    """Save the contents of the current tab to a file."""
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        current_tab = notebook.select()
        text_area = notebook.nametowidget(current_tab).winfo_children()[0]
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))

def cut_text():
    """Cut selected text in the current tab."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.event_generate("<<Cut>>")

def copy_text():
    """Copy selected text in the current tab."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.event_generate("<<Copy>>")

def paste_text():
    """Paste text into the current tab."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.event_generate("<<Paste>>")

def apply_bold():
    """Apply bold formatting to the selected text."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.tag_add("bold", text_area.index(tk.SEL_FIRST), text_area.index(tk.SEL_LAST))

def apply_italic():
    """Apply italic formatting to the selected text."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.tag_add("italic", text_area.index(tk.SEL_FIRST), text_area.index(tk.SEL_LAST))

def apply_underline():
    """Apply underline formatting to the selected text."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.tag_add("underline", text_area.index(tk.SEL_FIRST), text_area.index(tk.SEL_LAST))

def configure_text_tags(text_area):
    """Configure tags for bold, italic, and underline styles."""
    text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))
    text_area.tag_configure("italic", font=("Helvetica", 12, "italic"))
    text_area.tag_configure("underline", font=("Helvetica", 12, "underline"))

def undo_action():
    """Undo the last action in the current tab."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.edit_undo()

def redo_action():
    """Redo the last undone action in the current tab."""
    current_tab = notebook.select()
    text_area = notebook.nametowidget(current_tab).winfo_children()[0]
    text_area.edit_redo()

# Create the main application window
root = tk.Tk()
root.title("Text Editor - Your Notepad")

# Create the notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Add the first tab
new_tab()

# Create the menu bar
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New Tab", command=new_tab)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Close Tab", command=close_tab)
file_menu.add_command(label="Rename Tab", command=rename_tab)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Bold", command=apply_bold)  # Bold option
edit_menu.add_command(label="Italic", command=apply_italic)  # Italic option
edit_menu.add_command(label="Underline", command=apply_underline)  # Underline option
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Undo/Redo menu
undo_redo_menu = tk.Menu(menu_bar, tearoff=0)
undo_redo_menu.add_command(label="Undo", command=undo_action)
undo_redo_menu.add_command(label="Redo", command=redo_action)
menu_bar.add_cascade(label="Undo/Redo", menu=undo_redo_menu)

# Theme menu
theme_menu = tk.Menu(menu_bar, tearoff=0)
theme_menu.add_command(label="Dark Theme", command=toggle_theme)
menu_bar.add_cascade(label="Themes", menu=theme_menu)

# Configure the menu bar
root.config(menu=menu_bar)

# Run the application
root.mainloop()
