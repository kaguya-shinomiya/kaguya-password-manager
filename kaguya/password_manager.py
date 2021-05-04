import pyperclip

# Test variables.
domain = "email.com"
user1 = "username1"
pw1 = "password1"

# This is the database.
# placeholder
database = {}


class dbEntry:
    def __init__(self, domain_name, username, password):
        self.domain_name = domain_name
        self.username = username
        self.password = password
        database.update({domain_name: {username, password}})

    # This is the input method for a new username.
    def newusername(self, domain_name, username):
        self.newusername = username
        database[domain_name][self.newusername] = ""

    # This is the search method for an existing username.
    def searchusername(self, domain_name, username):
        if username in database[domain_name]:
            print(f"{username} was found in the database.")
            prompt_copypass = str(
                input(
                    "Copy password to clipboard? (Enter Y to proceed or any other button to exit the program.)"
                )
            )

            if prompt_copypass.lower() == "y":
                pyperclip.copy(database[domain_name][username])
                print("Password copied to clipboard!")

    # This is the input method for a new password.
    def newpassword(self, domain_name, username, password):
        pass

    # This is the input function for a new domain.
    def newdomain(self, domain_name):
        self.newdomain = domain_name
        database[self.newdomain] = {}
        return "Domain has been created in the database!"


# This is the search function for an existing domain.
def searchdomain(self, domain_name):
    if domain_name in database:
        print(f"{domain_name} was found in the database.")
        # If we have reached this point,
        # we have found the domainname in the database.
        # We now want to retrieve the username, and subsequently the password.
        return database[domain_name]
    # else:
    # print(f"{domain_name} was not found in the database.")
    # prompt_domcreate = str(
    # input(
    # "Create new domain in the database? (Enter Y to proceed or any other button to restart the search.)"
    # )
    # )
    # if prompt_domcreate.lower() == "y":
    # self.newdomain(domain_name)
    # self.searchdomain(domain_name)


def main():
    pass
