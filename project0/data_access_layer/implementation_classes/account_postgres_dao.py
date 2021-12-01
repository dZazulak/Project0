from data_access_layer.abstract_classes.account_dao import AccountDAO
from util.database_connection import connection
from entities.account import Account


# class AccountPostgresDAO(AccountDAO):
#     def create_account(self, account: Account) -> Account:
#         sql = "insert into account values"