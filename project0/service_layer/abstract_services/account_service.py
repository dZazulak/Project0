from abc import ABC, abstractmethod

from entities.account import Account


class AccountService(ABC):

    @abstractmethod
    def service_create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def service_get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def service_get_all_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def service_deposit_into_account_by_id(self, account: Account) -> Account:
        pass

    @abstractmethod
    def service_withdraw_from_account_by_id(self, account: Account) -> Account:
        pass

    @abstractmethod
    def service_transfer_money_between_accounts_by_their_ids(self, account: Account) -> Account:
        pass

    @abstractmethod
    def service_delete_account_by_id(self, account_id: int) -> bool:
        pass
