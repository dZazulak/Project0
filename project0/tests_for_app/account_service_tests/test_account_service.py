from custom_exceptions.duplicate_account_id_exception import AccountAlreadyCreatedException
from data_access_layer.implementation_classes.account_dao_imp import AccountDAOImp
from entities.account import Account
from service_layer.implementation_services.account_service_imp import AccountServiceImp

account_dao = AccountDAOImp()
account_service = AccountServiceImp(account_dao)
account = Account(500, 1, 1)


def test_validate_create_account_method():
    try:
        account_service.service_create_account(account)
        assert False
    except AccountAlreadyCreatedException as e:
        assert str(e) == "Account is already created"
