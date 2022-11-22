import os, subprocess, tkinter as tk
import json
import copy

from Handbrake_BMC_functions import *
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from os.path import isfile, join, abspath

##################################################################################################
#########################################Functions################################################
import os, subprocess, tkinter as tk
import json
import copy
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from os.path import isfile, join, abspath

#################################################################################################################################################################################
################################################      Functions      ########################################################### #################################################
#################################################################################################################################################################################

def rgb(rgb):
  return "#%02x%02x%02x" % rgb

def open_folder():
  folder = tk.filedialog.askdirectory(title="Select folder")
  if folder:
    return os.path.abspath(folder)

def open_file(title,extensions):
  file = tk.filedialog.askopenfilename(title=title, filetypes=[("File",extensions)])
  if file:
    return file

################################################Lire le JSON et extraire les dictionnaires et définir les variables###########################################################

def read_JSON_source_file(JSON_source_file):
  global main_list, main_dict, job_dict, destination_dict, source_dict, range_dict, source_ext, dest_ext

  f = open(JSON_source_file,"r")
  data = f.read()
  main_list = json.loads(data)
  main_dict=main_list[0]
  job_dict=main_dict["Job"]
  destination_dict=job_dict["Destination"]
  source_dict=job_dict["Source"]
  range_dict=source_dict["Range"]
  source_dict_file=source_dict["Path"]
  source_ext=source_dict_file[-4:]
  destination_dict_file=destination_dict["File"]
  dest_ext=destination_dict_file[-4:]
  print('don\'t close this windows if you want to see the output of HandBrakeCLI')

def Preview_Window(windows_location, preview):
  newWindow = Toplevel(windows_location)
  newWindow.title("Preview")
  newWindow.geometry("600x600")
  TextWidget=Text(newWindow, height=500, width=380)
  TextWidget.pack(side=tk.RIGHT, fill=tk.Y)
  TextWidget.insert(tk.END, preview)



####################      Liste des fichiers / Fenetres des fichiers à traiter     #############################################################################
def get_files_list():
  global source_path
  global source_ext
  global fileslist
  fileslist = []
  if os.path.exists(source_path): 
    for filename in os.listdir(source_path):
      if filename[-4:]==source_ext:
        filepath=os.path.join(source_path, filename)
        if os.path.isfile(filepath):
          fileslist.append(filename)
  
  return fileslist


def mousewheel(event):
  canvas_fileslist.yview_scroll(int(-1*(event.delta)/120), "units")


def fileslist_check_function():
  #nombre de fichier pour déterminer la taille de la fenetre
  global source_ext
  global source_path
  fileslist=get_files_list()
  files_number=len(fileslist)

  #Création du canvas > frame > canvas > cases à cocher
  global canvas_fileslist
  global root_frame_fileslist
  canvas_fileslist=Canvas(root_frame_fileslist, highlightthickness=0, borderwidth=0, bg=rgb((30,30,30)))
  scrollbar_fileslist = Scrollbar(root_frame_fileslist, orient=VERTICAL)
  scrollbar_fileslist.pack(side = RIGHT, fill = Y)
  scrollbar_fileslist.config(command=canvas_fileslist.yview)
  canvas_fileslist.config(width=600, height=files_number*23, yscrollcommand=scrollbar_fileslist.set, scrollregion=(0,0,600,files_number*23))
  canvas_fileslist.bind_all("<MouseWheel>", mousewheel)
  canvas_fileslist.pack(side=LEFT,expand=True,fill= BOTH)
  frame_fileslist = Frame(canvas_fileslist, style="VAD.TFrame")
  canvas_fileslist.create_window(0,0, window=frame_fileslist, anchor="nw")

#Création des cases à cocher
  
  global file_Check_Vars
  global file_Check_Buttons
  file_Check_Vars=[]
  file_Check_Buttons=[]
  for fileindex,file in enumerate(fileslist):
    file_Check_Vars.append(IntVar(value=1))
    file_Check_Buttons.append("file_Check_Button_"+str(fileindex))
    globals()[f'{file_Check_Buttons[fileindex]}']=Checkbutton(frame_fileslist, text=file, onvalue=int(1), offvalue=int(0), variable = file_Check_Vars[fileindex], style="VAD.TCheckbutton")
    globals()[f'{file_Check_Buttons[fileindex]}'].pack(side=TOP, anchor=W)


