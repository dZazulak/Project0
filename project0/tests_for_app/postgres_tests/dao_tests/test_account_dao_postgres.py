from data_access_layer.implementation_classes.account_postgres_dao import AccountPostgresDAO
from entities.account import Account

account_dao = AccountPostgresDAO()
account: Account = Account(50, 1, 1)
account_to_delete = Account(1, 3, 1)
account_to_deposit = Account(5, 2, 1)
account_to_withdraw = Account(1, 17, 17)


def test_create_account_success():
    created_account = account_dao.create_account(account)
    assert created_account.account_id != 0


def test_get_account_success():
    returned_account: Account = account_dao.get_account_by_id(2)
    assert returned_account.account_id == 2


def test_get_all_accounts_success():
    account_list = account_dao.get_all_accounts()
    assert len(account_list) >= 2


def test_delete_account_success():
    account_to_be_deleted = account_dao.create_account(account_to_delete)
    result = account_dao.delete_account_by_id(account_to_be_deleted.account_id)
    assert result


def test_deposit_account_success():
    account_to_be_deposited = account_dao.get_account_by_id(2)
    deposited_account = account_dao.deposit_into_account_by_id(account_to_be_deposited)
    assert deposited_account


def test_withdraw_account_success():
    account_to_withdrew = account_dao.get_account_by_id(17)
    withdrew_account = account_dao.withdraw_from_account_by_id(account_to_withdrew)
    assert withdrew_account
