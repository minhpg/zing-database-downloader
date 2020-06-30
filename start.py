from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from os import path


def create_credential():
    auth_and_save_credential()


# Authentication + token creation
def create_drive_manager():
    gAuth = GoogleAuth()
    typeOfAuth = None
    if not path.exists("credentials.txt"):
        typeOfAuth = input("Nhập 'Y' để lưu file credentials mới: ")
    bool = True if typeOfAuth == "Y" or path.exists("credentials.txt") else False
    authorize_from_credential(gAuth, bool)
    drive: GoogleDrive = GoogleDrive(gAuth)
    return drive


def authorize_from_credential(gAuth, isSaved):
    if not isSaved: #no credential.txt wanted
        auth_no_save(gAuth)
    if isSaved and not path.exists("credentials.txt"):
        create_credential()
        gAuth.LoadCredentialsFile("credentials.txt")
    if isSaved and gAuth.access_token_expired:
        gAuth.LoadCredentialsFile("credentials.txt")
        gAuth.Refresh()
        print("Token đã được làm mới!")
        gAuth.SaveCredentialsFile("credentials.txt")
    gAuth.Authorize()
    print("Đã được cấp quyền GoogleAPI!")

def auth_and_save_credential():
    gAuth = GoogleAuth()
    gAuth.LocalWebserverAuth()
    gAuth.SaveCredentialsFile("credentials.txt")
def auth_no_save(gAuth):
    gAuth.LocalWebserverAuth()
# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = create_drive_manager()

# Create GoogleDriveFile instance with title 'Hello.txt'.
file1 = drive.CreateFile({'title': 'Hello.txt'})
file1.Upload()
print('title: %s, id: %s' % (file1['title'], file1['id']))
