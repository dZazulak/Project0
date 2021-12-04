from data_access_layer.abstract_classes.account_dao import AccountDAO
from util.database_connection import connection
from entities.account import Account


class AccountPostgresDAO(AccountDAO):
    def create_account(self, account: Account) -> Account:
        sql = "insert into account values(%s, default, %s) returning account_id"
        cursor = connection.cursor()
        cursor.execute(sql, (account.balance, account.customer_id))
        connection.commit()
        account_id = cursor.fetchone()[0]
        account.account_id = account_id
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        sql = "select * from account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        account_record = cursor.fetchone()
        account = Account(*account_record)
        return account

    def get_all_accounts(self) -> list[Account]:
        sql = "select * from account"
        cursor = connection.cursor()
        cursor.execute(sql)
        account_records = cursor.fetchall()
        account_list = []
        for account in account_records:
            account_list.append(Account(*account))
        return account_list

    def deposit_into_account_by_id(self, account: Account) -> Account:
        sql = "select balance from account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [account.account_id])
        balance = cursor.fetchone()[0]
        account.balance += balance

        sql = "update account set balance = %s where account_id = %s returning balance"
        cursor.execute(sql, (account.balance, account.account_id))
        connection.commit()
        return account

    def withdraw_from_account_by_id(self, account: Account) -> Account:
        sql = "select balance from account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [account.account_id])
        balance = cursor.fetchone()[0]
        new_balance = balance - account.balance

        sql = "update account set balance = %s where account_id = %s returning balance"
        cursor.execute(sql, (new_balance, account.account_id))
        account.balance = cursor.fetchone()[0]
        connection.commit()
        return account

    def transfer_money_between_accounts_by_their_ids(self, transfer_account: Account, receiver_account: Account,
                                                     balance_transferred: float):
        sql = "select balance from account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [transfer_account.account_id])
        transfer_account_balance = cursor.fetchone()[0]

        sql = "select balance from account where account_id = %s"
        cursor.execute(sql, [receiver_account.account_id])
        receiver_account_balance = cursor.fetchone()[0]
        receiver_account_balance.balance += balance_transferred
        new_transfer_account_balance = balance_transferred - transfer_account_balance.balance

        sql = "update account set balance %s where account_id = %s returning balance"
        cursor.execute(sql, (receiver_account_balance.balance, receiver_account.account_id))
        receiver_account_balance.balance = cursor.fetchone()[0]

        sql = "update account set balance %s where account_id = %s returning balance"
        cursor.execute(sql, (new_transfer_account_balance, transfer_account.account_id))
        transfer_account_balance.balance = cursor.fetchone()[0]
        connection.commit()
        return self.transfer_money_between_accounts_by_their_ids(transfer_account, receiver_account, balance_transferred
                                                                 )

    def delete_account_by_id(self, account_id: int) -> bool:
        sql = "delete from account where account_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [account_id])
        connection.commit()
        return True
