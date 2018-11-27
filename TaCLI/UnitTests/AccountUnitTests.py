import unittest
from TaCLI.TextFileInterface import TextFileInterface
from TaCLI.Components.AccountCommands import CreateAccount, DeleteAccount, ViewAccounts
from TaCLI.Components.EditInfo import EditInfo
from TaCLI.Environment import Environment
from TaCLI.User import User
from TaApp.DjangoModelInterface import DjangoModelInterface


class CreateAccountUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_create_account_correct_args(self):
        self.environment.user = User("root", "administrator")
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNotNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "Account created.")

    def test_create_account_no_permissions(self):
        self.environment.user = User("ta_acct", "TA")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "ERROR")

    def test_create_account_not_logged_in(self):
        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertIsNone(self.environment.database.get_user(user_name))
        self.assertEqual(response, "ERROR")

    def test_create_account_account_exists(self):
        self.environment.user = User("root", "administrator")
        user_name = "new_user"
        self.environment.database.create_account(user_name, "password", "TA")

        create_account = CreateAccount(self.environment)
        response = create_account.action(["create_account", user_name, "password", "TA"])

        self.assertEqual(response, "ERROR")

    def test_create_account_not_enough_args(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        response = create_account.action(["create_account"])

        self.assertEqual(response, "ERROR")

        user_name = "new_user"
        response = create_account.action(["create_account", user_name])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))

        response = create_account.action(["create_account", user_name, "password"])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_create_account_invalid_role(self):
        self.environment.user = User("root", "administrator")

        create_account = CreateAccount(self.environment)
        user_name = "new_user"
        response = create_account.action(["create_account", user_name, "password", "invalid_role"])

        self.assertEqual(response, "ERROR")
        self.assertIsNone(self.environment.database.get_user(user_name))


class DeleteAccountUnitTests(unittest.TestCase):

    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()
        self.environment.database.create_account("root", "root", "administrator")

    def test_delete_account_correct_args(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "Account deleted.")
        self.assertIsNone(self.environment.database.get_user(user_name))

    def test_delete_account_that_doesnt_exist(self):
        self.environment.user = User("root", "administrator")
        user_name = "nonexisting_account"

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "ERROR")

    def test_delete_account_no_permissions(self):
        self.environment.user = User("TA_user", "TA")

        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))

    def test_delete_account_not_logged_in(self):
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account", user_name])

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))

    def test_delete_account_no_args(self):
        self.environment.user = User("root", "administrator")
        user_name = "existing_account"
        self.environment.database.create_account(user_name, "password", "TA")

        delete_command = DeleteAccount(self.environment)
        response = delete_command.action(["delete_account"])

        self.assertEqual(response, "ERROR")
        self.assertIsNotNone(self.environment.database.get_user(user_name))


class ViewAccountsUnitTests(unittest.TestCase):
    def setUp(self):
        tfi = TextFileInterface(relative_directory="TestDB/")
        self.environment = Environment(tfi)
        self.environment.database.clear_database()

    def test_view_accounts_none_in_database(self):
        self.environment.user = User("root", "administrator")
        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response, "")

    def test_view_accounts_3_valid_in_database(self):
        self.environment.user = User("root", "administrator")
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])

        self.assertEqual(response,  "InstructorUser - instructor\n" +
                                    "AdministratorUser - administrator\n" +
                                    "SupervisorUser - supervisor\n")

    def test_view_accounts_not_logged_in(self):
        self.environment.database.create_account("InstructorUser", "password", "instructor")
        self.environment.database.create_account("AdministratorUser", "password", "administrator")
        self.environment.database.create_account("SupervisorUser", "password", "supervisor")

        view_command = ViewAccounts(self.environment)
        response = view_command.action(["view_accounts"])
        self.assertEqual(response, "ERROR")


class EditInfoUnitTests(unittest.TestCase):

    def setUp(self):
        di = DjangoModelInterface()
        self.environment = Environment(di)
        self.environment.database.clear_database()
        self.environment.user = User("root", "administrator")

    def test_edit_info_wrong_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info"])
        self.assertEqual(response, "ERROR")

    def test_edit_info_phone_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "phone", "1234567"])
        self.assertEqual(response, "Phone Number has been updated successfully")

    def test_edit_info_address_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "address", "1234 Street City, State 53202"])
        self.assertEqual(response, "Address has been updated successfully.")

    def test_edit_info_email_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "email", "john3885@uwm.edu"])
        self.assertEqual(response, "Email has been updated successfully.")

    def test_edit_info_office_hours_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "office_hours", "MW", "10-12"])
        self.assertEqual(response, "Office Hours have been updated successfully.")

    def test_edit_info_name_correct_args(self):
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "name", "MW", "10-12"])
        self.assertEqual(response, "Name has been updated successfully.")

    def test_edit_account_not_logged_in(self):
        self.environment.user = None
        edit_info_command = EditInfo(self.environment)
        response = edit_info_command.action(["edit_info", "name", "MW", "10-12"])
        self.assertEqual(response, "ERROR")
