
import os
import tkinter.scrolledtext as st
from tkinter import *
from tkinter import messagebox as m
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

import steno.hover as ho
import steno.database as db
import steno.image as image_

root = Tk()
root.title('Steno')
root.config(bg='#FAF7F0')
root.resizable(False, False)

icon_filename = 'images/l2'

if "nt" == os.name:
    icon_filename = f"{icon_filename}.ico"
else:
    icon_filename = f"@{icon_filename}.xbm"

root.wm_iconbitmap(icon_filename)

# centering the main window
root_h, root_w = 300, 400
s_w = root.winfo_screenwidth()
s_h = root.winfo_screenheight()
x_coor = int((s_w / 2) - (root_w / 2))
y_coor = int((s_h / 2) - (root_h / 2))
root.geometry("{}x{}+{}+{}".format(root_w, root_h, x_coor, y_coor))

# defining the fonts used and images
cas = ('Cascadia Code', 10)
cas_big = ('Cascadia Code', 20)
img = PhotoImage(file="images/noshow.png").subsample(4, 4)
img2 = PhotoImage(file="images/show.png").subsample(4, 4)
img3 = PhotoImage(file="images/dots.png").subsample(3, 3)



def image_steno():
    """Image steganography function"""
    img_win = Toplevel(master=root, bg='#FAF7F0')
    img_win.title('Image steno')
    img_win.geometry('515x260')
    img_win.wm_iconbitmap('images/l2.ico')
    im_lb = Label(img_win, text='IMAGE - STEGANOGRAPHY', bg='#FAF7F0', fg='#05a6eb', font=cas_big)
    im_lb.place(x=10, y=10)

    def em_img():
        """Image steganography functions"""
        global file, mess
        select_lb = Label(img_win, text='Select File:', font=cas, bg='#FAF7F0', fg='#fa05bd')
        select_lb.place(x=5, y=50)
        file_im = Entry(img_win, width=55, font=cas, relief='ridge')
        file_im.place(x=7, y=75)
        file_im.place(x=7, y=75)
        file_im.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global file
            file = askopenfilename(parent=img_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                   filetypes=[('Image files', '.png')], defaultextension='.png')
            file_im.delete(0, END)
            file_im.insert(0, file)
            select_lb.config(text='Selected File:')

        se_bu = Button(img_win, text='Browse', bg='#FAF7F0', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def pan():
            """Opens message prompt to enter message"""
            global mess
            message = Toplevel(img_win)
            message.title('Enter Message')
            message.resizable(False, False)
            message.wm_iconbitmap('images/l2.ico')
            lm = Label(message, text='Enter your message that you want to hide:', bg='yellow', font=cas)
            lm.pack(side=TOP, fill=BOTH)
            ho.CreateToolTip(lm, 'The message that you\nenter here will be encoded\nin your chosen file.')
            t = st.ScrolledText(message)
            t.config(font=cas)
            t.pack()

            def click(event=None):
                """Collects the message entered by user"""
                global mess
                message.withdraw()
                mess = t.get("1.0", "end-1c")

            bm = Button(message, text='Done(Ctrl+b)', command=click, relief='flat', bg='yellow', font=cas)
            bm.pack(side=BOTTOM, fill=BOTH)
            ho.CreateToolTip(bm, 'This accepts the\nmessage you entered\nand encodes it.')
            message.bind('<Control-b>', click)

        b = Button(img_win, command=pan, text='Enter Message', font=cas, bg='#94f748')
        b.place(x=10, y=100)
        ho.CreateToolTip(b, 'Opens a prompt where you can enter message')
        success = Label(img_win, bg='#edaa82', font=cas)
        success.place(x=10, y=170)

        def done():
            """Main function which asks for saving file location and then embeds the data in image file"""
            global file, mess
            m.showinfo('Procedure', 'Where would you like the embedded file to be saved?\n'
                                    'Select the path in the next window.')
            out = asksaveasfilename(title='Save your embedded file as', filetypes=[('Image files', '.png')],
                                    defaultextension='.png', initialdir=os.getcwd(), parent=img_win)
            if mess != '' and file != '' and file_im.get() != '' and out != '':
                try:
                    image_.encrypt_image(img_path=file, message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
                except FileNotFoundError:
                    image_.encrypt_image(img_path=file_im.get(), message=mess, new_path=out)
                    success.config(text='Successfully embedded message in\n{}'.format(out))
            else:
                m.showerror('ERROR', 'Something went wrong try again')

        main_bu = Button(img_win, text='Embed Message', relief=FLAT, bg='#f79205', font=cas, command=done)
        main_bu.place(x=10, y=130)
        ho.CreateToolTip(main_bu, 'Checks everything and embeds your data')

    def ex_img():
        """Data extracting function of audio steno"""
        global ex_file
        ex_win = Toplevel(root, bg='#edaa82')
        ex_win.title('Image Steno-EXTRACT')
        ex_win.geometry('515x310')
        ex_win.wm_iconbitmap('images/l2.ico')
        ex_lb = Label(ex_win, text='Image Steganography[EXTRACT] ', bg='#FAF7F0', fg='#2192FF', font=cas_big)
        ex_lb.place(x=10, y=10)
        file_lb = Label(ex_win, text='Select File:', font=cas, bg='#FAF7F0', fg='#fa0505')
        file_lb.place(x=5, y=50)
        file_ex = Entry(ex_win, width=55, font=cas, relief='ridge')
        file_ex.place(x=7, y=75)
        file_ex.focus()

        def browse():
            """Opens a prompt for selecting files"""
            global ex_file
            ex_file = askopenfilename(parent=ex_win, initialdir=os.getcwd(), title='Select File to EMBED',
                                      filetypes=[('Image files', '.png')], defaultextension='.png')
            file_ex.delete(0, END)
            file_ex.insert(0, ex_file)
            file_lb.config(text='Selected File:')

        se_bu = Button(ex_win, text='Browse', bg='#8ed925', font=cas, command=browse, relief='ridge')
        se_bu.place(x=450, y=70)
        ho.CreateToolTip(se_bu, 'Browse thorough &\nselect the file')

        def extract_data(event=None):
            """Extracts data from the audio file and shows it in a text box"""
            dat = image_.decrypt_image(img_path=ex_file)
            suc_lb = Label(ex_win, text='Hidden message is:', font=cas, fg='#f50c81', bg='#edaa82').place(x=6, y=130)
            sh = st.ScrolledText(ex_win, width=60, height=7, font=cas)
            sh.place(x=8, y=155)
            sh.insert(INSERT, dat)
            sh.config(state=DISABLED)

        ex_bu = Button(ex_win, text='Extract Message', bg='#f79205', font=cas, command=extract_data)
        ex_bu.place(x=10, y=100)
        ho.CreateToolTip(ex_bu, 'Extracts the hidden \ndata & displays it')
        ex_win.bind('<Return>', extract_data)

        qu_bu = Button(ex_win, text='Exit', font=cas, bg='#f23f3f', fg='#e1f719', command=ex_win.destroy)
        qu_bu.place(x=467, y=278)
        ho.CreateToolTip(qu_bu, 'Exits window')

    bu_en = Button(img_win, text='Embed', font=cas, bg='#00fffb', fg='black', command=em_img)
    bu_en.place(x=70, y=220)
    ho.CreateToolTip(bu_en, 'Embeds data in image file')
    bu_ex = Button(img_win, text='Extract', font=cas, bg='#00fffb', fg='black', command=ex_img)
    bu_ex.place(x=260, y=220)
    ho.CreateToolTip(bu_ex, 'Extracts data from image file')
    qubu = Button(img_win, text='Exit', font=cas, bg='#00fffb', fg='black', command=img_win.destroy)
    qubu.place(x=410, y=220)
    ho.CreateToolTip(qubu, 'Exits window')






def password():
    ps = Toplevel(root, bg='#88b1f2')
    ps.geometry('400x300+800+200')
    ps.wm_iconbitmap('images/l2.ico')
    ps_lb = Label(ps, text='User Login[backup]', font=cas_big, bg='#88b1f2', fg='#5c1841')
    ps_lb.place(x=5, y=5)
    ps_name_lb = Label(ps, text='Enter name:', bg='#88b1f2', fg='#5c1841', font=cas).place(x=5, y=50)
    ps_name_entry = Entry(ps, width=30, font=cas)
    ps_name_entry.place(x=100, y=50)
    ps_username_lb = Label(ps, text='Enter\nusername:', bg='#88b1f2', fg='#5c1841', font=cas).place(x=9, y=80)
    ps_username_entry = Entry(ps, width=30, font=cas)
    ps_username_entry.place(x=100, y=100)
    ps_pass = Label(ps, text='Enter\npassword:', bg='#88b1f2', fg='#5c1841', font=cas).place(x=9, y=130)
    ps_pass_entry = Entry(ps, width=25, font=cas, show='*')
    ps_pass_entry.place(x=100, y=150)

    def ok_done(event=None):
        db.new(ps_name_entry.get(), ps_username_entry.get(), ps_pass_entry.get())
        suc_lb.config(text='Done!!')

    ps_button = Button(ps, text='Done', font=cas, command=ok_done, fg='#e08f1d')
    ps_button.place(x=350, y=250)
    suc_lb = Label(ps, text='', font=cas_big, bg='#88b1f2', fg='#5c1841')
    suc_lb.place(x=150, y=200)

    def show():
        """Here the password's eyes show & hide functions are carried out"""
        if ps_pass_entry["show"] == '*':
            ps_pass_entry.config(show="")
            pass_bu.config(image=img2)
        elif ps_pass_entry["show"] == "":
            ps_pass_entry.config(show='*')
            pass_bu.config(image=img)

    pass_bu = Button(ps, image=img, command=show, bg='#36f5eb', relief='ridge')
    pass_bu.place(x=310, y=140)
    ho.CreateToolTip(pass_bu, 'Show/ Hide password')
    ho.CreateToolTip(ps_button, 'Sets up your admin account')
    ps.bind('<Return>', ok_done)


lb = Label(root, text="\n IMAGE STEGANOGRAPHY", font=('Poppins', 20), bg='#FAF7F0', fg='#2192FF')
lb.place(x=18, y=20)



image = Button(root, text='          START           ', relief='flat', bg='#00FFD1', command=image_steno, font=cas)
image.place(x=132, y=220)
ho.CreateToolTip(image, 'Click here\nto hide your\ndata in an image file')



uni = Button(root, image=img3, relief='flat', bg='#FAF7F0', command=password)
uni.place(x=370, y=0)
ho.CreateToolTip(uni, 'Here you can create\nadmin account to\nretrieve forgotten passwords later.')

root.mainloop()
db.close()
