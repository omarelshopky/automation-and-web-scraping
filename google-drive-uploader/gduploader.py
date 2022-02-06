from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import pandas as pd
import os 
import sys

# Where user profile pictures uploaded
GD_FOLDER_LINK = 'GOOGLE_DRIVE_DIRECTORY_LINK'
PICS_COLUMN_NAME = 'picurl' # In the generated csv
CSV_FILE_PATH =  'UsersWithoutSignaturesOU.csv' # sys.argv[1]


if len(sys.argv) == 3:
    
    PICS_PATH = sys.argv[1]
    OU_VALUE = sys.argv[2]     

    # Downloads all OUs onto a csv
    os.system('gam print orgs > medarbetare.csv')

    # Creates a csv and seperates out the users via ou and prints their current signature, for backup and to make sure we dont overwite peoples signature
    os.system('gam redirect csv ./staff_signatures.csv multiprocess csv medarbetare.csv gam ou ~orgUnitPath print signature')

    # Prints the metatdatafields to tag into the signature html phone, name etc
    os.system(f"gam csvkmd users ./staff_signatures.csv keyfield User matchfield isPrimary True skipfield signature '.+' print fields name,organizations,ou,phones,thumbnailPhotoUrl > {CSV_FILE_PATH}")

    # Download all users profile pictures
    os.system(f'gam all users get photo targetfolder {PICS_PATH}')

    # Read CSV file
    csv_file = pd.read_csv(CSV_FILE_PATH, sep = ",")

    # Add a new column for the profile picture uploaded on google drive
    csv_file.insert(len(csv_file.columns), PICS_COLUMN_NAME, "tempurl")

    # Creates local webserver and auto handles authentication.
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()       
    drive = GoogleDrive(gauth)
    

    # Extract the folder id from its link
    GD_folder_ID = GD_FOLDER_LINK.split('/')[-1]


    # Iterating thought all the Pics
    for file in os.listdir(PICS_PATH):
        try:
            gfile = drive.CreateFile({'title' : file, 'parents': [{'id': GD_folder_ID}]})
            gfile.SetContentFile(os.path.join(PICS_PATH, file))
            gfile.Upload()

            permission = gfile.InsertPermission({
                                'type': 'anyone',
                                'value': 'anyone',
                                'role': 'reader'})

            # Remove .jpg from file name
            file = file[: len(file) - 4]

            # Update Pic URL value in the dataframe
            csv_file[csv_file["primaryEmail"] == file] = csv_file[csv_file["primaryEmail"] == file].replace('tempurl', "https://drive.google.com/uc?export=view&id=" +gfile['id'])

            print(f"[+] Success Add {file} Picture URL")
        except:
            print(f"[-] Faild Add {file} Picture URL")

        # Empty the variable to prevent memory leak
        gfile = None


    # Save the generated CSV File
    csv_file.to_csv(CSV_FILE_PATH, index= False)

    # Setting everyone in the OU department and pushing the metadata that was scraped onto a signature template. 
    os.system(f'gam csv {CSV_FILE_PATH} matchfield orgUnitPath "^/{OU_VALUE}.*" gam user ~primaryEmail signature file SigTemplate_IT.txt html replace first ~name.givenName replace last ~name.familyName replace title ~organizations.0.title replace email ~primaryEmail replace phone ~phones.0.value replace pic ~{PICS_COLUMN_NAME}')
    
else:
    print("\nUsage: gduploader <PICS_DIR_PATH> <OU_VALUE>\n")
