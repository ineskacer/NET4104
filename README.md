The goal of this project is to create a BLE device & distance detector with ESP32-S3.


How to use it :

Using ampy module (to flash your code)

    ampy --port <your port> put <file.py>

Using picocom (to monitor the output)

    picocom -b 115200 <your port>

In picocom : 

    import <file>
    import uasyncio

To call a function with uasyncio in picocom :

    uasyncio.run(file.function())

To start, we recommend calling the main funtion.
You will have access to the two features of our code.

    uasyncio.run(main.main())

You can also access these features by yourself.
To scan the nearby devices : 

    uasyncio.run(main.scan_around())


To monitor the distance between ESP32 and your device :

    uasynci.run(main.calibration_measure(<deviceAddress>))

The format of the input address should be "11:22:33:aa:bb:cc"




