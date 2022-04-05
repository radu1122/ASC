"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Lock
import logging
from logging.handlers import RotatingFileHandler
import time
import unittest

class TestMarketplace(unittest.TestCase):
    def register_producer(self):
        market = Marketplace()
        self.assertEquals(market.register_producer(), 0, "Expected to return id 0")

    def register_publish(self):
        market = Marketplace()
        producter_id = market.register_producer()
        self.assertTrue(market.publish(producter_id, "Tea"), "Expected to return True")

    def register_new_cart(self):
        market = Marketplace()
        self.assertEquals(market.new_cart(), 0, "Expected to return id 0")

    def register_remove_from_cart(self):
        market = Marketplace()
        cart_id = market.new_cart()
        market.add_to_cart(cart_id, "Tea")
        self.assertTrue(market.remove_from_cart(cart_id, "Tea"), "Expected to return True")

    def register_place_order(self):
        market = Marketplace()
        cart_id = market.new_cart()
        market.add_to_cart(cart_id, "Tea")
        self.assertEquals(market.place_order(cart_id, "Tea")[0], "Tea", "Expected to return Tea")


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.mutex = Lock()
        self.producers = []
        self.carts = []
        self.producers_no = -1
        self.consumers_no = -1


        logging.Formatter.converter = time.gmtime
        logFormatter = logging.Formatter("%(asctime)s:%(levelname)s: %(filename)s::%(funcName)s:%(lineno)d %(message)s")
        logger = logging.getLogger()
        logger.propagate = False
        handler_file = RotatingFileHandler('marketplace.log', maxBytes=4096, backupCount=1)

        handler_file.setFormatter(logFormatter)
        logger.addHandler(handler_file)
        logger.setLevel(logging.INFO)

        self.logger = logger

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.mutex.acquire()
        self.producers_no += 1
        self.producers.append([])
        producer_id = self.producers_no
        self.mutex.release()
        self.logger.info("New producer: {}".format(producer_id))

        return producer_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        publish_state = False

        self.mutex.acquire()
        if len(self.producers[producer_id]) <= self.queue_size_per_producer:
            self.producers[producer_id].append(product)
            publish_state = True
        self.mutex.release()
        
        self.logger.info("state: {} add product {} of producer: {}".format(publish_state, product, producer_id))

        return publish_state

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.mutex.acquire()
        cart = []
        self.carts.append(cart)
        self.consumers_no += 1
        cart_id = self.consumers_no
        self.mutex.release()
        self.logger.info("New char id: {}".format(cart_id))

        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        
        self.mutex.acquire()
        i = 0
        for prod in self.producers:
            for produs in prod:
                if product == produs:
                    self.carts[cart_id].append([product, i])
                    prod.remove(product)
                    self.mutex.release()
                    self.logger.info("add product {} to cart id: {}".format(product, cart_id))
                    return True
            i += 1
        self.mutex.release()
        self.logger.error("add product {} to cart id: {}".format(product, cart_id))

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.mutex.acquire()
        for produs in self.carts[cart_id]:
            if produs[0] == product:
                self.producers[produs[1]].append(produs[0])
                self.carts[cart_id].remove(produs)
                break
        self.mutex.release()
        self.logger.info("remove product {} to cart id: {}".format(product, cart_id))
        return True

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        products = [x[0] for x in self.carts[cart_id]]
        self.logger.info("place order {} to cart id: {}".format(products, cart_id))
        
        return products
