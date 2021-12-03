from custom_exceptions.account_not_found_exception import AccountNotFoundException
from custom_exceptions.duplicate_account_id_exception import DuplicateAccountIdException
from data_access_layer.implementation_classes.account_postgres_dao import AccountPostgresDAO
from entities.account import Account
from service_layer.implementation_services.account_postgres_service import AccountPostgresService

account_dao = AccountPostgresDAO()
account_service = AccountPostgresService(account_dao)

account = Account(500, 2, 1)


def test_validate_create_account_method():
    try:
        account_service.service_create_account(account)
        assert False
    except DuplicateAccountIdException as e:
        assert str(e) == "This account ID is already created."


def test_validate_get_account_by_id_method():
    try:
        account_service.service_get_account_by_id(account)
        assert False
    except AccountNotFoundException as e:
        assert str(e) == "This account could not be found in the database"


def test_validate_get_all_accounts_method():
    result = account_service.service_get_all_accounts()
    assert len(result) >= 2
