import transaction as Transaction

class ApplicationCall(Transaction):
    def __init__(self, transaction_id: str, sender: str, fee: float, application_id: int, application_description: str):
        super().__init__(transaction_id, sender, fee)
        self.application_id = application_id
        self.application_description = application_description
