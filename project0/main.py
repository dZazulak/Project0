from flask import Flask, request, jsonify

from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from data_access_layer.implementation_classes.customer_dao_imp import CustomerDAOImp
# from data_access_layer.implementation_classes.account_dao_imp import AccountDAOImp
from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customer import Customer
from entities.account import Account
from service_layer.implementation_services.customer_postgres_service import CustomerPostgresService
from service_layer.implementation_services.customer_service_imp import CustomerServiceImp

# from service_layer.implementation_services.account_service_imp import AccountServiceImp

app: Flask = Flask(__name__)

customer_dao = CustomerPostgresDAO()
customer_service = CustomerPostgresService(customer_dao)


@app.post("/customer")
def create_customer_entry():
    try:
        customer_data = request.get_json()
        new_customer = Customer(
            customer_data["firstName"],
            customer_data["lastName"],
            customer_data["customerId"]
        )
        customer_to_return = customer_service.service_create_new_customer(new_customer)
        customer_as_dictionary = customer_to_return.make_customers_dictionary()
        customer_as_json = jsonify(customer_as_dictionary)
        return customer_as_json
    except DuplicateCustomerIdException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.get("/customer/<customer_id>")
def get_customer_information(customer_id: str):
    try:
        result = customer_service.service_get_customer_by_id(int(customer_id))
        result_as_dictionary = result.make_customers_dictionary()
        result_as_json = jsonify(result_as_dictionary)
        return result_as_json
    except CustomerNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.get("/customer")
def get_all_customers_information():
    customers_as_customers = customer_service.service_get_all_customers()
    customers_as_dictionary = []
    for customers in customers_as_customers:
        dictionary_costumer = customers.make_customers_dictionary()
        customers_as_dictionary.append(dictionary_costumer)
    return jsonify(customers_as_dictionary)


# Not Working
@app.patch("/customer/<customer_id>")
def update_customer_information(customer_id: str):
    try:
        customer_data = request.get_json()
        new_customer = Customer(
            customer_data["firstName"],
            customer_data["lastName"],
            int(customer_id)
        )
        updated_customer = customer_service.service_update_customer_by_id(new_customer)
        updated_customer_as_dictionary = updated_customer.make_customers_dictionary()
        return jsonify(updated_customer_as_dictionary)

    except CustomerNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.delete("/customer/<customer_id>")
def delete_customer_information(customer_id: str):
    result = customer_service.service_delete_customer_by_id(int(customer_id))
    if result:
        return "Customer with id {} was deleted successfully".format(customer_id)
    else:
        return "Something went wrong: Customer with id {} was not deleted".format(customer_id)


app.run()
