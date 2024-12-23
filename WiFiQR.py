import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import qrcode

class WiFiQRApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wi-Fi QR Code Generator")

        # Create a frame to hold all widgets for better alignment
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10)

        # Row 0: SSID
        tk.Label(main_frame, text="SSID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ssid_var = tk.StringVar()
        self.ssid_entry = tk.Entry(main_frame, textvariable=self.ssid_var, width=30)
        self.ssid_entry.grid(row=0, column=1, padx=5, pady=5)

        clear_ssid_btn = tk.Button(main_frame, text="Clear", command=self.clear_ssid)
        clear_ssid_btn.grid(row=0, column=2, padx=5, pady=5)

        # Row 1: Password (visible text)
        tk.Label(main_frame, text="Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.pwd_var = tk.StringVar()
        # Remove 'show="*"' to make the password visible
        self.pwd_entry = tk.Entry(main_frame, textvariable=self.pwd_var, width=30)
        self.pwd_entry.grid(row=1, column=1, padx=5, pady=5)

        clear_pwd_btn = tk.Button(main_frame, text="Clear", command=self.clear_pwd)
        clear_pwd_btn.grid(row=1, column=2, padx=5, pady=5)

        # Row 2: Generate QR Code button
        generate_btn = tk.Button(main_frame, text="Generate QR Code", command=self.generate_qr)
        generate_btn.grid(row=2, column=0, columnspan=3, pady=10)

        # Row 3: QR Code Display
        self.qr_label = tk.Label(main_frame, text="No QR Code Generated")
        self.qr_label.grid(row=3, column=0, columnspan=3, pady=10)
        
        # Row 4: SSID Label below the QR code for clarity
        self.ssid_display_label = tk.Label(main_frame, text="", fg="black", font=("Helvetica", 10))
        self.ssid_display_label.grid(row=4, column=0, columnspan=3, pady=5)

        # Row 5: Save as Image button
        self.save_btn = tk.Button(main_frame, text="Save as Image", command=self.save_qr, state='disabled')
        self.save_btn.grid(row=5, column=0, columnspan=3, pady=5)

        # Signature at the bottom (Row 6)
        signature_label = tk.Label(main_frame, text="Made in Antwerp by Runaque", fg="slate gray", font=("Helvetica", 10))
        signature_label.grid(row=6, column=0, columnspan=3, pady=10)

        self.qr_image = None

    def clear_ssid(self):
        self.ssid_var.set("")

    def clear_pwd(self):
        self.pwd_var.set("")

    def generate_qr(self):
        ssid = self.ssid_var.get().strip()
        password = self.pwd_var.get().strip()

        if not ssid:
            messagebox.showwarning("Missing Information", "Please provide the SSID.")
            return

        # If password is provided, assume WPA encryption. Otherwise, nopass.
        if password:
            qr_text = f"WIFI:T:WPA;S:{ssid};P:{password};;"
        else:
            qr_text = f"WIFI:T:nopass;S:{ssid};;"

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(qr_text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to PhotoImage for Tkinter
        self.qr_image_pil = img
        self.qr_image = ImageTk.PhotoImage(img)
        self.qr_label.config(image=self.qr_image, text="")
        self.save_btn.config(state='normal')

        # Update the SSID display label below the QR code
        self.ssid_display_label.config(text=f"SSID: {ssid}")

    def save_qr(self):
        if self.qr_image is None:
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.qr_image_pil.save(file_path)
            messagebox.showinfo("Saved", f"QR code saved to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WiFiQRApp(root)
    root.mainloop()
