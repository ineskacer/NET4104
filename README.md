The goal of this project is to create an BLE device detector with ESP32-S3.


How to use it :

Using ampy module (to flash your code)

    ampy --port <your port> put <file.py>

Using picocom (to monitor the output)

    picocom -b 115200 <your port>

In picocom : 

    import <file>
    import uasyncio

To call a function (still in picocom)

    uasyncio.run(file.function())


