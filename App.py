from Main import main
import tkinter as tk

# create the main window
window = tk.Tk()
window.title("Planisuss")  # Change the title to "Planisuss"

# set up the background image
background_image_path = 'sfondo.png'
background_image = tk.PhotoImage(file=background_image_path)
background_label = tk.Label(window, image=background_image)
background_label.place(relwidth=1, relheight=1)  # use relative width and height to cover the entire window

# create a label for the title
title_label = tk.Label(window, text="Welcome to Planisuss", font=("Helvetica", 16))
title_label.pack(pady=40)  # Add some padding

# create a button to start the program
start_button = tk.Button(window, text="Start", command=main, padx=20, pady=10)
start_button.pack()

window.geometry("279x279")  # set the width and height of the window

# run the GUI
window.mainloop()