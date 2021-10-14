
    
#Child Class
# this class will create a user object and also tie a banking acct to that object
# objects made from this class will can have banking transactions done with them 
# ...b/c they do have a banking acct tied to its object

class Bank(User):
    def __init__(self,fname,lname,chk_bal):
        super().__init__(fname,lname,chk_bal)
        self.balance = 0

    def deposit(self,amount):
        self.amount = amount
        self.balance = self.balance + self.amount
        print("Account balance has been updated : £", self.balance)

    def withdraw(self,amount):
        self.amount = amount
        if self.amount > self.balance:
            print("Insufficient Funds | Balance Available : £", self.balance)
        else:
            self.balance = self.balance - self.amount
            print("Account balance has been updated : £", self.balance)
    
    def view_balance(self):
        self.show_details()
        print("Account balance: £", self.balance)