from custom_exceptions.account_not_found_exception import AccountNotFoundException
from custom_exceptions.duplicate_account_id_exception import DuplicateAccountIdException
from custom_exceptions.insufficient_funds_exception import InsufficientFundsException
from data_access_layer.implementation_classes.account_postgres_dao import AccountPostgresDAO
from entities.account import Account
from service_layer.abstract_services.account_service import AccountService


class AccountPostgresService(AccountService):
    def __init__(self, account_dao: AccountPostgresDAO):
        self.account_dao = account_dao

    def service_create_account(self, account: Account) -> Account:
        account_list = self.account_dao.get_all_accounts()
        for existing_account in account_list:
            if existing_account.account_id == account.account_id:
                raise DuplicateAccountIdException("This account ID is already created.")
        return self.account_dao.create_account(account)

    def service_get_account_by_id(self, account_id: int) -> Account:
        account_list = self.account_dao.get_all_accounts()
        for existing_account in account_list:
            if existing_account.account_id == account_id:
                return self.account_dao.get_account_by_id(account_id)
        raise AccountNotFoundException("This account could not be found in the database")

    def service_get_all_accounts(self) -> list[Account]:
        return self.account_dao.get_all_accounts()

    def service_deposit_into_account_by_id(self, account: Account) -> Account:
        account_list = self.account_dao.get_all_accounts()
        for account_to_deposit in account_list:
            if account_to_deposit.account_id == account.account_id:
                return self.account_dao.deposit_into_account_by_id(account)
        raise AccountNotFoundException("This account could not be found in the database")

    def service_withdraw_from_account_by_id(self, account: Account) -> Account:
        account_list = self.account_dao.get_all_accounts()
        for account_to_withdraw in account_list:
            if account_to_withdraw.account_id == account.account_id:
                if account_to_withdraw.customer_id == account.customer_id:
                    if account_to_withdraw.balance - account.balance > 0:
                        return self.account_dao.withdraw_from_account_by_id(account)
        raise InsufficientFundsException("You do not have enough money in your account")

    def service_transfer_money_between_accounts_by_their_ids(self, account: Account) -> Account:
        pass

    def service_delete_account_by_id(self, account_id: int) -> bool:
        return self.account_dao.delete_account_by_id(account_id)
