from tkinter import *
import os
import tkinter.filedialog # tkFileDialog is a module with open and save dialog functions
import tkinter.messagebox

root = Tk()  # initialising a tkinter window
root.iconbitmap('icons/favicon.ico')  # setting an icon for our app

PROGRAM_NAME = "TextEditor"  # Name for our app
root.title(PROGRAM_NAME)
file_name = None # A global variable declared to be used over and over in the program
root.geometry('800x400')  # geometry for our window

# all codes goes here


# FILE MENU

# This function is basically tu create a new file
def new_file(event=None): #A Tkinter application runs most of its time inside an event loop, which is entered via the mainloop method. It waiting for events to happen.
    # There are various types of events, hence. Here the type of the event is 'none'
    root.title("Untitled")  # default name of a new file
    global file_name
    file_name = None
    content_text.delete(1.0, END) #Text is a widget in the tkinter. '.delete' is a function used to clear the text
    # This would begin from the beginning to the end of he text
    on_content_changed()


# this function is to open a new file
def open_file(event=None):
    # tkFileDialog is a module with open and save dialog functions

    """
                                      tkFileDialog has 3 attributes:

      ||Attribute||             ||Parameters||                                ||Purpose||

    .askopenfilename      Directory, Title, Extension         To open file: Dialog that requests selection of
                                                                            an existing file
    .asksaveasfilename    Directory, Title, Extension         To save file: Dialog that requests creation or
                                                                            replacement of a file
      .askdirectory                  None                     To open directory
    """

    input_file_name = tkinter.filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                                                             ("Text Docs", "*.txt"),
                                                                                             ("HTML", "*.html"),
                                                                                             ("CSS", "*.css"),
                                                                                             ("JavaScript", "*.js")])
    # it is file dialog that requests the selection of an existing file
    if input_file_name:
        global file_name # the global variable
        file_name = input_file_name  # the path of the selected file is stored in this variable
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME)) # changing the title to that of the new file
        content_text.delete(1.0, END)
        with open(file_name) as _file:
            content_text.insert(1.0, _file.read()) # function to read the file requested
    
    on_content_changed()


# this function is responsible to write a file or simply store a file
def write_to_file(file_name):
    try:
        # The first part, "1.0" means that the input should be read from line one, character zero (ie: the very first
        # character). END is an imported constant which is set to the string "end". The END part means to read until
        # the end of the text box is reached. The only issue with this is that it actually adds a newline to our input.
        # So, in order to fix it we should change END to end-1c(Thanks Bryan Oakley) The -1c deletes 1 character, while
        # -2c would mean delete two characters, and so on
        content = content_text.get(1.0, 'end-1c')
        with open(file_name, 'w') as the_file:
            the_file.write(content) # function to write to the mentioned file
    except IOError:
        pass  


# this function is a save as function where I have used the .askesaveasfilename attribute of file dialog
def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"),
                                                                                               ("Text Docs", "*.txt"),
                                                                                               ("HTML", "*.html"),
                                                                                               ("CSS", "*.css"),
                                                                                               ("JavaScript", "*.js")])
    # File dailog that requests creation or replacement of a file
    if input_file_name:
        global file_name
        file_name = input_file_name  # path is stored here
        write_to_file(file_name)  # this will write a file
        # a function already defined above
        root.title('{} - {}'.format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"
    

# this function will save the file or overwrite the existing file with the changes
def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        write_to_file(file_name)
    return "break"



#EDIT MENU
# These are various typs of event bidings through which events can be generated to cut/cop/paste text or undo operations
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"
def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return "break"
def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"

def undo():
    content_text.event_generate("<<Undo>>")
    on_content_changed()
    return "break"

def redo(event=None):
    content_text.event_generate("<<Redo>>")
    on_content_changed()
    return "break"

def selectall(event=None):
    content_text.tag_add('sel','1.0','end')
    return "break"

   
def find_text(event=None):
    search_toplevel = Toplevel(root)
    #The Toplevel is a widget used to display new windows, dialogs, and other pop up windows
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    #Makes window a transient window for the given master 
    # Here root is the master/parent
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               content_text, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
    # we will get the text to be found as an input from the user and then pass the string as an arguement to be searched in our text

    def close_search_window():
        content_text.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"

def search_output(needle,if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove('match','1.0', END)
    matches_found=0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = content_text.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break

            end_pos = '{} + {}c'. format(start_pos, len(needle))
            content_text.tag_add('match', start_pos, end_pos)
            matches_found +=1
            start_pos = end_pos
        content_text.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))

