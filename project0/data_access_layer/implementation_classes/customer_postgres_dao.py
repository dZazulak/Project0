from data_access_layer.abstract_classes.customer_dao import CustomerDAO
from entities.customer import Customer
from util.database_connection import connection


class CustomerPostgresDAO(CustomerDAO):

    def create_new_customer(self, customer: Customer) -> Customer:
        sql = "insert into customer values(%s, %s, default) returning customer_id"
        cursor = connection.cursor()
        cursor.execute(sql, (customer.first_name, customer.last_name))
        connection.commit()
        generated_id = cursor.fetchone()[0]
        customer.customer_id = generated_id
        return customer

    def get_customer_by_id(self, customer_id: int) -> Customer:
        sql = "select * from customer where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        customer_record = cursor.fetchone()
        customer = Customer(*customer_record)
        return customer

    def get_all_customers(self) -> list[Customer]:
        sql = "select * from customer"
        cursor = connection.cursor()
        cursor.execute(sql)
        customer_records = cursor.fetchall()
        customer_list = []
        for customer in customer_records:
            customer_list.append(Customer(*customer))
        return customer_list

    def update_customer_by_id(self, customer: Customer) -> Customer:
        sql = "update customer set first_name = %s, last_name = %s where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (customer.first_name, customer.last_name, customer.customer_id))
        connection.commit()
        return customer

    def delete_customer_by_id(self, customer_id: int) -> bool:
        sql = "delete from customer where customer_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, [customer_id])
        connection.commit()
        return True
