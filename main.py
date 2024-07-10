from tkinter import *
from tkinter import Image, filedialog, messagebox, colorchooser, StringVar
from PIL import Image, ImageTk, ImageDraw, ImageFont
import cv2
import ttkbootstrap as ttk


# ------------- Functions -------------

def displayimage(edge):
    dispimage = ImageTk.PhotoImage(edge)
    label.configure(image=dispimage)
    label.image = dispimage


def open_file_fun():
    global file_path
    global edge
    global img
    global tk_edge
    global label
    global edge_width
    global edge_height
    global x, y
    file_path = filedialog.askopenfilename()
    img = cv2.imread(file_path)
    # Converts BGR to RGB, otherwise the images would have a blue filter over them
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    edge = Image.fromarray(img_rgb)
    edge.thumbnail((2000, 2000))
    tk_edge = ImageTk.PhotoImage(edge, size=(2000, 2000))
    label = Label(canvas, image=tk_edge)
    label.place(relx=0.5, rely=0.5, anchor=CENTER)
    add_text_entry()

    edge_width = edge.width
    edge_height = edge.height
    x, y = int(edge_width / 2), int(edge_height / 2)


def savefile():
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
    if not filename:
        return
    edge.save(filename)
    messagebox.showinfo("Success", "Image uploaded successfully!")


def add_text_entry():
    add_file_btn.pack(side=LEFT)
    add_text_button.pack(side=LEFT)
    save_file_btn.place(relx=1.0, y=0, anchor="ne")


def color_code():
    global color_
    color_ = colorchooser.askcolor(title="Choose color")


def add_text_btn():
    global entry
    global dropdown_fonts
    global drp
    add_text_button.pack_forget()
    open_popup()


def add_text():
    global edge
    d1 = ImageDraw.Draw(edge)
    font = ImageFont.truetype("arial.ttf", size=int(value_inside.get()))
    d1.text((x, y), text=entry.get(), fill=color_[0], font=font, anchor="ms")
    displayimage(edge)
    top.destroy()
    add_text_button.pack()


def open_popup():
    global top
    global button_color
    global color_button
    global ok_button
    global entry
    global options_list
    global value_inside
    global question_menu
    top = Toplevel(window)
    top.geometry("750x700")
    top.title("Add Text")
    button_color = Button(top, text='color', command=color_code)

    top_label = Label(top, text='Insert Text:', font='Calibri 15')
    top_label.pack(pady=10)
    entry = Entry(top, font='Calibri 15')
    entry.pack(pady=10)
    top_label = Label(top, text='Choose Text Color:', font='Calibri 15')
    top_label.pack(pady=10)
    color_button = Button(top, text='Text color', font='Calibri 15', command=color_code)
    color_button.pack(pady=10)
    ok_button = Button(top, text='Ok', font=f'Calibri 15', command=add_text)
    ok_button.pack(pady=10, side=BOTTOM)
    top.attributes('-topmost', True)
    size_label = Label(top, text='Choose Text Size:', font='Calibri 15')
    size_label.pack(pady=10)

    options_list = [i for i in range(1, 201)]
    value_inside = StringVar(top)
    value_inside.set("Select an Option")
    question_menu = ttk.Combobox(top, textvariable=value_inside, values=options_list, font='Calibri 15')
    question_menu.pack(pady=10)


# ------------- UI -------------


window = ttk.Window(themename="darkly")
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state("zoomed")
window.title("Watermarking Images")


canvas = Canvas(window)
canvas.pack(fill='both', expand=True, side=LEFT)


buttons_frame = Frame(canvas)
buttons_frame.pack()


add_file_btn = Button(buttons_frame, text='Add image', font='Calibri 15', command=open_file_fun)
add_file_btn.pack()


add_text_button = Button(buttons_frame, text='Add text', font='Calibri 15', command=add_text_btn)


save_file_btn = Button(canvas, text='Save', font='Calibri 15', command=savefile)


close_window = Button(canvas, text='Close', font='Calibri 15', command=window.destroy)
close_window.place(relx=0, y=0, anchor="nw")


window.mainloop()
