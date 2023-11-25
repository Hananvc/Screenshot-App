import tkinter as tk
from tkinter import messagebox, Entry, Label
from PIL import Image, ImageTk, ImageGrab, ImageOps
from PIL.Image import LANCZOS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ScreenshotUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Uploader")

        # GUI Elements
        self.screenshot_button = tk.Button(root, text="Take Screenshot", command=self.take_screenshot)
        self.screenshot_button.pack(pady=10)

        # Label for Remarks
        self.remarks_label = Label(root, text="Remarks:")
        self.remarks_label.pack(pady=5)

        # Entry field for remarks
        self.remarks_entry = Entry(root, width=40, state=tk.DISABLED)
        self.remarks_entry.pack(pady=5)

        # Label for Phone
        self.phone_label = Label(root, text="Phone:")
        self.phone_label.pack(pady=5)

        # Entry field for phone number
        self.phone_entry = Entry(root, width=40, state=tk.DISABLED)
        self.phone_entry.pack(pady=5)

        # Button to upload to API
        self.upload_button = tk.Button(root, text="Upload to API", command=self.upload_to_api, state=tk.DISABLED)
        self.upload_button.pack(pady=10)

        # Image label for screenshot preview
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Screenshot path variable
        self.screenshot_path = None

    def take_screenshot(self):
        # Hide the main window temporarily
        self.root.iconify()

        # Schedule the capture after a 1-second delay
        self.root.after(600, self.capture_screenshot)

    def capture_screenshot(self):
        # Capture screenshot using ImageGrab
        screenshot = ImageGrab.grab()

        # Save the screenshot to a temporary file (replace with actual logic)
        screenshot_path = "temp_screenshot.png"
        screenshot.save(screenshot_path)

        # Show the main window again
        self.root.deiconify()

        # Enable the entry fields and "Upload to API" button
        self.remarks_entry.config(state=tk.NORMAL)
        self.phone_entry.config(state=tk.NORMAL)
        self.upload_button.config(state=tk.NORMAL)

        # Store the screenshot path for later use in the API upload
        self.screenshot_path = screenshot_path

        # Display the screenshot preview
        self.display_screenshot_preview(screenshot)

    def display_screenshot_preview(self, image):
        # Display the entire screenshot in the GUI using LANCZOS resampling
        thumbnail_size = (450, 250)
        thumbnail = ImageOps.fit(image, thumbnail_size, LANCZOS)

        img = ImageTk.PhotoImage(thumbnail)
        self.image_label.config(image=img)
        self.image_label.image = img

    def upload_to_api(self):
        # Check if a screenshot has been taken
        if not self.screenshot_path:
            messagebox.showerror("Error", "Please take a screenshot first.")
            return

        # Get values from entry fields
        remarks = self.remarks_entry.get().strip()
        phone = self.phone_entry.get().strip()

        # Check if remarks is empty
        if not remarks:
            messagebox.showerror("Error", "Remarks should not be empty.")
            return

        # Check if phone is empty
        if not phone:
            messagebox.showerror("Error", "Phone number should not be empty.")
            return

        api_url = os.getenv("API_URL")

        # Prepare data for the API request
        with open(self.screenshot_path, 'rb') as image_file:
            files = {'image': ('screenshot.png', image_file, 'image/png')}
            data = {'remarks': remarks, 'phone': phone}

            # Make a POST request to the API
            try:
                response = requests.post(api_url, files=files, data=data)
                response_data = response.json()

                # Display the API response in a new dialog
                self.show_response_dialog(response_data)

            except requests.RequestException as e:
                # Handle API request errors
                messagebox.showerror("Error", f"Failed to upload: {e}")

    def show_response_dialog(self, response_data):
        # Create a new Toplevel window for showing API response
        response_window = tk.Toplevel(self.root)
        response_window.title("API Response")

        # Create labels to display API response details
        status_label = tk.Label(response_window, text=f"Status: {response_data.get('status')}")
        status_label.pack()

        message_label = tk.Label(response_window, text=f"Message: {response_data.get('message')}")
        message_label.pack()

        data_label = tk.Label(response_window, text=f"Data: {response_data.get('data')}")
        data_label.pack()


        # You can add more labels for additional details if needed

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotUploaderApp(root)
    root.mainloop()
