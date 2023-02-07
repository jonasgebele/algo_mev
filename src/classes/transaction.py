class Transaction:
    def __init__(self, transaction_id: str, sender: str, fee: float):
        self.transaction_id = transaction_id
        self.sender = sender
        self.fee = fee
