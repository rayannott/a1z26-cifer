import customtkinter

import cifer

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("480x480")
app.title("A1Z26 cifer")

cfr = cifer.A1Z26Cifer()

def button_callback():
    text = input_textbox.get("0.0", "end").strip()
    is_encode = bool(radiobutton_var.get())
    
    if is_encode:
        out_text = cfr.encode(text)
        feedback_text = ''
    else:
        out_text = cfr.decode(text)
        feedback_text = str(cfr.get_failed_words_dict())

    output_textbox.delete("0.0", "end")
    output_textbox.insert("0.0", out_text)

    feedback_textbox.delete("0.0", "end")
    feedback_textbox.insert("0.0",  feedback_text)

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=20, fill="both", expand=True)

input_textbox = customtkinter.CTkTextbox(master=frame_1, width=400, height=90)
input_textbox.pack(pady=10, padx=10)

# cifer_var = customtkinter.StringVar(value="caesar")
# optionmenu = customtkinter.CTkOptionMenu(frame_1, values=["caesar", "vigenere"], variable=cifer_var)
# optionmenu.pack(pady=10, padx=10)

radiobutton_var = customtkinter.IntVar(value=1)
radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, text='encode', variable=radiobutton_var, value=1)
radiobutton_1.pack(padx=10, pady=10)

radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, text='decode', variable=radiobutton_var, value=0)
radiobutton_2.pack(padx=10, pady=10)

# key_entry = customtkinter.CTkEntry(master=frame_1, width=200, height=30, placeholder_text='key')
# key_entry.pack(padx=10, pady=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text='encode/decode')
button_1.pack(pady=10, padx=10)

output_textbox = customtkinter.CTkTextbox(master=frame_1, width=400, height=90)
output_textbox.pack(pady=10, padx=10)

feedback_textbox = customtkinter.CTkTextbox(master=frame_1, width=400, height=50)
feedback_textbox.pack(pady=10, padx=10)

app.mainloop()
