import os, subprocess, tkinter as tk
import json
import copy
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from os.path import isfile, join, abspath

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


def get_files_list(sourcepath):
  global fileslist
  global source_ext
  fileslist = []
  if os.path.exists(sourcepath): 
    for filename in os.listdir(sourcepath):
      if filename[-4:]==source_ext:
        filepath=os.path.join(sourcepath, filename)
        if os.path.isfile(filepath):
          fileslist.append(filename)
  
  return fileslist

def Preview_Window(preview):
  newWindow = Toplevel(root)
  newWindow.title("Preview")
  newWindow.geometry("600x600")
  TextWidget=Text(newWindow, height=500, width=380)
  TextWidget.pack(side=tk.RIGHT, fill=tk.Y)
  TextWidget.insert(tk.END, preview)

################################################Lire le JSON et extraire les dictionnaires et définir les variables###########################################################
def open_JSON_source_file():
  JSON_source_file=open_file('Select Original JSON File',".json")
  JSON_source_file_browse_Value.set(JSON_source_file)
  read_JSON_source_file(JSON_source_file) 


def read_JSON_source_file(JSON_source_file):
  global main_list, main_dict, job_dict
  global destination_dict
  global source_dict
  global range_dict
  global source_ext
  global dest_ext
  global video_ext_for_tk

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
  video_ext_for_tk='[("Videos files", '+source_ext+')]'
  print('don\'t close this windows if you want to see the output of HandBrakeCLI')

###################################################  Root #############################################################################################

root = Tk()
root.title("Handbrake Splitter")
root.geometry("1150x280")
root.config(background=rgb((30,30,30)))

###################################################  Style après le root############################################################################################# 
PositionY=[10000,10,45,80,115,140,170,210,245,280,315]

grey=rgb((30,30,30))
grey2=rgb((90,90,90))


style = Style()
#style.theme_use('default')

style.configure("VAD.TLabel", foreground="white", background=grey)
style.configure("VAD.TFrame", foreground="white", background=grey)
style.configure("VAD.TCanvas", foreground="white", background=grey)
style.configure("VAD.TCheckbutton", foreground="white", background=grey)
style.configure("VAD.TButton", foreground="black", background=grey2)
style.configure("VADSmall.TButton", font=("Helvetica",12,"bold"), pady=2)
style.configure("VAD.TEntry", foreground="black", background=grey2)

##########################################################Set Original JSON File###################################################################

JSON_source_file_browse_Value = StringVar()
JSON_source_file_browse_Value.set('Open Original JSON from Handbrake Export for CLI')
JSON_source_file_browse_Entry = Entry(root, textvariable=JSON_source_file_browse_Value, style="VAD.TEntry")
JSON_source_file_browse_Entry.place(x=10, y=PositionY[1], width=500, height=25)   
JSON_source_file_browse_Button=Button(root, text="Browse", command=open_JSON_source_file, style="VAD.TButton")
JSON_source_file_browse_Button.place(x=520, y=PositionY[1], width=90, height=25) 
#style="VAD.TButton",

###########     Bouton => Set source folder avec bouton parcourir et ouvre la fenetre avec la liste des fichiers à cocher    ############################
def Set_Source_Folder():
  Source_folder=open_folder()
  source_browse_Value.set(Source_folder)
  fileslist_check_function(Source_folder)

source_browse_Value = StringVar()
source_browse_Value.set('Videos Source Folder')
source_browse_Entry = Entry(root, textvariable=source_browse_Value, style="VAD.TEntry")
source_browse_Entry.place(x=10, y=PositionY[2], width=500, height=25)  
source_browse_Button=Button(root, text="Browse", command=Set_Source_Folder, style="VAD.TButton")
source_browse_Button.place(x=520, y=PositionY[2], width=90, height=25) 

####################      Liste des fichiers / Fenetres des fichiers à traiter     #############################################################################

def mousewheel(event):
  canvas_fileslist.yview_scroll(int(-1*(event.delta)/120), "units")

def fileslist_check_function(sourcepath):
  #nombre de fichier pour déterminer la taille de la fenetre
  fileslist=get_files_list(sourcepath)
  files_number=len(fileslist)

  #Création du canvas > frame > canvas > cases à cocher
  global canvas_fileslist
  root_frame_fileslist=Frame(root, style="VAD.TFrame")
  root_frame_fileslist.place(x=620, y=10, width=500, height=260)
  canvas_fileslist=Canvas(root_frame_fileslist, highlightthickness=0, borderwidth=0, bg=rgb((30,30,30)))
  scrollbar_fileslist = Scrollbar(root_frame_fileslist, orient=VERTICAL)
  scrollbar_fileslist.pack(side = RIGHT, fill = Y)
  scrollbar_fileslist.config(command=canvas_fileslist.yview)
  canvas_fileslist.config(width=500, height=files_number*23, yscrollcommand=scrollbar_fileslist.set, scrollregion=(0,0,500,files_number*23))
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
    globals()[f'{file_Check_Buttons[fileindex]}'].pack(side=TOP, anchor=W)#.place(x=0, y=10+fileindex*20, width=480, height=20)


###########Set Destination folder avec bouton parcourir#########################################################################################################

def Set_Destination_Folder():
   Destination_folder=open_folder()
   destination_browse_Value.set(Destination_folder)

destination_browse_Value = StringVar()
destination_browse_Value.set('Videos Destination Folder')
destination_browse_Entry = Entry(root, textvariable=destination_browse_Value, style="VAD.TEntry")
destination_browse_Entry.place(x=10, y=PositionY[3], width=500, height=25)   
destination_browse_Button=Button(root, text="Browse", command=Set_Destination_Folder, style="VAD.TButton")
destination_browse_Button.place(x=520, y=PositionY[3], width=90, height=25) 

