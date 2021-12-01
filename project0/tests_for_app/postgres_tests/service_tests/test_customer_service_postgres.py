from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException
from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customer import Customer
from service_layer.implementation_services.customer_postgres_service import CustomerPostgresService

customer_dao = CustomerPostgresDAO()
customer_service = CustomerPostgresService(customer_dao)

customer_that_was_not_found = Customer("first", "last", 5000)
customer_with_duplicate_id = Customer("Kay", "Toups", 1)


def test_catch_duplicate_customer_id_for_create_method():
    try:
        customer_service.service_create_new_customer(customer_with_duplicate_id)
        assert False
    except DuplicateCustomerIdException as e:
        assert str(e) == "There is a duplicate customer ID in the database."


def test_catch_customer_not_found_for_update_method():
    try:
        customer_service.service_update_customer_by_id(customer_that_was_not_found)
        assert False
    except CustomerNotFoundException as e:
        assert str(e) == "This customer could not be found in the database"
