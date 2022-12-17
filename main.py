from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Zillow_Class import RentInformation
from Google_Form_Class import GoogleBot
from Sheet_API_Class import SheetApi

HD_LABEL = ("Helvetica", 20, "bold")
FR_FONT = ("Helvetica", 13, "bold")
LB_FONT = ("Helvetica", 12, "bold")
V_FONT = ("Helvetica", 13, "normal")
COLUMNS = ("No", "Location", "Price", "Link")
COLUMNS_1 = ("No", "Time", "Location", "Price")


class EntryJobAutomation:
    def __init__(self, window):
        self.window = window
        self.window.title("Find Cheap House Bot")
        self.window.geometry("1360x800")
        self.window.state("zoomed")
        self.window.configure(bg="pale goldenrod")
        # extra variables:
        self.result = []
        self.answer = []
        self.chosen_location = StringVar()
        self.chosen_price = StringVar()

        # interface:
        self.header = Label(self.window, text="Find House For The Cheapest Price", font=HD_LABEL, justify="center",
                            bd=1, highlightthickness=1, relief=RIDGE, bg="pale goldenrod", fg="navy")
        self.header.place(x=10, y=10, width=1340, height=50)

        home_image = Image.open("IMG/home.png")
        home_photo = ImageTk.PhotoImage(home_image)
        self.home = Label(self.window, image=home_photo, bg="pale goldenrod")
        self.home.image = home_photo
        self.home.place(x=90, y=60, width=1180, height=364)

        # ======================= FIND HOUSE SECTION ================================ #
        self.find_house = LabelFrame(self.window, text="Find House Section", labelanchor="n", bd=4, relief=RIDGE,
                                     font=FR_FONT, bg="pale goldenrod")
        self.find_house.place(x=10, y=430, width=660, height=260)

        self.location = Label(self.find_house, text="Location", font=LB_FONT, justify="center", bd=1,
                              highlightthickness=1, relief=RIDGE, bg="khaki", fg="maroon")
        self.location.place(x=5, y=5, width=150, height=30)

        self.location_entry = Entry(self.find_house, font=LB_FONT, justify="center", bd=1, highlightthickness=1,
                                    relief=RIDGE, textvariable=self.chosen_location)
        self.location_entry.place(x=160, y=5, width=170, height=31)

        self.type = Label(self.find_house, text="Arrangement Type", font=LB_FONT, justify="center", bd=1,
                          highlightthickness=1, relief=RIDGE, bg="khaki", fg="maroon")
        self.type.place(x=5, y=40, width=150, height=30)

        self.type_entry = ttk.Combobox(self.find_house, font=LB_FONT, justify="center")
        self.type_entry["values"] = ("For Sale", "For Rent")
        self.type_entry.current(0)
        self.type_entry.place(x=160, y=40, width=169, height=30)

        self.price = Label(self.find_house, text="Your Price", font=LB_FONT, justify="center", bd=1,
                           highlightthickness=1, relief=RIDGE, bg="khaki", fg="maroon")
        self.price.place(x=342, y=5, width=150, height=30)

        self.price_entry = Entry(self.find_house, font=LB_FONT, justify="center", bd=1, highlightthickness=1,
                                 relief=RIDGE, textvariable=self.chosen_price)
        self.price_entry.place(x=497, y=5, width=150, height=31)

        self.bed_room = Label(self.find_house, text="Bedrooms", font=LB_FONT, justify="center", bd=1,
                              highlightthickness=1, relief=RIDGE, bg="khaki", fg="maroon")
        self.bed_room.place(x=342, y=40, width=150, height=30)

        self.bed_entry = ttk.Combobox(self.find_house, font=LB_FONT, justify="center")
        self.bed_entry["values"] = ("1", "2", "3", "4", "5")
        self.bed_entry.current(0)
        self.bed_entry.place(x=497, y=40, width=150, height=30)

        refresh_image = Image.open("IMG/refresh.png")
        refresh_photo = ImageTk.PhotoImage(refresh_image)
        self.refresh_button = Button(self.find_house, image=refresh_photo, justify="center", bd=0, bg="pale goldenrod",
                                     highlightbackground="pale goldenrod", highlightcolor="pale goldenrod",
                                     command=self.refresh_method)
        self.refresh_button.image = refresh_photo
        self.refresh_button.place(x=10, y=77, width=119, height=35)

        find_image = Image.open("IMG/find.png")
        find_photo = ImageTk.PhotoImage(find_image)
        self.find_button = Button(self.find_house, image=find_photo, justify="center", bd=0, bg="pale goldenrod",
                                  highlightbackground="pale goldenrod", highlightcolor="pale goldenrod",
                                  command=self.find_method)
        self.find_button.image = find_photo
        self.find_button.place(x=140, y=77, width=377, height=35)

        close_image = Image.open("IMG/close.png")
        close_photo = ImageTk.PhotoImage(close_image)
        self.close_button = Button(self.find_house, image=close_photo, justify="center", bd=0, bg="pale goldenrod",
                                   highlightbackground="pale goldenrod", highlightcolor="pale goldenrod",
                                   command=self.close_method)
        self.close_button.image = close_photo
        self.close_button.place(x=530, y=77, width=107, height=35)

        self.table_frame = Frame(self.find_house, bd=1, highlightthickness=1, relief=RIDGE)
        self.table_frame.place(x=5, y=120, width=642, height=110)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="light grey", foreground="black", rowheight=25,
                        fieldbackground="light grey")
        style.map("Treeview", background=[("selected", "medium sea green")])
        style.configure("Treeview.Heading", background="light steel blue", font=("Arial", 10, "bold"))
        style.configure("Treeview", font=("Arial", 11, "normal"))

        self.house_table = ttk.Treeview(self.table_frame, columns=COLUMNS, show="headings")
        # ------------------ heading ------------------- #
        self.house_table.heading("No", text="No")
        self.house_table.heading("Location", text="Location")
        self.house_table.heading("Price", text="Price")
        self.house_table.heading("Link", text="Link")
        # ---------------- columns ------------------------ #
        self.house_table.column("No", width=10, minwidth=5, anchor=W)
        self.house_table.column("Location", width=200, minwidth=25, anchor=W)
        self.house_table.column("Price", width=50, minwidth=25, anchor=CENTER)
        self.house_table.column("Link", width=300, minwidth=25, anchor=W)
        # ---------------- pack ------------------------ #
        self.house_table.pack(fill="both", expand=True)

        # ======================= GOOGLE SHEET SECTION ================================ #
        self.google = LabelFrame(self.window, text="Google Sheet Section", labelanchor="n", bd=4, relief=RIDGE,
                                 font=FR_FONT, bg="pale goldenrod")
        self.google.place(x=680, y=430, width=660, height=260)

        fill_image = Image.open("IMG/fill.png")
        fill_photo = ImageTk.PhotoImage(fill_image)
        self.fill_button = Button(self.google, image=fill_photo, justify="center", bd=0, bg="pale goldenrod",
                                  highlightbackground="pale goldenrod", highlightcolor="pale goldenrod",
                                  command=self.fill_method)
        self.fill_button.image = fill_photo
        self.fill_button.place(x=140, y=3, width=373, height=38)

        get_image = Image.open("IMG/get.png")
        get_photo = ImageTk.PhotoImage(get_image)
        self.get_button = Button(self.google, image=get_photo, justify="center", bd=0, bg="pale goldenrod",
                                 highlightbackground="pale goldenrod", highlightcolor="pale goldenrod",
                                 command=self.get_method)
        self.get_button.image = get_photo
        self.get_button.place(x=96, y=42, width=448, height=39)

        self.sheet_frame = Frame(self.google, bd=1, highlightthickness=1, relief=RIDGE, bg="pale goldenrod")
        self.sheet_frame.place(x=5, y=90, width=642, height=140)

        self.sheet_table = ttk.Treeview(self.sheet_frame, columns=COLUMNS_1, show="headings")
        # ------------------ heading ------------------- #
        self.sheet_table.heading("No", text="No")
        self.sheet_table.heading("Time", text="Time")
        self.sheet_table.heading("Location", text="Location")
        self.sheet_table.heading("Price", text="Price")
        # ---------------- columns ------------------------ #
        self.sheet_table.column("No", width=30, minwidth=5, anchor=W)
        self.sheet_table.column("Time", width=100, minwidth=80, anchor=W)
        self.sheet_table.column("Location", width=400, minwidth=25, anchor=W)
        self.sheet_table.column("Price", width=100, minwidth=25, anchor=CENTER)
        # ---------------- pack ------------------------ #
        self.sheet_table.pack(fill="both", expand=True)

    # ============================ FUNCTIONALITY ================================= #
    def close_method(self):
        confirm = messagebox.askyesno(title="Find Cheapest House", message="Do You Want To Close The Program?")
        if confirm > 0:
            self.window.destroy()
            return
        else:
            pass

    def clean_table(self):
        self.house_table.delete(*self.house_table.get_children())

    def find_method(self):
        self.clean_table()
        # load new data:
        rent_tool = RentInformation()
        data = rent_tool.get_rent_info()
        address = data["address"]
        price = data["prices"]
        links = data["links"]
        for i in range(len(address)):
            self.result.append((f"{i+1})", f"{address[i]}", f"{price[i]}", f"{links[i]}"))
        # fill table with data
        for item in self.result:
            self.house_table.insert("", END, values=item)

    def refresh_method(self):
        self.clean_table()
        self.result = []
        self.answer = []
        self.chosen_location.set("")
        self.chosen_price.set("")

    def fill_method(self):
        form_data = [list(item) for item in self.result]
        bot_tool = GoogleBot()
        bot_tool.start_filling()
        for data in form_data:
            bot_tool.fill_form(list_value=data)
            bot_tool.send_form()
            bot_tool.fill_again()

    def get_method(self):
        # --------------- clean table ------------------ #
        self.sheet_table.delete(*self.sheet_table.get_children())
        # --------------- get data ------------------ #
        api_tool = SheetApi()
        data = api_tool.get_data()
        timestamp = data["times"]
        locations = data["locations"]
        prices = data["prices"]
        for i in range(len(locations)):
            self.answer.append((f"{i+1})", f"0{timestamp[i]}", f"{locations[i]}", f"$ {prices[i]}"))
        # --------------- fill table with data ------------------ #
        for item in self.answer:
            self.sheet_table.insert("", END, values=item)


def launch_app():
    app = Tk()
    EntryJobAutomation(app)
    app.mainloop()


if __name__ == "__main__":
    launch_app()