######################       Entrée de temps / Définition des ranges avec champs de saisie et bouton + ############################################################
 
#define times range   

def add_times_ranges():
  global starts_time
  global ends_time
  global time_ranges_readable
  starts_time=[]
  ends_time=[]
  time_ranges_readable=[]

  try: starts_time
  except NameError:
    starts_time=[]
    ends_time=[]
    time_ranges_readable=[]
  else:
    if starts_time_entry.get() != "" and len(starts_time)<5: 
      starts_time.append(int(starts_time_entry.get())*90000)
      ends_time.append(int(ends_time_entry.get())*90000)
      time_ranges_readable.append(str(int(starts_time_entry.get()))+'s to '+str(int(ends_time_entry.get()))+'s')
  time_range_label.config(text=time_ranges_readable)

def remove_times_ranges():
  global starts_time
  global ends_time
  global time_ranges_readable
  del starts_time[-1]
  del ends_time[-1]
  del time_ranges_readable[-1]
  time_range_label.config(text=time_ranges_readable)

#########################################Enable New ranges  button & Labels############################################################
def ranges_state():
  if split_method.get()==0:
    ranges_frame.place(y=PositionY[0])
  if split_method.get()==1:
    ranges_frame.place(y=PositionY[5])

split_method = IntVar()
split_method_Buttons = Checkbutton(root, text="Change ranges", onvalue= 1, offvalue= 0, variable = split_method, command=ranges_state, style="VAD.TCheckbutton")
split_method_Buttons.place(x=10, y=PositionY[4], width=120, height=20)

######################################### New ranges  button & Labels############################################################
ranges_frame=Frame(root, style="VAD.TFrame")
ranges_frame.place(x=10, y=PositionY[5], width=500, height=50)


time_label = Label(ranges_frame, text="Start to  End Time (s) :", anchor="w", style="VAD.TLabel")
time_label.place(x=0, y=0, height=20)

starts_time_entry_var=""
starts_time_entry = Entry(ranges_frame, textvariable=starts_time_entry_var, style="VAD.TEntry")
starts_time_entry.place(x=120, y=0, width=40, height=20)

ends_time_entry_var=""
ends_time_entry = Entry(ranges_frame, textvariable=ends_time_entry_var, style="VAD.TEntry")
ends_time_entry.place(x=165, y=0, width=40, height=20)

remove_time_range_Button = Button(ranges_frame, text="-", command = remove_times_ranges, style="VADSmall.TButton")
remove_time_range_Button.place(x=220, y=0, width=20, height=20) 

add_time_range_Button = Button(ranges_frame, text="+", command = add_times_ranges, style="VADSmall.TButton")
add_time_range_Button.place(x=245, y=0, width=20, height=20) 

time_range_label = Label(ranges_frame, text="No time range set", anchor="w", style="VAD.TLabel")
time_range_label.place(x=0, y=25, width=500, height=20)

ranges_state()



#########################            Fonction => Make JSON 2        ######################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
 #files variables
def generate_JSON():
  global file_Check_Vars
  global starts_time
  global ends_time
  global split_method
  JSONcontent=[]
  sourcepath=source_browse_Entry.get()
  destpath=destination_browse_Entry.get()  

  fileslist=get_files_list(sourcepath)

  fileslisttoprocess=[]
  for i,file in enumerate(fileslist):
    if file_Check_Vars[i].get() == 1:
        fileslisttoprocess.append(file)
      
  #process JSON
  
  
  if split_method.get() == 0:
    for filename in fileslisttoprocess:
      filename_noext=filename[:-4]
      source_dict["Path"]=sourcepath+'\\'+filename
      destination_dict["File"]=destpath+'\\'+ filename_noext+'_1'+dest_ext
      JSONcontent.append(copy.deepcopy(main_dict))

  if split_method.get() == 1:
    for filename in fileslisttoprocess:
      filename_noext=filename[:-4]
      source_dict["Path"]=sourcepath+'\\'+filename
      destination_dict["File"]=destpath+'\\'+ filename_noext+'_1'+dest_ext
      for range_index,start_time in enumerate(starts_time):
        range_dict["Type"]="time"
        range_dict["Start"]=starts_time[range_index]
        range_dict["End"]=ends_time[range_index]
        JSONcontent.append(copy.deepcopy(main_dict))
  return JSONcontent  
######################################################## Button => Lance la fabrication du Fichier JSON, formate et Lance le preview #############################

def generate_JSON_Press():
  global JSONFormatedContent
  JSONcontent=generate_JSON()
  JSONFormatedContent=json.dumps(JSONcontent, indent=2)
generate_JSON_Button=Button(root, text="Generate File", command=generate_JSON_Press, style="VAD.TButton")
generate_JSON_Button.place(x=10, y=PositionY[7], width=290, height=25) 


def preview_JSON_press():
  global JSONFormatedContent
  Preview_Window(JSONFormatedContent)

preview_Button=Button(root, text="Preview File", command=preview_JSON_press, style="VAD.TButton")
preview_Button.place(x=310, y=PositionY[7], width=200, height=25) 


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
LaunchHandbrake_Button=Button(root, text="Launch Queue in HandbrakeCLI", command=LaunchHandbrake, style="VAD.TButton")
LaunchHandbrake_Button.place(x=10, y=PositionY[8], width=500, height=25) 

########################################################

root.mainloop()
