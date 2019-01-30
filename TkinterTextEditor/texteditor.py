from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as tmb
from PIL import Image,ImageTk                # Required to convert images into Tkinter formats
import os

PROGRAM_NAME = 'Z-Editor'


def search_output(text_to_find, if_ignore_case, content_text, find_window, search_entry):

    ''' This is how the word will be searched '''
    content_text.tag_remove('match', '1.0', END)    # removing any previous 'match' tag if present
    match_count = 0                                 # counter to find no. of common words
    if text_to_find:
        start_pos = '1.0'
        while True:

            start_pos = content_text.search(text_to_find, start_pos, stopindex=END, nocase=if_ignore_case) # returns position of first letter 0f common word found
            if not start_pos:
                break
            end_pos = '{}+{}c'.format(start_pos, len(text_to_find))     # end position of common word
            content_text.tag_add('match', start_pos, end_pos)           # tagging the word
            start_pos = end_pos                                         # updating start_pos
            match_count += 1                                            # increase match_count
        content_text.tag_config('match', foreground='#f00', background='#0ff')
        find_window.title('{} words found'.format(match_count))

def copy(event=None):
    content_text.event_generate("<<Copy>>")
    on_content_change()
    return 'break'

def cut(event=None):
    content_text.event_generate("<<Cut>>")
    on_content_change()
    return 'break'

def paste(event=None):
    content_text.event_generate("<<Paste>>")
    on_content_change()
    return 'break'

def undo(event=None):
    content_text.event_generate("<<Undo>>")
    on_content_change()
    return 'break'


def redo(event=None):
    content_text.event_generate('<<Redo>>')
    on_content_change()
    return 'break'

def select_all(event=None):
    content_text.tag_add('sel', '1.0', 'end')
    return 'break'

def find(event=None):

    '''creating child window for search'''
    find_window = Toplevel(root)
    find_window.transient(root)                 #This ensures find_window is always above its root
    find_window.resizable(False, False)
    find_window.title('Find')
    Label(find_window, text='Find :').grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(find_window, width=20)
    search_entry_widget.focus_set()
    search_entry_widget.grid(row=0, column=1, sticky='we', padx=2, pady=2)

    ignore_case_value = IntVar()
    Checkbutton(find_window, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2,
                                                                                   pady=2)

    Button(find_window, text='Find_All', command=lambda: search_output(search_entry_widget.get(),
                                                                        ignore_case_value.get()
                                                                        , content_text, find_window,
                                                                        search_entry_widget)).grid(row=0, column=2,
                                                                                                   sticky='w', padx=2,
                                                                                                   pady=2)
    ''' close_search_window required to remove find_window'''
    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        find_window.destroy()

    find_window.protocol('WM_DELETE_WINDOW',
                             close_search_window)
    return "break"

def about_box(event=None):
    tmb.showinfo(title='About '+PROGRAM_NAME, message='{} \n\n {}'.format('This Product belongs to Z Corporation. \nAn '
                                                                        'exclusive subdivision of AllMech.co ',
                                                                        'All Rights Reserved'))
    return 'break'


def help_box(event=None):

    tmb.showinfo( "Help", "Help Book: \nTkinter GUI Application\n DevelopmentBlueprints", icon='question')
    return 'break'


file_name = None

def open(event=None):
    input_file_name = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{}-{}'.format(os.path.basename(file_name), PROGRAM_NAME))
        print(file_name)
        content_text.delete(1.0, END)

        with open(file_name) as _file:

            content_text.insert(1.0, _file.read())
    on_content_change()

    return 'break'


def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    on_content_change()

    return 'break'

def save_as(event=None):
    input_file_name = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('All files','*.*'), ('Text Documents', '*.txt')])
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{}-{}'.format(os.path.basename(file_name), PROGRAM_NAME))
        write_to_file(file_name)
    on_content_change()

    return 'break'

def write_to_file(file_name):

    try:
        content = content_text.get(1.0, END)
        with open(file_name, 'wb') as file:
            file.write(content)

    except IOError:
        pass

def new(event = None):
    on_content_change()
    root.title('Untitled')
    global file_name
    file_name = None
    content_text.delete(1.0, END)
    return 'break'

