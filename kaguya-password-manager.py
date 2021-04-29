import pyperclip as clip


# This is the database.
database = {}

# This is the input function for a new domain.
def kaguya_newdomain():
    newdomain = str(input("Please enter the new domain name: "))
    database[newdomain] = {}


# This is the input function for a new username.
def kaguya_newusername(domainname):
    newusername = str(input("Please enter the new username: "))
    newpassword = str(input("Please enter the new password: "))
    database[domainname][newusername] = newpassword


# This is the search function for an existing domain.
def kaguya_existingdomain():
    domainname = str(input("Please enter a domain name to begin the search: "))
    if domainname in database:
        print(f"{domainname} found in database.")
        # If we have reached this point, we have found the domainname in the database.
        # We now want to retrieve the username, and subsequently the password.
        kaguya_existingusername(domainname)
    else:
        print(f"{domainname} was not found in database.")
        confirm_domaincreation = str(
            input(
                "Create new domain in the database? (Enter Y to proceed or any other button to restart the search.)"
            )
        )
        if confirm_domaincreation.lower() == "y":
            kaguya_newdomain()
            print("Domain has been saved into the database!")
        else:
            kaguya_existingdomain()


def kaguya_existingusername(domainname):
    username = str(input("Please enter the username: "))
    if username in database[domainname]:
        clip.copy(database[domainname][username])
        print(
            f"{username} found in database under {domainname}. Password copied to clipboard!"
        )
