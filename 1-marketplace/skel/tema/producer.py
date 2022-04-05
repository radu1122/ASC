"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        Thread.__init__(self, **kwargs)

    def run(self):
        producer_id = self.marketplace.register_producer()
        
        while 1:
            for elem in self.products:
                (id, cantitate, timp_așteptare) = elem
                sleep_time = cantitate * timp_așteptare
                sleep(sleep_time)
                i = 0
                while 1:
                    if i >= cantitate:
                        break
                    while not self.marketplace.publish(producer_id, id):
                        sleep(self.republish_wait_time)
                    i += 1
