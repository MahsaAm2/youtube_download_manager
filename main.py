from pytube import YouTube
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
import re
import threading


class Application:
    def __init__(self, root):
        self.root = root
        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.config(bg="#ffdddd")

        top_label = Label(self.root, text="Youtube Download Manager", foreground="#99A3A4", font=("type zero", 70), background="#ffdddd")
        top_label.grid(pady=(0, 10))

        link_label = Label(self.root, text="Please enter any youtube video link blow", font=('type zero', 30), background="#ffdddd", foreground="#99A3A4")
        link_label.grid(pady=(0, 20))

        self.youtubeEntryVar = StringVar()
        self.youtubeEntry = Entry(self.root, width=70, textvariable=self.youtubeEntryVar, font=('Agency fb', 25), foreground="#F54077")
        self.youtubeEntry.grid(pady=(0, 15), ipady=2)

        self.youtubeEntryError = Label(self.root, text="", font=('Concert One', 20), background="#ffdddd")
        self.youtubeEntryError.grid(pady=(0, 8))

        self.youtubeFileSaveLabel = Label(self.root, text="Choose directory", font=("Concert One", 30),foreground="#99A3A4", background="#ffdddd")
        self.youtubeFileSaveLabel.grid()

        self.youtubeFileDirBtn = Button(self.root, text="Directory", font=("Bell Mt", 15), command=self.openDir, foreground="#F54077")
        self.youtubeFileDirBtn.grid(pady=(10, 3))

        self.fileLocLabel = Label(self.root, text="", font=("Freestyle Script", 25), background="#ffdddd")
        self.fileLocLabel.grid()

        self.youtubeChooseLabel = Label(self.root, text="Choose the download type", font=("Variety", 30), background="#ffdddd", foreground="#99A3A4")
        self.youtubeChooseLabel.grid()

        self.downloadChoices = [("Audio Mp3", 1), ("Video Mp4", 2)]
        self.ChoiceVar = StringVar()
        self.ChoiceVar.set(1)
        for text, mode in self.downloadChoices:
            self.youtubeChoices = Radiobutton(self.root, text=text, font=("Northwest old", 15), variable=self.ChoiceVar, value=mode, background="#ffdddd", foreground="#F54077")
            self.youtubeChoices.grid()

        self.downloadBtn = Button(self.root, text="Download", width=10, font=("Bell MT", 15), command=self.checkyoutubelink, foreground="#F54077")
        self.downloadBtn.grid(pady=(0, 5))



    def openDir(self):
        self.folderName = filedialog.askdirectory()
        if (len(self.folderName) > 0):
            self.fileLocLabel.config(text=self.folderName, fg="green")
            return True
        else:
           self.fileLocLabel.config(text="Please choose a directory", fg="red")

    def checkyoutubelink(self):
        self.matchlink = re.match("^https://www.youtube.com/.", self.youtubeEntryVar.get())
        if (not self.matchlink):
            self.youtubeEntryError.config(text="Invalid youtube link", foreground="red")
        elif(not self.openDir):
            self.fileLocLabel.config(text="Please choose a directory", foreground="red")
        elif(self.matchlink and self.openDir):
            self.downloadWin()


    def downloadWin(self):
        self.newWin = Toplevel(self.root)
        self.root.withdraw()
        self.newWin.state("zoomed")
        self.newWin.grid_rowconfigure(0, weight=0)
        self.newWin.grid_columnconfigure(0, weight=1)
        self.app = secondApp(self.newWin, self.youtubeEntryVar.get(), self.folderName, self.ChoiceVar.get())



class secondApp():
    def __init__(self, downloadWin, youtubeLink, folderName, choices):
        self.downloadWin = downloadWin
        self.youtubeLink = youtubeLink
        self.folderName = folderName
        self.choices = choices
        self.yt = YouTube(self.youtubeLink)
        if (choices==1):
            self.video_type = self.yt.streams.filter(only_audio=True).first()
            self.maxFileSize = self.video_type.filesize
        if (choices==2):
            self.video_type = self.yt.streams.first()
            self.maxFileSize = self.video_type.filesize
        self.loadingLabel = Label(self.downloadWin, text="Downloading in progress...", font=("Small Fonts", 40))
        self.loadingLabel.grid(pady=(100, 0))

        self.loadingPercent = Label(self.downloadWin, text="0", foreground="green", font=("Agency Fb", 40))
        self.loadingPercent.grid(pady=(50, 5))

        self.progressbar = ttk.Progressbar(self.downloadWin, length=500, orient='horizontal', mode='indeterminate')
        self.progressbar.grid(pady=(50, 0))

        self.progressbar.start()

        threading.Thread(target=self.yt.register_on_progress_callback(self.show_progress)).start()
        threading.Thread(target=self.downloadFile).start()

    def downloadFile(self):
        if(self.choices==1):
            self.yt.streams.filter(only_audio=True).first().download(self.folderName)
        if(self.choices==2):
            self.yt.streams.first().download(self.folderName)

    def show_progress(self, streams = None, Chunks=None, filehandle = None, byte_remaining=None ):
        self.percentCount = float("%0.2f" % (100-(100*(byte_remaining/self.maxFileSize))))
        if(self.percentCount < 100):
            self.loadingPercent.config(text=self.percentCount)
        else:
            self.progressbar.stop()
            self.loadingLabel.grid_forget()
            self.progressbar.grid_forget()
            self.downloadFinished = Label(self.downloadWin, text="Download finished", font=("Agency Fb",30))
            self.downloadFinished.grid(pady=(150, 0))

            self.downloadLoc = Label(self.downloadWin, text=self.yt.title, font=("Terminal", 30))
            self.downloadLoc.grid(pady=(50, 0))

            MB = float("%0.2f" % (self.maxFileSize/1000000))
            self.downloadFileSize = Label(self.downloadWin, text=str(MB), font=("Agency Fb", 30))
            self.downloadFileSize.grid(pady=(50, 0))




if __name__ == "__main__":
    win = Tk()
    win.title('Youtube Download Manager')
    win.state("zoomed")

    app = Application(win)
    mainloop()

