# Command-line Interface

import argparse
import random
import re
import string

import pyperclip
from loguru import logger

from .constants import DB_FILE
from .db_utils import DbUtils

# Description
_desc = """Welcome to Kaguya Password Manager!

%(prog)s - A bad password manager.

Stores and retrieves your passwords in a secure manner.

You may also check the strength of your passwords, or generate a strong password for your accounts.

"""


def create_argparser() -> argparse.ArgumentParser:
    kaguya_parser = argparse.ArgumentParser(
        prog="kaguya.py",
        description=_desc,
        usage="%(prog)s [options]",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    kaguya_parser.add_argument(
        "masterpass",
        nargs="?",  # this sets it to optional
        default="",  # required default value for nargs='?'
        type=str,
        help="master password",
    )

    kaguya_parser.add_argument(
        "-r",
        "--retrieve",
        type=str,  # this should be the account name to search for
        help="name of account to retrieve credentials for",
    )

    kaguya_parser.add_argument(
        "-e",
        "--edit",
        type=str,  # account name
        help="name of account to edit",
    )

    kaguya_parser.add_argument(
        "-d", "--delete", type=str, help="name of account to delete"
    )

    kaguya_parser.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="activate the insert function to create a new entry",
    )

    kaguya_parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="activate the password generator",
    )

    kaguya_parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="activate the password checker",
    )

    # kaguya_parser.add_argument(
    #     "-d",
    #     "--domain",
    #     type=str,
    #     help="domain that the account is used for",
    # )

    kaguya_parser.add_argument(
        "-u",
        "--username",
        type=str,
        help="username for the specified domain",
    )

    kaguya_parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="password for the specified username",
    )

    kaguya_parser.add_argument(
        "-mu",
        "--masteruser",
        type=str,
        help="login username for kaguya.py",
    )

    kaguya_parser.add_argument(
        "-mp",
        "--masterpass",
        type=str,
        help="login password for kaguya.py",
    )

    logger.debug("argparser created")

    return kaguya_parser


users = {}


