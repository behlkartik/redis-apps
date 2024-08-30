from redis import Redis
from redis.exceptions import WatchError

from functools import wraps
import sys

class ApplicationError(Exception):
    def __init__(self, msg: str):
        self.msg = f"Error: {msg}"
    def __str__(self) -> str:
        return self.msg

class OutOfStockError(ApplicationError):
    pass

class ProductNotFoundError(ApplicationError):
    pass

class IncorrectPurchaseError(ApplicationError):
    pass

def _buy_item_in_transaction(client: Redis, item_key: str):
    pipe = client.pipeline()
    pipe.multi()
    redis_client.hincrby(item_key, "quantity", -1)
    redis_client.hincrby(item_key, "npurchased", 1)
    pipe.execute()

def check_incorrect(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        client: Redis = kwargs.get("client")
        item_key = kwargs.get("item_key")
        npurchased = int(client.hget(item_key, "npurchased"))
        _check_purchase(npurchased, transaction_done=False)
        f(*args, **kwargs)
        _check_purchase(npurchased, transaction_done=True)
    return decorated

def _check_purchase(npurchased: int, transaction_done: bool):
    if not transaction_done and npurchased != 0 or transaction_done and npurchased == 0:
        raise IncorrectPurchaseError("500: Something went wrong. Check inventory.")


@check_incorrect
def buy_item(client: Redis, item_key: str):
    if not client.keys(item_key):
        raise ProductNotFoundError("404: Product not found....")
    retry_count = 0
    _name = client.hget(item_key, "name")
    name = str(_name)
    while True:
        try:
            client.watch()
            quantity = int(client.hget(item_key, "quantity"))
            if quantity >= 1:
                print(f"Purchasing 1 {name}")
                _buy_item_in_transaction(client, item_key)
                print(f"Purchased 1 {name}")    
            else:
                client.unwatch()
                raise OutOfStockError(f"400: Product is out of stock. Better luck next time.")
        except WatchError:
            retry_count += 1
            continue

if __name__ == "__main__":
    redis_client = Redis(host="localhost", port=6379, db=0)
    buy_item(client=redis_client, item_key=sys.argv[1])