from tkinter import *
from tkinter import filedialog, messagebox
import qrcode


class App:
    def __init__(self):
        self.qr = qrcode.QRCode(
            version= 15,
            box_size=10,
            border= 5
        )
        self.root = Tk()
        self.root.title("QR code generator")
        self.root.configure(bg="#222")
        self.root.resizable(False, False)

        self.label = Label(
            self.root,
            text="Enter the URL to convert to qrcode: ",
            font=("Serif", 15),
            anchor='w',
            bg="#222",
            fg="#FFF",
            padx=10,
            pady=10
        )
        self.entry = Entry(
            self.root, 
            width=24,
            font=("Serif", 18),
            bg="#222",
            fg="#FFF",
        )
        self.btn_create = Button(
            self.root,
            text="Create",
            width=14,
            font=("Serif", 15),
            bg="#666",
            fg="#FFF",
            padx=15,
            pady=15,
            relief="flat",
            command=self.create
        )
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.entry.grid(row=1, column=0, padx=10, pady=10)
        self.btn_create.grid(row=2, column=0, padx=10, pady=10)
        
        self.entry.bind("<Return>", self.create)
        self.root.mainloop()

    def create(self, event):
        url = self.entry.get().strip()
        if url == "":
            messagebox.showerror("Error", "\tInvalid URL\t")
            return
        
        file_path = filedialog.asksaveasfilename(initialfile="Untitled.png", defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if file_path:
            self.qr.add_data(url)
            self.qr.make(fit=True)
            image = self.qr.make_image(fill="black", back_color="white")
            image.save(file_path)
            messagebox.showinfo("Suceess", "QR code image saved successfully!")
            self.entry.delete(0, END)        


if __name__ == "__main__":
    App()
