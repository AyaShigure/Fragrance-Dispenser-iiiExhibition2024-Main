from machine import Pin, ADC
import time

time.sleep(3)

buzzer = Pin(0, Pin.OUT)

for i in range(5):
    buzzer.value(1)
    time.sleep(0.1)
    buzzer.value(0)
    time.sleep(0.1)

led = Pin(25, Pin.OUT)
pot = ADC(Pin(26))
start = time.time()
counter = 0

start = time.time()
for i in range(100):
    while (time.time() - start) != 2:
        pot_value = pot.read_u16() # read value, 0-65535 across voltage range 0.0v - 3.3v
        counter += 1

print(f'How many adc is read in 1 second? -> {counter}')

print('damn')

counter = 0
while(1):
    counter += 1
    if counter % 5 == 0:
        buzzer.value(1)
        time.sleep(0.1)
        buzzer.value(0)
        time.sleep(0.1)
        print('Damn')
    led.toggle()
    time.sleep(1)
