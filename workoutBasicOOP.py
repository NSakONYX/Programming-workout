"""
ZADANIE: SYSTEM ZARZĄDZANIA FLOTĄ (Vehicle & ElectricVehicle)

Zaimplementuj dwie klasy zgodnie z poniższą specyfikacją, łącząc:
- atrybuty klasowe i type(self)
- hermetyzację konwencyjną (_atrybut)
- dekoratory @property i @<property>.setter
- @staticmethod oraz @classmethod
- dziedziczenie, super() i nadpisywanie metod (overriding)

====================================================================
1. KLASA BAZOWA: Vehicle
====================================================================
Atrybuty klasy:
    - total_vehicles = 0  (licznik wszystkich pojazdów)

Konstruktor (__init__):
    - parametry: self, brand (str), model (str), year (int)
    - atrybuty publiczne:
        * self.brand = brand
        * self.model = model
        * self.year = year
    - atrybuty wewnętrzne (nie podawane w parametrach inita):
        * self._mileage = 0.0
        * self._speed = 0.0
    - licznik:
        * inkrementuj atrybut klasowy w locie za pomocą type(self).total_vehicles += 1

Właściwości (@property):
    - speed (getter):
        * zwraca self._speed
    - speed (setter):
        * przyjmuje nowa_predkosc (float/int)
        * walidacja: zakres od 0.0 do 250.0 km/h
        * jeśli wartość jest poza zakresem -> rzuć ValueError z czytelnym komunikatem
        * jeśli poprawna -> przypisz do self._speed
    - mileage (getter):
        * zwraca self._mileage
        * BRAK settera (pole ma być tylko do odczytu z zewnątrz)

Metody:
    - drive(self, distance_km):
        * jeśli distance_km > 0 -> zwiększa self._mileage o ten dystans
    - @staticmethod km_to_miles(km):
        * przyjmuje km (float/int)
        * zwraca przeliczoną wartość: km * 0.621371
    - @classmethod from_string(cls, vehicle_str):
        * przyjmuje string w formacie "Marka,Model,Rok" (np. "Renault,Clio,2023")
        * parsuje string (np. split(","))
        * rzutuje rok na int
        * zwraca nową instancję za pomocą cls(brand, model, year)

====================================================================
2. KLASA POCHODNA: ElectricVehicle(Vehicle)
====================================================================
Konstruktor (__init__):
    - parametry: self, brand, model, year, battery_capacity (float, w kWh)
    - wywołanie konstruktora bazy:
        * super().__init__(brand, model, year)
    - atrybuty własne:
        * self.battery_capacity = battery_capacity
        * self._battery_level = 100.0 (stan baterii w %, domyślnie pełna)

Właściwości (@property):
    - estimated_range (getter):
        * wyliczane dynamicznie: (self._battery_level / 100) * self.battery_capacity * 5
        * zwraca szacowany zasięg w km (float)

Nadpisanie metody (overriding):
    - drive(self, distance_km):
        * wywołaj metodę rodzica przez super().drive(distance_km)
        * zmniejsz poziom naładowania baterii (self._battery_level):
          zużycie = distance_km / 5.0 (czyli 1% na każde 5 km)
        * poziom baterii nie może spaść poniżej 0.0%
====================================================================
"""

class Vehicle:
    
    total_vehicles = 0
    
    '''Inicjalizator'''
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        
        self._mileage = 0.0
        self._speed = 0.0
        
        Vehicle.total_vehicles += 1
        
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, new_speed):
        if (0.0 < float(new_speed) and float(new_speed) < 250.0):
            self._speed = float(new_speed)
        else: 
            raise ValueError("Podana niewlasciwa predkosc.")
        
    @property
    def mileage(self):
        return self._mileage
    
    
    
    def drive(self, distance_km):
        if (distance_km>0): self._mileage += distance_km
        
    '''Metoda statyczna - mozliwa do wykorzystania bez tworzenia obiektu'''
    @staticmethod
    def km_to_miles(km):
        return km*0.621371
    
    @classmethod #classmethod - daja mozliwosc stworzenia alternatywnego konstruktora klasy gdyz w pythonie nie da sie stworzyc kilku __init__
    def from_string(cls, vehicle_str):
        brand, model, year = vehicle_str.split(",")
        
        return cls(brand, model, int(year)) #cls - referencja do samej klasy, a nie jej konkretnego obiektu
        #wywolanie przykladowe Vehicle = Vehicle.from_string(("Toyota", "Avensis", "2012"))
        
        

class ElectricVehicle(Vehicle):
    
    def __init__(self,brand,model,year,battery_capacity):
        super().__init__(brand,model,year)
        
        self.battery_capacity = battery_capacity
        self._battery_level = 100.0
        
    @property
    def estimated_range(self):
        return (self._battery_level/100)*self.battery_capacity*5
    
    def drive(self, distance_km):
        super().drive(distance_km)
        if (self._battery_level > distance_km/5.0):
            self._battery_level -= distance_km/5.0
        else:
            raise ValueError("Za malo procent baterii.")  
        
    
    
if __name__ == "__main__":
    print("--- 1. Test licznika i from_string ---")
    v1 = Vehicle("Toyota", "Corolla", 2020)
    v2 = Vehicle.from_string("Renault,Clio,2023")
    ev = ElectricVehicle("Tesla", "Model 3", 2024, battery_capacity=75.0)

    print(f"Liczba aut we flocie: {Vehicle.total_vehicles}")  # Oczekiwane: 3
    assert Vehicle.total_vehicles == 3, "Błąd: licznik powinien wynosić 3"

    print("\n--- 2. Test właściwości speed i walidacji ---")
    v1.speed = 120.0
    print(f"Prędkość v1: {v1.speed} km/h")  # Oczekiwane: 120.0
    assert v1.speed == 120.0

    try:
        v1.speed = -15.0
        print("BŁĄD: Setter przepuścił ujemną prędkość!")
    except ValueError as e:
        print(f"Walidacja ujemnej prędkości działa: {e}")

    try:
        v1.speed = 300.0
        print("BŁĄD: Setter przepuścił prędkość > 250!")
    except ValueError as e:
        print(f"Walidacja zbyt dużej prędkości działa: {e}")

    print("\n--- 3. Test blokady zapisu mileage (Read-Only) ---")
    try:
        v1.mileage = 150000.0
        print("BŁĄD: Mileage nie jest polem read-only!")
    except AttributeError:
        print("Mileage jest poprawnie zablokowane przed bezpośrednim zapisem.")

    print("\n--- 4. Test jazdy i baterii w ElectricVehicle ---")
    print(f"Początkowy zasięg EV: {ev.estimated_range:.1f} km")  # Oczekiwane: 375.0 km
    assert ev.estimated_range == 375.0

    ev.drive(100)
    print(f"Przebieg EV po jeździe: {ev.mileage} km")           # Oczekiwane: 100.0 km
    print(f"Poziom baterii EV: {ev._battery_level:.1f}%")        # Oczekiwane: 80.0%
    print(f"Nowy zasięg EV: {ev.estimated_range:.1f} km")       # Oczekiwane: 300.0 km
    assert ev.mileage == 100.0
    assert ev._battery_level == 80.0
    assert ev.estimated_range == 300.0

    print("\n--- 5. Test metody statycznej ---")
    miles = Vehicle.km_to_miles(100)
    print(f"100 km to w milach: {miles:.2f}")                   # Oczekiwane: 62.14
    assert round(miles, 2) == 62.14

    print("\nWSZYSTKIE TESTY ZALICZONE!")