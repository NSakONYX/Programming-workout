"""
ZADANIE: SYSTEM KONT BROKERSKICH (CashAccount & MarginAccount)

====================================================================
1. KLASA: CashAccount
====================================================================
- Atrybut klasy:
    * total_accounts = 0  (licznik wszystkich kont)

- Konstruktor (__init__):
    * parametry: self, owner (str), currency (str), initial_balance = 0.0
    * publiczne: self.owner, self.currency
    * wewnętrzne: self._balance = float(initial_balance)
    * licznik: CashAccount.total_accounts += 1

- Właściwość (@property):
    * balance: getter zwracający self._balance (brak settera, tylko do odczytu)

- Metody:
    * deposit(self, amount):
        - zwiększa self._balance o amount (dla amount > 0)
    * withdraw(self, amount):
        - walidacja: amount > 0 oraz amount <= self._balance
        - jeśli warunek niespełniony -> raise ValueError("...")
        - w przeciwnym razie zmniejsza self._balance
    * @staticmethod calculate_fee(amount, rate):
        - zwraca amount * rate
    * @classmethod from_string(cls, account_str):
        - format wejściowy: "Właściciel:Waluta:Saldo" (np. "Adam Nowak:EUR:2500")
        - rozdziela string po ':'
        - rzutuje saldo na float
        - zwraca nową instancję: cls(...)

====================================================================
2. KLASA: MarginAccount(CashAccount)
====================================================================
- Konstruktor (__init__):
    * parametry: self, owner, currency, initial_balance = 0.0, margin_limit = 0.0
    * wywołanie bazy: super().__init__(owner, currency, initial_balance)
    * atrybut własny: self.margin_limit = float(margin_limit)

- Właściwość (@property):
    * available_funds: getter zwracający (self._balance + self.margin_limit)

- Nadpisanie metody (overriding):
    * withdraw(self, amount):
        - walidacja: amount > 0 oraz amount <= self.available_funds
        - jeśli kwota przekracza dostępne środki -> raise ValueError("...")
        - w przeciwnym razie odejmuje amount od self._balance (saldo może być ujemne)
====================================================================
"""


class CashAccount:
    
    total_accounts = 0
    
    def __init__(self, owner, currency, initial_balance = 0.0):
        self.owner = owner
        self.currency = currency
        
        self._balance = float(initial_balance)
        CashAccount.total_account += 1
        
        
        @property
        def balance(self):
            return self._balance
        
        def deposit(self, amount):
            if (amount>0) : self._balance += amount
            
        def withdraw(self,amount):
            if (amount < self._balance and amount > 0) : self._balance -= amount
            else: raise ValueError("Niewystarczająca ilość środków")
            
        @staticmethod
        def calculate_fee(amount,rate):
            return amount*rate
        
        @classmethod
        def from_string(cls, account_str):
            owner, currency, _balance = account_str.split(":")
            
            return cls(owner, currency,float(_balance))
            
                