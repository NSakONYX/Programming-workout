import random

def make_dict():
    # 1. Pule danych do losowania
    tickery = ['NVDA', 'PLTR', 'TSLA']
    statusy = ['completed', 'completed', 'completed', 'completed', 'failed', 'rejected'] # Większa szansa na sukces

    # 2. Inicjalizacja pustego słownika z kluczami
    surowe_dane = {
        'symbol': [],
        'price': [],
        'volume': [],
        'status': []
    }

    # 3. Generowanie 500 losowych transakcji
    for _ in range(500):
        symbol = random.choice(tickery)
        
        # Symulacja wahań cenowych dla poszczególnych spółek
        if symbol == 'NVDA':
            cena = round(random.uniform(130.0, 145.0), 2)
        elif symbol == 'PLTR':
            cena = round(random.uniform(165.0, 175.0), 2)
        else: # TSLA
            cena = round(random.uniform(200.0, 220.0), 2)
            
        surowe_dane['symbol'].append(symbol)
        surowe_dane['price'].append(cena)
        surowe_dane['volume'].append(random.randint(10, 500))
        surowe_dane['status'].append(random.choice(statusy))
        
    print("Wygenerowano 500 transakcji")
    return surowe_dane
    