#ABOUT MENU
# message boxes help us to display any information we need to, on the window

def display_about(event=None):
    tkinter.messagebox.showinfo(
        "About", PROGRAM_NAME + "\nA simple Text Editor made in Python with Tkinter\n -Nabin Jaiswal")


def display_help(event=None):
    tkinter.messagebox.showinfo(
        "Help", "This Text Editor works similar to any other editors.",
        icon='question')


def exit_editor(event=None):
    if tkinter.messagebox.askokcancel("Exit", "Are you sure you want to Quit?"):
        root.destroy()

#adding Line Numbers Functionality
# this will help us to count the number of lines in the user's text
def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = content_text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output

# everytime the content in the editor are updated, this function is run to update the attributes
def on_content_changed(event=None):
    update_line_numbers()
    update_cursor()

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

# Adding Cursor Functionality
# we use the cursor functions and its various attributes
def show_cursor():
    show_cursor_info_checked = show_cursor_info.get()
    if show_cursor_info_checked:
        cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')
    else:
        cursor_info_bar.pack_forget()


def update_cursor(event=None):
    row, col = content_text.index(INSERT).split('.')
    line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0
    infotext = "Line: {0} | Column: {1}".format(line_num, col_num)
    cursor_info_bar.config(text=infotext)


#Adding Text Highlight Functionality
def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add(
        "active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)


def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")


def toggle_highlight(event=None):
    if to_highlight_line.get():
        highlight_line()
    else:
        undo_highlight()


#Adding Change Theme Functionality
def change_theme(event=None):
    selected_theme = theme_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    foreground_color, background_color = fg_bg_colors.split('.')
    content_text.config(
        background=background_color, fg=foreground_color)

#pop-up menu
def show_popup_menu(event):
    popup_menu.tk_popup(event.x_root, event.y_root)

    
    
# ICONS for the compound menu
# attaching the images for each and every function
new_file_icon = PhotoImage(file='icons/new_file.gif')
open_file_icon = PhotoImage(file='icons/open_file.gif')
save_file_icon = PhotoImage(file='icons/save.gif')
cut_icon = PhotoImage(file='icons/cut.gif')
copy_icon = PhotoImage(file='icons/copy.gif')
paste_icon = PhotoImage(file='icons/paste.gif')
undo_icon = PhotoImage(file='icons/undo.gif')
redo_icon = PhotoImage(file='icons/redo.gif')
find_icon = PhotoImage(file='icons/find_text.gif')


#MENU CODES GOES HERE
#we add various commands and we add their functionalities along and also, the triggers with them
menu_bar = Menu(root) #menu begins

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', compound='left', image=new_file_icon, underline=0, command=new_file)
file_menu.add_command(label='Open', accelerator='Ctrl+O', compound='left', image=open_file_icon, underline=0, command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=save_file_icon, underline=0, command=save)
file_menu.add_command(label="Save As", accelerator='Ctrl+Shift+S', compound='left', underline=0, command = save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Alt+F4', compound='left', underline=0, command=exit_editor)
menu_bar.add_cascade(label='File', menu=file_menu)
# end of File Menu

edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label='Undo', accelerator='Ctrl + Z', compound='left', image=undo_icon, underline=0, command=undo)
edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', image=redo_icon, underline=0, command=redo)
edit_menu.add_separator()
edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound='left',  image=cut_icon, underline=0, command=cut) 
edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound='left', image=copy_icon, underline=0, command=copy)
edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound='left',  image=paste_icon, underline=0, command=paste)
edit_menu.add_separator()
edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound='left',  image=find_icon, underline=0, command=find_text)
edit_menu.add_separator()
edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound='left', underline=0, command=selectall) 
menu_bar.add_cascade(label='Edit', menu=edit_menu)
#end of Edit Menu


