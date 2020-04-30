from tkinter import *
from tkinter import ttk 
from tkinter import filedialog
from cui import *

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("WhatsApp Analyzer")
        self.geometry("300x200")
        self.option_add('*foreground', 'black')  # set all tk widgets' foreground to black
        self.option_add('*activeForeground', 'black')  # set all tk widgets' foreground to black

        self.labelFrame = ttk.LabelFrame(self, text = "Input Text File")
        self.labelFrame.grid(column = 1, row = 1, padx = 10, pady = 10)

        self.button()

        self.option = StringVar()
        self.option_2 = StringVar()
        self.option_3 = StringVar()
        self.option_4 = StringVar()
        self.filename = ""
        self.radiobutton(self.option, self.option_2, self.option_3, self.option_4)

    def popupmsg(self, msg, msg2 = "OPTION NOT SELECTED"):
        popup = Tk()
        popup.geometry("400x80")
        popup.wm_title(msg2)
        label = ttk.Label(popup, text=msg)
        label.pack(side="top", fill="x", pady=10)
        b1 = ttk.Button(popup, text="Okay", command=popup.destroy)
        b1.pack()
        popup.mainloop()
        

    def validate(self):
        value = self.option.get()
        value_2 = self.option_2.get()
        value_3 = self.option_3.get()
        value_4 = self.option_4.get()
        if self.filename == "":
            self.popupmsg("Select A WhatsApp Text File")
        else:
            output_path = self.filename[:-4] + ".csv"
            if value == "android" or value == "ios":
                if value == "android":
                    parsedData = get_data(self.filename, 0)
                elif value == "ios":
                    parsedData = get_data(self.filename, 1)
                df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
                df_, _ = remove_media(df)
                if value_2 == "remove_emoji":
                    df_ = remove_lines_with_only_emojis(df_)
                if value_3 == "gs":
                    if value_4 == "ss":
                        get_statistics(df,1)
                    else:
                        get_statistics(df,0)
                else:
                    self.popupmsg("", "Done!")
                df_.to_csv(output_path, index = False)
            else:
                self.popupmsg("Select Your Device's Operating Framework")

    def radiobutton(self, option, option_2, option_3, option_4):
        self.R1 = ttk.Radiobutton(self, text="Android", value="android", var=option)
        self.R2 = ttk.Radiobutton(self, text="IOS", value="ios", var=option)
        self.R3 = ttk.Radiobutton(self, text = "Remove Emojis", value= "remove_emoji", var=option_2)
        self.R4 = ttk.Radiobutton(self, text = "Get Statistics", value = "gs", var = option_3)
        self.R5 = ttk.Radiobutton(self, text = "Save Statistics", value = "ss", var = option_4)
        self.button = ttk.Button(self, text="Get CSV File", command=self.validate)
        self.R1.grid(column = 1, row = 2, padx = 5, pady = 5)
        self.R2.grid(column = 1, row = 3, padx = 5, pady = 5)
        self.R3.grid(column = 1, row = 4, padx = 5, pady = 5)
        self.R4.grid(column = 2, row = 2, padx = 5, pady = 5)
        self.R5.grid(column = 2, row = 3, padx = 5, pady = 5)
        self.button.grid(column = 1, row = 5, padx = 5, pady = 5)

        
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse File", command = self.fileDialog)
        self.button.grid(column = 3, row = 1)   

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir = "/", title = "Select The Text File", filetypes = (("txt", "*.txt"), ("All Files", "*.*")))
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure()

   
        
if __name__ == '__main__':
    my_gui = Root()
    my_gui.mainloop()