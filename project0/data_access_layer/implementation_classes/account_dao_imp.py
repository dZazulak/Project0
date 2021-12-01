from data_access_layer.abstract_classes.account_dao import AccountDAO
from entities.account import Account


class AccountDAOImp(AccountDAO):
    account_one = Account(1000, 1, 1)
    account_two = Account(5, 2, 2)
    account_to_delete = Account(5000, 3, 3)

    account_list = [account_one, account_two, account_to_delete]

    account_id_generator = 4

    def create_account(self, account: Account) -> Account:
        account.account_id = AccountDAOImp.account_id_generator
        AccountDAOImp.account_id_generator += 1
        AccountDAOImp.account_list.append(account)
        return account

    def get_account_by_id(self, account_id: int) -> Account:
        for account in AccountDAOImp.account_list:
            if account.account_id == account_id:
                return account

    def get_all_accounts(self) -> list[Account]:
        return AccountDAOImp.account_list

    def deposit_into_account_by_id(self, account: Account) -> Account:
        for account_in_list in AccountDAOImp.account_list:
            if account_in_list.account_id == account.account_id:
                index = AccountDAOImp.account_list.index(account_in_list)
                AccountDAOImp.account_list[index] = account
                return account

    def withdraw_from_account_by_id(self, account: Account) -> Account:
        for account_in_list in AccountDAOImp.account_list:
            if account_in_list.account_id == account.account_id:
                index = AccountDAOImp.account_list.index(account_in_list)
                AccountDAOImp.account_list[index] = account
                return account

    def transfer_money_between_accounts_by_their_ids(self, account: Account) -> Account:
        for account_in_list in AccountDAOImp.account_list:
            if account_in_list.customer_id == account.customer_id:
                if account_in_list.account_id == account.account_id:
                    index = AccountDAOImp.account_list.index(account_in_list)
                    AccountDAOImp.account_list[index] = account
                    return account

    def delete_account_by_id(self, account_id: int):
        for account_in_list in AccountDAOImp.account_list:
            if account_in_list.account_id == account_id:
                index = AccountDAOImp.account_list.index(account_in_list)
                del AccountDAOImp.account_list[index]
                return True
