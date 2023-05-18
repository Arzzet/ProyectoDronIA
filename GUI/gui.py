import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, PhotoImage
from ttkthemes import ThemedStyle

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("600x480")
        self.root.title("Login")

        style = ThemedStyle(self.root)
        style.set_theme("black") 

        self.canvas = tk.Canvas(self.root, height=480, width=600)
        self.canvas.pack()

        # self.background_image = PhotoImage(file="dron.png") 
        # self.canvas.create_image(0, 0, anchor='nw', image=self.background_image)

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        ttk.Label(self.login_frame, text="User:", foreground="lime").grid(row=0, column=0)
        ttk.Entry(self.login_frame, textvariable=self.username).grid(row=0, column=1)

        ttk.Label(self.login_frame, text="Password:", foreground="lime").grid(row=1, column=0)
        ttk.Entry(self.login_frame, textvariable=self.password, show="*").grid(row=1, column=1)

        ttk.Button(self.login_frame, text="Log in", command=self.login).grid(row=2, columnspan=2)

    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "Please fill all the fields")
        else:
            messagebox.showinfo("Login successful", f"Welcome {self.username.get()}")
            self.login_frame.place_forget()
            self.after_login()

    def after_login(self):
        self.home_frame = ttk.Frame(self.root)
        self.home_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Button(self.home_frame, text="FaceDetection").pack()
        ttk.Button(self.home_frame, text="SearchObject").pack()
        ttk.Button(self.home_frame, text="MachineVision").pack()

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
