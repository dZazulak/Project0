from data_access_layer.implementation_classes.customer_dao_imp import CustomerDAOImp
from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customer import Customer

customer_dao_imp = CustomerDAOImp()
customer_dao_postgres = CustomerPostgresDAO()
customer = Customer("Test", "Customer", 1)
customer_for_postgres = Customer("David", "Zazulak", 1)


def test_create_customer_success():
    new_customer: Customer = customer_dao_imp.create_new_customer(customer)
    assert new_customer.customer_id != 0


def test_get_customer_success():
    returned_customer: Customer = customer_dao_imp.get_customer_by_id(1)
    assert returned_customer.customer_id == 1


def test_get_all_customers_success():
    customer_list = customer_dao_imp.get_all_customers()
    assert len(customer_list) >= 2


def test_update_customer_success():
    updated_info = Customer("Changed by", "Update player method", 1)
    updated_customer: Customer = customer_dao_imp.update_customer_by_id(updated_info)
    assert updated_customer.customer_id == updated_info.customer_id


def test_delete_customer_success():
    confirm_customer_deleted = customer_dao_imp.delete_customer_by_id(1)
    assert confirm_customer_deleted

