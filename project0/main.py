from flask import Flask, request, jsonify

from custom_exceptions.duplicate_customer_id_exception import DuplicateCustomerIdException
from custom_exceptions.customer_not_found_exception import CustomerNotFoundException
from custom_exceptions.account_not_found_exception import AccountNotFoundException
from custom_exceptions.duplicate_account_id_exception import DuplicateAccountIdException
from custom_exceptions.insufficient_funds_exception import InsufficientFundsException
from custom_exceptions.one_account_in_transfer_not_found_exception import OneAccountInTransferNotFoundException
from data_access_layer.implementation_classes.account_postgres_dao import AccountPostgresDAO
from data_access_layer.implementation_classes.customer_dao_imp import CustomerDAOImp
from data_access_layer.implementation_classes.account_dao_imp import AccountDAOImp
from data_access_layer.implementation_classes.customer_postgres_dao import CustomerPostgresDAO
from entities.customer import Customer
from entities.account import Account
from service_layer.implementation_services.account_postgres_service import AccountPostgresService
from service_layer.implementation_services.customer_postgres_service import CustomerPostgresService
from service_layer.implementation_services.customer_service_imp import CustomerServiceImp
from service_layer.implementation_services.account_service_imp import AccountServiceImp
import logging

logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(message)s")

app: Flask = Flask(__name__)

customer_dao = CustomerPostgresDAO()
customer_service = CustomerPostgresService(customer_dao)
account_dao = AccountPostgresDAO()
account_service = AccountPostgresService(account_dao)


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
    try:
        result = customer_service.service_delete_customer_by_id(int(customer_id))
        if result:
            return "Customer with id {} was deleted successfully".format(customer_id)
    except CustomerNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.post("/account")
def create_account():
    try:
        body = request.get_json()
        new_account = Account(
            body["balance"],
            body["accountId"],
            body["customerId"]
        )
        created_account = account_service.service_create_account(new_account)
        created_account_as_dictionary = created_account.account_as_dictionary()
        return jsonify(created_account_as_dictionary), 201

    except DuplicateAccountIdException as e:
        error_message = {"errorMessage": str(e)}
        return jsonify(error_message), 400


@app.get("/account/<account_id>")
def get_account_information(account_id: str):
    try:
        result = account_service.service_get_account_by_id(int(account_id))
        result_as_dictionary = result.account_as_dictionary()
        result_as_json = jsonify(result_as_dictionary)
        return result_as_json
    except AccountNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.get("/account")
def get_all_accounts_information():
    accounts_as_accounts = account_service.service_get_all_accounts()
    accounts_as_dictionary = []
    for accounts in accounts_as_accounts:
        account_dictionary = accounts.account_as_dictionary()
        accounts_as_dictionary.append(account_dictionary)
    return jsonify(accounts_as_dictionary)


@app.patch("/account/deposit/<account_id>/customer/<customer_id>")
def deposit_from_account_by_id(account_id: str, customer_id: str):
    try:
        account_data = request.get_json()
        new_account = Account(
            account_data["balance"],
            int(account_id),
            int(customer_id)
        )
        updated_account = account_service.service_deposit_into_account_by_id(new_account)
        updated_account_as_dictionary = updated_account.account_as_dictionary()
        return jsonify(updated_account_as_dictionary)

    except AccountNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.patch("/account/withdraw/<account_id>/customer/<customer_id>")
def withdraw_from_account_by_id(account_id: str, customer_id: str):
    try:
        account_data = request.get_json()
        new_account = Account(
            account_data["balance"],
            int(account_id),
            int(customer_id)
        )
        updated_account = account_service.service_withdraw_from_account_by_id(new_account)
        updated_account_as_dictionary = updated_account.account_as_dictionary()
        return jsonify(updated_account_as_dictionary)

    except InsufficientFundsException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json

    except AccountNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json

    except CustomerNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.patch("/account/transfer/<transfer_id>/receive/<receive_id>/customer/<customer_id>")
def transfer_between_accounts_by_id(transfer_id: str, receive_id: str, customer_id: str):
    try:
        account_data = request.get_json()
        new_transfer_account = Account(
            account_data["balance"],
            int(transfer_id),
            int(customer_id)
        )
        new_receiver_account = Account(
            account_data["balance"],
            int(receive_id),
            int(customer_id)
        )

        updated_transfer_account = account_service.service_withdraw_from_account_by_id(new_transfer_account)
        updated_receiver_account = account_service.service_deposit_into_account_by_id(new_receiver_account)
        updated_transfer_account_as_dictionary = updated_transfer_account.account_as_dictionary()
        updated_receiver_account_as_dictionary = updated_receiver_account.account_as_dictionary()
        return jsonify(updated_transfer_account_as_dictionary, updated_receiver_account_as_dictionary)

    except AccountNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json

    except InsufficientFundsException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


@app.delete("/account/<account_id>")
def delete_account_information(account_id: str):
    try:
        result = account_service.service_delete_account_by_id(int(account_id))
        if result:
            return "Account with id {} was deleted successfully".format(account_id)
    except AccountNotFoundException as e:
        exception_dictionary = {"message": str(e)}
        exception_json = jsonify(exception_dictionary)
        return exception_json


app.run()
