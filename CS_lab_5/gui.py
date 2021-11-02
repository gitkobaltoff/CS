import glob
import json
import subprocess
import tarfile
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import requests
import view_audit_structure
import re

global previous
main = Tk()
myFont = Font(family="Courier New", size=8)
s = ttk.Style()
s.configure('TFrame', background='#f0f0f0')
main.title("LabCS")
main.geometry("1100x600")
frame = ttk.Frame(main, width=1100, height=600, style='TFrame', padding=(4, 4, 4, 4))
frame.grid(column=0, row=0)
previous = []
index = 0
arr = []
matching = []

SystemDict = {}
querry = StringVar()
vars = StringVar()
tofile = []
structure = []

success = []
fail = []
unknown = []

toChange=[]
vars2=StringVar()
arr2=[]
arr2copy=[]

failedselected=[]

def make_query(struct):
    query = 'reg query ' + struct ['reg_key'] + ' /v ' + struct ['reg_item']
    out = subprocess.Popen(query,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    output = out.communicate() [0].decode('ascii', 'ignore')
    str = ''
    for char in output:
        if char.isprintable() and char != '\n' and char != '\r':
            str += char
    output = str
    output = output.split(' ')
    output = [x for x in output if len(x) > 0]
    value = ''
    if 'ERROR' in output [0]:
        unknown.append(struct ['reg_key'] + struct ['reg_item'])
    for i in range(len(output)):
        if 'REG_' in output [i]:
            for element in output [i + 1:]:
                value = value + element + ' '
            value = value [:len(value) - 1]
            if struct ['value_data'] [:2] == '0x':
                struct ['value_data'] = struct ['value_data'] [2:]
            struct ['value_data'] = hex(int(struct ['value_data']))
            p = re.compile('.*' + struct ['value_data'] + '.*')
            if p.match(value):
                print('Patern:', struct ['value_data'])
                print('Value:', value)
                success.append(struct ['reg_key'] + struct ['reg_item'] + '\n' + 'Value:' + value)
            else:
                print('Did not pass: ', struct ['value_data'])
                print('Value which did not pass: ', value)
                fail.append([struct, value])

def check():

    for struct in structure:
        if 'reg_key' in struct and 'reg_item' in struct and 'value_data' in struct:
            make_query(struct)

    for i in range(len(fail)):
        item=fail[i]
        arr2.append(' Item:' + item[0]['reg_item'] + ' Value:' + item[1] + ' Desired:' + item[0]['value_data'])
        global arr2copy
        arr2copy=arr2
    vars2.set(arr2)

    frame2 = Frame(main, bd=10, bg='#e6e6e6', highlightthickness=1)
    frame2.config(highlightbackground="black")
    frame2.place(relx=0.5, rely=0.1, width=400, relwidth=0.4, relheight=0.8, anchor='n')

    text2 = Text(frame2, bg="#ffffff", width=50, height=27.5, highlightthickness=3)
    text2.place(relx=0.07, rely=0.03, relwidth=0.4, relheight=0.9)
    text2.insert(END, '\n\n'.join(success))

    listbox_fail = Listbox(frame2, bg="#ffffff", font=myFont, fg="white", listvariable=vars2, selectmode=MULTIPLE,
                           width=50, height=27, highlightthickness=3)
    listbox_fail.place(relx=0.5, rely=0.03, relwidth=0.4, relheight=0.9)
    listbox_fail.config(highlightbackground="white")
    listbox_fail.bind('<<ListboxSelect>>', on_select_failed)

    def exit():
        frame2.destroy()

    exit_btn = Button(frame2, text='Back', command=exit, bg="#cacaca", fg="black", font=myFont, padx='10px',
                      pady='3px')
    exit_btn.place(relx=0.93, rely=0.95)

    def changeFailures():
        global arr2copy
        global arr2
        backup()
        for i in range(len(failedselected)):
            struct=failedselected[i][0]
            query = 'reg add "' + struct ['reg_key'] + '" /v ' + struct ['reg_item'] +' /d "'+ struct['value_data']+ '" /f'
            print(query)
            out = subprocess.Popen(query,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            output = out.communicate() [0].decode('ascii', 'ignore')
            str = ''
            for char in output:
                if char.isprintable() and char != '\n' and char != '\r':
                    str += char
            output = str
            print(output)
            vars2.set(arr2)
            arr2copy=arr2

    def restore():
        f=open('backup.txt')
        fail=json.loads(f.read())
        print(fail)
        f.close()

        for i in range(len(fail)):
            struct=fail[i][0]
            query = 'reg add ' + struct ['reg_key'] + ' /v ' + struct ['reg_item'] +' /d '+ fail[i][1]+ ' /f'
            print('Query:',query)
            out = subprocess.Popen(query,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
            output = out.communicate() [0].decode('ascii', 'ignore')
            str = ''
            for char in output:
                if char.isprintable() and char != '\n' and char != '\r':
                    str += char
            output = str
            print(output)


    def backup():
        f=open('backup.txt','w')
        backupString=json.dumps(fail)
        f.write(backupString)
        f.close()

    changeBtn = Button(frame2, text='Change', command=changeFailures, bg="#cacaca", fg="black", font=myFont,
                       padx='10px',
                       pady='3px')
    changeBtn.place(relx=0.23, rely=0.95)

    backupBtn = Button(frame2, text='Restore', command=restore, bg="#cacaca", fg="black", font=myFont,
                       padx='10px',
                       pady='3px')
    backupBtn.place(relx=0.66, rely=0.95)



def on_select_failed(evt):
    w = evt.widget
    actual = w.curselection()

    global failedselected
    global arr2
    failedselected=[]
    for i in actual:
        failedselected.append(fail[i])
    localarr2=[]
    for i in actual:
        localarr2.append(arr2copy[i])
    arr2=localarr2
    arr2=[x for x in arr2copy if x not in arr2]
    print(failedselected)



def entersearch(evt):
    search()


def search():
    global structure
    q = querry.get()
    arr = [struct['description'] for struct in structure if q.lower() in struct['description'].lower()]
    global matching
    matching = [struct for struct in structure if q in struct['description']]
    vars.set(arr)


def on_select_configuration(evt):
    global previous
    global index
    w = evt.widget
    actual = w.curselection()

    difference = [item for item in actual if item not in previous]
    if len(difference) > 0:
        index = [item for item in actual if item not in previous][0]
    previous = w.curselection()

    text.delete(1.0, END)
    str = '\n'
    for key in matching[index]:
        str += key + ':' + matching[index][key] + '\n'
    text.insert(END, str)


def import_audit():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global structure
    structure = view_audit_structure.main(file_name)
    for element in structure:
        for key in element:
            str = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    str += char
            isspacefirst = True
            str2 = ''
            for char in str:
                if char == ' ' and isspacefirst:
                    continue
                else:
                    str2 += char
                    isspacefirst = False
            element[key] = str2

    global matching
    matching = structure
    if len(structure) == 0:
        f = open(file_name, 'r')
        structure = json.loads(f.read())
        f.close()
    for struct in structure:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars.set(arr)


lstbox = Listbox(frame, bg="#ffffff", font=myFont, fg="black", listvariable=vars, selectmode=MULTIPLE, width=70,
                 height=20, highlightthickness=3)
lstbox.config(highlightbackground="#f0f0f0")
lstbox.grid(row=1, column=0, columnspan=4)
lstbox.bind('<<ListboxSelect>>', on_select_configuration)


def save_config():
    file_name = fd.asksaveasfilename(filetypes=(("Audit FILES", ".audit"),
                                                ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(matching[i])
    json.dump(tofile, file)
    file.close()


def select_all():
    lstbox.select_set(0, END)
    for struct in structure:
        lstbox.insert(END, struct)


def deselect_all():
    for struct in structure:
        lstbox.selection_clear(0, END)


def download_url(url, save_path, chunk_size=1024):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_download():
    url = "https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true"
    path = "audits.tar.gz"
    download_url(url, path)
    tf = tarfile.open("audits.tar.gz")
    tf.extractall()
    print(glob.glob("portal_audits/*"))


text = Text(frame, bg="#ffffff", fg="black", font=myFont, width=70, height=30, highlightthickness=3)
text.config(highlightbackground="#f0f0f0")
text.grid(row=1, column=5, columnspan=4, rowspan=4)
import_button = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Import", width=6, height=1,
                       command=import_audit, padx='10px', pady='3px').grid(row=2, column=0)
saveButton = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Save", width=7, height=1,
                    command=save_config, padx='10px').grid(row=0, column=0)
selectAllButton = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Select All", width=9, height=1,
                         command=select_all, padx='10px', pady='3px').place(relx=0.25, rely=0.78)
deselectAllButton = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Deselect All", width=9, height=1,
                           command=deselect_all, padx='10px', pady='3px').grid(row=2, column=3)
downloadButton = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Download", width=6, height=1,
                        command=extract_download, padx='10px', pady='3px').grid(row=3, column=0)
global e
e = Entry(frame, bg="#f1e6df", font=myFont, width=20, textvariable=querry).place(relx=0.25, rely=0.01)

search_button = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Search", width=9,
                       command=search).place(relx=0.4, rely=0)
check_button = Button(frame, bg="#cacaca", fg="black", font=myFont, text="Check", width=9, height=1,
                      command=check).place(relx=0.5, rely=0)
main.bind('<Return>', entersearch)
main.mainloop()
