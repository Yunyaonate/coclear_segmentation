

import tkinter as tk
from tkinter import filedialog, Label, Frame
from PIL import Image, ImageTk, ImageDraw
import os

root = tk.Tk()
root.geometry("1200x800")
root.title("Simple Image Drawing Tool")

pen_color = "black"
pen_size = 5  # Default pen size
image_files = []
undo_stack = []
redo_stack = []
current_image_index = -1
image = None
draw = None

# Global variable for the zoom level
zoom_level = 1.0


def open_folder():
    global image_files, current_image_index,folder_path
    folder_path = filedialog.askdirectory()
    image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    current_image_index = 0
    show_image(current_image_index)

MAX_ZOOM_LEVEL = 3.0  # This will allow the image to be zoomed up to 3 times its original size

def zoom_in():
    global photo, image, zoom_level, canvas, MAX_ZOOM_LEVEL
    if zoom_level < MAX_ZOOM_LEVEL:
        zoom_level += 0.1
        new_size = (int(image.width * zoom_level), int(image.height * zoom_level))
        resized_image = image.resize(new_size, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(resized_image)
        canvas.delete("all")
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.config(scrollregion=canvas.bbox("all"))

# def zoom_in():
#     global photo, image, zoom_level, canvas
#     zoom_level += 0.1  # Increase the zoom level
#     new_size = (int(image.width * zoom_level), int(image.height * zoom_level))
#     resized_image = image.resize(new_size, Image.ANTIALIAS)
#     photo = ImageTk.PhotoImage(resized_image)
#     canvas.delete("all")
#     canvas.create_image(0, 0, image=photo, anchor="nw")
#     canvas.config(width=new_size[0], height=new_size[1])


# Update canvas configuration to use scrollregion
def update_canvas():
    global photo, canvas
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.config(scrollregion=canvas.bbox("all"))


# Update canvas configuration to use scrollregion
def update_canvas():
    global photo, canvas
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.config(scrollregion=canvas.bbox("all"))


def zoom_out():
    global photo, image, zoom_level, canvas
    zoom_level -= 0.1  # Decrease the zoom level
    # Ensure the zoom level does not go below 1
    zoom_level = max(zoom_level, 0.1)
    new_size = (int(image.width * zoom_level), int(image.height * zoom_level))
    resized_image = image.resize(new_size, Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(resized_image)
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.config(width=new_size[0], height=new_size[1])

def show_image(index):
    global image, photo, draw, file_path
    if 0 <= index < len(image_files):
        file_path = image_files[index]
        file_name = os.path.basename(file_path)
        file_name_label.config(text=f"File: {file_name}")  # Update status bar
        image = Image.open(file_path).convert("RGB")
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.config(width=image.width, height=image.height)
        draw = ImageDraw.Draw(image)  # Create a drawing context
        canvas.delete("all")  # Clear the canvas
        canvas.create_image(0, 0, image=photo, anchor="nw")
    else:
        print("No more images in the folder.")

def show_previous_image():
    global current_image_index
    undo_stack.clear()
    redo_stack.clear()
    if current_image_index > 0:
        current_image_index -= 1
        show_image(current_image_index)

def show_next_image():
    global current_image_index
    undo_stack.clear()
    redo_stack.clear()
    if current_image_index < len(image_files) - 1:
        current_image_index += 1
        show_image(current_image_index)

def make_backup():
    global image, undo_stack
    if image:
        # Save the current state of the image
        undo_stack.append(image.copy())
        # Clear the redo stack whenever a new action is performed
        redo_stack.clear()

def undo():
    global image, photo, draw, canvas, undo_stack, redo_stack
    if undo_stack:
        # Push the current state to the redo stack
        redo_stack.append(image.copy())
        # Pop the last saved state from the undo stack and make it the current image
        image = undo_stack.pop()
        draw = ImageDraw.Draw(image)
        photo = ImageTk.PhotoImage(image)
        update_canvas()

def redo():
    global image, photo, draw, canvas, undo_stack, redo_stack
    if redo_stack:
        # Push the current state to the undo stack
        undo_stack.append(image.copy())
        # Pop the last undone state from the redo stack and make it the current image
        image = redo_stack.pop()
        draw = ImageDraw.Draw(image)
        photo = ImageTk.PhotoImage(image)
        update_canvas()

# def update_canvas():
#     global photo, canvas
#     canvas.delete("all")
#     canvas.create_image(0, 0, image=photo, anchor="nw")

# Update canvas configuration to use scrollregion
def update_canvas():
    global photo, canvas
    canvas.delete("all")
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.config(scrollregion=canvas.bbox("all"))

def use_black_pen():
    global pen_color
    pen_color = "black"

def use_white_pen():
    global pen_color
    pen_color = "white"

def set_pen_size(size):
    global pen_size
    pen_size = int(size)  # Convert the size to an integer


def draw_on_image(event):
    make_backup()
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline=pen_color)
    if draw:
        draw.ellipse([x1, y1, x2, y2], fill=pen_color)


def save_image():
    global image, folder_path
    if image:
        # Get the parent directory of the original file
        parent_dir = os.path.dirname(folder_path)
        # Create a new directory name "edited_filtered" within the parent directory
        save_dir = os.path.join(parent_dir, "edited_filtered")
        
        # If the directory does not exist, create it
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        # Construct the new file path within the "edited_filtered" directory
        save_path = os.path.join(save_dir, os.path.basename(file_path))
        
        # Save the image to the new file path
        image.save(save_path, 'PNG')
        print(f"Image saved to {save_path}")


canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Create a status bar at the bottom of the window to display file name
status_bar = Frame(root, height=20, bg='grey')
status_bar.pack(side=tk.TOP, fill=tk.X)
file_name_label = Label(status_bar, text='No image loaded', bg='grey')
file_name_label.pack(side=tk.LEFT)


# Update open button to call open_folder
open_button = tk.Button(root, text="Open Folder", command=open_folder)
open_button.pack(side=tk.LEFT)

# Add previous and next buttons
prev_button = tk.Button(root, text="Previous Image", command=show_previous_image)
prev_button.pack(side=tk.LEFT)

next_button = tk.Button(root, text="Next Image", command=show_next_image)
next_button.pack(side=tk.LEFT)

black_pen_button = tk.Button(root, text="Black Pen", command=use_black_pen)
black_pen_button.pack(side=tk.LEFT)

white_pen_button = tk.Button(root, text="White Pen", command=use_white_pen)
white_pen_button.pack(side=tk.LEFT)

# Add Undo and Redo buttons 
undo_button = tk.Button(root, text="Undo", command=undo)
undo_button.pack(side=tk.LEFT)

redo_button = tk.Button(root, text="Redo", command=redo)
redo_button.pack(side=tk.LEFT)

# Add zoom in and zoom out buttons to your GUI
zoom_in_button = tk.Button(root, text="Zoom In", command=zoom_in)
zoom_in_button.pack(side=tk.LEFT)

zoom_out_button = tk.Button(root, text="Zoom Out", command=zoom_out)
zoom_out_button.pack(side=tk.LEFT)

# Create scrollbars and configure them to work with the canvas
hbar = tk.Scrollbar(root, orient=tk.HORIZONTAL)
hbar.pack(side=tk.BOTTOM, fill=tk.X)
vbar = tk.Scrollbar(root, orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT, fill=tk.Y)

hbar.config(command=canvas.xview)
vbar.config(command=canvas.yview)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

# Make sure to pack the Scale widget with the correct settings
pen_size_slider = tk.Scale(root, from_=1, to=50, orient='horizontal', command=set_pen_size)
pen_size_slider.set(pen_size)  # Initialize the pen size
pen_size_slider.pack(side=tk.LEFT)

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(side=tk.LEFT)

canvas.bind("<B1-Motion>", draw_on_image)

root.mainloop()
