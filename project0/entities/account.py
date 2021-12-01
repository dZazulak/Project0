class Account:
    def __init__(self, balance: float, account_id: int, customer_id: int):
        self.balance = balance
        self.account_id = account_id
        self.customer_id = customer_id

    def account_as_dictionary(self):
        return {
            "balance": self.balance,
            "accountId": self.account_id,
            "customerId": self.customer_id
        }
