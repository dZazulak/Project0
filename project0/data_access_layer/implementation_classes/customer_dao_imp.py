from entities.customer import Customer
from data_access_layer.abstract_classes.customer_dao import CustomerDAO


class CustomerDAOImp(CustomerDAO):

    customer_one = Customer("David", "Zazulak", 1)
    customer_two = Customer("Eric", "Suminski", 2)
    customer_to_delete = Customer("Delete", "this later", 3)

    customer_list = [customer_one, customer_two, customer_to_delete]

    customer_id_generator = 4

    def create_new_customer(self, customer: Customer) -> Customer:
        customer.customer_id = CustomerDAOImp.customer_id_generator
        CustomerDAOImp.customer_id_generator += 1
        CustomerDAOImp.customer_list.append(customer)
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        for customer in CustomerDAOImp.customer_list:
            if customer.customer_id == customer_id:
                return customer

    def get_all_customers(self) -> list[Customer]:
        return CustomerDAOImp.customer_list

    def update_customer_by_id(self, customer: Customer) -> Customer:
        for customer_in_list in CustomerDAOImp.customer_list:
            if customer_in_list.customer_id == customer.customer_id:
                index = CustomerDAOImp.customer_list.index(customer_in_list)
                CustomerDAOImp.customer_list[index] = customer
                return customer

    def delete_customer_by_id(self, customer_id: int) -> bool:
        for customer_in_list in CustomerDAOImp.customer_list:
            if customer_in_list.customer_id == customer_id:
                index = CustomerDAOImp.customer_list.index(customer_in_list)
                del CustomerDAOImp.customer_list[index]
                return bool