#####################"#Addd and remove times ranges times range   

def range_add(range_start_entry_get, range_end_entry_get, ):
  global range_starts
  global range_ends
  global ranges_readable
  global range_type
  global ranges_label

  try: range_starts
  except NameError:
    range_starts=[]
    range_ends=[]
    ranges_readable=[]
  finally:
    if range_start_entry_get != "" and len(range_starts)<5: 
      range_starts.append(int(range_start_entry_get)*90000)
      range_ends.append(int(range_end_entry_get)*90000)
      ranges_readable.append(range_type+' : From '+str(int(range_start_entry_get))+' to '+str(int(range_end_entry_get)))
  
  ranges_label.config(text=ranges_readable)

def range_remove(ranges_label):
  global range_starts
  global range_ends
  global ranges_readable
  del range_starts[-1]
  del range_ends[-1]
  del ranges_readable[-1]
  ranges_label.config(text=ranges_readable)



################################################## ################################################## ################################################## 
##################################################  Root #############################################################################################
################################################## ################################################## ################################################## 
root = Tk()
root.title("Handbrake BMC (Batch MultiCut)")
root.geometry("620x620")
root.config(background=rgb((30,30,30)))
################################################## ################################################## ################################################## 
###################################################  Style après le root############################################################################################# 
################################################## ################################################## ################################################## 
PositionY=[10000,10,25+10+10,45+25+10,80+25+10,115+320+10,445+25+10,480+25+10,515+25+10,550+25+10,585+25+10]

grey=rgb((30,30,30))
grey2=rgb((90,90,90))


style = Style()
#style.theme_use('default')

style.configure("VAD.TLabel", foreground="white", background=grey)
style.configure("VAD.TFrame", foreground="white", background=grey)
style.configure("VAD_fileslist.TFrame", foreground="white", background=grey, highlightthickness=1, relief="groove")
style.configure("VAD.TCanvas", foreground="white", background=grey)
style.configure("VAD.TCheckbutton", foreground="white", background=grey, padx=10)
style.configure("VAD.TButton", foreground="black", background=grey2, text = "Packed LEFT")
style.configure("VADSmall.TButton", font=("Helvetica",13,"bold"))
style.configure("VAD.TEntry", foreground="black", background=grey2)


################################################## ################################################## ################################################## 
##################################################              Main Code               ##################################################  
################################################## ################################################## ################################################## 



#############################################Set Original JSON File => Lire le JSON et extraire les dictionnaires et définir les variables###################

def open_JSON_source_file():
  JSON_source_file=open_file('Select Original JSON File',".json")
  JSON_source_file_browse_Value.set(JSON_source_file)
  read_JSON_source_file(JSON_source_file) 

JSON_source_file_browse_Value = StringVar()
JSON_source_file_browse_Value.set('Open Original JSON from Handbrake Export for CLI')
JSON_source_file_browse_Entry = Entry(root, textvariable=JSON_source_file_browse_Value, state="readonly", style="VAD.TEntry")
JSON_source_file_browse_Entry.place(x=110, y=PositionY[1], width=500, height=25)   
JSON_source_file_browse_Button=Button(root, text="1 - Browse", command=open_JSON_source_file, style="VAD.TButton")
JSON_source_file_browse_Button.place(x=10, y=PositionY[1], width=90, height=25) 
#style="VAD.TButton",

###########     Bouton => Set source folder avec bouton parcourir et active la function qui ouvre la fenetre avec la liste des fichiers à cocher    ############################
def set_source_path():
  global source_path
  source_path=open_folder()
  source_browse_Value.set(source_path)
  fileslist_check_function()

source_browse_Value = StringVar()
source_browse_Value.set('Videos Source Folder')
source_browse_Entry = Entry(root, textvariable=source_browse_Value, state="readonly", style="VAD.TEntry")
source_browse_Entry.place(x=110, y=PositionY[2], width=500, height=25)  
source_browse_Button=Button(root, text="2 - Browse", command=set_source_path, style="VAD.TButton")
source_browse_Button.place(x=10, y=PositionY[2], width=90, height=25) 


