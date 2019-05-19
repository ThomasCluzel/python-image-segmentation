#!/usr/bin/env python3
# coding: utf8

"""
This file contains the GUI.
"""

import os
import sys
import tempfile
from shutil import copyfile
from tkinter import Tk, Frame, Label, Entry, Button, Canvas, Text, Scale, StringVar, IntVar
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

from picture2avatar import main as picture2avatar_main


class Picture2AvatarGUI(Frame):
    """
    The window to display
    """
    OUTPUT_PATH = tempfile.gettempdir() + "/out.png" # temporary location of the generated picture

    def __init__(self, window, width=800, height=600, **kwargs):
        """
        Sets up all the widgets in the window
        """
        Frame.__init__(self, window, width=width, height=height, **kwargs)
        self.pack(fill="both")
        # Create the frames
        self.frame_input = Frame(self)
        self.frame_pictures = Frame(self)
        self.frame_message = Frame(self)
        self.frame_alg_pre = Frame(self)
        self.frame_alg_grow = Frame(self)
        self.frame_alg_clu = Frame(self)
        self.frame_alg_greed = Frame(self)
        self.frame_save_as = Frame(self)
        # Create the widgets
        self.label_input_path = Label(self.frame_input, text="Input image : ")
        self.str_input_path = StringVar()
        self.entry_input_path = Entry(self.frame_input, textvariable=self.str_input_path, width=50)
        self.button_browse_input_path = Button(self.frame_input, text="Browse", command=self.browse)
        self.canvas_input_image = Canvas(self.frame_pictures)
        self.input_image = self.canvas_input_image.create_image(0,0, anchor="nw")
        self.canvas_output_image = Canvas(self.frame_pictures)
        self.output_image = self.canvas_output_image.create_image(0,0, anchor="nw")
        self.label_message = Label(self.frame_message, text="")
        self.label_alg_pre = Label(self.frame_alg_pre, text="mask_length=")
        self.str_alg_pre_max_length = StringVar()
        self.scale_alg_pre_max_length = Entry(self.frame_alg_pre, textvariable=self.str_alg_pre_max_length, width=5)
        self.button_alg_pre_run = Button(self.frame_alg_pre, text="run pre", command=self.run_pre)
        self.label_alg_grow = Label(self.frame_alg_grow, text="maxgap=")
        self.str_alg_grow_maxgap = StringVar()
        self.scale_alg_grow_maxgap = Entry(self.frame_alg_grow, textvariable=self.str_alg_grow_maxgap, width=5)
        self.button_alg_grow_run = Button(self.frame_alg_grow, text="run grow", command=self.run_grow)
        self.label_alg_clu = Label(self.frame_alg_clu, text="nb_color_keep=")
        self.str_alg_clu_nb_color_keep = StringVar()
        self.scale_alg_clu_nb_color_keep = Entry(self.frame_alg_clu, textvariable=self.str_alg_clu_nb_color_keep, width=5)
        self.button_alg_clu_run = Button(self.frame_alg_clu, text="run clu", command=self.run_clu)
        self.label_alg_greed = Label(self.frame_alg_greed, text="nb_color_keep=")
        self.str_alg_greed_nb_color_keep = StringVar()
        self.scale_alg_greed_nb_color_keep = Entry(self.frame_alg_greed, textvariable=self.str_alg_greed_nb_color_keep, width=5)
        self.button_alg_greed_run = Button(self.frame_alg_greed, text="run greed", command=self.run_greed)
        self.button_save_as = Button(self.frame_save_as, text="Save output as", command=self.save_as)
        # Display the widgets in the window
        self.frame_input.pack(fill="x", expand=1)
        self.frame_pictures.pack(fill="x", expand=1)
        self.frame_message.pack(fill="x", expand=1)
        self.frame_alg_pre.pack(fill="x", expand=1)
        self.frame_alg_grow.pack(fill="x", expand=1)
        self.frame_alg_clu.pack(fill="x", expand=1)
        self.frame_alg_greed.pack(fill="x", expand=1)
        self.frame_save_as.pack(fill="x", expand=1)
        self.label_input_path.pack(side="left")
        self.entry_input_path.pack(side="left", fill="x")
        self.button_browse_input_path.pack(side="left")
        self.canvas_input_image.pack(side="left")
        self.canvas_output_image.pack(side="left")
        self.label_message.pack(fill="x")
        self.label_alg_pre.pack(side="left")
        self.scale_alg_pre_max_length.pack(side="left")
        self.button_alg_pre_run.pack(side="left")
        self.label_alg_grow.pack(side="left")
        self.scale_alg_grow_maxgap.pack(side="left")
        self.button_alg_grow_run.pack(side="left")
        self.label_alg_clu.pack(side="left")
        self.scale_alg_clu_nb_color_keep.pack(side="left")
        self.button_alg_clu_run.pack(side="left")
        self.label_alg_greed.pack(side="left")
        self.scale_alg_greed_nb_color_keep.pack(side="left")
        self.button_alg_greed_run.pack(side="left")
        self.button_save_as.pack(side="right")

    def destroy(self):
        """
        This method is called when the program is closed (because it is
        the main window). It removes temporary files.
        """
        Frame.destroy(self)
        try:
            os.remove(Picture2AvatarGUI.OUTPUT_PATH)
        except:
            pass # FileNotFoundError, we remove if it exists

    def browse(self):
        """
        This method is called when the user click the browse button to select an input picture.
        It opens a dialog box to select a file.
        """
        filename = filedialog.askopenfilename(initialdir=".", title="Select a picture",
            filetypes=(("all files","*.*"),("jpeg files","*.jpg"),("png files","*.png"),("bitmap files","*.bmp")))
        self.str_input_path.set(filename)
        img = None
        try:
            img = Image.open(filename)
        except IOError:
            messagebox.showerror("Error", "The file %s is not a picture." % filename, parent=self)
            return
        img = img.resize((400, 400*img.size[1]//img.size[0]))
        self.canvas_input_image["width"] = img.size[0]
        self.canvas_input_image["height"] = img.size[1]
        self.input_image_tk = ImageTk.PhotoImage(img) # Warning: we must keep a reference on the PhotoImage otherwise it is destroyed and nothing is displayed
        self.canvas_input_image.itemconfig(self.input_image, image=self.input_image_tk)

    def run_pre(self):
        """
        This method is called when the user click the "run pre" button.
        It runs the algorithm to perform the computation and then display the picture.
        """
        # parse the argument if any
        param = self.str_alg_pre_max_length.get()
        try:
            param = int(param) if param else 1
        except ValueError:
            messagebox.showerror("Error", "Please enter an integer value between 1 and 8.", parent=self)
            return
        if(not 1<=param<=8):
            messagebox.showerror("Error", "Please enter a value between 1 and 8.", parent=self)
            return
        self.label_message["text"] = "Processing input..."
        self.after_idle(callback_run, self, "pre", param)

    def run_grow(self):
        """
        This method is called when the user click the "run grow" button.
        It runs the algorithm to perform the computation and then display the picture.
        """
        # parse the argument if any
        param = self.str_alg_grow_maxgap.get()
        try:
            param = int(param) if param else 25
        except ValueError:
            messagebox.showerror("Error", "Please enter an integer value between 1 and 254.", parent=self)
            return
        if(not 1<=param<=254):
            messagebox.showerror("Error", "Please enter a value between 1 and 254.", parent=self)
            return
        self.label_message["text"] = "Processing input..."
        self.after_idle(callback_run, self, "grow", param)
    
    def run_clu(self):
        """
        This method is called when the user click the "run clu" button.
        It runs the algorithm to perform the computation and then display the picture.
        """
        # parse the argument if any
        param = self.str_alg_clu_nb_color_keep.get()
        try:
            param = int(param) if param else 15
        except ValueError:
            messagebox.showerror("Error", "Please enter an integer value greater than 1.", parent=self)
            return
        if(not 1<=param):
            messagebox.showerror("Error", "Please enter a value greater than 1.", parent=self)
            return
        self.label_message["text"] = "Processing input..."
        self.after_idle(callback_run, self, "clu", param)

    def run_greed(self):
        """
        This method is called when the user click the "run greed".
        It runs the algorithm to perform the computation and then display the picture.
        """
        # parse the argument if any
        param = self.str_alg_greed_nb_color_keep.get()
        try:
            param = int(param) if param else 10
        except ValueError:
            messagebox.showerror("Error", "Please enter an integer value greater than 1.", parent=self)
            return
        if(not 1<=param):
            messagebox.showerror("Error", "Please enter a value greater than 1.", parent=self)
            return
        self.label_message["text"] = "Processing input..."
        self.after_idle(callback_run, self, "greed", param)

    def save_as(self):
        """
        This method is called when the user press the save as button and prompts
        a dialog box for him to save the output image.
        """
        save_filename = filedialog.asksaveasfilename(initialdir=".", title="Select a file",
            filetypes=(("png files","*.png"),("jpeg files","*.jpg"),("bitmap files","*.bmp"),("all files","*.*")))
        if("." not in save_filename[-5:]): # give png as default extension if the file does not have any
            save_filename += ".png"
        try:
            copyfile(Picture2AvatarGUI.OUTPUT_PATH, save_filename)
        except:
            messagebox.showerror("Error", "The image could not be saved.", parent=self)


def callback_run(self, algorithm, param):
    """
    This function is to be called by run_*() methods of the GUI class to
    process input images outside the event loop. 
    """
    try:
        picture2avatar_main(self.str_input_path.get(), algorithm, Picture2AvatarGUI.OUTPUT_PATH, param)
    except:
        if(not self.str_input_path.get()):
            messagebox.showerror("Error", "Please, select a picture.", parent=self)
        else:
            messagebox.showerror("Error", "The picture cannot be openned.", parent=self)
        self.label_message["text"] = ""
        return
    # get the result
    img = None
    try:
        img = Image.open(Picture2AvatarGUI.OUTPUT_PATH)
    except IOError:
        messagebox.showerror("Error", "The output was not generated.", parent=self)
        self.label_message["text"] = ""
        return
    # display the result
    img = img.resize((400, 400*img.size[1]//img.size[0]))
    self.canvas_output_image["width"] = img.size[0]
    self.canvas_output_image["height"] = img.size[1]
    self.output_image_tk = ImageTk.PhotoImage(img) # to keep a reference
    self.canvas_output_image.itemconfig(self.output_image, image=self.output_image_tk)
    self.label_message["text"] = ""

def gui():
    """
    This function display the GUI.
    """
    # Create the window and its contents
    root = Tk()
    root.title("Picture2Avatar")
    root.iconbitmap("icon.ico")
    inter = Picture2AvatarGUI(root)
    # Show the window
    inter.mainloop()


if __name__ == "__main__":
    gui()
