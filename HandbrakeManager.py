import os, subprocess, tkinter as tk
import json
import copy
from tkinter import *
from tkinter import filedialog
from os.path import isfile, join, abspath
from functools import partial


PositionY=[0,10,45,80,110,140,170,210,245,280,315]

def RGB(rgb):
  return "#%02x%02x%02x" % rgb

def open_folder():
  folder = tk.filedialog.askdirectory(title="Select folder")
  if folder:
    return os.path.abspath(folder)

def open_file(title,extensions):
  file = tk.filedialog.askopenfilename(title=title, filetypes=[("File",extensions)])
  if file:
    print(file)
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
  TextWidget=tk.Text(newWindow, height=500, width=380)
  TextWidget.pack(side=tk.RIGHT, fill=tk.Y)
  TextWidget.insert(tk.END, preview)


################################################Lire le JSON et extraire les dictionnaires et définir les variables###########################################################
def Open_JSON_Source_File():
  JSON_Source_File=open_file('Select Original JSON File',".json")
  print(JSON_Source_File)
  JSON_Source_File_Browse_Value.set(JSON_Source_File)
  Read_JSON_Source_File(JSON_Source_File) 


def Read_JSON_Source_File(JSON_Source_File):
  global main_list, main_dict, job_dict
  global destination_dict
  global source_dict
  global range_dict
  global source_ext
  global dest_ext
  global video_ext_for_tk

  f = open(JSON_Source_File,"r")
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
  print(source_ext)

 

###################################################  Root #############################################################################################
root = tk.Tk()
root.title("Handbrake Splitter")
root.geometry("1280x500")
root.config(background=RGB((30,30,30)))

##########################################################Set Original JSON File###################################################################

JSON_Source_File_Browse_Value = StringVar()
JSON_Source_File_Browse_Value.set('Open Original JSON from Handbrake Export for CLI')
JSON_Source_File_Browse_Entry = tk.Entry(root, textvariable=JSON_Source_File_Browse_Value,  bg=RGB((90,90,90)), fg=RGB((255,255,255)))
JSON_Source_File_Browse_Entry.place(x=10, y=PositionY[1], width=500, height=25)   
JSON_Source_File_Browse_Button=tk.Button(root, text="Browse", command=Open_JSON_Source_File, pady=2, padx=10)
JSON_Source_File_Browse_Button.place(x=520, y=PositionY[1], width=90, height=25) 

###########     Bouton => Set source folder avec bouton parcourir et ouvre la fenetre avec la liste des fichiers à cocher    ############################
def Set_Source_Folder():
  Source_folder=open_folder()
  Source_Browse_Value.set(Source_folder)
  fileslist_check_function(Source_folder)

Source_Browse_Value = StringVar()
Source_Browse_Value.set('Videos Source Folder')
Source_Browse_Entry = tk.Entry(root, textvariable=Source_Browse_Value,  bg=RGB((90,90,90)), fg=RGB((255,255,255)))
Source_Browse_Entry.place(x=10, y=PositionY[2], width=500, height=25)  
Source_Browse_Button=tk.Button(root, text="Browse", command=Set_Source_Folder, pady=2, padx=10)
Source_Browse_Button.place(x=520, y=PositionY[2], width=90, height=25) 


####################      Liste des fichiers / Fenetres des fichiers à traiter     #############################################################################

