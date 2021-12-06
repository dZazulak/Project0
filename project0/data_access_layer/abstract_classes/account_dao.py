from abc import ABC, abstractmethod

from entities.account import Account


class AccountDAO(ABC):

    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_account_by_id(self, account_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self) -> list[Account]:
        pass

    @abstractmethod
    def deposit_into_account_by_id(self, account: Account) -> Account:
        pass

    @abstractmethod
    def withdraw_from_account_by_id(self, account: Account) -> Account:
        pass

    @abstractmethod
    def transfer_money_between_accounts_by_their_ids(self, transfer_account: Account, receiver_account: Account, balanced_transferred: float):
        pass

    @abstractmethod
    def delete_account_by_id(self, account_id: int) -> bool:
        pass
