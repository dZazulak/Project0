from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO

from entities.customer import Customer

customer_dao = CustomerPostgresDAO()
customer: Customer = Customer("first", "last", 1)

random_names = {"Bob"}
random_names.add("Sally")
random_names.add("Bill")
random_names.add("Susie")
random_name = random_names.pop()
update_customer = Customer(random_name, "Player", 4)

customer_to_delete = Customer(random_names.pop(), random_names.pop(), 4)


def test_create_player_success():
    created_customer = customer_dao.create_new_customer(customer)
    assert created_customer.customer_id != 0


def test_get_customer_success():
    returned_customer: Customer = customer_dao.get_customer_by_id(1)
    assert returned_customer.customer_id == 1


def test_get_all_customers_success():
    customer_list = customer_dao.get_all_customers()
    assert len(customer_list) >= 2


def test_update_customer_success():
    updated_customer = customer_dao.update_customer_by_id(update_customer)
    assert updated_customer.first_name == random_name


def test_delete_customer_success():
    customer_to_be_deleted = customer_dao.create_new_customer(customer_to_delete)
    result = customer_dao.delete_customer_by_id(customer_to_be_deleted.customer_id)
    assert result