###########Set Destination folder avec bouton parcourir#########################################################################################################

def set_destination_folder_press():
  global dest_path
  dest_path=open_folder()
  destination_browse_Value.set(dest_path)

destination_browse_Value = StringVar()
destination_browse_Value.set('Videos Destination Folder')
destination_browse_Entry = Entry(root, textvariable=destination_browse_Value, state="readonly", style="VAD.TEntry")
destination_browse_Entry.place(x=110, y=PositionY[3], width=500, height=25)   
destination_browse_Button=Button(root, text="3 - Browse", command=set_destination_folder_press, style="VAD.TButton")
destination_browse_Button.place(x=10, y=PositionY[3], width=90, height=25) 

#########################################Frame with check filelist ############################################################

root_frame_fileslist=Frame(root, style="VAD_fileslist.TFrame")
root_frame_fileslist.place(x=10, y=PositionY[4], width=600, height=320)

#########################################Enable New ranges  button & Labels############################################################

ranges_type=["4 - Keep original range from HandBrake","4 - Set new range(s) of type Time (second)","4 - Set new range(s) of type Chapter","4 - Set new range(s) of type Frames"]

def ranges_frame_state():
  global ranges_type
  global range_type

  if range_type_combo_var.get() == str(ranges_type[0]) :
      range_type="Original"
      ranges_frame.place(y=PositionY[0])
      ranges_label.place(y=PositionY[0])
  elif range_type_combo_var.get() == str(ranges_type[1]) :
      range_type="Time"
  elif range_type_combo_var.get() == str(ranges_type[2]) :
      range_type="Chapter"
  elif range_type_combo_var.get() == str(ranges_type[3]) :
      range_type="Frame"

  if range_type_combo_var.get() != str(ranges_type[0]) :
      ranges_frame.place(y=PositionY[5])
      ranges_label.place(y=PositionY[6])


range_type_combo_var= StringVar()
range_type_combobox = Combobox(root, textvariable=range_type_combo_var, style="VAD.TCombobox", values=ranges_type, state="readonly")
range_type_combobox.place(x=10, y=PositionY[5], width=380, height=25)
range_type_combo_var.set(ranges_type[0])
range_type_combobox.bind("<<ComboboxSelected>>", lambda _ :ranges_frame_state())

######################################### New ranges  button & Labels############################################################

ranges_frame=Frame(root, style="VAD.TFrame")
ranges_frame.place(x=400, y=PositionY[5], width=200, height=50)
range_start_entry_value=IntVar()
range_start_entry = Entry(ranges_frame, textvariable=range_start_entry_value, style="VAD.TEntry")
range_start_entry.place(x=10, y=0, width=40, height=25)

range_end_entry_value=IntVar()
range_end_entry = Entry(ranges_frame, textvariable=range_end_entry_value, style="VAD.TEntry")
range_end_entry.place(x=60, y=0, width=40, height=25)

def range_add_press():
  range_add(range_start_entry.get(), range_end_entry.get())
  range_start_entry_value.set(0)
  range_end_entry_value.set(0)

range_add_Button = Button(ranges_frame, text="+", command = range_add_press, style="VADSmall.TButton")
range_add_Button.place(x=120, y=0, width=25, height=25) 

def range_remove_press():
  range_remove(ranges_label)

range_remove_Button = Button(ranges_frame, text="-", command = range_remove_press, style="VADSmall.TButton")
range_remove_Button.place(x=150, y=0, width=25, height=25) 

ranges_label = Label(root, text="No new ranges set", anchor="w", style="VAD.TLabel")
ranges_label.place(x=10, y=PositionY[6], width=500, height=20)

ranges_frame_state()

###########################################################################################################################################################################
####################################################################            Fonction => Make JSON 2        ##########################################################
##########################################################################################################################################################################

