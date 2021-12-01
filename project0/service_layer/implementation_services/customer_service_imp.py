from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from data_access_layer.implementation_classes.customer_dao_imp import CustomerDAOImp
from entities.customer import Customer
from service_layer.abstract_services.customer_service import CustomerService


class CustomerServiceImp(CustomerService):
    def __init__(self, customer_dao):
        self.customer_dao: CustomerDAOImp = customer_dao

    def service_create_new_customer(self, customer: Customer) -> Customer:
        for current_customer in self.customer_dao.customer_list:
            if current_customer.customer_id == customer.customer_id:
                raise DuplicateCustomerIdException("There is a duplicate customer ID in the database.")
        return self.customer_dao.create_new_customer(customer)

    def service_get_customer_by_id(self, customer_id: int) -> Customer:
        return self.customer_dao.get_customer_by_id(customer_id)

    def service_get_all_customers(self) -> list[Customer]:
        return self.customer_dao.get_all_customers()

    # Needs fixing
    def service_update_customer_by_id(self, customer: Customer) -> Customer:
        for current_customer in self.customer_dao.customer_list:
            if current_customer.customer_id == customer.customer_id:
                return self.customer_dao.update_customer_by_id(customer)
            elif current_customer.customer_id != customer.customer_id and current_customer.customer_id <= len(self.customer_dao.customer_list):
                return self.customer_dao.update_customer_by_id(customer)
            else:
                raise CustomerNotFoundException("This customer could not be found in the database")

    def service_delete_customer_by_id(self, customer_id: int) -> bool:
        return self.customer_dao.delete_customer_by_id(customer_id)
