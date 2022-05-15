import requests
from tkinter import *
import tkinter as tk

#This is a program that will take a text and send it to the quillbot AI and return the formated result to a new window



def get_text():
    # output text to new box and add a button to clear the text and to copy the text to clipboard
    # On clear button destroy the text box and create a new one
    # On copy button copy the text to clipboard
    # On close button destroy the window

    def copy_text():
        text.clipboard_clear()
        text.clipboard_append(text.get("1.0", "end-1c"))

    def close_window():
        window.destroy()

    window = tk.Tk()
    window.title("Quillbot")
    window.geometry("500x500")
    text = Text(window, width=50, height=10)
    text.pack()
    text.insert(tk.END, result)
    text.focus()
    button2 = tk.Button(window, text="Copy", command=copy_text)
    button2.pack()
    button3 = tk.Button(window, text="Close", command=close_window)
    button3.pack()
    window.mainloop()


def main():
    global value
    global result
    result = ''
    TEXT = t.get(1.0, "end-1c")
    s = requests.session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0"
    }

    abid = s.get("https://quillbot.com/", headers=headers)
    sid = s.post("https://quillbot.com/api/tracking", headers=headers)
    splitter_url= 'https://quillbot.com/api/utils/sentence-spiltter'
    cookies = {
        "abID": abid.cookies.values(),
        "authenticated": "false",
        "premium": "false",
        "acceptedPremiumModesTnc": "false",
        "connect.sid": sid.cookies.values(),
    }

    qdid = s.get("https://quillbot.com/api/auth/spam-check", headers=headers)
    #for each paragraph in TEXT get the sentences and send them to the server
    for paragraph in TEXT.split("\n"):
        url = f"https://quillbot.com/api/paraphraser/single-paraphrase/2?text={paragraph}&strength=2&autoflip=false&wikify=false&fthresh=-1&inputLang=en&quoteIndex=-2"
        x = s.get(url, headers=headers)
        response = x.json()
        paras3 = response["data"][0]["paras_3"]

        min = -1
        value = ""
        for i in paras3:
            if float(i["dist"]) > min:
                value = i["alt"]
                min = float(i["dist"])
                #add value to result
                result += value + "\n"
    print(result)
    get_text()


if __name__ == "__main__":

    root = Tk()
    root.title("GUI QUill Bout")
    root.geometry("1000x500")
    root.configure(background="black")
    label = Label(root, text="Enter Text", bg="black", fg="white", height=2)
    label.place()
    t = tk.Text(root, width=20, height=3)
    t.grid(column=1, row=15)
    t.pack(fill="both", expand=True, padx=10, pady=10)
    button = Button(root, text="Submit", command=main)
    button.pack()
    root.mainloop()
