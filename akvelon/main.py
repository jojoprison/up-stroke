from akvelon.api import API
from akvelon.db import DB
from akvelon.queues import Queues

api = API()
db = DB()

queues = Queues(
    producer=api, consumer=db
)
