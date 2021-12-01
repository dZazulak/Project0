class Customer:

    def __init__(self, first_name: str, last_name: str, customer_id: int):
        self.first_name = first_name
        self.last_name = last_name
        self.customer_id = customer_id

    def make_customers_dictionary(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "customerId": self.customer_id
        }

    def __str__(self):
        return "first name: {}, last name: {}, customer ID: {}".format(
            self.first_name,
            self.last_name,
            self.customer_id)