view_menu = Menu(menu_bar, tearoff=0)
show_line_number=IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number)
show_cursor_info=IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label='Show Cursor Location at Bottom', variable=show_cursor_info, command=show_cursor)
to_highlight_line=IntVar()
view_menu.add_checkbutton(label='Highlight Current Line', variable=to_highlight_line, onvalue=1, offvalue=0,command=toggle_highlight)
themes_menu=Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label='Themes', menu=themes_menu, command=change_theme)

''' THEMES OPTIONS'''
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

theme_choice=StringVar()
theme_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=theme_choice, command=change_theme)

menu_bar.add_cascade(label='View', menu=view_menu)


#start of About Menu
about_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='About', menu=about_menu)
about_menu.add_command(label='About', underline=0, command=display_about)
about_menu.add_command(label='Help', underline=0, command=display_help)
#end of About Menu
root.config(menu=menu_bar)

#adding top shortcut bar and left line number bar
shortcut_bar=Frame(root, height=25)
shortcut_bar.pack(expand='no', fill='x')

#adding shortcut icons
icons=('new_file', 'open_file', 'save', 'cut', 'copy', 'paste','undo', 'redo', 'find_text')
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file='icons/{}.gif'.format(icon)).zoom(2,2)
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, height=35,width=35, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side='left')


line_number_bar = Text(root, width=4, padx=3, takefocus=0, fg='white', border=0, background='#282828', state='disabled',  wrap='none')
line_number_bar.pack(side='left', fill='y')

#adding the main context Text widget and Scrollbar Widget
# providing the scroll function by creating a scrollbar and using its various attributes
content_text = Text(root, wrap='word')
content_text.pack(expand='yes', fill='both')

scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=content_text.yview)
scroll_bar.pack(side='right', fill='y')

# adding cursor info label
cursor_info_bar = Label(content_text, text='Line: 1 | Column: 1')
cursor_info_bar.pack(expand='no', fill=None, side='right', anchor='se')

# setting up the pop-up menu
popup_menu = Menu(content_text)
for i in ('cut', 'copy', 'paste', 'undo', 'redo'):
    cmd = eval(i)
    popup_menu.add_command(label=i, compound='left', command=cmd)
popup_menu.add_separator()
popup_menu.add_command(label='Select All', underline=7, command=selectall)
content_text.bind('<Button-3>', show_popup_menu)


#handling binding
# we bind together, the events with their functions through 'bind'

content_text.bind('<Control-N>', new_file)
content_text.bind('<Control-n>', new_file)
content_text.bind('<Control-O>', open_file)
content_text.bind('<Control-o>', open_file)
content_text.bind('<Control-S>', save)
content_text.bind('<Control-s>', save)

content_text.bind('<Control-Y>',redo)
content_text.bind('<Control-y>',redo)
content_text.bind('<Control-A>',selectall)
content_text.bind('<Control-a>',selectall)
content_text.bind('<Control-F>',find_text)
content_text.bind('<Control-f>',find_text)

content_text.bind('<KeyPress-F1>', display_help)

content_text.bind('<Any-KeyPress>', on_content_changed)
content_text.tag_configure('active_line', background='ivory2')

content_text.bind('<Button-3>', show_popup_menu)
content_text.focus_set()


#END OF MENU

root.protocol('WM_DELETE_WINDOW', exit_editor)
root.mainloop()
