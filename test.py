import aioble
import uasyncio as asyncio


async def main():
    #On mettre ici le programme principal de notre code final
    return None
            

#Scan BLE devices around         
async def scan_around():
     while True: 
        async with aioble.scan(duration_ms=5000) as scanner:
            async for result in scanner:
                print(result, result.name(), result.rssi, result.services())
       
             
       
                
deviceName = "Amazfit GTS 4 Mini" # montre de julien
#Cette fonction scan et retourne uniquement le device que vous voulez détecter
async def device_to_detect():
    # Scan for 5 seconds, in active mode, with very low interval/window (to
    # maximise detection rate).
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            # Match avec le nom du device (on détectera avec l'adresse MAC dès qu'on saura faire)
            if result.name() == deviceName:
                print("Object found : " + result.name())
                
                return("Scan exit")            
    return None
    
asyncio.run(device_to_detect())