def fileslist_check_function(sourcepath):
  #nombre de fichier pour déterminer la taille de la fenetre
  fileslist=get_files_list(sourcepath)
  files_number=len(fileslist)

  #Création du canvas > frame > canvas > cases à cocher
  root_frame_fileslist=tk.Frame(root, bg= RGB((30,30,30)), relief=FLAT)
  root_frame_fileslist.place(x=620, y=0, width=500, height=300)
  canvas_fileslist=tk.Canvas(root_frame_fileslist, bg= RGB((30,30,30)), highlightthickness=0, borderwidth=0)
  scrollbar_fileslist = tk.Scrollbar(root_frame_fileslist, orient=VERTICAL)
  scrollbar_fileslist.pack(side = RIGHT, fill = Y)
  scrollbar_fileslist.config(command=canvas_fileslist.yview)
  canvas_fileslist.config(width=500, height=files_number*25, yscrollcommand=scrollbar_fileslist.set, scrollregion=(0,0,500,files_number*25))
  canvas_fileslist.pack(side=LEFT,expand=True,fill= BOTH)
  frame_fileslist = tk.Frame(canvas_fileslist, bg= RGB((30,30,30)))
  canvas_fileslist.create_window(0,0, window=frame_fileslist, anchor="nw")
  
  #Création des cases à cocher
  
  global file_Check_Vars
  global file_Check_Buttons
  file_Check_Vars=[]
  file_Check_Buttons=[]
  for fileindex,file in enumerate(fileslist):
    file_Check_Vars.append(IntVar(value=1))
    file_Check_Buttons.append("file_Check_Button_"+str(fileindex))
    globals()[f'{file_Check_Buttons[fileindex]}']=tk.Checkbutton(frame_fileslist, text=file, pady=1, padx=10, bg= RGB((30,30,30)), fg= RGB((200,200,200)), onvalue=int(1), offvalue=int(0), selectcolor="black", anchor=W, variable = file_Check_Vars[fileindex])
    globals()[f'{file_Check_Buttons[fileindex]}'].pack(side=TOP, anchor=W)#.place(x=0, y=10+fileindex*20, width=480, height=20)


###########Set Destination folder avec bouton parcourir#########################################################################################################

def Set_Destination_Folder():
   Destination_folder=open_folder()
   Destination_Browse_Value.set(Destination_folder)

Destination_Browse_Value = StringVar()
Destination_Browse_Value.set('Videos Destination Folder')
Destination_Browse_Entry = tk.Entry(root, textvariable=Destination_Browse_Value,  bg=RGB((90,90,90)), fg=RGB((255,255,255)))
Destination_Browse_Entry.place(x=10, y=PositionY[3], width=500, height=25)   
Destination_Browse_Button=tk.Button(root, text="Browse", command=Set_Destination_Folder, pady=2, padx=10)
Destination_Browse_Button.place(x=520, y=PositionY[3], width=90, height=25) 

######################       Entrée de temps / Définition des ranges avec champs de saisie et bouton + ############################################################

 

#define times range   
Start_Time=[]
End_Time=[]
Time_ranges_readable=[]
def Set_Times_Ranges():
  global Start_Time
  global End_Time
  global Time_ranges_readable
  try: Start_Time
  except NameError:
    Start_Time=[]
    End_Time=[]
    Time_ranges_readable=[]
  else:
    if start_time_entry.get() != "" and len(Start_Time)<5: 
      Start_Time.append(str(int(start_time_entry.get())*90000))
      End_Time.append(str(int(end_time_entry.get())*90000))
      Time_ranges_readable.append(str(int(start_time_entry.get()))+'s to '+str(int(end_time_entry.get()))+'s , ')
  Time_Range_label.config(text=Time_ranges_readable)

#########################################Times button & Labels############################################################
Split_method_var = IntVar()
Split_method_Buttons = tk.Checkbutton(root, text="Change ranges", pady=1, padx=10, bg= RGB((30,30,30)), fg= RGB((200,200,200)), onvalue= 1, offvalue= 0, selectcolor="black", anchor=W, variable = Split_method_var)
Split_method_Buttons.place(x=0, y=PositionY[5], width=120, height=20)

time_label = tk.Label(root, text="Start to  End Time (s) :",  bg=RGB((30,30,30)), fg=RGB((255,255,255)), anchor="w")
time_label.place(x=150, y=PositionY[5], width=150, height=20)

start_time_entry_var=""
start_time_entry = tk.Entry(root, textvariable=start_time_entry_var,  bg=RGB((90,90,90)), fg=RGB((255,255,255)))
start_time_entry.place(x=310, y=PositionY[5], width=40, height=20)

end_time_entry_var=""
end_time_entry = tk.Entry(root, textvariable=end_time_entry_var,  bg=RGB((90,90,90)), fg=RGB((255,255,255)))
end_time_entry.place(x=360, y=PositionY[5], width=40, height=20)

