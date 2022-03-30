from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from threading import Thread
from . import parse
from . import thumbnail
from . import filter


class GUI:
    def __init__(self, master):
        """Define user interface's objects."""
        # Define all variables
        self.image_list = []
        self.images = []
        self.store_path = []
        self.size = []
        self.filter_values = ["", "Blur", "Contour", "Detail", "Edge Enhance", "Edge Enhance More", "Emboss",
                              "Find Edges", "Smooth", "Smooth More", "Sharpen", "Invert Colors", "Black and White",
                              "Auto Contrast", "Mirror", "Solarize", "Remove RED Color", "Remove GREEN Color",
                              "Remove BLUE Color"]

        # Add frames labels
        self.store_LF = LabelFrame(master, text="Source file(s)", padx=10, pady=10)
        self.destination_LF = LabelFrame(master, text="Destination folder", padx=10, pady=10)
        self.output_LF = LabelFrame(master, text="Modifications", padx=10, pady=10)
        self.finish_LF = LabelFrame(master, padx=10, pady=10)

        # Add frames
        self.store_frame = Frame(self.store_LF)
        self.destination_frame = Frame(self.destination_LF)
        self.output_frame = Frame(self.output_LF)
        self.finish_frame = Frame(self.finish_LF)

        # Add texts
        self.source_text = Text(self.store_frame, width=74, height=1, state=DISABLED)
        self.destination_text = Text(self.destination_frame, width=74, height=1, state=DISABLED)
        self.width_text = Entry(self.output_frame, width=10)
        self.height_text = Entry(self.output_frame, width=10)

        # Add buttons
        self.start_button = Button(self.finish_frame, text="Save", width=105, command=self.thread_for_thumb,
                                   state=DISABLED)
        self.source_button = Button(self.store_frame, text="Browse files", command=self.open_files,
                                    height=1, width=17)
        self.destination_button = Button(self.destination_frame, text="Destination folder", command=self.save_location,
                                         height=1, width=17)
        self.resize_button = ttk.Combobox(self.output_frame, state="readonly", values=["No Resize",
                                                                                       "Best Fit (Thumbnail)",
                                                                                       "Exact Size"])
        self.filters_button = ttk.Combobox(self.output_frame, state="readonly", values=self.filter_values)

        # Add labels
        self.resize_label = Label(self.output_frame, text="Resize method:", fg="black")
        self.filters_label = Label(self.output_frame, text="Filter:", fg="black")
        self.width_label = Label(self.output_frame, text="Width:", fg="black")
        self.height_label = Label(self.output_frame, text="Height:", fg="black")

        # Get default color
        self.default_color = self.start_button.cget("bg")

        # Run packing for all GUI objects
        self.packing()

    def open_files(self):
        """Let user select file(s) from directory."""
        # Open directory window for file selection
        self.image_list = filedialog.askopenfilenames(filetypes=[("All files", "*.*")])
        # Parse all selected files
        self.images = parse.parse_photo(self.image_list)
        # Handle information text
        self.source_text_handler()
        # Check if selected images can be saved
        self.start_enabler()

    def save_location(self):
        """Let user select where to save file(s)."""
        # Open directory window for folder selection
        self.store_path = filedialog.askdirectory()
        # Handle information text
        self.destination_text_handler()
        # Check if selected images can be saved
        self.start_enabler()

    def start_enabler(self):
        """Control when to enable "Save" option."""
        # Get width and height from user
        self.wanted_size()

        # If user selects "No Resize" option
        if self.resize_button.current() == 0:
            # Enable "Save"option if all data is provided
            if len(self.store_path) > 0 and self.images is not None and len(self.images) > 0:
                self.start_button.config(bg="green", fg="white", state=NORMAL)

            # Otherwise, leave button disabled
            else:
                self.start_button.config(bg=self.default_color, state=DISABLED)

        # If user selects other resize method
        if self.resize_button.current() != 0:
            # Enable "Save"option if all data is provided
            if len(self.store_path) > 0 and self.images is not None and len(self.images) > 0 and self.size is not None:
                self.start_button.config(bg="green", fg="white", state=NORMAL)

            # Otherwise, leave button disabled
            else:
                self.start_button.config(bg=self.default_color, state=DISABLED)

    def thumb(self):
        """Apply filters if selected and save image(s)."""
        # Inform user that program is running
        self.start_button.config(bg=self.default_color, state=DISABLED)
        self.source_text.config(state=NORMAL)
        self.source_text.delete(0.0, END)
        self.source_text.config(bg="yellow", fg="black")
        self.source_text.insert(0.0, "Processing...")
        self.source_text.config(state=DISABLED)
        # Apply filters if selected
        if self.filters_button.current() != 0:
            self.images = filter.image_filter(self.images, self.filters_button.current())
        # Save image(s)
        thumbnail.thumbnails(self.images, self.image_list, self.store_path, self.resize_button.current(), self.size)
        # Clear program's window after saving image(s) and display completion message
        self.images.clear()
        self.source_text.config(state=NORMAL)
        self.source_text.delete(0.0, END)
        self.source_text.config(bg="green", fg="white")
        self.source_text.insert(0.0, "Finished")
        self.source_text.config(state=DISABLED)

    def source_text_handler(self):
        """Handle source textbox's messages."""
        # Display this message if user selects unsupported type file(s)
        if self.images is None:
            self.source_text.config(state=NORMAL)
            self.source_text.delete(0.0, END)
            self.source_text.config(bg="red", fg="white")
            self.source_text.insert(0.0, "Selected unsupported type file(s)!")
            self.source_text.config(state=DISABLED)

        # Display this message if no files were selected
        elif not self.images:
            self.source_text.config(state=NORMAL)
            self.source_text.delete(0.0, END)
            self.source_text.config(bg="white", fg="black")
            self.source_text.insert(0.0, "No files selected")
            self.source_text.config(state=DISABLED)

        # Display this message if user selects file(s)
        else:
            self.source_text.config(state=NORMAL)
            self.source_text.delete(0.0, END)
            self.source_text.config(bg="white", fg="black")
            self.source_text.insert(0.0, "Selected {} image(s)".format(len(self.image_list)))
            self.source_text.config(state=DISABLED)

    def destination_text_handler(self):
        """Handle destination folder's textbox messages."""
        # Delete text if where is no directory in the memory
        if len(self.store_path) == 0:
            self.destination_text.config(state=NORMAL)
            self.destination_text.delete(0.0, END)
            self.destination_text.config(height=1)
            self.destination_text.config(state=DISABLED)

        # Display destination folder's path
        if len(self.store_path) > 0:
            # Check what height text widget is needed
            length = round(len(self.store_path) / 74)
            if length * 74 < len(self.store_path):
                length += 1
            self.destination_text.config(state=NORMAL)
            self.destination_text.config(height=length)
            self.destination_text.delete(0.0, END)
            self.destination_text.insert(0.0, self.store_path)
            self.destination_text.config(state=DISABLED)

    def width_height(self):
        """Display option for width and height selection."""
        self.width_text.delete(0, END)
        self.height_text.delete(0, END)
        # Display width and height widgets if "Best Fit (Thumbnail)" or "Exact Size" resize method is selected
        if not self.resize_button.current() == 0:
            self.width_label.grid(row=0, column=3, padx=25, pady=10, sticky=E)
            self.height_label.grid(row=1, column=3, padx=25, pady=10, sticky=E)
            self.width_text.grid(row=0, column=4, pady=10)
            # Make every of entry of width's textbox visible for certain functions
            self.width_text.bind("<KeyRelease>", lambda event: self.is_width_number(), add="+")
            self.width_text.bind("<KeyRelease>", lambda event: self.start_enabler(), add="+")
            self.height_text.grid(row=1, column=4, pady=10)
            # Make every of entry of height's textbox visible for certain functions
            self.height_text.bind("<KeyRelease>", lambda event: self.is_height_number(), add="+")
            self.height_text.bind("<KeyRelease>", lambda event: self.start_enabler(), add="+")

        else:
            # Hide width and height widgets if "No Resize" method is selected
            self.width_label.grid_forget()
            self.height_label.grid_forget()
            self.width_text.grid_forget()
            self.height_text.grid_forget()

    def is_width_number(self):
        """Make sure user entered width value is a number."""
        entered_number = self.width_text.get()
        try:
            if len(entered_number) > 0:
                # Make sure there is no whitespaces
                if entered_number[-1] == " ":
                    raise ValueError
            # Make sure user entered only digits
            int(entered_number)

        except ValueError:
            # Otherwise, delete entry
            self.width_text.delete(0, END)

    def is_height_number(self):
        """Make sure user entered height value is a number."""
        entered_number = self.height_text.get()
        try:
            if len(entered_number) > 0:
                # Make sure there is no whitespaces
                if entered_number[-1] == " ":
                    raise ValueError
            # Make sure user entered only digits
            int(entered_number)

        except ValueError:
            # Otherwise, delete entry
            self.height_text.delete(0, END)

    def wanted_size(self):
        """Combine width and height into list if both is provided."""
        width = 0
        height = 0
        # Check if there is a width's value
        if len(self.width_text.get()) > 0:
            width = int(self.width_text.get())

        # Check if there is a height's value
        if len(self.height_text.get()) > 0:
            height = int(self.height_text.get())

        # Combine width and height into list if both have values
        if width > 0 and height > 0:
            self.size = [width, height]

        # Otherwise, return None
        else:
            self.size = None

    def thread_for_thumb(self):
        """Create thread for "thumb" function in oder to not freeze GUI."""
        # Create thread
        thumb_thread = Thread(target=self.thumb, args=())
        # Start thread
        thumb_thread.start()

    def packing(self):
        """Place user interface's objects into program"""
        # Pack all frame labels
        self.store_LF.pack(padx=10, pady=10, fill=X)
        self.destination_LF.pack(padx=10, pady=10, fill=X)
        self.output_LF.pack(padx=10, pady=10, fill=X)
        self.finish_LF.pack(padx=10, pady=10, fill=X)

        # Pack all frames
        self.store_frame.pack()
        self.destination_frame.pack()
        self.output_frame.pack(side=LEFT)
        self.finish_frame.pack()

        # Put all buttons in rows and columns
        self.source_button.grid(row=0, column=2, padx=10, pady=10)
        self.destination_button.grid(row=0, column=2, padx=10, pady=10)
        self.filters_button.grid(row=1, column=2, padx=25)
        self.start_button.grid(row=0, column=1)
        self.resize_button.grid(row=0, column=2, padx=25)
        self.resize_button.current(0)
        # Call selected functions when value of resize combobox is changed
        self.resize_button.bind("<<ComboboxSelected>>", lambda event: self.width_height(), add="+")
        self.resize_button.bind("<<ComboboxSelected>>", lambda event: self.start_enabler(), add="+")

        # Put all texts in rows and columns
        self.source_text.grid(row=0, column=1)
        self.destination_text.grid(row=0, column=1)

        # Put all labels in rows and columns
        self.resize_label.grid(row=0, column=1, pady=10, sticky=E)
        self.filters_label.grid(row=1, column=1, pady=10, sticky=E)


def base():
    """Run user interface."""
    root = Tk()
    # Title of the program
    root.title("Thumbnail")
    # Make program's window non-resizable
    root.resizable(False, False)
    GUI(root)
    root.mainloop()
