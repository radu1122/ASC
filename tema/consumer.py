"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        Thread.__init__(self, **kwargs)
        self.name = kwargs["name"]

    def run(self):
        id_cart = self.marketplace.new_cart()

        for cart in self.carts:
            for com in cart:
                type_com = com['type']
                quantity = com['quantity']
                product = com['product']
                if type_com == "remove":
                    for i in range(quantity):
                        self.marketplace.remove_from_cart(id_cart, product)
                elif type_com == "add":
                    i = 0
                    while 1:
                        if i >= quantity:
                            break
                        while not self.marketplace.add_to_cart(id_cart, product):
                            sleep(self.retry_wait_time)
                        i += 1
        for prod in self.marketplace.place_order(id_cart):
            to_print = "{} bought {}".format(self.name, prod)
            print(to_print)
