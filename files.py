import os
from PIL import Image, ImageSequence




def countFiles(folder_path):
    file_count = 0
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file():
                file_count += 1
    return file_count
"""
def findPath(item_name, start_dir="."):
    
    for root, dirs, files in os.walk(start_dir):
        if item_name in files:
            return os.path.join(root, item_name)  # It's a file
        if item_name in dirs:
            return os.path.join(root, item_name)  # It's a folder
    return None
"""
def findFile(filename, start_dir="."):

    
    for root, dirs, files in os.walk(start_dir):
        if filename in files:
            found_path = os.path.join(root, filename)
            return found_path
    
    
    return None

def importImage(path):  #path is a folder path (standby mode folder/ drift mode folder)

    image_index = 0

    #ask user for image
    image_name = input("Enter the name of your image file: ")
    image_path = findFile(image_name)
    
    if image_path == None:
        return False


    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File not found at: {image_path}")
        return False
    
    # Check if output folder exists
    if not os.path.exists(path):
        print(f"Error: Output folder not found: {path}")
        return False


    try:
        #finding image type
        image_format = ""
        with Image.open(image_path) as im:
            image_format = im.format

        if image_format in ["JPEG", "PNG", "JPG"]:

            #open image file
            with Image.open(image_path ) as im:    
                
                #convert frame to RGBA to handle transparency correctly
                image = im.convert("RGBA")          #image now holds the handled image    


                output_path = os.path.join(path, f"{image_index}.png")
                image_index += 1

                # Save image
                image.save(output_path, "PNG")
            
            return True
        
        elif image_format == "GIF":
                # Open the GIF file
            try:
                image = Image.open(image_path)
            except FileNotFoundError:
                print(f"Error: The file '{image_path}' was not found.")
                return
            except Exception as e:
                print(f"Error opening image: {e}")
                return

            frames_list = []
            
            # Iterate through the frames using ImageSequence
            for frame in ImageSequence.Iterator(image):
                # Convert frame to RGBA to handle transparency correctly
                new_frame = frame.convert("RGBA")
                frames_list.append(new_frame)
                
                # Define the output file path
                # Use a consistent naming convention (e.g., frame_001.png)
                output_path = os.path.join(path, f"{image_index}.png")
                
                # Save the frame as a PNG file
                try:
                    new_frame.save(output_path, "PNG")
                except Exception as e:
                    print(f"Error saving frame {image_index}: {e}")
                    
                image_index += 1
            
            image.close()
            return True
        
        else:
            print("Please enter a file with file type 'JPEG'/'PNG'/'GIF'")
            return False
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

    




def createFolder(text):

    #make new character folder
    current_path = os.path.dirname(os.path.abspath("characters"))
    character_path = os.path.join(current_path, "./characters")
    folder_path = os.path.join(character_path, text)
    os.makedirs(folder_path, exist_ok=True)
    standby_path = os.path.join(folder_path, "standby_mode")
    os.makedirs(standby_path, exist_ok=True)
    drift_path = os.path.join(folder_path, "drift_mode")
    os.makedirs(drift_path, exist_ok=True)

    #make standby mode folder

    print("We will now make the standby mode of the new character")
    standbySuccess = False

    while not standbySuccess:
        standbySuccess = importImage(standby_path)


    #make drift mode folder
    print("We will now make the drift mode of the new character")

    driftSuccess = False
    
    while not driftSuccess:
        driftSuccess = importImage(drift_path)
    
    return folder_path





def findCharacter():

    #create list of characters
    character_list=[]
    unamed_character = 0

    folder_path = "characters"
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_dir():
                if entry.name.startswith("unnamed_character"):
                    unamed_character += 1
                character_list.append(entry.name)


    #get user's input 
    text = input("input the character's name \n'N/A' for new character \ndefault character otherwise\n")

    if text != "N/A":

        #vaild character's name
        for name in character_list:
            if (name == text):
                character_path = os.path.join("characters", name)
                if os.path.exists(character_path):
                    return character_path
            
        #invalid character's name(default)
        default_path = os.path.join("characters", "oiiai")
        if os.path.exists(default_path):
            return default_path

    #add new character
    else: 
        new_name = input("Enter the name of your new character: ")
        if new_name == None:
            unamed_character += 1
            new_name = f"unnamed_character{unamed_character}"
        path = createFolder(new_name)
        return path
        