Remove_Time_Range_Button = tk.Button(root, text="-", command = Set_Times_Ranges, pady=5, padx=10, font=("helvetica 12 bold"))
Remove_Time_Range_Button.place(x=420, y=PositionY[5], width=20, height=20) 
Add_Time_Range_Button = tk.Button(root, text="+", command = Set_Times_Ranges, pady=5, padx=10, font=("helvetica 12 bold"))
Add_Time_Range_Button.place(x=450, y=PositionY[5], width=20, height=20) 

Time_Range_label = tk.Label(root, text="No time range set",  bg=RGB((60,60,60)), fg=RGB((255,255,255)), anchor="w")
Time_Range_label.place(x=10, y=PositionY[6], width=500, height=20)

########################       Changer les paramètres de coupure    ###########################################################################################################



#########################            Fonction => Make JSON 2        ######################################################################################################
##########################################################################################################################################################################
##########################################################################################################################################################################
 #files variables
def JSON_make(file_Check_Vars):
  JSONContent=[]
  sourcepath=Source_Browse_Entry.get()
  destpath=Destination_Browse_Entry.get()  

  fileslist=get_files_list(sourcepath)

  fileslisttoprocess=[]
  for i,file in enumerate(fileslist):
    if file_Check_Vars[i].get() == 1:
        fileslisttoprocess.append(file)
  #récupérer la variable pour savoir si on splitte par chapitre ou en fonction du temps      
  Split_method=Split_method_var.get()
  #Formatage des elements à intégrer dans le JSON
  destination_dict_file=destination_dict["File"]
  dest_ext=destination_dict_file[-4:]


  #process JSON
  
  Split_method=Split_method_var.get()

  #creation de dictionnaire temporaire  

  
  if Split_method == 0:

    for filename in fileslisttoprocess:
      filename_noext=filename[:-4]
      source_dict["Path"]=sourcepath+'\\'+filename
      destination_dict["File"]=destpath+'\\'+ filename_noext+'_1'+dest_ext
      JSONContent.append(copy.deepcopy(main_dict))

  if Split_method == 1:
    for filename in fileslisttoprocess:
      filename_noext=filename[:-4]
      source_dict["Path"]=sourcepath+'\\'+filename
      destination_dict["File"]=destpath+'\\'+ filename_noext+'_1'+dest_ext
      for RangeIndex in enumerate(Start_Time):
        range_dict["Type"]="time"
        range_dict["Start"]=Start_Time[RangeIndex]
        range_dict["End"]=End_Time[RangeIndex]
        JSONContent.append(copy.deepcopy(main_dict))
  return JSONContent  
######################################################## Button => Lance la fabrication du Fichier JSON, formate et Lance le preview #############################

def Make_JSON_Press():
  global JSONFormatedContent
  JSONContent=JSON_make(file_Check_Vars)
  JSONFormatedContent=json.dumps(JSONContent, indent=2)
  Preview_Window(JSONFormatedContent)
Preview_Button=tk.Button(root, text="Make and Preview JSON", command=Make_JSON_Press, pady=2, padx=10)
Preview_Button.place(x=10, y=PositionY[7], width=500, height=25) 


########################################################### Fonction => Ecrit le JSON ################################################################ 
def write_JSONfile():
  JSONFile =open(Source_Browse_Entry.get()+"\\handbrake.JSON", "w")
  JSONFile.write(str(JSONFormatedContent))
  JSONFile.close  
#JSON_Write_Button=tk.Button(root, text="Write JSON", command=write_JSONfile, pady=2, padx=10)
#JSON_Write_Button.place(x=10, y=PositionY[6], width=600, height=25)   


########################################################### Bouton => Lance la fonction d'écriture du fichier JSON +  Lance HandrakeCLI  ################################################################
def LaunchHandbrake():
  write_JSONfile()
  cmd='C:\\Program Files\\HandBrake\\HandBrakeCLI.exe', r'--queue-import-file' ,Source_Browse_Entry.get()+r'\handbrake.JSON'
  subprocess.Popen(cmd)
LaunchHandbrake_Button=tk.Button(root, text="Launch Handbrake", command=LaunchHandbrake, pady=2, padx=10)
LaunchHandbrake_Button.place(x=10, y=PositionY[8], width=500, height=25) 

########################################################

root.mainloop()