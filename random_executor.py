import os
import random
import PySimpleGUI as sg

# Set Theme
sg.theme("Material1")

# By default path is set to current working directory
path = os.getcwd()

layout = [
    [sg.Text("Source Directory")], 
    [sg.Text("Path: "+ path, size=(40,1), key='-OUTPUT-'), sg.Button("Browse")],
    [sg.Checkbox("Look in subdirectories?", key='-OPTION-', default=False, text_color="black")],
    [sg.Button("Execute!"), sg.Button("Quit")]
]

# Create the window
window = sg.Window("Random Executor", layout)
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Quit":
        break

    if event == "Browse":
        path = sg.PopupGetFolder("Choose a Directory")
        if path != None and path != "":
            window['-OUTPUT-'].update("Path: " + path)

    if event == "Execute!":
        file = ""
        files = []
        # If the user wants subdirs, else if they don't
        if values['-OPTION-']:
            # Get all files and subdirectories and their files
            folders_and_files = [(names[0], names[2]) for names in os.walk(path)]
            # Append folder path to each filename
            for folder_and_files in folders_and_files:
                folder = folder_and_files[0]
                filenames = folder_and_files[1]
                files += [folder + "/" + filename for filename in filenames]
            # Choose a random file
            if len(files) != 0:
                file = files[random.randint(0, len(files)-1)]
        else:    
            # Get names of all files that aren't directories
            files = [filename for filename in os.listdir(path) if not os.path.isdir(filename)]
            if len(files) != 0:
                # Choose a random file and append absolute path to it
                file = path + "/" + files[random.randint(0, len(files)-1)]
        if os.name == "posix":
            # Unix command to open file
            os.system("xdg-open " + file)
        else:
            # Windows command to open file (work in progress)
            os.system(file)
            
# Finish up by removing from the screen
window.close()