class ArgsHandler:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.db_utils = DbUtils(DB_FILE)

    def dispatch(self):
        args = self.args  # create local ref
        db_utils = self.db_utils  # local ref

        if args.masterpass:
            logger.debug("master password found")
            # TODO validate main password
            pass
        elif args.retrieve:
            logger.debug("retrieve option found")
            res = db_utils.select_chika_by_name(args.retrieve)
            if len(res) == 0:
                print(f"No entries found for {args.retrieve}")
            elif len(res) == 1:
                # TODO print or pyperclip or something
                pass
            else:
                # TODO display results and ask which one to retrieve
                pass
        elif args.new:
            logger.debug("new option found")
            # TODO display some creation screen prompting for info
            pass
        elif args.edit:
            logger.debug("edit option found")
            res = db_utils.select_chika_by_name(args.retrieve)
            if len(res) == 0:
                print(f"No entries found for {args.retrieve}")
            elif len(res) == 1:
                # TODO display some editing interface i guess
                pass
            else:
                # TODO display results and ask which one to edit
                pass
        elif args.delete:
            logger.debug("delete option found")
            res = db_utils.select_chika_by_name(args.retrieve)
            if len(res) == 0:
                print(f"No entries found for {args.retrieve}")
            elif len(res) == 1:
                # TODO confirmation first
                # TODO delete the damned entry
                pass
            else:
                # TODO display results and ask which one to delete
                pass
        elif args.generate:
            logger.info("generate option found")
            self.generate()
        elif args.check:
            logger.info("check option found")
            self.check(args.password)
        else:
            logger.debug("no options were declared")
            # if we reach here, then no arguments were passed
            # TODO prompt for masterpass
            # display options selection screen
            pass

    def retrieve(self, domain, username):
        # TODO: Database linking
        pass

    def edit(self, domain, username):
        """
        Replaces a value with another value.

        Specification of the account credentials are required.

        Usage: kaguya.py [edit] [domain] [username]
        """
        self.retrieve(domain, username)
        logger.info("Account has been found.")
        replaced_val = str(
            input(
                "Enter 'd' to replace the domain, 'u' to replace the username, or 'p' to replace the password."
            )
        )
        replace_val = str(input("What do you want to replace it with?"))
        if replaced_val == "d":
            # TODO: Database linking
            pass
        if replaced_val == "u":
            # TODO: Database linking
            pass
        if replaced_val == "p":
            # TODO: Database linking
            pass

    def insert(self, domain, username, password):
        """
        Create a new entry in the database.

        Specification of the account credentials are required.

        Usage: kaguya.py [edit] [domain] [username] [password]
        """
        if not domain or not username or not password:
            print(
                f"You must provide an argument for the following: {'domain' if not domain else ''} {'username' if not username else ''} {'password' if not password else ''}"
            )
            exit()
        # TODO: Database linking
        pass

    # The password generator. Takes no arguments and outputs
    # a single string value which is the password.
    @staticmethod
    def generate() -> str:
        """
        Creates a password based on strong password criterias.

        Checks itself to be a strong password before being returned as a value.

        Usage: kaguya.py [generate]
        """
        upperletters = string.ascii_uppercase
        lowerletters = string.ascii_lowercase
        digits = string.digits
        symbols = r"[!#$%&'()*+,-.\^_`{|}~" + r'"]'
        allchar = upperletters + lowerletters + digits + symbols

        length = random.randint(8, 32)
        strong_password = [
            random.choice(upperletters),
            random.choice(lowerletters),
            random.choice(digits),
            random.choice(symbols),
        ]
        for i in range(length - 3):
            strong_password.append(random.choice(allchar))
        random.shuffle(strong_password)
        strong_password = "".join(strong_password)
        # Check that it is strong
        if not ArgsHandler.check(strong_password):
            ArgsHandler.generate()
        else:
            print("Password generated and copied to the clipboard.")
            pyperclip.copy(strong_password)

    # The strong password checker. Takes the password as the only argument,
    #  outputs a boolean value on strength of password.
    @staticmethod
    def check(password) -> bool:
        """
        Verify the strength of a 'password'.

        Returns the strength of the password.

        A password is considered strong if:

        8 characters in length or more,
        1 digit or more,
        1 symbol or more,
        1 uppercase letter or more,
        1 lowercase letter or more.

        Usage: kaguya.py [check] [password]
        """
        # Check for input
        if not password:
            print("Please enter a password using the -p option.")
            exit()
        else:
            # Checks the length.
            length_error = len(password) < 8

            # Checks for digit.
            digit_error = re.search(r"\d", password) is None

            # Checks for symbol.
            symbol_error = re.search(r"\W", password) is None

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

            print("Password is strong.") if password_ok else print("Password is weak.")

            return password_ok

    @staticmethod
    def login_account(masteruser, masterpass) -> bool:
        logstat = False
        tries = 5

        print("Welcome to Kaguya Password Manager!")

        while logstat == False:
            if masteruser in users:
                if users[masteruser] == masterpass:
                    print("Logged in successfully.")
                    logstat = True
                    return logstat
                else:
                    tries -= 1
                    if tries > 0:
                        prompt = str(
                            input(
                                "Username or password is incorrect, please try again or sign up using by pressing q."
                            )
                        )
                        if prompt.lower() == "q":
                            ArgsHandler.register_account()
                        else:
                            print(f"You have {tries} tries remaining.")
                    if tries == 0:
                        print(
                            "You have failed to login for the 5th time. Please try again in 15 minutes."
                        )
                        exit()
            else:
                tries -= 1
                if tries > 0:
                    prompt = str(
                        input(
                            "Username or password is incorrect, please try again or sign up using by pressing q."
                        )
                    )
                    if prompt.lower() == "q":
                        ArgsHandler.register_account()
                    else:
                        print(f"You have {tries} tries remaining.")
                if tries == 0:
                    print(
                        "You have failed to login for the 5th time. Please try again in 15 minutes."
                    )
                    exit()

    @staticmethod
    def register_account() -> None:
        username, password = (
            str(input("Enter username: ")),
            str(input("Enter password: ")),
        )
        users[username] = password
        print("Account successfully created.")


if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()
    ArgsHandler(args)
