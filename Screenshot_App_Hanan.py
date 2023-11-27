import tkinter as tk
from tkinter import messagebox, Entry, Label
from PIL import Image, ImageTk, ImageGrab, ImageOps
from PIL.Image import LANCZOS
import requests
import os
import psutil

class ScreenshotUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot Uploader")

        # GUI Elements
        self.screenshot_button = tk.Button(root, text="Take Screenshot", command=self.take_and_upload_screenshot)
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

        # Image label for screenshot preview
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Variable to track button state
        self.screenshot_button_disabled = False

    def take_and_upload_screenshot(self):
        if not self.screenshot_button_disabled:
            self.root.iconify()
            self.root.after(600)
            # Capture screenshot using ImageGrab
            screenshot = ImageGrab.grab()

            # Save screenshot to a temporary file
            screenshot_path = "temp_screenshot.png"
            screenshot.save(screenshot_path)
            self.root.deiconify()

            # Enable the entry fields
            self.remarks_entry.config(state=tk.NORMAL)
            self.phone_entry.config(state=tk.NORMAL)

            # Display the screenshot preview
            self.display_screenshot_preview(screenshot)

            # Set the remarks entry to the active app name
            self.remarks_entry.delete(0, tk.END)
            self.remarks_entry.insert(0, self.get_active_app_name())

            static_phone_number = "8893443363"
            self.phone_entry.delete(0, tk.END)  # Clear existing text
            self.phone_entry.insert(0, static_phone_number)

            # Upload the screenshot to the API and show the response
            self.upload_screenshot_to_api(screenshot_path)

            # Disable the "Take Screenshot" button
            self.screenshot_button.config(state=tk.DISABLED)
            self.screenshot_button_disabled = True

    def get_active_app_name(self):
        foreground_pid = psutil.Process(os.getpid()).ppid()
        active_app_name = psutil.Process(foreground_pid).name()
        return active_app_name

    def display_screenshot_preview(self, image):
        # Display the entire screenshot in the GUI using LANCZOS resampling
        thumbnail_size = (450, 250)
        thumbnail = ImageOps.fit(image, thumbnail_size, LANCZOS)

        img = ImageTk.PhotoImage(thumbnail)
        self.image_label.config(image=img)
        self.image_label.image = img

    def upload_screenshot_to_api(self, screenshot_path):
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

        api_url = "https://trogon.info/interview/python/index.php"

        # Prepare data for the API request
        with open(screenshot_path, 'rb') as image_file:
            files = {'image': ('screenshot.png', image_file, 'image/png')}
            data = {'remarks': remarks, 'phone': phone}

            print("Sending files:", files)  # Add this line for debugging
            print("Sending data:", data)  # Add this line for debugging

            # Make a POST request to the API
            try:
                response = requests.post(api_url, files=files, data=data)
                response_data = response.json()

                print("API Response:", response_data)  # Add this line for debugging

                # Display the API response in a new dialog
                self.show_response_in_app(response_data)

            except requests.RequestException as e:
                # Handle API request errors
                messagebox.showerror("Error", f"Failed to upload: {e}")

    def show_response_in_app(self, response_data):
        # Create labels to display API response details
        status_label = tk.Label(self.root, text=f"Status: {response_data.get('status')}")
        status_label.pack()

        message_label = tk.Label(self.root, text=f"Message: {response_data.get('message')}")
        message_label.pack()

        data_label = tk.Label(self.root, text=f"Data: {response_data.get('data')}")
        data_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotUploaderApp(root)
    root.mainloop()
