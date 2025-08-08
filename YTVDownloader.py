from pytubefix import YouTube
from tkinter import *
from tkinter import ttk, messagebox,filedialog

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize or 1
    bytes_downloaded = total_size - bytes_remaining
    percent = int((bytes_downloaded / total_size) * 100)

    progress_var.set(percent)
    progress_label.config(text=f"{percent}% downloaded")
    window.update_idletasks()

def download_video():
    url = link.get()
    choice = format_choice.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link!")
        return
    download_btn.config(text="Downloading...", state=DISABLED)  
    status_label.config(text="Downloading...")
    window.update_idletasks()
    try:
        yt = YouTube(url,on_progress_callback=on_progress)
        save_path = filedialog.askdirectory()
        if not save_path:
            status_label.config(text="Download failed!")
            download_btn.config(text="Download", state=NORMAL)
            return
        if choice =="Video":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(only_audio=True).first()
        stream.download(output_path=save_path)
        status_label.config(text= "Download completed!")
        messagebox.showinfo("Success", "Download completed!")

    except Exception as e:
        status_label.config(text=" Download failed!")
        messagebox.showerror("Error", f"Something went wrong:\n{str(e)}")

    download_btn.config(text="Download", state=NORMAL)

# GUI Setup
window = Tk()
window.title("YouTube Video Downloader By Harsh Saini")
window.geometry("600x300")
window.resizable(False, False)

Label(window, text="Enter YouTube Video URL:", font=("Arial", 14)).pack(pady=15)
link = StringVar()
Entry(window, textvariable=link, width=50, font=("Arial", 12)).pack()

format_choice = StringVar(value="Video")
Radiobutton(window, text="📹 Video", variable=format_choice, value="Video", font=("Arial", 12)).pack()
Radiobutton(window, text="🎵 Audio", variable=format_choice, value="Audio", font=("Arial", 12)).pack()

download_btn = Button(window, text="Download", command=download_video, font=("Arial", 12), bg="#4CAF50", fg="white")
download_btn.pack(pady=20)

progress_var= IntVar()
progress_bar = ttk.Progressbar(window, length = 400, variable = progress_var, maximum = 100)
progress_bar.pack(pady= 10)

progress_label = Label(window, text="", font=("Arial", 12))
progress_label.pack()

status_label = Label(window, text="", font=("Arial", 12))
status_label.pack()

window.mainloop()


