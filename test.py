import aioble
import uasyncio as asyncio
import binascii


async def main():
    #On mettre ici le programme principal de notre code final
    return None
            

#Scan BLE devices around         
async def scan_around():
     while True: 
        async with aioble.scan(duration_ms=5000) as scanner:
            async for result in scanner:
                #Des données sont encore redondantes ici car phase de test
                print(result)
                print(result.device)
                #Obtenu avec doc github class Device.py, Addr MAC au format str
                print(binascii.hexlify(result.device.addr, ":").decode())
                print(result.name())
                print(result.services())
                print(result.rssi)
                print("////////////////////////////\n")
             
             
# montre de julien
deviceAddress = "c9:5d:58:11:33:7d"
deviceName = "Amazfit GTS 4 Mini" 

#Cette fonction scan et retourne uniquement le device que vous voulez détecter et s'arrête après détection
async def device_to_detect():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # Match avec le nom du device 
            #if result.name() == deviceName:binascii.hexlify(result.device.addr, ":").decode())
            #    print("Object found : " + result.name())
            # Ou match avec MAC
            if binascii.hexlify(result.device.addr, ":").decode() == deviceAddress:
                print("Object found : " + result.name() + " ///// MAC addr: " + deviceAddress)
                
                return("Scan exit")            
    return None
    
asyncio.run(device_to_detect())