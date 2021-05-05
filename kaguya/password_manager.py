import pyperclip, argparse, os, sys, random, string

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


# The strong password checker. Takes the password as the only argument.
def password_check(password):
    """
    Verify the strength of a 'password'.
    Returns the strength of the password.
    A password is considered strong if:
        At least 8 characters in length.
        1 digit or more.
        1 symbol or more.
        1 uppercase letter or more.
        1 lowercase letter or more.
    """
    # Checks the length.
    length_error = len(password) < 8 or len(password)

    # Checks for digit.
    digit_error = re.search(r"\d", password) is None

    # Checks for symbol.
    symbol_error = re.search(r"[!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None

    # Checks for uppercase letter.
    uppercase_error = re.search(r"[A-Z]", password) is None

    # Checks for lowercase letter.
    lowercase_error = re.search(r"[a-z]", password) is None

    # Overall result
    password_ok = not (
        length_error
        or digit_error
        or symbol_error
        or uppercase_error
        or lowercase_error
    )

    return password_ok


# The password generation function. Takes no arguments and outputs a single strong password.
def generate():
    """
    Creates a password based on above criteria.
    Checks itself to be a strong password before being returned as a value.
    """
    strong_password = []
    password_characters = (
        string.ascii_letters + string.digits + r"[!#$%&'()*+,-./[\\\]^_`{|}~" + r'"]'
    )
    length = random.randint(8, 32)
    for i in range(length + 1):
        strong_password.append(random.choice(password_characters))
    strong_password = "".join(password)
    # Check that it is strong
    if not password_check(strong_password):
        generate()
    else:
        return strong_password


# Command-line Interface Arguments:

# Create the parser
kaguya_parser = argparse.ArgumentParser(
    prog="password_manager.py", description="A bad password manager"
)

# Add the arguments
kaguya_parser.add_argument(
    "-d",
    "--domain",
    metavar="",
    type=str,
    help="Domain that the account belongs to. Used for insertion and search functions.",
)

kaguya_parser.add_argument(
    "-u",
    "--username",
    metavar="",
    type=str,
    help="Username for the specified domain. Used for insertion and search functions.",
)

kaguya_parser.add_argument(
    "-p",
    "--password",
    metavar="",
    type=str,
    help="Password for the specified username. Used for insertions.",
)

kaguya_parser.add_argument(
    "-g",
    "--generate",
    action="store_true",
    help="Generates a strong password. Intended for use without any other arguments.",
)

# Execute the parse_args() method
args = kaguya_parser.parse_args()


def main():
    pass