'The below written 3fxns cover line numbers in line_number_bar'

def get_line_no():
    output = ''
    if show_line_no.get():

        row, col = content_text.index('end').split('.')
        for i in range(int(row)):
            output+= str(i+1)+'\n'

    return output

def update_line_no(event=None):
    line_no = get_line_no()
    text_number_bar.configure(state='normal')
    text_number_bar.delete('1.0', 'end')
    text_number_bar.insert('1.0', line_no)
    text_number_bar.config(state='disabled')

def on_content_change(event=None):
    update_line_no()
    update_label_bar()
    return 'break'


'''the next 3fxns cover highlighting active line'''
def highlight_line():
    content_text.tag_remove('active', 1.0, END)
    content_text.tag_add('active', 'insert linestart', 'insert lineend +1c')
    content_text.after(100, toggle_highlight)

def undo_highlight_line():
    content_text.tag_remove('active', 1.0, END)

def toggle_highlight(event=None):
    if highlight_current_line.get():
        highlight_line()
    else :
        undo_highlight_line()

'''the next fxn cover'''

def update_label_bar(event=None):
    if show_cursor.get():
        cursor_info_bar.pack(expand=NO, fill=None, side=RIGHT, anchor='se')
        row, column =content_text.index(INSERT).split('.')
        tex ='Line:'+row + ' | Column:' + column
        cursor_info_bar.config(text=tex)
    else:
        cursor_info_bar.pack_forget()

'''the next fxn covers pop up menu'''
def show_popup_menu(event=None):
    pop_up_menu.tk_popup(event.x_root, event.y_root)

'''the next fxn covers theme aspect'''
def change_theme(evenr=None):
    selected_theme = theme_name.get()
    fg, bg = color_schemes[selected_theme].split('.')
    content_text.configure(fg=fg, bg=bg)





icons = ['new', 'save', 'open', 'cut', 'copy', 'paste', 'undo','redo']  #icon list for toolbar
#for i in icons:
#    img1 = Image.open(r'E:\icons\{}.ico'.format(i))
#    img1 = img1.resize((18, 18))
#    photu.append(ImageTk.PhotoImage(img1))
#img = PhotoImage('E:\icons\ open.png')

root = Tk()
root.title(PROGRAM_NAME)
menu_bar = Menu(root)  # adding menu bar
file_menu = Menu(menu_bar, tearoff=0)   # creating file menu in menu bar
edit_menu = Menu(menu_bar, tearoff=0)   # creating edit menu
view_menu = Menu(menu_bar, tearoff=0)   # creating view menu
about_menu = Menu(menu_bar, tearoff=0)  # creating about menu
menu_bar.add_cascade(label='File', menu=file_menu)      # adding file menu
menu_bar.add_cascade(label='Edit', menu=edit_menu)      # adding edit menu
menu_bar.add_cascade(label='View', menu=view_menu)      # adding view menu
menu_bar.add_cascade(label='About', menu=about_menu)    # adding about menu
root.config(menu=menu_bar)

file_menu.add_command(label="New", accelerator='Ctrl + N', compound='left', underline=0, command=new)        # ''' Adding Menu Items  '''
file_menu.add_command(label='Open', accelerator='Ctrl + 0', compound=LEFT, underline=0, command=open)
file_menu.add_command(label='Save', accelerator='Ctrl + S', compound=LEFT, underline=0, command=save)
file_menu.add_separator()
file_menu.add_command(label='Save_As', accelerator='Shift + Ctrl + S', underline=0, command=save_as)
file_menu.add_command(label='Exit', accelerator='Alt + F4', underline=0)

edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound=LEFT, command=undo)                      # Addding edit menu items
edit_menu.add_command(label='Redo', accelerator='Ctrl + Y', compound=LEFT, command=redo)
edit_menu.add_command(label='Cut', accelerator='Ctrl + X', compound=LEFT, command=cut)
edit_menu.add_command(label='Copy', accelerator='Ctrl + C', compound=LEFT, underline=0, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl + V', compound=LEFT, command=paste)
edit_menu.add_command(label='Find', accelerator='Ctrl + F', compound=LEFT, underline=0, command=find)
edit_menu.add_command(label='Select_All', accelerator='Ctrl + A', compound=LEFT, command=select_all, underline=8)

about_menu.add_command(label='About', command=about_box)                                                           # Adding about menu items
about_menu.add_command(label='Help', accelerator='F1', command=help_box)



theme_name = StringVar()
theme_name.set('Default')
show_line_no = IntVar()
highlight_current_line = IntVar()
show_cursor = BooleanVar()
highlight_current_line.set(0)
show_line_no.set(1)
show_cursor.set(TRUE)
view_menu.add_checkbutton(label='Show Line Number', variable=show_line_no, command=on_content_change)                   # Adding view menu items
view_menu.add_checkbutton(label='Show Cursor Location At Bottom',variable=show_cursor,command=update_label_bar)
view_menu.add_checkbutton(label='Highlight Current Line', variable=highlight_current_line, command=toggle_highlight)
themes_menu = Menu(view_menu, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu)

color_schemes = {                                                                # different themes for theme menu
    'Default': '#000000.#FFFFFF',
    'Greygarious':'#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue':'#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000'
    }
for i in color_schemes:
    themes_menu.add_radiobutton(label=i, variable=theme_name, command=change_theme)




shortcut_bar = Frame(root, background='light sea green', height = 25 )      # Adding frame for short cut bar



#icons = ['new', 'save', 'open', 'cut', 'copy', 'paste', 'undo', 'redo']                              #icon list for toolbar
photo = []
for i in icons:
    img1 = Image.open(r'E:\icons\{}.ico'.format(i))
    img1 = img1.resize((18, 18))
    photo.append(ImageTk.PhotoImage(img1))
    cmd = eval(i)
    tool_bar = Button(shortcut_bar, image=photo[-1], command=cmd, bg='#aaf')
    tool_bar.pack(padx=2, pady=2, side='left')



shortcut_bar.pack(side=TOP, fill=X, expand='no')



text_number_bar = Text(root, background='khaki', width=5, padx=5, pady=3, wrap='none', takefocus=0, border=0,
                       state='disabled')                                                  # Adding line number bar
text_number_bar.pack(fill=Y, side=LEFT)                            #This statement returms none type object
                                                                   #so never add pack while creating widget



content_text = Text(root, undo=1)                                                       # Adding text space
content_text.focus_set()
content_text.tag_configure('active', background='ivory2')          # setting bg colour for higlight current line option
'''Text Bindings '''
content_text.bind('<Control - Y>', redo)               # Overriding Ctrl + V for redo For both cases of 'y'
content_text.bind('<Control - y>', redo)
content_text.bind('<Control - A>', select_all)              # Binding content text to select all feature via event Control + a or A
content_text.bind('<Control - a>', select_all)
content_text.bind('<Control - F>', find)              # Binding content_text to find via event ctrl + F or f
content_text.bind('<Control - f>', find)
content_text.bind('<Control - s>', save)
content_text.bind('<Control - S>', save)
content_text.bind('<Control - N>', new)
content_text.bind('<Control - n>', new)
content_text.bind('<Shift - Control - s>', save_as)
content_text.bind('<Shift - Control - S>', save_as)
content_text.bind('<Control - O>', open)
content_text.bind('<Control - o>', open)
content_text.bind('<Any-KeyPress>', on_content_change)
root.bind_all('<F1>', help_box)


scroll_bar = Scrollbar(content_text)                                            # Adding scroll bar
content_text.configure(yscrollcommand=scroll_bar.set)                           # Creating links between
scroll_bar.config(command=content_text.yview)                                   # scroll bar and text space
scroll_bar.pack(side=RIGHT, fill=Y)
content_text.pack(expand=YES, fill=BOTH)


cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')              #creating cursor position bar


pop_up_menu = Menu(content_text)
for i in icons:
    pop_up_menu.add_command(label=i, compound='left', command=eval(i))
pop_up_menu.add_separator()
pop_up_menu.add_command(label='Select_All', command=select_all)
content_text.bind('<Button-3>', show_popup_menu)




root.mainloop()
