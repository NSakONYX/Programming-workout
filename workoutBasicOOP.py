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
        
        type(self).total_vehicles += 1
        
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, new_speed):
        if (0.0 < new_speed < 250.0):
            self._speed = new_speed
        else: 
            return ValueError("Podana niewlasciwa predkosc.")
        
    @property
    def getMileage(self):
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
        return (self._battery_level/100)*self.battery_capacity
    
    def drive(self, distance_km):
        super().drive(distance_km)
        if (self._battery_level > distance_km/5.0):
            self._battery_level -= distance_km/5.0
        else:
            return ValueError("Za malo procent baterii.")  
        
    