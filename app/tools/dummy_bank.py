from uuid import uuid4
class DummyBankService:
    def __init__(self):
        self.accounts={"demo-user":{"current":{"id":"acc-current-001","name":"Current Account","balance":4250.0},"savings":{"id":"acc-savings-001","name":"Savings Account","balance":12000.0}}}; self.cards={"demo-user":[{"id":"card-001","name":"Everyday Debit Card","status":"Active","last4":"1234"},{"id":"card-002","name":"Travel Credit Card","status":"Active","last4":"5678"}]}; self.transactions={}
    def get_balances(self,customer_id): return self.accounts.get(customer_id,{})
    def get_cards(self,customer_id): return self.cards.get(customer_id,[])
    def transfer(self,customer_id,source,destination,amount,idempotency_key):
        if idempotency_key in self.transactions:return self.transactions[idempotency_key]
        a=self.accounts.get(customer_id)
        if not a:raise ValueError("Customer not found.")
        if source not in a or destination not in a:raise ValueError("Invalid account.")
        if amount<=0:raise ValueError("Amount must be positive.")
        if a[source]["balance"]<amount:raise ValueError("Insufficient funds.")
        a[source]["balance"]-=amount;a[destination]["balance"]+=amount
        r={"transaction_id":f"txn-{uuid4().hex[:12]}","status":"COMPLETED","amount":amount,"source":a[source]["name"],"destination":a[destination]["name"]};self.transactions[idempotency_key]=r;return r
