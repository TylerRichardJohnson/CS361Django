from TaCLI.Components import Command


class CreateAccount(Command.Command):

    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["create_account", "username", "password", "role"]
    """

    def action(self, args):

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["supervisor", "administrator"]:
            return "Permission Denied."

        if len(args) != 4:
            return "Invalid Arguments.\nCorrect Parameters: create_account <USERNAME> <PASSWORD> <ROLE>"

        if self.environment.database.get_user(args[1]) is not None:
            return "Username is already taken."

        if not self.environment.database.is_valid_role(args[3]):
            self.environment.debug("Invalid Role")
            return "Invalid Role.\nValid Roles: administrator, supervisor, instructor, TA"

        self.environment.database.create_account(args[1], args[2], args[3])

        return "Account created."


class DeleteAccount(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        args is a list containing the following:
            ["delete_account", username]
    """

    def action(self, args):

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            return "Permission denied."

        if len(args) != 2:
            return "Invalid arguments.\nCorrect Parameters: delete_account <USERNAME>"

        if self.environment.database.get_user(args[1]) is None:
            return "User to delete doesn't exist."

        self.environment.database.delete_account(args[1])
        return "Account deleted."


class ViewAccounts(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        takes no arguments and returns list of all accounts in database like:
            Username Role
            Username Role
    """

    def action(self, args):
        result = ""

        if len(args) != 1:
            return "Invalid arguments."

        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if self.environment.user.get_role() not in ["administrator", "supervisor"]:
            return "Permission denied"

        accounts = self.environment.database.get_accounts()
        for account in accounts:
            result += f"{account['name']} {account['role']}\n"
        return result


class ViewInfo(Command.Command):
    def __init__(self, environment):
        self.environment = environment

    """
        if has no arguments, return logged in user's information:
            Username, Role, Email, Office hours, Address, Phone           

        if has one argument and argument is a valid user,

            if user is administrator or supervisor, return all information:
                Username, Role, Email, Office hours, Address, Phone

            if user is not administrator or supervisor, return public information:
                Username, Role, Email, Office hours
    """

    def action(self, args):
        if self.environment.user is None:
            return "You must be logged in to perform this action."

        if len(args) == 1:
            user = self.environment.database.get_user(self.environment.database.get_logged_in())
            return self.environment.database.get_private_info(user)
        else:
            user = self.environment.database.get_user(args[1])
            if user is not None:
                if self.environment.user.get_role() not in ["administrator", "supervisor"]:
                    return self.environment.database.get_private_info(user)
                else:
                    return "private information"
            else:
                return "That user does not exist."
