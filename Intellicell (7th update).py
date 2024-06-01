import tkinter as tk
import tkinter.messagebox
import ttkbootstrap as tb
import customtkinter
from PIL import ImageTk, Image
import serial
import time
import cv2

# the following functions (line 112 - 172) involves the interfacing code
# for the petri dish

# list of x and y coordinates, initiates camera at top left corner
positions = [[10, 155, 41]]
file = "Gcode_file.gcode"


def scale_to_size_pd(x, y):  # scales tkinter coordinate system to ender coordinate system
    # 22.5 accounts for the distance between the center of objective turret to
    # the center of the objective hole
    ender_x = 130 - 22.5
    ender_y = 100
    x_scaled = (x / 10) + ender_x  # might need to change scaling
    y_scaled = ender_y - (y / 10)
    print("Scaled coordinates - X:", x_scaled, "Y:", y_scaled)
    # calls function generate list to generate the positions list
    generate_list(x_scaled, y_scaled)
    return x_scaled, y_scaled


def scale_to_size_H96(x, y):  # scales tkinter coordinate system to ender coordinate system
    # 22.5 accounts for the distance between the center of objective turret to
    # the center of the objective hole
    ender_x = 21 - 22.5
    ender_y = 210
    offset = 103
    x_scaled = (x / 10) + ender_x + offset
    y_scaled = ender_y - (y / 10)
    print("Scaled coordinates - X:", x_scaled, "Y:", y_scaled)
    # calls function generate list to generate the postions list
    generate_list(x_scaled, y_scaled)
    return x_scaled, y_scaled


def scale_to_size_V96(x, y):  # scales tkinter coordinate system to ender coordinate system
    # 22.5 accounts for the distance between the center of objective turret to
    # the center of the objective hole
    ender_x = 21 - 22.5
    ender_y = 210
    x_scaled = (x / 10) + ender_x
    y_scaled = ender_y - (y / 10)
    print("Scaled coordinates - X:", x_scaled, "Y:", y_scaled)
    # calls function generate list to generate the postions list
    generate_list(x_scaled, y_scaled)
    return x_scaled, y_scaled


# function to take photos
cap = cv2.VideoCapture(0)

# Get a frame from the capture device
ret, frame = cap.read()
print(ret) # We should get true in the terminal if the camera is connected

# Display the frame
cv2.imshow('Frame', frame)
cv2.waitKey(0)
cv2.destroyAllWindows() # This closes the all the OpenVNC windows

# Define Function to take a photo
def take_photo():
    cap = cv2.VideoCapture(0)
    ret,frame = cap.read()
    if ret:
        # Save the photo with a unique name to avoid overwriting
        filename = f'UsbCameraPhoto_{int(time.time())}.jpg'
        cv2.imwrite(filename, frame)
    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close any OpenCV windows

take_photo()

# generates list of coordinates and appends coordinates to larger
# positions list
def generate_list(x, y):
    coordinate_list = []
    coordinate_list.append(x)
    coordinate_list.append(y)
    positions.append(coordinate_list)
    print(positions)
    return positions


'''
To use add fxn to image cells button
like so: make_gcode(positions,file)
'''


def make_gcode(positions, file_name):  # creates a gcode file using positions list
    with open(file_name, 'w') as f:
        for coordinates in positions:
            if len(coordinates) == 3:
                x, y, z = coordinates
                gcode_line = f'G1 X{x} Y{y} Z{z}\n'
                f.write(gcode_line)
            else:
                x, y = coordinates
                gcode_line = f'G1 X{x} Y{y}\n'
                f.write(gcode_line)

    print("it opened")  # for testing remove later


'''
To use add fxn to image cells button
like so: send_code_to_intellicell(file)
'''


def send_code_to_intellicell(file_name):  # sends gcode file to ender

    # replace COMX with port name
    ser = serial.Serial('COM11', 115200, timeout=1)

    # reads gcode file
    with open(file_name, 'r') as file:
        gcode_commands = file.readlines()

    # Sends each G-code command to the printer
    for command in gcode_commands:
        ser.write(command.encode('utf-8'))
        time.sleep(1)  # adjust later, controls time in between each location
        take_photo()

    ser.close()


#def select_all_pd(positions):
    #all_coordinates = [200, 200, 600, 200, 200, 675,
                       # 600, 475]  # insert all coordinates here
   # scaled_coordinates = []
    #for i in range(0, len(all_coordinates), 2):
        #x = all_coordinates[i]
        #y = all_coordinates[i + 1]
        #scaled_coordinates.append(scale_to_size_pd(x, y))


def select_all_V96(positions):
    A = 695
    B = 595
    C = 495
    D = 405
    E = 315
    F = 235
    G = 145
    H = 45

    C1 = 60
    C2 = 150
    C3 = 240
    C4 = 330
    C5 = 420
    C6 = 510
    C7 = 600
    C8 = 690
    C9 = 780
    C10 = 870
    C11 = 960
    C12 = 1050

    all_coordinates = [A,C1,B,C1,C,C1,D,C1,E,C1,F,C1,G,C1,H,C1,
                       A,C2,B,C2,C,C2,D,C2,E,C2,F,C2,G,C2,H,C2,
                       A,C3,B,C3,C,C3,D,C3,E,C3,F,C3,G,C3,H,C3,
                       A,C4,B,C4,C,C4,D,C4,E,C4,F,C4,G,C4,H,C4,
                       A,C5,B,C5,C,C5,D,C5,E,C5,F,C5,G,C5,H,C5,
                       A,C6,B,C6,C,C6,D,C6,E,C6,F,C6,G,C6,H,C6,
                       A,C7,B,C7,C,C7,D,C7,E,C7,F,C7,G,C7,H,C7,
                       A,C8,B,C8,C,C8,D,C8,E,C8,F,C8,G,C8,H,C8,
                       A,C9,B,C9,C,C9,D,C9,E,C9,F,C9,G,C9,H,C9,
                       A,C10,B,C10,C,C10,D,C10,E,C10,F,C10,G,C10,H,C10,
                       A,C11,B,C11,C,C11,D,C11,E,C11,F,C11,G,C11,H,C11,
                       A,C12,B,C12,C,C12,D,C12,E,C12,F,C12,G,C12,H,C12]  # insert all coordinates here
    scaled_coordinates = []
    for i in range(0, len(all_coordinates), 2):
        x = all_coordinates[i]
        y = all_coordinates[i + 1]
        scaled_coordinates.append(scale_to_size_V96(x, y))


def select_all_H96(positions):
    A = 695
    B = 595
    C = 495
    D = 405
    E = 315
    F = 235
    G = 145
    H = 45

    C1 = 60
    C2 = 150
    C3 = 240
    C4 = 330
    C5 = 420
    C6 = 510
    C7 = 600
    C8 = 690
    C9 = 780
    C10 = 870
    C11 = 960
    C12 = 1050

    all_coordinates = [A, C1, B, C1, C, C1, D, C1, E, C1, F, C1, G, C1, H, C1,
                       A, C2, B, C2, C, C2, D, C2, E, C2, F, C2, G, C2, H, C2,
                       A, C3, B, C3, C, C3, D, C3, E, C3, F, C3, G, C3, H, C3,
                       A, C4, B, C4, C, C4, D, C4, E, C4, F, C4, G, C4, H, C4,
                       A, C5, B, C5, C, C5, D, C5, E, C5, F, C5, G, C5, H, C5,
                       A, C6, B, C6, C, C6, D, C6, E, C6, F, C6, G, C6, H, C6,
                       A, C7, B, C7, C, C7, D, C7, E, C7, F, C7, G, C7, H, C7,
                       A, C8, B, C8, C, C8, D, C8, E, C8, F, C8, G, C8, H, C8,
                       A, C9, B, C9, C, C9, D, C9, E, C9, F, C9, G, C9, H, C9,
                       A, C10, B, C10, C, C10, D, C10, E, C10, F, C10, G, C10, H, C10,
                       A, C11, B, C11, C, C11, D, C11, E, C11, F, C11, G, C11, H, C11,
                       A, C12, B, C12, C, C12, D, C12, E, C12, F, C12, G, C12, H, C12]
    scaled_coordinates = []
    for i in range(0, len(all_coordinates), 2):
        x = all_coordinates[i]
        y = all_coordinates[i + 1]
        scaled_coordinates.append(scale_to_size_H96(x, y))


def clear_all(positions):
    del positions[1:]
    print(positions)
    return positions


# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("IntelliCell")
        self.geometry(f"{1500}x{700}")

        # configure grid layout

        self.grid_columnconfigure((1, 2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="IntelliCell",
            font=customtkinter.CTkFont(
                size=20,
                weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Start Run",
            command=lambda: [
                make_gcode(
                    positions,
                    file),
                send_code_to_intellicell(file)])
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Save File", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=[
                "Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))

        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame,
            values=[
                "80%",
                "90%",
                "100%",
                "110%",
                "120%"],
            command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(
            row=0, column=1, padx=(
                20, 0), pady=(
                20, 0), sticky="nsew")
        self.textbox.insert("0.0", "Welcome!\n\n" +
                            "Thank you for using our device.\n\n " +
                            "Please select the following\n plate(s) " +
                            "corresponding to the\n slots on our device." +
                            "\n\nPress 'Start Run' to begin\n scanning.")
        self.textbox_invisible = customtkinter.CTkTextbox(
            self, width=250, fg_color="transparent")
        self.textbox_invisible.grid(
            row=1, column=1, rowspan=4, padx=(
                20, 0), pady=(
                20, 0), sticky="nsew")

        # create slot image buttons
        self.slot_frame = customtkinter.CTkFrame(self, width=250)
        self.slot_frame.grid(
            row=0, column=2, rowspan=4, padx=(
                20, 0), pady=(
                20, 0), sticky="nsew")
        self.slot_frame.rowconfigure(4, weight=1)

        # Petri Dish Slot Button
        #slot1_img = Image.open("Petri Dish Image.png")
        #slot1_img = slot1_img.resize((200, 200))
        #self.slot1_img = ImageTk.PhotoImage(slot1_img)
        # self.slot1_img = customtkinter.CTkImage(slot1_img)
        #self.slot1_btn = customtkinter.CTkButton(
            #master=self.slot_frame,
            #text="Petri Dish (1)",
            #fg_color="transparent",
            #border_width=2,
            #text_color=(
                #"gray10",
                #"#DCE4EE"),
            #image=self.slot1_img,
            #command=self.slot_petri_button_event)
        #self.slot1_btn.grid(
            #row=1, column=1, padx=(
                #20, 20), pady=(
                #20, 20), sticky="nsew")

        # 96 well plate slot button (vertical)
        slot2_img = Image.open("96-Well_plate.JPG")
        slot2_img = slot2_img.rotate(270, expand=True)
        slot2_img = slot2_img.resize((150, 200))
        self.slot2_img = ImageTk.PhotoImage(slot2_img)
        # self.slot2_img = customtkinter.CTkImage(slot2_img)
        self.slot2_btn = customtkinter.CTkButton(
            master=self.slot_frame,
            text="96-well Plate (1)",
            fg_color="transparent",
            border_width=2,
            text_color=(
                "gray10",
                "#DCE4EE"),
            image=self.slot2_img,
            command=self.slot_96well_2_button_event)
        self.slot2_btn.grid(
            row=1, column=2, padx=(
                20, 20), pady=(
                20, 20), sticky="nsew")

        # 96 well plate slot button (horizontal)
        slot3_img = Image.open("96-Well_plate.JPG")
        slot3_img = slot3_img.rotate(270, expand=True)
        slot3_img = slot3_img.resize((150, 200))
        self.slot3_img = ImageTk.PhotoImage(slot3_img)
        # self.slot3_img = customtkinter.CTkImage(slot3_img)
        self.slot3_btn = customtkinter.CTkButton(
            master=self.slot_frame,
            text="96-well Plate (2)",
            fg_color="transparent",
            border_width=2,
            text_color=(
                "gray10",
                "#DCE4EE"),
            image=self.slot3_img,
            command=self.slot_96well_3_button_event)
        self.slot3_btn.grid(
            row=1, column=3, padx=(
                20, 20), pady=(
                20, 20), sticky="nsew")

        # Select all slots button
        self.select_all_slots_btn = customtkinter.CTkButton(
            master=self.slot_frame,
            text="Select All",
            fg_color="transparent",
            border_width=2,
            text_color=(
                "gray10",
                "#DCE4EE"),
            command=self.select_all_slots_btn)

        self.select_all_slots_btn.grid(
            row=5, column=3, padx=(
                20, 20), pady=(
                20, 20), sticky="nsew")

        # Default Values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    #def slot_petri_button_event(self):
        #slot_popup = customtkinter.CTkToplevel(self)
        #slot_popup.geometry("850x650")
        #slot_popup.title("Petri Dish (1)")

        # Configuring grid layout (4x4)
        #slot_popup.grid_rowconfigure((0, 1, 2, 3), weight=1)
        #slot_popup.grid_columnconfigure((1), weight=1)

        # Frame for select all button
        #self.slot_popup_frame = customtkinter.CTkFrame(
            #slot_popup, width=100, corner_radius=0)
        #self.slot_popup_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        #self.logo_label = customtkinter.CTkLabel(
            #self.slot_popup_frame,
            #text="Petri Dish (1)",
            #font=customtkinter.CTkFont(
                #size=20,
                #weight="bold"))
        #self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Select All Button for petri
        #self.select_all_slot = customtkinter.CTkButton(
            #master=self.slot_popup_frame, text="Select All", command=lambda: [
                #self.select_all_wells(), select_all_pd(positions)])
        #self.select_all_slot.grid(
           # row=2, column=0, padx=10, pady=10, sticky="nsew")
        # Deselect All Button for petri
        #self.select_all_slot = customtkinter.CTkButton(
            #master=self.slot_popup_frame, text="Deselect All", command=lambda: [
                #ect_all_slot.grid(
            #row=3, column=0, padx=10, pady=10, sticky="nsew")
        # Done Button
        #self.done_btn = customtkinter.CTkButton(
            #self.slot_popup_frame,
            #text="Done",
            #fg_color="transparent",
            #border_width=2,
            #text_color=(
                #"gray10",
                #"#DCE4EE"))
        #self.done_btn.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Adding Petri Dish Selection Image
       # self.petri_frame = customtkinter.CTkFrame(
            #slot_popup, width=100, corner_radius=5)
        #self.petri_frame.grid(
            #row=0, column=1, rowspan=4, padx=(
                #10, 0), pady=(
                #10, 0), sticky="nsew")
        #self.petri_frame.grid_rowconfigure(0, weight=0)
        #self.petri_frame.grid_columnconfigure(0, weight=0)

        #slot_img = Image.open("Petri-Dish Selection.png")  # open image
        #slot_img = slot_img.resize((650, 650))  # resize image
        # convert image to Tkinter-compatible format
        #self.slot_img = ImageTk.PhotoImage(slot_img)
        #self.slot_img_label = tk.Label(self.petri_frame, image=self.slot_img)
        #self.slot_img_label.grid(
            #row=0,
            #column=1,
            #padx=10,
            #pady=10,
            #sticky="nsew")

        # Place buttons on Petri Dish Image

        #self.slot_buttons = []
        #self.selected_wells = set()

        #self.petri_select_top_left = customtkinter.CTkButton(
            #master=self.petri_frame,
            #text="1",
           #width=50,
            #height=50,
            #fg_color="blue",
            #command=lambda: [
                #self.toggle_well_petri(
                    #0,
                    #0),
                #scale_to_size_pd(
                    #200,
                    #200)])
        #self.petri_select_top_left.place(x=200, y=200)
        # self.petri_select_top_left.grid(row=0,column=0, padx=10, pady=10, sticky="nsew")
        #self.slot_buttons.append(self.petri_select_top_left)

        #self.petri_select_top_right = customtkinter.CTkButton(
            #master=self.petri_frame,
            #text="2",
            #width=50,
            #height=50,
            #fg_color="blue",
            #command=lambda: [
                #self.toggle_well_petri(
                    #0,
                    #1),
                #scale_to_size_pd(
                    #600,
                    #200)])  # nobody touch this
        #self.petri_select_top_right.place(x=400, y=200)
        # self.petri_select_top_right.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        #self.slot_buttons.append(self.petri_select_top_right)

        #self.petri_select_bottom_left = customtkinter.CTkButton(
            #master=self.petri_frame,
            #text="3",
            #width=50,
            #height=50,
            #fg_color="blue",
            #command=lambda: [
                #self.toggle_well_petri(
                    #1,
                    #0),
                #scale_to_size_pd(
                    #200,
                    #425 +
                    #250)])  # nobody touchy
        #self.petri_select_bottom_left.place(x=200, y=425)
        # self.petri_select_top_right.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        #self.slot_buttons.append(self.petri_select_bottom_left)

        #self.petri_select_bottom_right = customtkinter.CTkButton(
            #master=self.petri_frame,
            #text="4",
            #width=50,
            #height=50,
            #fg_color="blue",
            #command=lambda: [
                #self.toggle_well_petri(
                    #1,
                    #1),
                #scale_to_size_pd(
                    #600,
                    #425 + 250)])
        #self.petri_select_bottom_right.place(x=400, y=425)
        # self.petri_select_top_right.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        #self.slot_buttons.append(self.petri_select_bottom_right)

        # Brings pop-up window to front
        #slot_popup.attributes("-topmost", True)
        #print("slot_petri_button_event click")

    def slot_96well_2_button_event(self):
        slot_popup = customtkinter.CTkToplevel(self)
        slot_popup.geometry("850x750")
        slot_popup.title("96-Well Plate (2)")

        # Configuring grid layout (4x4)
        slot_popup.grid_rowconfigure((1, 2, 3), weight=1)
        slot_popup.grid_columnconfigure((1, 2), weight=1)

        # Frame for select all button
        self.slot_popup_frame = customtkinter.CTkFrame(
            slot_popup, width=100, corner_radius=0)
        self.slot_popup_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(
            self.slot_popup_frame,
            text="96-Well Plate (2)",
            font=customtkinter.CTkFont(
                size=20,
                weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Select All Button for vertical
        self.select_all_slot_1 = customtkinter.CTkButton(
            master=self.slot_popup_frame, text="Select All", command=lambda: [
                self.select_all_wells_1(), select_all_V96(positions)])
        self.select_all_slot_1.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew")
        # Deselect All Button for vertical
        self.select_all_slot_1 = customtkinter.CTkButton(
            master=self.slot_popup_frame, text="Deselect All", command=lambda: [
                self.deselect_all_wells_1(), clear_all(positions)])
        self.select_all_slot_1.grid(
            row=3, column=0, padx=10, pady=10, sticky="nsew")
        # Done Button
        self.done_btn = customtkinter.CTkButton(
            self.slot_popup_frame,
            text="Done",
            fg_color="transparent",
            border_width=2,
            text_color=(
                "gray10",
                "#DCE4EE"))
        self.done_btn.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # 96-well plate Image

        # Set up background, reconfigure to match Ender 3 specifications

        # w = tk.Canvas(self.slot_popup_frame, width=550, height=1350)
        self.slot_frame = customtkinter.CTkFrame(slot_popup, width=250)
        self.slot_frame.grid(
            row=0, column=1, rowspan=1, padx=(
                20, 0), pady=(
                20, 0), sticky="nsew")

        original = Image.open("96-Well_plate.JPG")
        original = original.resize((700, 550))
        rotated_image = original.transpose(Image.ROTATE_270)
        background_img = ImageTk.PhotoImage(rotated_image)
        # w.create_image(row=0,column=1, image=background_img, anchor="nw")
        self.original_label = customtkinter.CTkLabel(
            self.slot_frame, image=background_img)
        self.original_label.grid(row=0, column=1, sticky="nsew")
        #for vertical placement
        # button set-up
        multiplier = 78

        self.btn_buttons = []
        self.selected_btn = set()

        # row 1

        A = 695
        B = 595
        C = 495
        D = 405
        E = 315
        F = 235
        G = 145
        H = 45

        C1 = 60
        C2 = 150
        C3 = 240
        C4 = 330
        C5 = 420
        C6 = 510
        C7 = 600
        C8 = 690
        C9 = 780
        C10 = 870
        C11 = 960
        C12 = 1050

        self.btn_1 = customtkinter.CTkButton(
            self.slot_frame,
            text='H1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    0),
                scale_to_size_V96(H,C1)])
        self.btn_1.place(x=47, y=66)
        self.btn_buttons.append(self.btn_1)

        # btn_1 = tk.Button(self, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_1.winfo_x(), btn_1.winfo_y())])
        # btn_1.pack(side='top')
        # btn_1.config(height=1, width=2)
        # button = w.create_window(47, 66, anchor='nw', window=btn_1)  # Change
        # X and Y coordinates here

        self.btn_2 = customtkinter.CTkButton(
            self.slot_frame,
            text='G1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    1),
                scale_to_size_V96(G,C1)])
        self.btn_2.place(x=47 + (57 * 1), y=66)
        self.btn_buttons.append(self.btn_2)

        # btn_2 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_2.winfo_x(), btn_2.winfo_y())])
        # btn_2.config(height=1, width=2)
        # btn_2.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 66, anchor='nw',
        # window=btn_2)  # Change X and Y coordinates here
        self.btn_3 = customtkinter.CTkButton(
            self.slot_frame,
            text='F1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    2),
                scale_to_size_V96(F,C1)])
        self.btn_3.place(x=47 + (57 * 2), y=66)
        self.btn_buttons.append(self.btn_3)
        # btn_3 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_3.winfo_x(), btn_3.winfo_y())])
        # btn_3.pack(side='top')
        # btn_3.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 66, anchor='nw',
        # window=btn_3)  # Change X and Y coordinates here
        self.btn_4 = customtkinter.CTkButton(
            self.slot_frame,
            text='E1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    3),
                scale_to_size_V96(E,C1)])
        self.btn_4.place(x=47 + (57 * 3), y=66)
        self.btn_buttons.append(self.btn_4)
        # btn_4 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_4.winfo_x(), btn_4.winfo_y())])
        # btn_4.pack(side='top')
        # btn_4.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 66, anchor='nw',
        # window=btn_4)  # Change X and Y coordinates here
        self.btn_5 = customtkinter.CTkButton(
            self.slot_frame,
            text='D1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    4),
                scale_to_size_V96(D,C1)])
        self.btn_5.place(x=47 + (57 * 4), y=66)
        self.btn_buttons.append(self.btn_5)
        # btn_5 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_5.winfo_x(), btn_5.winfo_y())])
        # btn_5.pack(side='top')
        # btn_5.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 66, anchor='nw',
        # window=btn_5)  # Change X and Y coordinates here
        self.btn_6 = customtkinter.CTkButton(
            self.slot_frame,
            text='C1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    5),
                scale_to_size_V96(C,C1)])
        self.btn_6.place(x=47 + (57 * 5), y=66)
        self.btn_buttons.append(self.btn_6)
        # btn_6 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_6.winfo_x(), btn_6.winfo_y())])
        # btn_6.pack(side='top')
        # btn_6.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 66, anchor='nw',
        # window=btn_6)  # Change X and Y coordinates here
        self.btn_7 = customtkinter.CTkButton(
            self.slot_frame,
            text='B1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    6),
                scale_to_size_V96(B,C1)])
        self.btn_7.place(x=47 + (57 * 6), y=66)
        self.btn_buttons.append(self.btn_7)
        # btn_7 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_7.winfo_x(), btn_7.winfo_y())])
        # btn_7.pack(side='top')
        # btn_7.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 66, anchor='nw',
        # window=btn_7)  # Change X and Y coordinates here
        self.btn_8 = customtkinter.CTkButton(
            self.slot_frame,
            text='A1',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    7),
                scale_to_size_V96(A,C1)])
        self.btn_8.place(x=47 + (57 * 7), y=66)
        self.btn_buttons.append(self.btn_8)
        # btn_8 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_8.winfo_x(), btn_8.winfo_y())])
        # btn_8.pack(side='top')
        # btn_8.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 66, anchor='nw', window=btn_8)  # Change X and Y coordinates here
        #
        # # row 2
        self.btn_9 = customtkinter.CTkButton(
            self.slot_frame,
            text='H2',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    8),
                scale_to_size_V96(H,C2)])
        self.btn_9.place(x=47, y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_9)
        # btn_9 = Button(root, text='click here', bd=5,
        #                anchor='w', command=lambda: [print_coords(),
        #                                             generate_list(btn_9.winfo_x(), btn_9.winfo_y())])
        # btn_9.pack(side='top')
        # btn_9.config(height=1, width=2)
        # button = w.create_window(47, 66 + (51 * 1), anchor='nw',
        # window=btn_9)  # Change X and Y coordinates here
        self.btn_10 = customtkinter.CTkButton(self.slot_frame,
                                              text='G2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               9),
                                                               scale_to_size_V96(G,C2)])
        self.btn_10.place(x=47 + (57 * 1), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_10)
        # btn_10 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_10.winfo_x(), btn_10.winfo_y())])
        # btn_10.config(height=1, width=2)
        # btn_10.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 66 + (51 * 1), anchor='nw',
        # window=btn_10)  # Change X and Y coordinates here
        self.btn_11 = customtkinter.CTkButton(self.slot_frame,
                                              text='F2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               10),
                                                               scale_to_size_V96(F,C2)])
        self.btn_11.place(x=47 + (57 * 2), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_11)
        # btn_11 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_11.winfo_x(), btn_11.winfo_y())])
        # btn_11.pack(side='top')
        # btn_11.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 66 + (51 * 1), anchor='nw',
        # window=btn_11)  # Change X and Y coordinates here
        self.btn_12 = customtkinter.CTkButton(self.slot_frame,
                                              text='E2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               11),
                                                               scale_to_size_V96(E,C2)])
        self.btn_12.place(x=47 + (57 * 3), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_12)
        # btn_12 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_12.winfo_x(), btn_12.winfo_y())])
        # btn_12.pack(side='top')
        # btn_12.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 66 + (51 * 1), anchor='nw',
        # window=btn_12)  # Change X and Y coordinates here
        self.btn_13 = customtkinter.CTkButton(self.slot_frame,
                                              text='D2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               12),
                                                               scale_to_size_V96(D,C2)])
        self.btn_13.place(x=47 + (57 * 4), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_13)
        # btn_13 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_13.winfo_x(), btn_13.winfo_y())])
        # btn_13.pack(side='top')
        # btn_13.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 66 + (51 * 1), anchor='nw',
        # window=btn_13)  # Change X and Y coordinates here
        self.btn_14 = customtkinter.CTkButton(self.slot_frame,
                                              text='C2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               13),
                                                               scale_to_size_V96(C,C2)])
        self.btn_14.place(x=47 + (57 * 5), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_14)
        # btn_14 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_14.winfo_x(), btn_14.winfo_y())])
        # btn_14.pack(side='top')
        # btn_14.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 66 + (51 * 1), anchor='nw',
        # window=btn_14)  # Change X and Y coordinates here
        self.btn_15 = customtkinter.CTkButton(self.slot_frame,
                                              text='B2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               14),
                                                               scale_to_size_V96(B,C2)])
        self.btn_15.place(x=47 + (57 * 6), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_15)
        # btn_15 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_15.winfo_x(), btn_15.winfo_y())])
        # btn_15.pack(side='top')
        # btn_15.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 66 + (51 * 1), anchor='nw',
        # window=btn_15)  # Change X and Y coordinates here
        self.btn_16 = customtkinter.CTkButton(self.slot_frame,
                                              text='A2',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               15),
                                                               scale_to_size_V96(A,C2)])
        self.btn_16.place(x=47 + (57 * 7), y=66 + (51 * 1))
        self.btn_buttons.append(self.btn_16)
        # btn_16 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_16.winfo_x(), btn_16.winfo_y())])
        # btn_16.pack(side='top')
        # btn_16.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 66 + (51 * 1), anchor='nw',
        #                          window=btn_16)  # Change X and Y coordinates here
        #
        # # row 3
        self.btn_17 = customtkinter.CTkButton(
            self.slot_frame,
            text='H3',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    16),
                scale_to_size_V96(H,C3)])
        self.btn_17.place(x=47, y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_17)
        # btn_17 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_17.winfo_x(), btn_17.winfo_y())])
        # btn_17.pack(side='top')
        # btn_17.config(height=1, width=2)
        # button = w.create_window(47, 66 + (51 * 2), anchor='nw',
        # window=btn_17)  # Change X and Y coordinates here
        self.btn_18 = customtkinter.CTkButton(self.slot_frame,
                                              text='G3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               17),
                                                               scale_to_size_V96(G,C3)])
        self.btn_18.place(x=47 + (57 * 1), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_18)
        # btn_18 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_18.winfo_x(), btn_18.winfo_y())])
        # btn_18.config(height=1, width=2)
        # btn_18.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 66 + (51 * 2), anchor='nw',
        # window=btn_18)  # Change X and Y coordinates here
        self.btn_19 = customtkinter.CTkButton(self.slot_frame,
                                              text='F3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               18),
                                                               scale_to_size_V96(F,C3)])
        self.btn_19.place(x=47 + (57 * 2), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_19)
        # btn_19 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_19.winfo_x(), btn_19.winfo_y())])
        # btn_19.pack(side='top')
        # btn_19.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 66 + (51 * 2), anchor='nw',
        # window=btn_19)  # Change X and Y coordinates here
        self.btn_20 = customtkinter.CTkButton(self.slot_frame,
                                              text='E3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               19),
                                                               scale_to_size_V96(E,C3)])
        self.btn_20.place(x=47 + (57 * 3), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_20)
        # btn_20 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_20.winfo_x(), btn_20.winfo_y())])
        # btn_20.pack(side='top')
        # btn_20.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 66 + (51 * 2), anchor='nw',
        # window=btn_20)  # Change X and Y coordinates here
        self.btn_21 = customtkinter.CTkButton(self.slot_frame,
                                              text='D3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               20),
                                                               scale_to_size_V96(D,C3)])
        self.btn_21.place(x=47 + (57 * 4), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_21)
        # btn_21 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_21.winfo_x(), btn_21.winfo_y())])
        # btn_21.pack(side='top')
        # btn_21.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 66 + (51 * 2), anchor='nw',
        # window=btn_21)  # Change X and Y coordinates here
        self.btn_22 = customtkinter.CTkButton(self.slot_frame,
                                              text='C3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               21),
                                                               scale_to_size_V96(C,C3)])
        self.btn_22.place(x=47 + (57 * 5), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_22)
        # btn_22 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_22.winfo_x(), btn_22.winfo_y())])
        # btn_22.pack(side='top')
        # btn_22.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 66 + (51 * 2), anchor='nw',
        #                          window=btn_22)  # Change X and Y coordinates here
        #
        # btn_22 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_22.winfo_x(), btn_22.winfo_y())])
        # btn_22.pack(side='top')
        # btn_22.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 66 + (51 * 2), anchor='nw',
        # window=btn_22)  # Change X and Y coordinates here
        self.btn_23 = customtkinter.CTkButton(self.slot_frame,
                                              text='B3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               22),
                                                               scale_to_size_V96(B,C3)])
        self.btn_23.place(x=47 + (57 * 6), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_23)
        # btn_23 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_23.winfo_x(), btn_23.winfo_y())])
        # btn_23.pack(side='top')
        # btn_23.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 66 + (51 * 2), anchor='nw', window=btn_23)
        self.btn_24 = customtkinter.CTkButton(self.slot_frame,
                                              text='A3',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               23),
                                                               scale_to_size_V96(A,C3)])
        self.btn_24.place(x=47 + (57 * 7), y=66 + (51 * 2))
        self.btn_buttons.append(self.btn_24)
        # # row 4
        self.btn_25 = customtkinter.CTkButton(
            self.slot_frame,
            text='H4',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    24),
                scale_to_size_V96(H,C4)])
        self.btn_25.place(x=47, y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_25)
        # btn_24 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_24.winfo_x(), btn_24.winfo_y())])
        # btn_24.pack(side='top')
        # btn_24.config(height=1, width=2)
        # button = w.create_window(47, 66 + (51 * 3), anchor='nw',
        # window=btn_24)  # Change X and Y coordinates here
        self.btn_26 = customtkinter.CTkButton(self.slot_frame,
                                              text='G4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               25),
                                                               scale_to_size_V96(G,C4)])
        self.btn_26.place(x=47 + (57 * 1), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_26)
        # btn_25 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_25.winfo_x(), btn_25.winfo_y())])
        # btn_25.config(height=1, width=2)
        # btn_25.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 66 + (51 * 3), anchor='nw',
        # window=btn_25)  # Change X and Y coordinates here
        self.btn_27 = customtkinter.CTkButton(self.slot_frame,
                                              text='F4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               26),
                                                               scale_to_size_V96(F,C4)])
        self.btn_27.place(x=47 + (57 * 2), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_27)
        # btn_26 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_26.winfo_x(), btn_26.winfo_y())])
        # btn_26.pack(side='top')
        # btn_26.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 66 + (51 * 3), anchor='nw',
        # window=btn_26)  # Change X and Y coordinates here
        self.btn_28 = customtkinter.CTkButton(self.slot_frame,
                                              text='E4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               27),
                                                               scale_to_size_V96(E,C4)])
        self.btn_28.place(x=47 + (57 * 3), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_28)
        # btn_27 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_27.winfo_x(), btn_27.winfo_y())])
        # btn_27.pack(side='top')
        # btn_27.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 66 + (51 * 3), anchor='nw',
        # window=btn_27)  # Change X and Y coordinates here
        self.btn_29 = customtkinter.CTkButton(self.slot_frame,
                                              text='D4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               28),
                                                               scale_to_size_V96(D,C4)])
        self.btn_29.place(x=47 + (57 * 4), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_29)
        # btn_28 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_28.winfo_x(), btn_28.winfo_y())])
        # btn_28.pack(side='top')
        # btn_28.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 66 + (51 * 3), anchor='nw',
        # window=btn_28)  # Change X and Y coordinates here
        self.btn_30 = customtkinter.CTkButton(self.slot_frame,
                                              text='C4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               29),
                                                               scale_to_size_V96(C,C4)])
        self.btn_30.place(x=47 + (57 * 5), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_30)
        # btn_29 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_29.winfo_x(), btn_29.winfo_y())])
        # btn_29.pack(side='top')
        # btn_29.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 66 + (51 * 3), anchor='nw',
        # window=btn_29)  # Change X and Y coordinates here
        self.btn_31 = customtkinter.CTkButton(self.slot_frame,
                                              text='B4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               30),
                                                               scale_to_size_V96(B,C4)])
        self.btn_31.place(x=47 + (57 * 6), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_31)
        # btn_30 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_30.winfo_x(), btn_30.winfo_y())])
        # btn_30.pack(side='top')
        # btn_30.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 66 + (51 * 3), anchor='nw',
        # window=btn_30)  # Change X and Y coordinates here
        self.btn_32 = customtkinter.CTkButton(self.slot_frame,
                                              text='A4',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               31),
                                                               scale_to_size_V96(A,C4)])
        self.btn_32.place(x=47 + (57 * 7), y=66 + (51 * 3))
        self.btn_buttons.append(self.btn_32)
        # btn_31 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_31.winfo_x(), btn_31.winfo_y())])
        # btn_31.pack(side='top')
        # btn_31.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 66 + (51 * 3), anchor='nw', window=btn_31)
        #
        # # row 5
        self.btn_33 = customtkinter.CTkButton(
            self.slot_frame,
            text='H5',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    32),
                scale_to_size_V96(H,C5)])
        self.btn_33.place(x=47, y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_33)
        # btn_32 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_32.winfo_x(), btn_32.winfo_y())])
        # btn_32.pack(side='top')
        # btn_32.config(height=1, width=2)
        # button = w.create_window(47, 65 + (51 * 4), anchor='nw',
        # window=btn_32)  # Change X and Y coordinates here
        self.btn_34 = customtkinter.CTkButton(self.slot_frame,
                                              text='G5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               33),
                                                               scale_to_size_V96(G,C5)])
        self.btn_34.place(x=47 + (57 * 1), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_34)
        # btn_33 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_33.winfo_x(), btn_33.winfo_y())])
        # btn_33.config(height=1, width=2)
        # btn_33.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 65 + (51 * 4), anchor='nw',
        # window=btn_33)  # Change X and Y coordinates here
        self.btn_35 = customtkinter.CTkButton(self.slot_frame,
                                              text='F5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               34),
                                                               scale_to_size_V96(F,C5)])
        self.btn_35.place(x=47 + (57 * 2), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_35)
        # btn_34 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_34.winfo_x(), btn_34.winfo_y())])
        # btn_34.pack(side='top')
        # btn_34.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 65 + (51 * 4), anchor='nw',
        # window=btn_34)  # Change X and Y coordinates here
        self.btn_36 = customtkinter.CTkButton(self.slot_frame,
                                              text='E5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               35),
                                                               scale_to_size_V96(E,C5)])
        self.btn_36.place(x=47 + (57 * 3), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_36)
        # btn_35 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_35.winfo_x(), btn_35.winfo_y())])
        # btn_35.pack(side='top')
        # btn_35.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 65 + (51 * 4), anchor='nw',
        # window=btn_35)  # Change X and Y coordinates here
        self.btn_37 = customtkinter.CTkButton(self.slot_frame,
                                              text='D5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               36),
                                                               scale_to_size_V96(D,C5)])
        self.btn_37.place(x=47 + (57 * 4), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_37)
        # btn_36 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_36.winfo_x(), btn_36.winfo_y())])
        # btn_36.pack(side='top')
        # btn_36.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 65 + (51 * 4), anchor='nw',
        # window=btn_36)  # Change X and Y coordinates here
        self.btn_38 = customtkinter.CTkButton(self.slot_frame,
                                              text='C5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               37),
                                                               scale_to_size_V96(C,C5)])
        self.btn_38.place(x=47 + (57 * 5), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_38)
        # btn_37 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_37.winfo_x(), btn_37.winfo_y())])
        # btn_37.pack(side='top')
        # btn_37.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 65 + (51 * 4), anchor='nw',
        # window=btn_37)  # Change X and Y coordinates here
        self.btn_39 = customtkinter.CTkButton(self.slot_frame,
                                              text='B5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               38),
                                                               scale_to_size_V96(B,C5)])
        self.btn_39.place(x=47 + (57 * 6), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_39)
        # btn_38 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_38.winfo_x(), btn_38.winfo_y())])
        # btn_38.pack(side='top')
        # btn_38.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 65 + (51 * 4), anchor='nw',
        # window=btn_38)  # Change X and Y coordinates here
        self.btn_40 = customtkinter.CTkButton(self.slot_frame,
                                              text='A5',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               39),
                                                               scale_to_size_V96(A,C5)])
        self.btn_40.place(x=47 + (57 * 7), y=66 + (51 * 4))
        self.btn_buttons.append(self.btn_40)
        # btn_39 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_39.winfo_x(), btn_39.winfo_y())])
        # btn_39.pack(side='top')
        # btn_39.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 65 + (51 * 4), anchor='nw', window=btn_39)
        #
        # # row 6
        self.btn_41 = customtkinter.CTkButton(
            self.slot_frame,
            text='H6',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    40),
                scale_to_size_V96(H,C6)])
        self.btn_41.place(x=47, y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_41)
        # btn_40 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_40.winfo_x(), btn_40.winfo_y())])
        # btn_40.pack(side='top')
        # btn_40.config(height=1, width=2)
        # button = w.create_window(47, 65 + (51 * 5), anchor='nw',
        # window=btn_40)  # Change X and Y coordinates here
        self.btn_42 = customtkinter.CTkButton(self.slot_frame,
                                              text='G6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               41),
                                                               scale_to_size_V96(G,C6)])
        self.btn_42.place(x=47 + (57 * 1), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_42)
        # btn_41 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_41.winfo_x(), btn_41.winfo_y())])
        # btn_41.config(height=1, width=2)
        # btn_41.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 65 + (51 * 5), anchor='nw',
        # window=btn_41)  # Change X and Y coordinates here
        self.btn_43 = customtkinter.CTkButton(self.slot_frame,
                                              text='F6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               42),
                                                               scale_to_size_V96(F,C6)])
        self.btn_43.place(x=47 + (57 * 2), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_43)
        # btn_42 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_42.winfo_x(), btn_42.winfo_y())])
        # btn_42.pack(side='top')
        # btn_42.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 65 + (51 * 5), anchor='nw',
        # window=btn_42)  # Change X and Y coordinates here
        self.btn_44 = customtkinter.CTkButton(self.slot_frame,
                                              text='E6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               43),
                                                               scale_to_size_V96(E,C6)])
        self.btn_44.place(x=47 + (57 * 3), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_44)
        # btn_43 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_43.winfo_x(), btn_43.winfo_y())])
        # btn_43.pack(side='top')
        # btn_43.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 65 + (51 * 5), anchor='nw',
        # window=btn_43)  # Change X and Y coordinates here
        self.btn_45 = customtkinter.CTkButton(self.slot_frame,
                                              text='D6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               44),
                                                               scale_to_size_V96(D,C6)])
        self.btn_45.place(x=47 + (57 * 4), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_45)
        # btn_44 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_44.winfo_x(), btn_44.winfo_y())])
        # btn_44.pack(side='top')
        # btn_44.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 65 + (51 * 5), anchor='nw',
        # window=btn_44)  # Change X and Y coordinates here
        self.btn_46 = customtkinter.CTkButton(self.slot_frame,
                                              text='C6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               45),
                                                               scale_to_size_V96(C,C6)])
        self.btn_46.place(x=47 + (57 * 5), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_46)
        # btn_45 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_45.winfo_x(), btn_45.winfo_y())])
        # btn_45.pack(side='top')
        # btn_45.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 65 + (51 * 5), anchor='nw',
        # window=btn_45)  # Change X and Y coordinates here
        self.btn_47 = customtkinter.CTkButton(self.slot_frame,
                                              text='B6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               46),
                                                               scale_to_size_V96(B,C6)])
        self.btn_47.place(x=47 + (57 * 6), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_47)
        # btn_46 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_46.winfo_x(), btn_46.winfo_y())])
        # btn_46.pack(side='top')
        # btn_46.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 65 + (51 * 5), anchor='nw',
        # window=btn_46)  # Change X and Y coordinates here
        self.btn_48 = customtkinter.CTkButton(self.slot_frame,
                                              text='A6',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               47),
                                                               scale_to_size_V96(A,C6)])
        self.btn_48.place(x=47 + (57 * 7), y=66 + (51 * 5))
        self.btn_buttons.append(self.btn_48)
        # btn_47 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_47.winfo_x(), btn_47.winfo_y())])
        # btn_47.pack(side='top')
        # btn_47.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 65 + (51 * 5), anchor='nw', window=btn_47)
        #
        # # row 7
        self.btn_49 = customtkinter.CTkButton(
            self.slot_frame,
            text='H7',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    48),
                scale_to_size_V96(H,C7)])
        self.btn_49.place(x=47, y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_49)
        # btn_48 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_48.winfo_x(), btn_48.winfo_y())])
        # btn_48.pack(side='top')
        # btn_48.config(height=1, width=2)
        # button = w.create_window(47, 64 + (51 * 6), anchor='nw',
        # window=btn_48)  # Change X and Y coordinates here
        self.btn_50 = customtkinter.CTkButton(self.slot_frame,
                                              text='G7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               49),
                                                               scale_to_size_V96(G,C7)])
        self.btn_50.place(x=47 + (57 * 1), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_50)
        # btn_49 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_49.winfo_x(), btn_49.winfo_y())])
        # btn_49.config(height=1, width=2)
        # btn_49.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 64 + (51 * 6), anchor='nw',
        # window=btn_49)  # Change X and Y coordinates here
        self.btn_51 = customtkinter.CTkButton(self.slot_frame,
                                              text='F7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               50),
                                                               scale_to_size_V96(F,C7)])
        self.btn_51.place(x=47 + (57 * 2), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_51)
        # btn_50 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_50.winfo_x(), btn_50.winfo_y())])
        # btn_50.pack(side='top')
        # btn_50.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 64 + (51 * 6), anchor='nw',
        # window=btn_50)  # Change X and Y coordinates here
        self.btn_52 = customtkinter.CTkButton(self.slot_frame,
                                              text='E7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               51),
                                                               scale_to_size_V96(E,C7)])
        self.btn_52.place(x=47 + (57 * 3), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_52)
        # btn_51 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_51.winfo_x(), btn_51.winfo_y())])
        # btn_51.pack(side='top')
        # btn_51.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 64 + (51 * 6), anchor='nw',
        # window=btn_51)  # Change X and Y coordinates here
        self.btn_53 = customtkinter.CTkButton(self.slot_frame,
                                              text='D7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               52),
                                                               scale_to_size_V96(D,C7)])
        self.btn_53.place(x=47 + (57 * 4), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_53)
        # btn_52 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_52.winfo_x(), btn_52.winfo_y())])
        # btn_52.pack(side='top')
        # btn_52.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 64 + (51 * 6), anchor='nw',
        # window=btn_52)  # Change X and Y coordinates here
        self.btn_54 = customtkinter.CTkButton(self.slot_frame,
                                              text='C7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               53),
                                                               scale_to_size_V96(C,C7)])
        self.btn_54.place(x=47 + (57 * 5), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_54)
        # btn_53 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_53.winfo_x(), btn_53.winfo_y())])
        # btn_53.pack(side='top')
        # btn_53.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 64 + (51 * 6), anchor='nw',
        # window=btn_53)  # Change X and Y coordinates here
        self.btn_55 = customtkinter.CTkButton(self.slot_frame,
                                              text='B7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               54),
                                                               scale_to_size_V96(B,C7)])
        self.btn_55.place(x=47 + (57 * 6), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_55)
        # btn_54 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_54.winfo_x(), btn_54.winfo_y())])
        # btn_54.pack(side='top')
        # btn_54.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 64 + (51 * 6), anchor='nw',
        # window=btn_54)  # Change X and Y coordinates here
        self.btn_56 = customtkinter.CTkButton(self.slot_frame,
                                              text='A7',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               55),
                                                               scale_to_size_V96(A,C7)])
        self.btn_56.place(x=47 + (57 * 7), y=66 + (51 * 6))
        self.btn_buttons.append(self.btn_56)
        # btn_55 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_55.winfo_x(), btn_55.winfo_y())])
        # btn_55.pack(side='top')
        # btn_55.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 64 + (51 * 6), anchor='nw', window=btn_55)
        #
        # # row 8
        self.btn_57 = customtkinter.CTkButton(
            self.slot_frame,
            text='H8',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    56),
                scale_to_size_V96(H,C8)])
        self.btn_57.place(x=47, y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_57)
        # btn_56 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_56.winfo_x(), btn_56.winfo_y())])
        # btn_56.pack(side='top')
        # btn_56.config(height=1, width=2)
        # button = w.create_window(47, 64 + (51 * 7), anchor='nw',
        # window=btn_56)  # Change X and Y coordinates here
        self.btn_58 = customtkinter.CTkButton(self.slot_frame,
                                              text='G8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               57),
                                                               scale_to_size_V96(G,C8)])
        self.btn_58.place(x=47 + (57 * 1), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_58)
        # btn_57 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_57.winfo_x(), btn_57.winfo_y())])
        # btn_57.config(height=1, width=2)
        # btn_57.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 64 + (51 * 7), anchor='nw',
        # window=btn_57)  # Change X and Y coordinates here
        self.btn_59 = customtkinter.CTkButton(self.slot_frame,
                                              text='F8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               58),
                                                               scale_to_size_V96(F,C8)])
        self.btn_59.place(x=47 + (57 * 2), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_59)
        # btn_58 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_58.winfo_x(), btn_58.winfo_y())])
        # btn_58.pack(side='top')
        # btn_58.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 64 + (51 * 7), anchor='nw',
        # window=btn_58)  # Change X and Y coordinates here
        self.btn_60 = customtkinter.CTkButton(self.slot_frame,
                                              text='E8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               59),
                                                               scale_to_size_V96(E,C8)])
        self.btn_60.place(x=47 + (57 * 3), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_60)
        # btn_59 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_59.winfo_x(), btn_59.winfo_y())])
        # btn_59.pack(side='top')
        # btn_59.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 64 + (51 * 7), anchor='nw',
        # window=btn_59)  # Change X and Y coordinates here
        self.btn_61 = customtkinter.CTkButton(self.slot_frame,
                                              text='D8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               60),
                                                               scale_to_size_V96(D,C8)])
        self.btn_61.place(x=47 + (57 * 4), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_61)
        # btn_60 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_60.winfo_x(), btn_60.winfo_y())])
        # btn_60.pack(side='top')
        # btn_60.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 64 + (51 * 7), anchor='nw',
        # window=btn_60)  # Change X and Y coordinates here
        self.btn_62 = customtkinter.CTkButton(self.slot_frame,
                                              text='C8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               61),
                                                               scale_to_size_V96(C,C8)])
        self.btn_62.place(x=47 + (57 * 5), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_62)
        # btn_61 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_61.winfo_x(), btn_61.winfo_y())])
        # btn_61.pack(side='top')
        # btn_61.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 64 + (51 * 7), anchor='nw',
        # window=btn_61)  # Change X and Y coordinates here
        self.btn_63 = customtkinter.CTkButton(self.slot_frame,
                                              text='B8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               62),
                                                               scale_to_size_V96(B,C8)])
        self.btn_63.place(x=47 + (57 * 6), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_63)
        # btn_62 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_62.winfo_x(), btn_62.winfo_y())])
        # btn_62.pack(side='top')
        # btn_62.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 64 + (51 * 7), anchor='nw',
        # window=btn_62)  # Change X and Y coordinates here
        self.btn_64 = customtkinter.CTkButton(self.slot_frame,
                                              text='A8',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               63),
                                                               scale_to_size_V96(A,C8)])
        self.btn_64.place(x=47 + (57 * 7), y=66 + (51 * 7))
        self.btn_buttons.append(self.btn_64)
        # btn_63 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_63.winfo_x(), btn_63.winfo_y())])
        # btn_63.pack(side='top')
        # btn_63.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 64 + (51 * 7), anchor='nw', window=btn_63)
        #
        # # row 9
        self.btn_65 = customtkinter.CTkButton(
            self.slot_frame,
            text='H9',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    64),
                scale_to_size_V96(H,C9)])
        self.btn_65.place(x=47, y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_65)
        # btn_64 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_64.winfo_x(), btn_64.winfo_y())])
        # btn_64.pack(side='top')
        # btn_64.config(height=1, width=2)
        # button = w.create_window(47, 64 + (51 * 8), anchor='nw',
        # window=btn_64)  # Change X and Y coordinates here
        self.btn_66 = customtkinter.CTkButton(self.slot_frame,
                                              text='G9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               65),
                                                               scale_to_size_V96(G,C9)])
        self.btn_66.place(x=47 + (57 * 1), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_66)
        # btn_65 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_65.winfo_x(), btn_65.winfo_y())])
        # btn_65.config(height=1, width=2)
        # btn_65.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 64 + (51 * 8), anchor='nw',
        # window=btn_65)  # Change X and Y coordinates here
        self.btn_67 = customtkinter.CTkButton(self.slot_frame,
                                              text='F9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               66),
                                                               scale_to_size_V96(F,C9)])
        self.btn_67.place(x=47 + (57 * 2), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_67)
        # btn_66 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_66.winfo_x(), btn_66.winfo_y())])
        # btn_66.pack(side='top')
        # btn_66.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 64 + (51 * 8), anchor='nw',
        # window=btn_66)  # Change X and Y coordinates here
        self.btn_68 = customtkinter.CTkButton(self.slot_frame,
                                              text='E9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               67),
                                                               scale_to_size_V96(E,C9)])
        self.btn_68.place(x=47 + (57 * 3), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_68)
        # btn_67 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_67.winfo_x(), btn_67.winfo_y())])
        # btn_67.pack(side='top')
        # btn_67.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 64 + (51 * 8), anchor='nw',
        # window=btn_67)  # Change X and Y coordinates here
        self.btn_69 = customtkinter.CTkButton(self.slot_frame,
                                              text='D9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               68),
                                                               scale_to_size_V96(D,C9)])
        self.btn_69.place(x=47 + (57 * 4), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_69)
        # btn_68 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_68.winfo_x(), btn_68.winfo_y())])
        # btn_68.pack(side='top')
        # btn_68.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 64 + (51 * 8), anchor='nw',
        # window=btn_68)  # Change X and Y coordinates here
        self.btn_70 = customtkinter.CTkButton(self.slot_frame,
                                              text='C9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               69),
                                                               scale_to_size_V96(C,C9)])
        self.btn_70.place(x=47 + (57 * 5), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_70)
        # btn_69 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_69.winfo_x(), btn_69.winfo_y())])
        # btn_69.pack(side='top')
        # btn_69.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 64 + (51 * 8), anchor='nw',
        # window=btn_69)  # Change X and Y coordinates here
        self.btn_71 = customtkinter.CTkButton(self.slot_frame,
                                              text='B9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               70),
                                                               scale_to_size_V96(B,C9)])
        self.btn_71.place(x=47 + (57 * 6), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_71)
        # btn_70 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_70.winfo_x(), btn_70.winfo_y())])
        # btn_70.pack(side='top')
        # btn_70.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 64 + (51 * 8), anchor='nw',
        # window=btn_70)  # Change X and Y coordinates here
        self.btn_72 = customtkinter.CTkButton(self.slot_frame,
                                              text='A9',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               71),
                                                               scale_to_size_V96(A,C9)])
        self.btn_72.place(x=47 + (57 * 7), y=66 + (51 * 8))
        self.btn_buttons.append(self.btn_72)
        # btn_71 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_71.winfo_x(), btn_71.winfo_y())])
        # btn_71.pack(side='top')
        # btn_71.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 64 + (51 * 8), anchor='nw', window=btn_71)
        #
        # # row 10
        self.btn_73 = customtkinter.CTkButton(
            self.slot_frame,
            text='H10',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    72),
                scale_to_size_V96(H,C10)])
        self.btn_73.place(x=47, y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_73)
        # btn_72 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_72.winfo_x(), btn_72.winfo_y())])
        # btn_72.pack(side='top')
        # btn_72.config(height=1, width=2)
        # button = w.create_window(47, 64 + (51 * 9), anchor='nw',
        # window=btn_72)  # Change X and Y coordinates here
        self.btn_74 = customtkinter.CTkButton(self.slot_frame,
                                              text='G10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               73),
                                                               scale_to_size_V96(G,C10)])
        self.btn_74.place(x=47 + (57 * 1), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_74)
        # btn_73 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_73.winfo_x(), btn_73.winfo_y())])
        # btn_73.config(height=1, width=2)
        # btn_73.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 64 + (51 * 9), anchor='nw',
        # window=btn_73)  # Change X and Y coordinates here
        self.btn_75 = customtkinter.CTkButton(self.slot_frame,
                                              text='F10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               74),
                                                               scale_to_size_V96(F,C10)])
        self.btn_75.place(x=47 + (57 * 2), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_75)
        # btn_74 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_74.winfo_x(), btn_74.winfo_y())])
        # btn_74.pack(side='top')
        # btn_74.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 64 + (51 * 9), anchor='nw',
        # window=btn_74)  # Change X and Y coordinates here
        self.btn_76 = customtkinter.CTkButton(self.slot_frame,
                                              text='E10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               75),
                                                               scale_to_size_V96(E,C10)])
        self.btn_76.place(x=47 + (57 * 3), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_76)
        # btn_75 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_75.winfo_x(), btn_75.winfo_y())])
        # btn_75.pack(side='top')
        # btn_75.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 64 + (51 * 9), anchor='nw',
        # window=btn_75)  # Change X and Y coordinates here
        self.btn_77 = customtkinter.CTkButton(self.slot_frame,
                                              text='D10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               76),
                                                               scale_to_size_V96(D,C10)])
        self.btn_77.place(x=47 + (57 * 4), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_77)
        # btn_76 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_76.winfo_x(), btn_76.winfo_y())])
        # btn_76.pack(side='top')
        # btn_76.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 64 + (51 * 9), anchor='nw',
        # window=btn_76)  # Change X and Y coordinates here
        self.btn_78 = customtkinter.CTkButton(self.slot_frame,
                                              text='C10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               77),
                                                               scale_to_size_V96(C,C10)])
        self.btn_78.place(x=47 + (57 * 5), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_78)
        # btn_77 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_77.winfo_x(), btn_77.winfo_y())])
        # btn_77.pack(side='top')
        # btn_77.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 64 + (51 * 9), anchor='nw',
        # window=btn_77)  # Change X and Y coordinates here
        self.btn_79 = customtkinter.CTkButton(self.slot_frame,
                                              text='B10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               78),
                                                               scale_to_size_V96(B,C10)])
        self.btn_79.place(x=47 + (57 * 6), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_79)
        # btn_78 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_78.winfo_x(), btn_78.winfo_y())])
        # btn_78.pack(side='top')
        # btn_78.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 64 + (51 * 9), anchor='nw',
        # window=btn_78)  # Change X and Y coordinates here
        self.btn_80 = customtkinter.CTkButton(self.slot_frame,
                                              text='A10',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               79),
                                                               scale_to_size_V96(A,C10)])
        self.btn_80.place(x=47 + (57 * 7), y=66 + (51 * 9))
        self.btn_buttons.append(self.btn_80)
        # btn_79 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_79.winfo_x(), btn_79.winfo_y())])
        # btn_79.pack(side='top')
        # btn_79.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 64 + (51 * 9), anchor='nw', window=btn_79)
        #
        # # row 11
        self.btn_81 = customtkinter.CTkButton(
            self.slot_frame,
            text='H11',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    80),
                scale_to_size_V96(H,C11)])
        self.btn_81.place(x=47, y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_81)
        # btn_80 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_80.winfo_x(), btn_80.winfo_y())])
        # btn_80.pack(side='top')
        # btn_80.config(height=1, width=2)
        # button = w.create_window(47, 64 + (51 * 10), anchor='nw',
        # window=btn_80)  # Change X and Y coordinates here
        self.btn_82 = customtkinter.CTkButton(self.slot_frame,
                                              text='G11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               81),
                                                               scale_to_size_V96(G,C11)])
        self.btn_82.place(x=47 + (57 * 1), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_82)
        # btn_81 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_81.winfo_x(), btn_81.winfo_y())])
        # btn_81.config(height=1, width=2)
        # btn_81.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 64 + (51 * 10), anchor='nw',
        # window=btn_81)  # Change X and Y coordinates here
        self.btn_83 = customtkinter.CTkButton(self.slot_frame,
                                              text='F11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               82),
                                                               scale_to_size_V96(F,C11)])
        self.btn_83.place(x=47 + (57 * 2), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_83)
        # btn_82 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_82.winfo_x(), btn_82.winfo_y())])
        # btn_82.pack(side='top')
        # btn_82.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 64 + (51 * 10), anchor='nw',
        # window=btn_82)  # Change X and Y coordinates here
        self.btn_84 = customtkinter.CTkButton(self.slot_frame,
                                              text='E11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               83),
                                                               scale_to_size_V96(E,C11)])
        self.btn_84.place(x=47 + (57 * 3), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_84)
        # btn_83 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_83.winfo_x(), btn_83.winfo_y())])
        # btn_83.pack(side='top')
        # btn_83.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 64 + (51 * 10), anchor='nw',
        # window=btn_83)  # Change X and Y coordinates here
        self.btn_85 = customtkinter.CTkButton(self.slot_frame,
                                              text='D11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               84),
                                                               scale_to_size_V96(D,C11)])
        self.btn_85.place(x=47 + (57 * 4), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_85)
        # btn_84 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_84.winfo_x(), btn_84.winfo_y())])
        # btn_84.pack(side='top')
        # btn_84.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 4), 64 + (51 * 10), anchor='nw',
        # window=btn_84)  # Change X and Y coordinates here
        self.btn_86 = customtkinter.CTkButton(self.slot_frame,
                                              text='C11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               85),
                                                               scale_to_size_V96(C,C11)])
        self.btn_86.place(x=47 + (57 * 5), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_86)
        # btn_85 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_85.winfo_x(), btn_85.winfo_y())])
        # btn_85.pack(side='top')
        # btn_85.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 5), 64 + (51 * 10), anchor='nw',
        # window=btn_85)  # Change X and Y coordinates here
        self.btn_87 = customtkinter.CTkButton(self.slot_frame,
                                              text='B11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               86),
                                                               scale_to_size_V96(B,C11)])
        self.btn_87.place(x=47 + (57 * 6), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_87)
        # btn_86 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_86.winfo_x(), btn_86.winfo_y())])
        # btn_86.pack(side='top')
        # btn_86.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 6), 64 + (51 * 10), anchor='nw',
        # window=btn_86)  # Change X and Y coordinates here
        self.btn_88 = customtkinter.CTkButton(self.slot_frame,
                                              text='A11',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               87),
                                                               scale_to_size_V96(A,C11)])
        self.btn_88.place(x=47 + (57 * 7), y=66 + (51 * 10))
        self.btn_buttons.append(self.btn_88)
        # btn_87 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_87.winfo_x(), btn_87.winfo_y())])
        # btn_87.pack(side='top')
        # btn_87.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 7), 64 + (51 * 10), anchor='nw', window=btn_87)
        #
        # # row 12
        self.btn_89 = customtkinter.CTkButton(
            self.slot_frame,
            text='H12',
            anchor='c',
            fg_color="blue",
            height=30,
            width=30,
            command=lambda: [
                self.toggle_btn(
                    0,
                    88),
                scale_to_size_V96(H,C12)])
        self.btn_89.place(x=47, y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_89)
        # btn_88 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_88.winfo_x(), btn_88.winfo_y())])
        # btn_88.pack(side='top')
        # btn_88.config(height=1, width=2)
        # button = w.create_window(47, 63 + (51 * 11), anchor='nw',
        # window=btn_88)  # Change X and Y coordinates here
        self.btn_90 = customtkinter.CTkButton(self.slot_frame,
                                              text='G12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               89),
                                                               scale_to_size_V96(G,C12)])
        self.btn_90.place(x=47 + (57 * 1), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_90)
        # btn_89 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_89.winfo_x(), btn_89.winfo_y())])
        # btn_89.config(height=1, width=2)
        # btn_89.pack(side='top')
        # button = w.create_window(47 + (57 * 1), 63 + (51 * 11), anchor='nw',
        # window=btn_89)  # Change X and Y coordinates here
        self.btn_91 = customtkinter.CTkButton(self.slot_frame,
                                              text='F12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               90),
                                                               scale_to_size_V96(F,C12)])
        self.btn_91.place(x=47 + (57 * 2), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_91)
        # btn_90 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_90.winfo_x(), btn_90.winfo_y())])
        # btn_90.pack(side='top')
        # btn_90.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 2), 63 + (51 * 11), anchor='nw',
        # window=btn_90)  # Change X and Y coordinates here
        self.btn_92 = customtkinter.CTkButton(self.slot_frame,
                                              text='E12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               91),
                                                               scale_to_size_V96(E,C12)])
        self.btn_92.place(x=47 + (57 * 3), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_92)
        # btn_91 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_91.winfo_x(), btn_91.winfo_y())])
        # btn_91.pack(side='top')
        # btn_91.config(height=1, width=2)
        # button = w.create_window(47 + (57 * 3), 63 + (51 * 11), anchor='nw',
        # window=btn_91)  # Change X and Y coordinates here
        self.btn_93 = customtkinter.CTkButton(self.slot_frame,
                                              text='D12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               92),
                                                               scale_to_size_V96(D,C12)])
        self.btn_93.place(x=47 + (57 * 4), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_93)
        # btn_92 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_92.winfo_x(), btn_92.winfo_y())])
        # btn_92.pack(side='top')
        # btn_92.config(height=1, width=2)
        # button = w.create_window(48 + (57 * 4), 63 + (51 * 11), anchor='nw',
        # window=btn_92)  # Change X and Y coordinates here
        self.btn_94 = customtkinter.CTkButton(self.slot_frame,
                                              text='C12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               93),
                                                               scale_to_size_V96(C,C12)])
        self.btn_94.place(x=47 + (57 * 5), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_94)
        # btn_93 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_93.winfo_x(), btn_93.winfo_y())])
        # btn_93.pack(side='top')
        # btn_93.config(height=1, width=2)
        # button = w.create_window(48 + (57 * 5), 63 + (51 * 11), anchor='nw',
        # window=btn_93)  # Change X and Y coordinates here
        self.btn_95 = customtkinter.CTkButton(self.slot_frame,
                                              text='B12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               94),
                                                               scale_to_size_V96(B,C12)])
        self.btn_95.place(x=47 + (57 * 6), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_95)
        # btn_94 = Button(root, text='click here', bd=5,
        #                 anchor='w', command=lambda: [print_coords(),
        #                                              generate_list(btn_94.winfo_x(), btn_94.winfo_y())])
        # btn_94.pack(side='top')
        # btn_94.config(height=1, width=2)
        # button = w.create_window(48 + (57 * 6), 63 + (51 * 11), anchor='nw',
        # window=btn_94)  # Change X and Y coordinates here
        self.btn_96 = customtkinter.CTkButton(self.slot_frame,
                                              text='A12',
                                              anchor='c',
                                              fg_color="blue",
                                              height=30,
                                              width=30,
                                              command=lambda: [self.toggle_btn(0,
                                                                               95),
                                                               scale_to_size_V96(A,C12)])
        self.btn_96.place(x=47 + (57 * 7), y=66 + (51 * 11))
        self.btn_buttons.append(self.btn_96)

        # Brings pop-up window to front
        slot_popup.attributes("-topmost", True)
        print("slot_96well_2_button_event click")

    def slot_96well_3_button_event(self):
        slot_popup = customtkinter.CTkToplevel(self)
        slot_popup.geometry("850x750")
        slot_popup.title("96-Well Plate (3)")

        # Configuring grid layout (4x4)
        slot_popup.grid_rowconfigure((1, 2, 3), weight=1)
        slot_popup.grid_columnconfigure((1), weight=1)

        # Frame for select all button
        self.slot_popup_frame = customtkinter.CTkFrame(
            slot_popup, width=100, corner_radius=0)
        self.slot_popup_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(
            self.slot_popup_frame,
            text="96-Well Plate (3)",
            font=customtkinter.CTkFont(
                size=20,
                weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Select All Button for horizontal
        self.select_all_slot_2 = customtkinter.CTkButton(
            master=self.slot_popup_frame, text="Select All", command=lambda: [
                self.select_all_wells_2(), select_all_H96(positions)])
        self.select_all_slot_2.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew")
        # Deselect All Button for horizontal
        self.select_all_slot_2 = customtkinter.CTkButton(
            master=self.slot_popup_frame, text="Deselect All", command=lambda: [
                self.deselect_all_wells_2(), clear_all(positions)])
        self.select_all_slot_2.grid(
            row=3, column=0, padx=10, pady=10, sticky="nsew")
        # Done Button
        self.done_btn = customtkinter.CTkButton(
            self.slot_popup_frame,
            text="Done",
            fg_color="transparent",
            border_width=2,
            text_color=(
                "gray10",
                "#DCE4EE"))
        self.done_btn.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        # Adding 96-well (3) Selection Image
        self.well_96_3_frame = customtkinter.CTkFrame(
            slot_popup, width=250, corner_radius=5)
        self.well_96_3_frame.grid(
            row=0, column=1, rowspan=1, padx=(
                20, 0), pady=(
                20, 0), sticky="nsew")

        orig = Image.open("96-Well_plate.JPG")
        orig = orig.resize((700, 550))
        rotated_image = orig.transpose(Image.ROTATE_270)
        self.background_image = ImageTk.PhotoImage(rotated_image)
        self.background_image_label = tk.Label(
            self.well_96_3_frame, image=self.background_image)
        self.background_image_label.grid(
            row=0, column=1, sticky="nsew")

        # 96 well selection buttons for horizontal

        self.slot_buttons_1 = []
        self.selected_wells_1 = set()  # Keep track of selected wells

        A = 695
        B = 595
        C = 495
        D = 405
        E = 315
        F = 235
        G = 145
        H = 45

        C1 = 60
        C2 = 150
        C3 = 240
        C4 = 330
        C5 = 420
        C6 = 510
        C7 = 600
        C8 = 690
        C9 = 780
        C10 = 870
        C11 = 960
        C12 = 1050

        # First row
        slot_button_1_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 0), scale_to_size_H96(
                    H,C1)])
        # slot_button_1_1.grid(row=1, column=1, padx=1, pady=8)
        slot_button_1_1.place(x=47, y=66)
        self.slot_buttons_1.append(slot_button_1_1)

        slot_button_1_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 1), scale_to_size_H96(G,C1)])
        # slot_button_1_2.grid(row=1, column=2, padx=1, pady=8)
        slot_button_1_2.place(x=47 + (57 * 1), y=66)
        self.slot_buttons_1.append(slot_button_1_2)

        slot_button_1_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 2), scale_to_size_H96(F,C1)])
        # slot_button_1_3.grid(row=1, column=3, padx=1, pady=8)
        slot_button_1_3.place(x=47 + (57 * 2), y=66)
        self.slot_buttons_1.append(slot_button_1_3)

        slot_button_1_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 3), scale_to_size_H96(E,C1)])
        # slot_button_1_4.grid(row=1, column=4, padx=1, pady=8)
        slot_button_1_4.place(x=(47 + (57 * 3)), y=66)
        self.slot_buttons_1.append(slot_button_1_4)

        slot_button_1_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 4), scale_to_size_H96(D,C1)])
        # slot_button_1_5.grid(row=1, column=5, padx=1, pady=8)
        slot_button_1_5.place(x=(47 + (57 * 4)), y=66)
        self.slot_buttons_1.append(slot_button_1_5)

        slot_button_1_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 5), scale_to_size_H96(C,C1)])
        # slot_button_1_6.grid(row=1, column=6, padx=1, pady=8)
        slot_button_1_6.place(x=(47 + (57 * 5)), y=66)
        self.slot_buttons_1.append(slot_button_1_6)

        slot_button_1_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 6), scale_to_size_H96(B,C1)])
        # slot_button_1_7.grid(row=1, column=7, padx=1, pady=8)
        slot_button_1_7.place(x=(47 + (57 * 6)), y=66)
        self.slot_buttons_1.append(slot_button_1_7)

        slot_button_1_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A1", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 7), scale_to_size_H96(A,C1)])
        # slot_button_1_8.grid(row=1, column=8, padx=1, pady=8)
        slot_button_1_8.place(x=(47 + (57 * 7)), y=66)
        self.slot_buttons_1.append(slot_button_1_8)

        slot_button_1_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 8), scale_to_size_H96(H,C2)])
        # slot_button_1_9.grid(row=1, column=9, padx=1, pady=8)
        slot_button_1_9.place(x=47, y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_1_9)

        slot_button_1_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 9), scale_to_size_H96(G,C2)])
        # slot_button_1_10.grid(row=1, column=10, padx=1, pady=8)
        slot_button_1_10.place(x=(47 + (57 * 1)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_1_10)

        slot_button_1_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 10), scale_to_size_H96(F,C2)])
        # slot_button_1_11.grid(row=1, column=11, padx=1, pady=8)
        slot_button_1_11.place(x=(47 + (57 * 2)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_1_11)

        slot_button_1_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 11), scale_to_size_H96(E,C2)])
        # slot_button_1_12.grid(row=1, column=12, padx=1, pady=8)
        slot_button_1_12.place(x=(47 + (57 * 3)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_1_12)

        # Second row
        slot_button_2_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 12), scale_to_size_H96(D,C2)])
        # slot_button_2_1.grid(row=2, column=1, padx=1, pady=8)
        slot_button_2_1.place(x=(47 + (57 * 4)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_2_1)

        slot_button_2_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 13), scale_to_size_H96(C,C2)])
        # slot_button_2_2.grid(row=2, column=2, padx=1, pady=8)
        slot_button_2_2.place(x=(47 + (57 * 5)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_2_2)

        slot_button_2_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 14), scale_to_size_H96(
                    80 + (
                            50.5 * 2), 85 + 57)])
        # slot_button_2_3.grid(row=2, column=3, padx=1, pady=8)
        slot_button_2_3.place(x=(47 + (57 * 6)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_2_3)

        slot_button_2_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A2", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 15), scale_to_size_H96(A,C2)])
        # slot_button_2_4.grid(row=2, column=4, padx=1, pady=8)
        slot_button_2_4.place(x=(47 + (57 * 7)), y=(66 + (51 * 1)))
        self.slot_buttons_1.append(slot_button_2_4)
        #
        slot_button_2_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 16), scale_to_size_H96(H,C3)])
        # slot_button_2_5.grid(row=2, column=5, padx=1, pady=8)
        slot_button_2_5.place(x=47, y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_5)
        #
        slot_button_2_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 17), scale_to_size_H96(G,C3)])
        # slot_button_2_6.grid(row=2, column=6, padx=1, pady=8)
        slot_button_2_6.place(x=(47 + (57 * 1)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_6)

        slot_button_2_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 18), scale_to_size_H96(F,C3)])
        # slot_button_2_7.grid(row=2, column=7, padx=1, pady=8)
        slot_button_2_7.place(x=(47 + (57 * 2)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_7)

        slot_button_2_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 19), scale_to_size_H96(E,C3)])
        # slot_button_2_8.grid(row=2, column=8, padx=1, pady=8)
        slot_button_2_8.place(x=(47 + (57 * 3)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_8)

        slot_button_2_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 20), scale_to_size_H96(D,C3)])
        # slot_button_2_9.grid(row=2, column=9, padx=1, pady=8)
        slot_button_2_9.place(x=(47 + (57 * 4)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_9)

        slot_button_2_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 21), scale_to_size_H96(C,C3)])
        # slot_button_2_10.grid(row=2, column=10, padx=1, pady=8)
        slot_button_2_10.place(x=(47 + (57 * 5)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_10)

        slot_button_2_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 22), scale_to_size_H96(B,C3)])
        # slot_button_2_11.grid(row=2, column=11, padx=1, pady=8)
        slot_button_2_11.place(x=(47 + (57 * 6)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_11)

        slot_button_2_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A3", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 23), scale_to_size_H96(A,C3)])
        # slot_button_2_12.grid(row=2, column=12, padx=1, pady=8)
        slot_button_2_12.place(x=(47 + (57 * 7)), y=(66 + (51 * 2)))
        self.slot_buttons_1.append(slot_button_2_12)

        # 3rd row
        slot_button_3_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 24), scale_to_size_H96(H,C4)])
        # slot_button_3_1.grid(row=3, column=1, padx=1, pady=8)
        slot_button_3_1.place(x=47, y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_1)

        slot_button_3_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 25), scale_to_size_H96(G,C4)])
        # slot_button_3_2.grid(row=3, column=2, padx=1, pady=8)
        slot_button_3_2.place(x=(47 + (57 * 1)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_2)

        slot_button_3_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 26), scale_to_size_H96(F,C4)])
        # slot_button_3_3.grid(row=3, column=3, padx=1, pady=8)
        slot_button_3_3.place(x=(47 + (57 * 2)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_3)

        slot_button_3_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 27), scale_to_size_H96(E,C4)])
        # slot_button_3_4.grid(row=3, column=4, padx=1, pady=8)
        slot_button_3_4.place(x=(47 + (57 * 3)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_4)

        slot_button_3_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 28), scale_to_size_H96(D,C4)])
        # slot_button_3_5.grid(row=3, column=5, padx=1, pady=8)
        slot_button_3_5.place(x=(47 + (57 * 4)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_5)

        slot_button_3_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 29), scale_to_size_H96(C,C4)])
        # slot_button_3_6.grid(row=3, column=6, padx=1, pady=8)
        slot_button_3_6.place(x=(47 + (57 * 5)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_6)

        slot_button_3_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 30), scale_to_size_H96(B,C4)])
        # slot_button_3_7.grid(row=3, column=6, padx=1, pady=8)
        slot_button_3_7.place(x=(47 + (57 * 6)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_7)

        slot_button_3_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A4", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 31), scale_to_size_H96(A,C4)])
        # slot_button_3_8.grid(row=3, column=6, padx=1, pady=8)
        slot_button_3_8.place(x=(47 + (57 * 7)), y=(66 + (51 * 3)))
        self.slot_buttons_1.append(slot_button_3_8)

        slot_button_3_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 32), scale_to_size_H96(H,C5)])
        # slot_button_3_9.grid(row=3, column=6, padx=1, pady=8)
        slot_button_3_9.place(x=47, y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_3_9)

        slot_button_3_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 33), scale_to_size_H96(G,C5)])
        # slot_button_3_10.grid(row=3, column=10, padx=1, pady=8)
        slot_button_3_10.place(x=(47 + (57 * 1)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_3_10)

        slot_button_3_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 34), scale_to_size_H96(F,C5)])
        # slot_button_3_11.grid(row=3, column=11, padx=1, pady=8)
        slot_button_3_11.place(x=(47 + (57 * 2)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_3_11)

        slot_button_3_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 35), scale_to_size_H96(E,C5)])
        # slot_button_3_12.grid(row=3, column=12, padx=1, pady=8)
        slot_button_3_12.place(x=(47 + (57 * 3)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_3_12)

        # row 4
        slot_button_4_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 36), scale_to_size_H96(D,C5)])
        # slot_button_4_1.grid(row=4, column=1, padx=1, pady=8)
        slot_button_4_1.place(x=(47 + (57 * 4)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_4_1)

        slot_button_4_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 37), scale_to_size_H96(C,C5)])
        # slot_button_4_2.grid(row=4, column=2, padx=1, pady=8)
        slot_button_4_2.place(x=(47 + (57 * 5)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_4_2)

        slot_button_4_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 38), scale_to_size_H96(B,C5)])
        # slot_button_4_3.grid(row=4, column=3, padx=1, pady=8)
        slot_button_4_3.place(x=(47 + (57 * 6)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_4_3)

        slot_button_4_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A5", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 39), scale_to_size_H96(A,C5)])
        # slot_button_4_4.grid(row=4, column=4, padx=1, pady=8)
        slot_button_4_4.place(x=(47 + (57 * 7)), y=(66 + (51 * 4)))
        self.slot_buttons_1.append(slot_button_4_4)

        slot_button_4_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 40), scale_to_size_H96(H,C6)])
        # slot_button_4_5.grid(row=4, column=5, padx=1, pady=8)
        slot_button_4_5.place(x=47, y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_5)

        slot_button_4_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 41), scale_to_size_H96(G,C6)])
        # slot_button_4_6.grid(row=4, column=6, padx=1, pady=8)
        slot_button_4_6.place(x=(47 + (57 * 1)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_6)

        slot_button_4_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 42), scale_to_size_H96(F,C6)])
        # slot_button_4_7.grid(row=4, column=7, padx=1, pady=8)
        slot_button_4_7.place(x=(47 + (57 * 2)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_7)

        slot_button_4_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 43), scale_to_size_H96(E,C6)])
        # slot_button_4_8.grid(row=4, column=8, padx=1, pady=8)
        slot_button_4_8.place(x=(47 + (57 * 3)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_8)

        slot_button_4_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 44), scale_to_size_H96(D,C6)])
        # slot_button_4_9.grid(row=4, column=9, padx=1, pady=8)
        slot_button_4_9.place(x=(47 + (57 * 4)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_9)

        slot_button_4_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 45), scale_to_size_H96(C,C6)])
        # slot_button_4_10.grid(row=4, column=10, padx=1, pady=8)
        slot_button_4_10.place(x=(47 + (57 * 5)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_10)

        slot_button_4_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 46), scale_to_size_H96(B,B6)])
        # slot_button_4_11.grid(row=4, column=11, padx=1, pady=8)
        slot_button_4_11.place(x=(47 + (57 * 6)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_11)

        slot_button_4_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A6", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 47), scale_to_size_H96(A,C6)])
        # slot_button_4_12.grid(row=4, column=12, padx=1, pady=8)
        slot_button_4_12.place(x=(47 + (57 * 7)), y=(66 + (51 * 5)))
        self.slot_buttons_1.append(slot_button_4_12)

        # row 5
        slot_button_5_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 48), scale_to_size_H96(H,C7)])
        # slot_button_5_1.grid(row=5, column=1, padx=1, pady=8)
        slot_button_5_1.place(x=47, y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_1)

        slot_button_5_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 49), scale_to_size_H96(G,C7)])
        # slot_button_5_2.grid(row=5, column=2, padx=1, pady=8)
        slot_button_5_2.place(x=(47 + (57 * 1)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_2)

        slot_button_5_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 50), scale_to_size_H96(F,C7)])
        # slot_button_5_3.grid(row=5, column=3, padx=1, pady=8)
        slot_button_5_3.place(x=(47 + (57 * 2)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_3)

        slot_button_5_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 51), scale_to_size_H96(E,C7)])
        # slot_button_5_4.grid(row=5, column=4, padx=1, pady=8)
        slot_button_5_4.place(x=(47 + (57 * 3)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_4)

        slot_button_5_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 52), scale_to_size_H96(D,C7)])
        # slot_button_5_5.grid(row=5, column=5, padx=1, pady=8)
        slot_button_5_5.place(x=(47 + (57 * 4)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_5)

        slot_button_5_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 53), scale_to_size_H96(C,C7)])
        # slot_button_5_6.grid(row=5, column=6, padx=1, pady=8)
        slot_button_5_6.place(x=(47 + (57 * 5)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_6)

        slot_button_5_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 54), scale_to_size_H96(B,C7)])
        # slot_button_5_7.grid(row=5, column=7, padx=1, pady=8)
        slot_button_5_7.place(x=(47 + (57 * 6)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_7)

        slot_button_5_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A7", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 55), scale_to_size_H96(A,C7)])
        # slot_button_5_8.grid(row=5, column=8, padx=1, pady=8)
        slot_button_5_8.place(x=(47 + (57 * 7)), y=(66 + (51 * 6)))
        self.slot_buttons_1.append(slot_button_5_8)

        slot_button_5_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 56), scale_to_size_H96(H,C8)])
        # slot_button_5_9.grid(row=5, column=9, padx=1, pady=8)
        slot_button_5_9.place(x=47, y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_5_9)

        slot_button_5_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 57), scale_to_size_H96(G,C8)])
        # slot_button_5_10.grid(row=5, column=10, padx=1, pady=8)
        slot_button_5_10.place(x=(47 + (57 * 1)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_5_10)

        slot_button_5_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 58), scale_to_size_H96(F,C8)])
        # slot_button_5_11.grid(row=5, column=11, padx=1, pady=8)
        slot_button_5_11.place(x=(47 + (57 * 2)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_5_11)

        slot_button_5_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 59), scale_to_size_H96(E,C8)])
        # slot_button_5_12.grid(row=5, column=12, padx=1, pady=8)
        slot_button_5_12.place(x=(47 + (57 * 3)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_5_12)

        # row 6
        slot_button_6_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 60), scale_to_size_H96(D,C8)])
        # slot_button_6_1.grid(row=6, column=1, padx=1, pady=8)
        slot_button_6_1.place(x=(47 + (57 * 4)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_6_1)

        slot_button_6_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 61), scale_to_size_H96(C,C8)])
        # slot_button_6_2.grid(row=6, column=2, padx=1, pady=8)
        slot_button_6_2.place(x=(47 + (57 * 5)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_6_2)

        slot_button_6_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 62), scale_to_size_H96(B,C8)])
        # slot_button_6_3.grid(row=6, column=3, padx=1, pady=8)
        slot_button_6_3.place(x=(47 + (57 * 6)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_6_3)

        slot_button_6_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A8", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 63), scale_to_size_H96(A,C8)])
        # slot_button_6_4.grid(row=6, column=4, padx=1, pady=8)
        slot_button_6_4.place(x=(47 + (57 * 7)), y=(66 + (51 * 7)))
        self.slot_buttons_1.append(slot_button_6_4)

        slot_button_6_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 64), scale_to_size_H96(H,C9)])
        # slot_button_6_5.grid(row=6, column=5, padx=1, pady=8)
        slot_button_6_5.place(x=47, y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_5)

        slot_button_6_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 65), scale_to_size_H96(G,C9)])
        # slot_button_6_6.grid(row=6, column=6, padx=1, pady=8)
        slot_button_6_6.place(x=(47 + (57 * 1)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_6)

        slot_button_6_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 66), scale_to_size_H96(F,C9)])
        # slot_button_6_7.grid(row=6, column=7, padx=1, pady=8)
        slot_button_6_7.place(x=(47 + (57 * 2)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_7)

        slot_button_6_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 67), scale_to_size_H96(E,C9)])
        # slot_button_6_8.grid(row=6, column=8, padx=1, pady=8)
        slot_button_6_8.place(x=(47 + (57 * 3)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_8)

        slot_button_6_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 68), scale_to_size_H96(D,C9)])
        # slot_button_6_9.grid(row=6, column=9, padx=1, pady=8)
        slot_button_6_9.place(x=(47 + (57 * 4)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_9)

        slot_button_6_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 69), scale_to_size_H96(C,C9)])
        # slot_button_6_10.grid(row=6, column=10, padx=1, pady=8)
        slot_button_6_10.place(x=(47 + (57 * 5)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_10)

        slot_button_6_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 70), scale_to_size_H96(B,C9)])
        # slot_button_6_11.grid(row=6, column=11, padx=1, pady=8)
        slot_button_6_11.place(x=(47 + (57 * 6)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_11)

        slot_button_6_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A9", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 71), scale_to_size_H96(A,C9)])
        # slot_button_6_12.grid(row=6, column=12, padx=1, pady=8)
        slot_button_6_12.place(x=(47 + (57 * 7)), y=(66 + (51 * 8)))
        self.slot_buttons_1.append(slot_button_6_12)

        # row 7
        slot_button_7_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 72), scale_to_size_H96(H,C10)])
        # slot_button_7_1.grid(row=7, column=1, padx=1, pady=8)
        slot_button_7_1.place(x=47, y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_1)

        slot_button_7_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 73), scale_to_size_H96(G,C10)])
        # slot_button_7_2.grid(row=7, column=2, padx=1, pady=8)
        slot_button_7_2.place(x=(47 + (57 * 1)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_2)

        slot_button_7_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 74), scale_to_size_H96(F,C10)])
        # slot_button_7_3.grid(row=7, column=3, padx=1, pady=8)
        slot_button_7_3.place(x=(47 + (57 * 2)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_3)

        slot_button_7_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 75), scale_to_size_H96(E,C10)])
        # slot_button_7_4.grid(row=7, column=4, padx=1, pady=8)
        slot_button_7_4.place(x=(47 + (57 * 3)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_4)

        slot_button_7_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 76), scale_to_size_H96(D,C10)])
        # slot_button_7_5.grid(row=7, column=5, padx=1, pady=8)
        slot_button_7_5.place(x=(47 + (57 * 4)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_5)

        slot_button_7_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 77), scale_to_size_H96(C,C10)])
        # slot_button_7_6.grid(row=7, column=6, padx=1, pady=8)
        slot_button_7_6.place(x=(47 + (57 * 5)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_6)

        slot_button_7_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 78), scale_to_size_H96(B,C10)])
        # slot_button_7_7.grid(row=7, column=7, padx=1, pady=8)
        slot_button_7_7.place(x=(47 + (57 * 6)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_7)

        slot_button_7_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A10", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 79), scale_to_size_H96(A,C10)])
        # slot_button_7_8.grid(row=7, column=8, padx=1, pady=8)
        slot_button_7_8.place(x=(47 + (57 * 7)), y=(66 + (51 * 9)))
        self.slot_buttons_1.append(slot_button_7_8)

        slot_button_7_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 80), scale_to_size_H96(H,C11)])
        # slot_button_7_9.grid(row=7, column=9, padx=1, pady=8)
        slot_button_7_9.place(x=47, y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_7_9)

        slot_button_7_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 81), scale_to_size_H96(G,C11)])
        # slot_button_7_10.grid(row=7, column=10, padx=1, pady=8)
        slot_button_7_10.place(x=(47 + (57 * 1)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_7_10)

        slot_button_7_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 82), scale_to_size_H96(F,C11)])
        # slot_button_7_11.grid(row=7, column=11, padx=1, pady=8)
        slot_button_7_11.place(x=(47 + (57 * 2)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_7_11)

        slot_button_7_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 83), scale_to_size_H96(E,C11)])
        # slot_button_7_12.grid(row=7, column=12, padx=1, pady=8)
        slot_button_7_12.place(x=(47 + (57 * 3)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_7_12)

        # row 8
        slot_button_8_1 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 84), scale_to_size_H96(D,C11)])
        # slot_button_8_1.grid(row=8, column=1, padx=1, pady=8)
        slot_button_8_1.place(x=(47 + (57 * 4)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_8_1)

        slot_button_8_2 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 85), scale_to_size_H96(C,C11)])
        # slot_button_8_2.grid(row=8, column=2, padx=1, pady=8)
        slot_button_8_2.place(x=(47 + (57 * 5)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_8_2)

        slot_button_8_3 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 86), scale_to_size_H96(B,C11)])
        # slot_button_8_3.grid(row=8, column=3, padx=1, pady=8)
        slot_button_8_3.place(x=(47 + (57 * 6)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_8_3)

        slot_button_8_4 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A11", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 87), scale_to_size_H96(A,C11)])
        # slot_button_8_4.grid(row=8, column=4, padx=1, pady=8)
        slot_button_8_4.place(x=(47 + (57 * 7)), y=(66 + (51 * 10)))
        self.slot_buttons_1.append(slot_button_8_4)

        slot_button_8_5 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="H12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 88), scale_to_size_H96(H,C12)])
        # slot_button_8_5.grid(row=8, column=5, padx=1, pady=8)
        slot_button_8_5.place(x=47, y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_5)

        slot_button_8_6 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="G12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 89), scale_to_size_H96(G,C12)])
        # slot_button_8_6.grid(row=8, column=6, padx=1, pady=8)
        slot_button_8_6.place(x=(47 + (57 * 1)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_6)

        slot_button_8_7 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="F12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 90), scale_to_size_H96(F,C12)])
        # slot_button_8_7.grid(row=8, column=7, padx=1, pady=8)
        slot_button_8_7.place(x=(47 + (57 * 2)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_7)

        slot_button_8_8 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="E12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 91), scale_to_size_H96(E,C12)])
        # slot_button_8_8.grid(row=8, column=8, padx=1, pady=8)
        slot_button_8_8.place(x=(47 + (57 * 3)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_8)

        slot_button_8_9 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="D12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 92), scale_to_size_H96(D,C12)])
        # slot_button_8_9.grid(row=8, column=9, padx=1, pady=8)
        slot_button_8_9.place(x=(47 + (57 * 4)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_9)

        slot_button_8_10 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="C12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 93), scale_to_size_H96(C,C12)])
        # slot_button_8_10.grid(row=8, column=10, padx=1, pady=8)
        slot_button_8_10.place(x=(47 + (57 * 5)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_10)

        slot_button_8_11 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="B12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 94), scale_to_size_H96(B,C12)])
        # slot_button_8_11.grid(row=8, column=11, padx=1, pady=8)
        slot_button_8_11.place(x=(47 + (57 * 6)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_11)

        slot_button_8_12 = customtkinter.CTkButton(
            master=self.well_96_3_frame, text="A12", fg_color="blue", text_color=(
                "gray10", "#DCE4EE"), height=30, width=30, command=lambda: [
                self.toggle_well(
                    0, 95), scale_to_size_H96(A,C12)])
        # slot_button_8_12.grid(row=8, column=12, padx=1, pady=8)
        slot_button_8_12.place(x=(47 + (57 * 7)), y=(66 + (51 * 11)))
        self.slot_buttons_1.append(slot_button_8_12)

        # Brings pop-up window to front
        slot_popup.attributes("-topmost", True)
        print("slot_96well_3_button_event click")

# selection of culture vessels
    def select_all_slots_btn(self):
        self.slot_96well_3_button_event()
        self.slot_96well_2_button_event()
        #self.slot_petri_button_event()

# for petri dish
    #def toggle_well_petri(self, i, j):
        # Toggle selected well
        #if (i, j) in self.selected_wells:
            #self.selected_wells.discard((i, j))
            # Reset color
            #self.slot_buttons[i * 2 + j].configure(fg_color="blue")
        #else:
            #self.selected_wells.add((i, j))
            # change color to indicate selection
            #self.slot_buttons[i * 2 + j].configure(fg_color="green")

    # toggle selected wells for vertical
    def toggle_btn(self, i, j):
        if (i, j) in self.selected_btn:
            self.selected_btn.discard((i, j))
            # Reset color
            self.btn_buttons[i * 12 + j].configure(fg_color="blue")
        else:
            self.selected_btn.add((i, j))
            # change color to indicate selection
            self.btn_buttons[i * 12 + j].configure(fg_color="green")

# toggle selected wells for horizontal
    def toggle_well(self, i, j):
        # Toggle the selected state of a well
        if (i, j) in self.selected_wells_1:
            self.selected_wells_1.discard((i, j))
            self.slot_buttons_1[i * 12 +
                               j].configure(fg_color="blue")  # Reset color
        else:
            self.selected_wells_1.add((i, j))
            # change color to indicate selection
            self.slot_buttons_1[i * 12 + j].configure(fg_color="green")

# for petri dish

    #def select_all_wells(self):
        # Select all wells
        #for i in range(8):
            #for j in range(12):
                #self.selected_wells.add((i, j))
                # Change color to indicate selection
                #self.slot_buttons[i * 12 + j].configure(fg_color="green")

    #def deselect_all_wells(self):
        # Deselect all wells
        #for i in range(8):
            #for j in range(12):
                #self.selected_wells.discard((i, j))
                #self.slot_buttons[i * 12 +
                                  #j].configure(fg_color="blue")  # Reset color


# for vertical 96 well plate

    def select_all_wells_1(self):
        # Select all wells
        for i in range(8):
            for j in range(12):
                self.selected_btn.add((i, j))
                # Change color to indicate selection
                self.btn_buttons[i * 12 + j].configure(fg_color="green")

    def deselect_all_wells_1(self):
        # Deselect all wells
        for i in range(8):
            for j in range(12):
                self.selected_btn.discard((i, j))
                # Reset color
                self.btn_buttons[i * 12 + j].configure(fg_color="blue")

# for horizontal 96 well plate
    def select_all_wells_2(self):
        # Select all wells
        for i in range(8):
            for j in range(12):
                self.selected_wells_1.add((i, j))
                # Change color to indicate selection
                self.slot_buttons_1[i * 12 + j].configure(fg_color="green")

    def deselect_all_wells_2(self):
        # Deselect all wells
        for i in range(8):
            for j in range(12):
                self.selected_wells_1.discard((i, j))
                self.slot_buttons_1[i * 12 +
                                    j].configure(fg_color="blue")  # Reset color


if __name__ == "__main__":
    app = App()
    app.mainloop()