def generate_JSON():
  global range_starts
  global range_ends
  global source_ext
  global source_path
  global dest_path
  global file_Check_Vars
  global fileslist
  global range_type
  JSONcontent=[]

  fileslisttoprocess=[]
  for f,file in enumerate(fileslist):
    if file_Check_Vars[f].get() == 1:
        fileslisttoprocess.append(file)
      
  #process JSON
  if range_type == "Original":
    for filename in fileslisttoprocess:
      filename_noext=filename[:-4]
      source_dict["Path"]=source_path+'\\'+filename
      destination_dict["File"]=dest_path+'\\'+ filename_noext+'_1'+dest_ext
      JSONcontent.append(copy.deepcopy(main_dict))
      
  
  if range_type == "Time":
    for filename in fileslisttoprocess:
      for range_index,range_start in enumerate(range_starts):
        filename_noext=filename[:-4]
        source_dict["Path"]=source_path+'\\'+filename
        destination_dict["File"]=dest_path+'\\'+ filename_noext+'_'+str(range_index)+dest_ext
        range_dict["Type"]="time"
        range_dict["Start"]=range_starts[range_index]
        range_dict["End"]=range_ends[range_index]
        JSONcontent.append(copy.deepcopy(main_dict))
      
  if range_type == "Chapter":
    for filename in fileslisttoprocess:
      for range_index,range_start in enumerate(range_starts):
        filename_noext=filename[:-4]
        source_dict["Path"]=source_path+'\\'+filename
        destination_dict["File"]=dest_path+'\\'+ filename_noext+'_'+str(range_index)+dest_ext
        range_dict["Type"]="Chapter"
        range_dict["Start"]=range_starts[range_index]
        range_dict["End"]=range_ends[range_index]
        JSONcontent.append(copy.deepcopy(main_dict))

    if range_type == "Frame":
      for filename in fileslisttoprocess:
        for range_index,range_start in enumerate(range_starts):
          filename_noext=filename[:-4]
          source_dict["Path"]=source_path+'\\'+filename
          destination_dict["File"]=dest_path+'\\'+ filename_noext+'_'+str(range_index)+dest_ext
          range_dict["Type"]="frame"
          range_dict["Start"]=range_starts[range_index]
          range_dict["End"]=range_ends[range_index]
          JSONcontent.append(copy.deepcopy(main_dict))
  return JSONcontent  
######################################################## Button => Lance la fabrication du Fichier JSON, formate et Lance le preview #############################

def generate_JSON_Press():
  global JSONFormatedContent
  JSONcontent=generate_JSON()
  JSONFormatedContent=json.dumps(JSONcontent, indent=2)
generate_JSON_Button=Button(root, text="5 - Generate File", command=generate_JSON_Press, style="VAD.TButton")
generate_JSON_Button.place(x=10, y=PositionY[7], width=600, height=25) 


def preview_JSON_press():
  global JSONFormatedContent
  Preview_Window(root, JSONFormatedContent)

preview_Button=Button(root, text="6 - Preview File (optional)", command=preview_JSON_press, style="VAD.TButton")
preview_Button.place(x=10, y=PositionY[8], width=600, height=25) 


########################################################### Fonction => Ecrit le JSON ################################################################ 
def write_JSONfile():
  JSONfile =open(source_browse_Entry.get()+"\\handbrake.JSON", "w")
  JSONfile.write(str(JSONFormatedContent))
  JSONfile.close  
#JSON_Write_Button=Button(root, text="Write JSON", command=write_JSONfile)
#JSON_Write_Button.place(x=10, y=PositionY[6], width=600, height=25)   


########################################################### Bouton => Lance la fonction d'écriture du fichier JSON +  Lance HandrakeCLI  ################################################################
def LaunchHandbrake():
  write_JSONfile()
  cmd='C:\\Program Files\\HandBrake\\HandBrakeCLI.exe', r'--queue-import-file' ,source_browse_Entry.get()+r'\handbrake.JSON'
  subprocess.Popen(cmd)
LaunchHandbrake_Button=Button(root, text="7 - Launch Queue in HandbrakeCLI", command=LaunchHandbrake, style="VAD.TButton")
LaunchHandbrake_Button.place(x=10, y=PositionY[9], width=600, height=25) 

########################################################

root.mainloop()
