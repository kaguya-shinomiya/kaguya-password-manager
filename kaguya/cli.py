# Command-line Interface

import argparse
import random
import re
import string
import sys

import pyperclip
from . import master_db
from loguru import logger
from argon2 import PasswordHasher, exceptions
from pathlib import Path

from .constants import DB_FILE
from .db_utils import Chika, DbUtils

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
ph = PasswordHasher()


class ArgsHandler:
    def __init__(self, args: argparse.Namespace, db_echo=True):
        self.args = args
        self.db_utils = DbUtils(DB_FILE, echo=db_echo)

    def dispatch(self):
        args = self.args  # create local ref
        db_utils = self.db_utils  # local ref

        while not args.masteruser and not args.masterpass:
            args.masteruser = input("Enter username: ")
            args.masterpass = input("Enter password: ")

        logger.info(f"{args.masteruser} and {args.masterpass} found.")

        if args.masteruser and args.masterpass:
            if ArgsHandler.login_account(args.masteruser, args.masterpass):
                if args.retrieve:
                    logger.debug("retrieve option found")
                    res = db_utils.select_chika_by_name(args.retrieve)
                    logger.debug(res)
                    if len(res) == 0:
                        print(f"No entries found for {args.retrieve}")
                    elif len(res) == 1:
                        logger.info(f"Found 1 entry for {args.retrieve}")

                        # TODO print or pyperclip or something
                        pass
                    else:

                        def get_selection() -> Chika:
                            selection = input(
                                "Select an account number (press Enter to exit): "
                            )
                            if selection == "":  # they pressed
                                logger.info("exiting program")
                                sys.exit()
                            if not selection.isnumeric():
                                logger.error(f"received invalid number '{selection}'")
                                return get_selection()
                            try:
                                selected_chika = res[int(selection) - 1]
                                logger.info(f"Selected account: {selected_chika}")
                                return selected_chika
                            except IndexError:
                                logger.error(f"selecction {selection} is out of range!")
                                return get_selection()

                        for i, entry in enumerate(res, 1):
                            print(f"{i}) {entry.username}")
                        print(f"Found {len(res)} entries for {args.retrieve}")
                        chika = get_selection()
                        pyperclip.copy(chika.password)
                        logger.info("password copied to clipboard")
                        return chika.password

                elif args.new:
                    logger.debug("new option found")
                    # TODO display some creation screen prompting for info
                    print("Creating a new account")
                    new_chika_name = input("Name of new account: ")
                    new_username = input("Username: ")
                    new_password = input("Password (hit Enter to auto-generate): ")
                    new_domain = input("Domain (optional): ") or None

                    if not new_password:
                        # TODO auto-gen password
                        pass

                    db_utils.create_chika(
                        name=new_chika_name,
                        username=new_username,
                        password=new_password,
                        domain=new_domain,
                    )

                    logger.debug(f"Created new entry for {new_chika_name}")
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
                        chika = res[0]
                        print(
                            f"found 1 entry for {args.retrieve} with username '{chika.username}'"
                        )
                        confirmation = input("confirm delete? (y/n) ")

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

        DB_FILE = Path(__file__).parent / "data" / "testmasteruser.db"
        masterdb = master_db.MasterDbUtils(DB_FILE)

        print("Welcome to Kaguya Password Manager!")

        # Problem:
        # If conflicting master username exists, a list of accounts is returned.

        if masterdb.select_account_by_masteruser(
            masteruser
        ):  # check if the username is in the database
            account = masterdb.select_account_by_masteruser(masteruser)[0]
            dbpass = account.masterpass  # retrieve the password in database
            try:
                logstat = ph.verify(dbpass, masterpass)  # compare the passwords
                if logstat:
                    print("Logged in successfully.")
                    masterdb.close_session()
                    return logstat
            except exceptions.VerifyMismatchError:
                prompt = str(
                    input(
                        "Username or password is incorrect, please try again or sign up using by pressing q. \n"
                    )
                )
                if prompt.lower() == "q":
                    ArgsHandler.register_account()
                else:
                    masterdb.close_session()
                    exit()
        else:
            prompt = str(
                input(
                    "Username or password is incorrect, please try again or sign up using by pressing q. \n"
                )
            )
            if prompt.lower() == "q":
                ArgsHandler.register_account()
            else:
                masterdb.close_session()
                exit()

    @staticmethod
    def register_account() -> None:
        DB_FILE = Path(__file__).parent / "data" / "testmasteruser.db"
        masterdb = master_db.MasterDbUtils(DB_FILE)

        def inputs():
            username, password = (
                str(input("Enter username: ")),
                str(input("Enter password: ")),
            )
            hash = ph.hash(password)
            return (username, hash)

        accountsuccess = False
        while not accountsuccess:
            credentials = inputs()
            if masterdb.create_account(credentials[0], credentials[1]):
                print(hash)
                print("Account successfully created.")
                masterdb.close_session()
                accountsuccess = True
                print("Please try logging in with your new account.")


if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()
    ArgsHandler(args)
