from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException
from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customer import Customer
from service_layer.abstract_services.customer_service import CustomerService


class CustomerPostgresService(CustomerService):
    def __init__(self, customer_dao: CustomerPostgresDAO):
        self.customer_dao = customer_dao

    def service_create_new_customer(self, customer: Customer) -> Customer:
        customer_list = self.customer_dao.get_all_customers()
        for existing_customer in customer_list:
            if existing_customer.customer_id == customer.customer_id:
                raise DuplicateCustomerIdException("There is a duplicate customer ID in the database.")
        created_customer = self.customer_dao.create_new_customer(customer)
        return created_customer

    def service_get_customer_by_id(self, customer_id: int) -> Customer:
        return self.customer_dao.get_customer_by_id(customer_id)

    def service_get_all_customers(self) -> list[Customer]:
        return self.customer_dao.get_all_customers()

    def service_update_customer_by_id(self, customer: Customer) -> Customer:
        customer_list = self.customer_dao.get_all_customers()
        for current_customer in customer_list:
            # if current_customer.customer_id == customer.customer_id:
            #     return self.customer_dao.update_customer_by_id(customer)
            # elif current_customer.customer_id != customer.customer_id and current_customer.customer_id > len(customer_list):
            #     return self.customer_dao.update_customer_by_id(customer)
            # else:
            #     raise CustomerNotFoundException("This customer could not be found in the database")
            if current_customer.customer_id != customer.customer_id and current_customer.customer_id > customer.customer_id:
                raise CustomerNotFoundException("This customer could not be found in the database")
            else:
                return self.customer_dao.update_customer_by_id(customer)

    def service_delete_customer_by_id(self, customer_id: int) -> bool:
        return self.customer_dao.delete_customer_by_id(customer_id)
