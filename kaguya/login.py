users = {}


class User:
    def __init__(self, username=None, password=None) -> None:
        self.username = username
        self.password = password
        users[self.username] = self.password

    @staticmethod
    def login_account() -> bool:
        logstat = False
        tries = 5

        print("Welcome to Kaguya Password Manager!")

        while logstat == False:
            username, password = (
                str(input("Enter username.")),
                str(input("Enter password.")),
            )
            if username in users:
                if users[username] == password:
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
                            User.register_account()
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
                        User.register_account()
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
        User(username, password)
        print("Account successfully created.")


User.login_account()
