import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
from PIL import ImageTk, Image

# Database initialization
conn = sqlite3.connect('tour.db')
c = conn.cursor()

# Create customers table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                tour_period TEXT,
                places_to_visit TEXT
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS tour_booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hotel_booking TEXT,
                transport TEXT,
                tour_period TEXT,
                places_to_visit TEXT
            )''')


conn.commit()


main_window = None

def login_clicked():
    username = username_entry.get()
    password = password_entry.get()
    
    # Replace with your authentication logic
    if username == "polo" and password == "polo":
        messagebox.showinfo("Login Successful", "Welcome, Admin")
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_main_window():
    global main_window
    root.withdraw()  # Hide login window

    # Create main window
    main_window = tk.Toplevel()
    main_window.title("Exploration of New Cities")
    main_window.geometry("800x600")

    # Load background image for main window
    bg_image_main = Image.open("11.jpeg")
    bg_image_main = bg_image_main.resize((1700, 1000), Image.LANCZOS)
    bg_photo_main = ImageTk.PhotoImage(bg_image_main)

    # Create a canvas for main window
    canvas_main = tk.Canvas(main_window, width=800, height=600)
    canvas_main.pack(fill="both", expand=True)
    canvas_main.create_image(0, 0, image=bg_photo_main, anchor="nw")

    # Create a frame for tour booking options
    tour_booking_frame = tk.Frame(canvas_main, bg="white", bd=5)
    tour_booking_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Tour Booking heading label
    tour_booking_label = tk.Label(tour_booking_frame, text="Tour Booking", bg="grey", font=("Arial", 16))
    tour_booking_label.grid(row=0, columnspan=2, padx=10, pady=10)

    # Add Customer button
    add_customer_button = ttk.Button(tour_booking_frame, text="Add Customer", command=add_customer_clicked)
    add_customer_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    # View Customer button
    view_customer_button = ttk.Button(tour_booking_frame, text="View Customer", command=view_customer_clicked)
    view_customer_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Add Tour Booking button
    add_tour_booking_button = ttk.Button(tour_booking_frame, text="Add Tour Booking", command=add_tour_booking_clicked)
    add_tour_booking_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")



    # View Tour Booking button
    view_tour_booking_button = ttk.Button(tour_booking_frame, text="View Tour Booking", command=view_tour_booking_clicked)
    view_tour_booking_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

    # Ensure canvas size is updated when the window size changes
    def resize(event):
        canvas_main.config(width=main_window.winfo_width(), height=main_window.winfo_height())

    main_window.bind("<Configure>", resize)

    main_window.mainloop()


def add_tour_booking_clicked():
    global main_window

    # Function to save tour booking details to database
    def save_booking():
        hotel_booking = hotel_entry.get()
        transport = transport_entry.get()
        tour_period = time_entry.get()
        places = places_entry.get()

        # Basic validation (you can add more as per your requirements)
        if hotel_booking == "" or transport == "":
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Insert into database
        c.execute('''INSERT INTO tour_booking (hotel_booking, transport, tour_period, places_to_visit) 
                     VALUES (?, ?, ?, ?)''', (hotel_booking, transport, tour_period, places))
        conn.commit()
        messagebox.showinfo("Success", "Tour booking added successfully.")

        # Clear input fields after adding
        hotel_entry.delete(0, tk.END)
        transport_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        places_entry.delete(0, tk.END)

    main_window.withdraw()

    # Create add tour booking window
    add_booking_window = tk.Toplevel()
    add_booking_window.title("Add Tour Booking")
    add_booking_window.geometry("600x400")

    # Load background image for add booking window
    bg_image_add_booking = Image.open("10.jpeg")
    bg_image_add_booking = bg_image_add_booking.resize((1700, 1000), Image.LANCZOS)
    bg_photo_add_booking = ImageTk.PhotoImage(bg_image_add_booking)

    # Create a canvas for add booking window
    canvas_add_booking = tk.Canvas(add_booking_window, width=600, height=400)
    canvas_add_booking.pack(fill="both", expand=True)
    canvas_add_booking.create_image(0, 0, image=bg_photo_add_booking, anchor="nw")

    # Create a frame for tour booking details
    booking_frame = tk.Frame(canvas_add_booking, bg="white", bd=5)
    booking_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Tour Booking heading label
    booking_label = tk.Label(booking_frame, text="Tour Booking Details", bg="grey", font=("Arial", 16))
    booking_label.grid(row=0, columnspan=2, padx=10, pady=10)

    # Hotel Booking label and entry
    hotel_label = tk.Label(booking_frame, text="Hotel Booking")
    hotel_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    hotel_entry = ttk.Entry(booking_frame)
    hotel_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Transport label and entry
    transport_label = tk.Label(booking_frame, text="Transport")
    transport_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    transport_entry = ttk.Entry(booking_frame)
    transport_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Tour Time Period label and entry
    time_label = tk.Label(booking_frame, text="Tour Time Period")
    time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    time_entry = ttk.Entry(booking_frame)
    time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Places to Visit label and entry
    places_label = tk.Label(booking_frame, text="Places to Visit")
    places_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    places_entry = ttk.Entry(booking_frame)
    places_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Save button
    save_button = ttk.Button(booking_frame, text="Save", command=save_booking)
    save_button.grid(row=5, columnspan=2, padx=10, pady=10, sticky="ew")
    def backmenu():
        add_booking_window.destroy()
        open_main_window()
    close_button = ttk.Button(booking_frame, text="Back", command=backmenu)
    close_button.grid(row=6, columnspan=2, padx=10, pady=10, sticky="ew")



    def resize_add_booking(event):
        canvas_add_booking.config(width=add_booking_window.winfo_width(), height=add_booking_window.winfo_height())

    add_booking_window.bind("<Configure>", resize_add_booking)
    add_booking_window.mainloop()


 

def add_customer_clicked():
    global main_window

    # Function to save customer details to database
    def save_customer():
        name = Name_entry.get()
        phone = Phone_entry.get()
        tour_period = time_entry.get()
        places = places_entry.get()

        # Basic validation (you can add more as per your requirements)
        if name == "" or phone == "":
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Insert into database
        c.execute('''INSERT INTO customers (name, phone, tour_period, places_to_visit) 
                     VALUES (?, ?, ?, ?)''', (name, phone, tour_period, places))
        conn.commit()
        messagebox.showinfo("Success", "Customer added successfully.")

        # Clear input fields after adding
        Name_entry.delete(0, tk.END)
        Phone_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        places_entry.delete(0, tk.END)

    main_window.withdraw()

    # Create add customer window
    add_customer_window = tk.Toplevel()
    add_customer_window.title("Add Customer")
    add_customer_window.geometry("600x400")

    # Load background image for add customer window
    bg_image_add_customer = Image.open("10.jpeg")
    bg_image_add_customer = bg_image_add_customer.resize((1700, 1000), Image.LANCZOS)
    bg_photo_add_customer = ImageTk.PhotoImage(bg_image_add_customer)

    # Create a canvas for add customer window
    canvas_add_customer = tk.Canvas(add_customer_window, width=600, height=400)
    canvas_add_customer.pack(fill="both", expand=True)
    canvas_add_customer.create_image(0, 0, image=bg_photo_add_customer, anchor="nw")

    # Create a frame for customer details
    customer_frame = tk.Frame(canvas_add_customer, bg="white", bd=5)
    customer_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Customer details heading label
    customer_label = tk.Label(customer_frame, text="Customer Details", bg="grey", font=("Arial", 16))
    customer_label.grid(row=0, columnspan=2, padx=10, pady=10)

    # Customer Name label and entry
    Name_label = tk.Label(customer_frame, text="Customer Name")
    Name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    Name_entry = ttk.Entry(customer_frame)
    Name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    # Customer Phone label and entry
    Phone_label = tk.Label(customer_frame, text="Customer Phone")
    Phone_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    Phone_entry = ttk.Entry(customer_frame)
    Phone_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    # Tour Time Period label and entry
    time_label = tk.Label(customer_frame, text="Tour Time Period")
    time_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    time_entry = ttk.Entry(customer_frame)
    time_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Places to Visit label and entry
    places_label = tk.Label(customer_frame, text="Places to Visit")
    places_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    places_entry = ttk.Entry(customer_frame)
    places_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    # Save button
    save_button = ttk.Button(customer_frame, text="Save", command=save_customer)
    save_button.grid(row=5, columnspan=2, padx=10, pady=10, sticky="ew")

    def backmenu():
        add_customer_window.destroy()
        open_main_window()
    close_button = ttk.Button(customer_frame, text="Back", command=backmenu)
    close_button.grid(row=6, columnspan=2, padx=10, pady=10, sticky="ew")


    def resize_add_customer(event):
        canvas_add_customer.config(width=add_customer_window.winfo_width(), height=add_customer_window.winfo_height())

    add_customer_window.bind("<Configure>", resize_add_customer)
    add_customer_window.mainloop()




def fetch_customers():
    c.execute("SELECT * FROM customers")
    rows = c.fetchall()
    return rows

def view_customer_clicked():
    global main_window

    def populate_treeview():
        for row in fetch_customers():
            tree.insert('', 'end', values=row)

    main_window.withdraw()

    view_customer_window = tk.Toplevel()
    view_customer_window.title("View Customer Details")
    view_customer_window.geometry("800x600")

    bg_image = Image.open("10.jpeg")
    bg_image = bg_image.resize((1700, 1000), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(view_customer_window, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    customer_frame = tk.Frame(canvas, bg="white", bd=5)
    customer_frame.place(relx=0.5, rely=0.5, anchor="center")

    customer_label = tk.Label(customer_frame, text="Customer Details", bg="grey", font=("Arial", 16))
    customer_label.grid(row=0, columnspan=2, padx=10, pady=10)

    tree = ttk.Treeview(customer_frame, columns=(1,2,3,4,5), show="headings", height="10")
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    tree.heading(1, text="ID")
    tree.heading(2, text="Name")
    tree.heading(3, text="Phone")
    tree.heading(4, text="tour_period")
    tree.heading(5, text="places_to_visit")

    populate_treeview()

    close_button = ttk.Button(customer_frame, text="Close", command=view_customer_window.destroy)
    close_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def backmenu():
        view_customer_window.destroy()
        open_main_window()
    close_button = ttk.Button(customer_frame, text="Back", command=backmenu)
    close_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def resize(event):
        canvas.config(width=view_customer_window.winfo_width(), height=view_customer_window.winfo_height())

    view_customer_window.bind("<Configure>", resize)
    view_customer_window.mainloop()


def fetch_tour_booking():
    c.execute("SELECT * FROM tour_booking")
    rows = c.fetchall()
    return rows


def view_tour_booking_clicked():
    global main_window

    def populate_treeview():
        for row in fetch_tour_booking():
            tree.insert('', 'end', values=row)

    main_window.withdraw()

    view_customer_window = tk.Toplevel()
    view_customer_window.title("View Tour Booking Details")
    view_customer_window.geometry("800x600")

    bg_image = Image.open("10.jpeg")
    bg_image = bg_image.resize((1700, 1000), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(view_customer_window, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    customer_frame = tk.Frame(canvas, bg="white", bd=5)
    customer_frame.place(relx=0.5, rely=0.5, anchor="center")

    customer_label = tk.Label(customer_frame, text="Tour Booking  Details", bg="grey", font=("Arial", 16))
    customer_label.grid(row=0, columnspan=2, padx=10, pady=10)

    tree = ttk.Treeview(customer_frame, columns=(1,2,3,4,5), show="headings", height="10")
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    tree.heading(1, text="ID")
    tree.heading(2, text="hotel_booking")
    tree.heading(3, text="transport")
    tree.heading(4, text="tour_period")
    tree.heading(5, text="places_to_visit")

    populate_treeview()

    close_button = ttk.Button(customer_frame, text="Close", command=view_customer_window.destroy)
    close_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def backmenu():
        view_customer_window.destroy()
        open_main_window()
    close_button = ttk.Button(customer_frame, text="Back", command=backmenu)
    close_button.grid(row=2, columnspan=2, padx=10, pady=10, sticky="ew")

    def resize(event):
        canvas.config(width=view_customer_window.winfo_width(), height=view_customer_window.winfo_height())

    view_customer_window.bind("<Configure>", resize)
    view_customer_window.mainloop()



# Create main window
root = tk.Tk()
root.title("Login")
root.geometry("600x400")

# Load background image for login window
bg_image = Image.open("10.jpeg")
bg_image = bg_image.resize((1700, 1000), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas for login window
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create a frame for login
login_frame = tk.Frame(canvas, bg="white", bd=5)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Username label and entry
username_label = tk.Label(login_frame, text="Username", bg="grey")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ttk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=10, pady=10)

# Password label and entry
password_label = tk.Label(login_frame, text="Password", bg="grey")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Login button
login_button = ttk.Button(login_frame, text="Login", command=login_clicked)
login_button.grid(row=2, columnspan=2, padx=20, pady=10, sticky="ew")

# Ensure canvas size is updated when the window size changes
def resize(event):
    canvas.config(width=root.winfo_width(), height=root.winfo_height())

root.bind("<Configure>", resize)

root.mainloop()
