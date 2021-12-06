from custom_exceptions.account_not_found_exception import AccountNotFoundException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.duplicate_account_id_exception import DuplicateAccountIdException
from custom_exceptions.insufficient_funds_exception import InsufficientFundsException
from data_access_layer.implementation_classes.account_postgres_dao import AccountPostgresDAO
from entities.account import Account
from service_layer.implementation_services.account_postgres_service import AccountPostgresService

account_dao = AccountPostgresDAO()
account_service = AccountPostgresService(account_dao)

account = Account(500, 2, 1)
deposit_account_account_id_fail = Account(500, 1, 1)
withdraw_account_account_id_fail = Account(500, 1, 17)
withdraw_account_customer_id_fail = Account(500, 3, 9999)
withdraw_account_funds_fail = Account(999999999, 3, 1)
transfer_account_funds_fail = Account(1, 1, 1)
receive_account = Account(1, 15, 1)


def test_validate_create_account_method():
    try:
        account_service.service_create_account(account)
        assert False
    except DuplicateAccountIdException as e:
        assert str(e) == "This account ID is already created."


def test_validate_deposit_into_account_by_id_method_account_id_fail():
    try:
        account_service.service_deposit_into_account_by_id(deposit_account_account_id_fail)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "This account could not be found in the database"


def test_validate_withdraw_from_account_by_id_method_account_id_fail():
    try:
        account_service.service_withdraw_from_account_by_id(withdraw_account_account_id_fail)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "This account could not be found in the database"


def test_validate_withdraw_from_account_by_id_method_funds_fail():
    try:
        account_service.service_withdraw_from_account_by_id(withdraw_account_funds_fail)
        assert False
    except InsufficientFundsException as e:
        assert str(e) == "You do not have enough money in your account"


def test_validate_transfer_from_account_by_id_method_account_id_fail():
    try:
        account_service.service_transfer_money_between_accounts_by_their_ids(transfer_account_funds_fail,
                                                                             receive_account,
                                                                             9999999)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "This account could not be found in the database"
