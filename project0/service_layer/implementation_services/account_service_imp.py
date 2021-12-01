from data_access_layer.implementation_classes.account_dao_imp import AccountDAOImp
from entities.account import Account
from service_layer.abstract_services.account_service import AccountService
from custom_exceptions.account_already_created_exception import AccountAlreadyCreatedException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.account_not_found_exception import AccountNotFoundException


class AccountServiceImp(AccountService):

    def __init__(self, account_dao):
        self.account_dao: AccountDAOImp = account_dao

    def service_create_account(self, account: Account) -> Account:
        for current_account in self.account_dao.account_list:
            if current_account.customer_id == account.customer_id and current_account.account_id == account.account_id:
                raise AccountAlreadyCreatedException("Account is already created")
            else:
                return self.account_dao.create_account(account)

    def service_get_account_by_id(self, account_id: int) -> Account:
        return self.account_dao.get_account_by_id(account_id)

    def service_get_all_accounts(self) -> list[Account]:
        return self.account_dao.get_all_accounts()

    def service_deposit_into_account_by_id(self, account: Account) -> Account:
        for current_account in self.account_dao.account_list:
            if current_account.customer_id == account.customer_id:
                if current_account.account_id == account.account_id:
                    return self.account_dao.deposit_into_account_by_id(account)
                else:
                    raise AccountNotFoundException("We could not find your account in the database")
            else:
                raise CustomerNotFoundException("This customer could not be found in the database")

    def service_withdraw_from_account_by_id(self, account: Account) -> Account:
        # for current_account in self.account_dao.account_list:
        #     if current_account.customer_id == account.customer_id:
        #         if current_account.account_id == account.account_id:
        #             try:
        #                 current_account.balance -= account.balance
        pass

    def service_transfer_money_between_accounts_by_their_ids(self, account: Account) -> Account:
        pass

    def service_delete_account_by_id(self, account_id: int) -> bool:
        return self.account_dao.delete_account_by_id(account_id)
