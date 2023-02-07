import transaction as Transaction

class Payment(Transaction):
    def __init__(self, transaction_id: str, sender: str, fee: float,  recipient: str,  amount: float, asset_id: int):
        super().__init__(transaction_id, sender, fee)
        self.recipient = recipient
        self.amount = amount
        self.asset_id = asset_id
