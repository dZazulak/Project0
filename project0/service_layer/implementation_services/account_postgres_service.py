from custom_exceptions.account_not_found_exception import AccountNotFoundException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.duplicate_account_id_exception import DuplicateAccountIdException
from custom_exceptions.insufficient_funds_exception import InsufficientFundsException
from custom_exceptions.one_account_in_transfer_not_found_exception import OneAccountInTransferNotFoundException
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
                    if account_to_withdraw.balance - account.balance >= 0:
                        return self.account_dao.withdraw_from_account_by_id(account)
                    else:
                        raise InsufficientFundsException("You do not have enough money in your account")
                else:
                    raise CustomerNotFoundException("This customer could not be found in the database")
        raise AccountNotFoundException("This account could not be found in the database")

    def service_transfer_money_between_accounts_by_their_ids(self, transfer_account: Account, receiver_account: Account,
                                                             balance_transferred: float):
        account_list = self.account_dao.get_all_accounts()
        for account in account_list:
            if account.account_id == transfer_account.account_id:
                if account.account_id == receiver_account.account_id:
                    if transfer_account.balance >= balance_transferred:
                        return self.account_dao.transfer_money_between_accounts_by_their_ids(transfer_account,
                                                                                             receiver_account,
                                                                                             balance_transferred)
                    else:
                        raise InsufficientFundsException("You do not have enough money in your account")

            else:
                raise AccountNotFoundException("This account could not be found in the database")

    def service_delete_account_by_id(self, account_id: int) -> bool:
        account_list = self.account_dao.get_all_accounts()
        for account in account_list:
            if account.account_id == account_id:
                return self.account_dao.delete_account_by_id(account_id)
        raise AccountNotFoundException("This account could not be found in the database")
