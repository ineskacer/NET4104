import aioble
import uasyncio as asyncio
import binascii
import time

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
deviceJulienAddress = "c9:5d:58:11:33:7d"
deviceJulienName = "Amazfit GTS 4 Mini" 
orainNovaAddress = "34:81:f4:32:7a:07"
sarahTelAddress= "44:ea:30:84:12:fb"

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
            if binascii.hexlify(result.device.addr, ":").decode() == deviceJulienAddress:
                print("Object found : " + result.name() + " ///// MAC addr: " + deviceJulienAddress)
                
                return("Scan exit")            
    return None

async def device_rssi_print():
    
    while True:
        tab = []
        t = time.time()
        while(time.time()-t<6):
            async with aioble.scan(500, interval_us=30000, window_us=30000, active=True) as scanner:
                async for result in scanner: 
                    if binascii.hexlify(result.device.addr, ":").decode() == deviceJulienAddress:
                        
                            #print("Object found : ")
                            #print(" ///// RSSI: ")
                            #print(result.rssi)
                            tab.append(result.rssi)
                            #print("/////")
        print("Moyenne sur 3 sceondes RSSI : ")
        print(moyenne(tab))
        print("/////////////////")
      

def moyenne(tab):   
    res=0
    for i in tab:
          res+=i
    if(len(tab)!=0):
     return (res/len(tab))  