import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from rembg import remove

import os
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class FGIsolationTool(customtkinter.CTk):
    def __init__(self,*args,**kwargs):
        super().__init__()
        self.title("Foreground Isolation Tool")
        self.geometry("800x600")
        self.configure(bg="EFEFEF")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        self.frame=customtkinter.CTkFrame(self,corner_radius=20, fg_color="transparent")

        img_path=os.path.join(os.path.dirname(__file__),"resources")
        self.logo = customtkinter.CTkImage(Image.open(os.path.join(img_path,"logo_w.png")),size=(200,180))
        self.ImgContainer = customtkinter.CTkLabel(self.frame,text="",image=self.logo)
        
        

        self.input_canvas=tk.Canvas(self.frame,width=300,height=300, bg="grey",highlightthickness=0)
        self.output_canvas=tk.Canvas(self.frame,width=300,height=300, bg="grey",highlightthickness=0)
        
        self.browse_btn=customtkinter.CTkButton(self,text="Select Image",text_color="black",fg_color="white",command=self.browse_image)


        self.frame.grid()
        self.ImgContainer.grid(row=0,column=0, pady=(0,20), columnspan=2, sticky ="nsew")

        self.input_canvas.grid(row=1,column=0,padx=15)
        self.output_canvas.grid(row=1,column=1 ,padx=15)
        
        self.browse_btn.grid(row=2,column=0,padx=15,pady=(0,30))
    

    def browse_image(self):
        file_path=filedialog.askopenfilename(filetypes=[])
        if file_path:
            self.file_path=file_path

        self.input_image=Image.open(self.file_path).resize((300,300))
        self.input_photo=ImageTk.PhotoImage(self.input_image)

        self.input_canvas.create_image(0,0,anchor=tk.NW, image=self.input_photo)
        self.browse_btn.configure(text="Isolate Foreground",command=self.isolate_FG,state='normal')

    def isolate_FG(self):
        output_path=filedialog.asksaveasfilename(defaultextension=".jpg",filetypes=[])
        if output_path:
            with open(self.file_path ,"rb") as i:
                with open(output_path,"wb") as o:
                    inputImg=i.read()
                    result=remove(inputImg)
                    o.write(result)
            self.output_image=Image.open(output_path).resize((300,300))

            self.output_photo =ImageTk.PhotoImage(self.output_image)
            self.output_canvas.create_image(0,0,anchor=tk.NW, image=self.output_photo)
            self.browse_btn.configure(text="Select Image",command=self.browse_image,state='normal')




if __name__=="__main__":
    app=FGIsolationTool()
    app.mainloop()
