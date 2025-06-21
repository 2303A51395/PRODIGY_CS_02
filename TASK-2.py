import tkinter as tk
from tkinter import filedialog, messagebox
import random
import os

window = tk.Tk()
window.geometry("1000x700")
window.title("Image Encryption & Decryption")

original_image = None
image_path = None
encrypted_data = None
key_data = None
panelA = None
panelB = None

def open_image():
    global image_path, original_image, panelA, panelB

    path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    if not path:
        return

    try:
        image_path = path
        original_image = tk.PhotoImage(file=image_path)

        if panelA is not None:
            panelA.configure(image=original_image)
            panelA.image = original_image
        else:
            panelA_new = tk.Label(window, image=original_image, bg="white", bd=5, relief="groove")
            panelA_new.image = original_image
            panelA_new.place(x=50, y=150)
            globals()['panelA'] = panelA_new  

        if panelB is not None:
            panelB.configure(image=original_image)
            panelB.image = original_image
        else:
            panelB_new = tk.Label(window, image=original_image, bg="white", bd=5, relief="groove")
            panelB_new.image = original_image
            panelB_new.place(x=550, y=150)
            globals()['panelB'] = panelB_new 

    except tk.TclError:
        messagebox.showerror("Error", "Unable to load image. Use a simple PNG image.")

def encrypt_image():
    global encrypted_data, key_data, panelB

    if not image_path:
        messagebox.showwarning("Warning", "No image selected.")
        return

    with open(image_path, "rb") as f:
        original_bytes = f.read()

    key_data = [random.randint(0, 255) for _ in original_bytes]
    encrypted_data = bytes([b ^ k for b, k in zip(original_bytes, key_data)])

    with open("temp_encrypted.png", "wb") as f:
        f.write(encrypted_data)

    try:
        encrypted_img = tk.PhotoImage(file="temp_encrypted.png")
    except:
        messagebox.showerror("Error", "Encrypted file is invalid. Try with a different PNG image.")
        return

    if panelB is not None:
        panelB.configure(image=encrypted_img)
        panelB.image = encrypted_img
    else:
        panelB_new = tk.Label(window, image=encrypted_img, bg="lightgrey", bd=5, relief="groove")
        panelB_new.image = encrypted_img
        panelB_new.place(x=550, y=150)
        globals()['panelB'] = panelB_new

    messagebox.showinfo("Success", "Image encrypted successfully!")

def decrypt_image():
    global encrypted_data, key_data, panelB

    if not encrypted_data or not key_data:
        messagebox.showwarning("Warning", "No encrypted data found.")
        return

    decrypted = bytes([b ^ k for b, k in zip(encrypted_data, key_data)])

    with open("temp_decrypted.png", "wb") as f:
        f.write(decrypted)

    try:
        decrypted_img = tk.PhotoImage(file="temp_decrypted.png")
    except:
        messagebox.showerror("Error", "Decrypted image is not valid.")
        return

    if panelB is not None:
        panelB.configure(image=decrypted_img)
        panelB.image = decrypted_img
    else:
        panelB_new = tk.Label(window, image=decrypted_img, bg="lightgrey", bd=5, relief="groove")
        panelB_new.image = decrypted_img
        panelB_new.place(x=550, y=150)
        globals()['panelB'] = panelB_new

    messagebox.showinfo("Success", "Image decrypted successfully!")

def save_encrypted():
    if not encrypted_data:
        messagebox.showwarning("Warning", "No encrypted image to save.")
        return

    path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if path:
        with open(path, "wb") as f:
            f.write(encrypted_data)
        messagebox.showinfo("Saved", "Encrypted image saved successfully.")

def exit_app():
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
        window.destroy()

tk.Label(window, text="Image Encryption & Decryption", font=("Helvetica", 28, "bold"), fg="blue", bg="white").pack(pady=20, fill='x')

tk.Button(window, text="Choose Image", command=open_image, font=("Arial", 15), bg="#FFA500", fg="black").place(x=50, y=80)
tk.Button(window, text="Encrypt", command=encrypt_image, font=("Arial", 15), bg="#228B22", fg="white").place(x=200, y=80)
tk.Button(window, text="Decrypt", command=decrypt_image, font=("Arial", 15), bg="#FFD700", fg="black").place(x=310, y=80)
tk.Button(window, text="Save Encrypted", command=save_encrypted, font=("Arial", 15), bg="#4682B4", fg="white").place(x=440, y=80)
tk.Button(window, text="Exit", command=exit_app, font=("Arial", 15), bg="#B22222", fg="white").place(x=620, y=80)

window.configure(bg="white")
window.protocol("WM_DELETE_WINDOW", exit_app)
window.mainloop()