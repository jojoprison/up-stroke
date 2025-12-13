class Queues:

    producer = None
    consumer = None

    def __init__(
            self, producer, consumer
    ):
        self.producer = producer
        self.consumer = consumer