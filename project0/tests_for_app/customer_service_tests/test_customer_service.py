from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from data_access_layer.implementation_classes.customer_dao_imp import CustomerDAOImp
from entities.customer import Customer
from service_layer.implementation_services.customer_service_imp import CustomerServiceImp
from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException

customer_dao = CustomerDAOImp()
customer_service = CustomerServiceImp(customer_dao)
customer = Customer("Service", "testing", 1)
customer_update = Customer("David", "Zazulak", 1)


def test_validate_create_customer_method():
    try:
        customer_service.service_create_new_customer(customer)
        assert False
    except DuplicateCustomerIdException as e:
        assert str(e) == "There is a duplicate customer ID in the database."


def test_validate_update_customer_method():
    try:
        customer_service.service_update_customer_by_id(customer_update)
        assert False
    except CustomerNotFoundException as e:
        assert str(e) == "This customer could not be found in the database"


def test_validate_get_customer_by_id_method():
    returned_customer: Customer = customer_service.service_get_customer_by_id(1)
    assert returned_customer.customer_id == 1


def test_validate_get_all_customers_method():
    customer_list = customer_service.service_get_all_customers()
    assert len(customer_list) >= 2


def test_validate_delete_customer_by_id():
    confirm_customer_deleted = customer_service.service_delete_customer_by_id(1)
    assert confirm_customer_deleted
