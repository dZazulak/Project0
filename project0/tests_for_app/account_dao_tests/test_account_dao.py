from data_access_layer.implementation_classes.account_dao_imp import AccountDAOImp
from entities.account import Account

account_dao_imp = AccountDAOImp()
account = Account(5000, 1, 1)
account_to_delete = Account(1, 2, 2)


def test_create_account_success():
    new_account = account_dao_imp.create_account(account)
    for accounts in account_dao_imp.account_list:
        print(accounts)
    print(new_account.account_id)
    assert new_account.account_id != 0


def test_get_account_success():
    returned_account: Account = account_dao_imp.get_account_by_id(1)
    assert returned_account.account_id == 1


def test_get_all_accounts_success():
    account_list = account_dao_imp.get_all_accounts()
    assert len(account_list) >= 2


def test_delete_account_success():
    confirm_account_deleted = account_dao_imp.delete_account_by_id(2)
    assert confirm_account_deleted
