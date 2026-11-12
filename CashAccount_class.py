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
        CashAccount.total_accounts += 1
        
        
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
            
                
                
class MarginAccount(CashAccount):
    def __init__(self, owner, currency, initial_balance = 0.0, margin_limit = 0.0):
        super().__init__(owner, currency, initial_balance)
        self.margin_limit = float(margin_limit)
        
    @property
    def available_funds(self):
        return self._balance + self.margin_limit
    
    
    def withdraw(self, amount):
        if (amount > 0 and amount<=self.available_funds):
            self._balance -= amount
        else: 
            raise ValueError("Brak wystarczajacych srodkow.")
    
    
    
if __name__ == "__main__":
    print("--- 1. Tworzenie kont, licznik i alternatywny konstruktor ---")
    acc1 = CashAccount("Jan Kowalski", "PLN", 1000.0)
    acc2 = CashAccount.from_string("Adam Nowak:EUR:2500")
    margin_acc = MarginAccount("Piotr Wiśniewski", "PLN", 500.0, margin_limit=1500.0)

    assert CashAccount.total_accounts == 3, f"Błąd: oczekiwano 3 kont, jest {CashAccount.total_accounts}"
    print("Licznik i from_string: OK")

    print("\n--- 2. Wpłata i blokada edycji salda ---")
    acc1.deposit(500.0)
    assert acc1.balance == 1500.0

    try:
        acc1.balance = 999999.0
        assert False, "BŁĄD: Saldo nie powinno być bezpośrednio modyfikowalne!"
    except AttributeError:
        print("Blokada bezpośredniego zapisu salda: OK")

    print("\n--- 3. Wypłata z konta gotówkowego ---")
    acc1.withdraw(1200.0)
    assert acc1.balance == 300.0

    try:
        acc1.withdraw(500.0)  # Próba debetu
        assert False, "BŁĄD: CashAccount nie powinien pozwolić na ujemne saldo!"
    except ValueError:
        print("Walidacja salda CashAccount: OK")

    print("\n--- 4. Obsługa MarginAccount (debet) ---")
    assert margin_acc.available_funds == 2000.0  # 500 własne + 1500 limitu
    margin_acc.withdraw(1200.0)                  # Zejście na minus: saldo = -700.0

    assert margin_acc.balance == -700.0
    assert margin_acc.available_funds == 800.0   # 1500 limitu - 700 debetu

    try:
        margin_acc.withdraw(1000.0)              # Przekroczenie limitu debetu
        assert False, "BŁĄD: MarginAccount pozwolił przekroczyć limit debetu!"
    except ValueError:
        print("Kontrola limitu debetu: OK")

    print("\n--- 5. Metoda statyczna (prowizja) ---")
    fee = CashAccount.calculate_fee(10000.0, 0.0039)
    assert round(fee, 2) == 39.0
    print("Metoda statyczna: OK")

    print("\nWSZYSTKIE TESTY ZALICZONE!")