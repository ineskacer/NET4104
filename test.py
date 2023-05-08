import aioble
import uasyncio as asyncio
import binascii
import time


# montre de julien
deviceJulienAddress = "c9:5d:58:11:33:7d"
deviceJulienName = "Amazfit GTS 4 Mini" 
orainNovaAddress = "34:81:f4:32:7a:07"
sarahTelAddress= "44:ea:30:84:12:fb"

async def main():
    #On mettre ici le programme principal de notre code final
    return None

#Calibration for the distance
async def calibration(deviceAdress):
    distances = [5, 10, 20]
    measures = []
    for distance in distances:
        print("Déplacez-vous à " + distance + "m de l'appareil")
        rssi_values = []
        char = input("Tapez 'ok' lorsque vous êtes prêt.")
        if (char != "ok"):
            print("Erreur de saisie")
            print("Veuillez recommencer la calibration")
            return None
        else:
            # Scan for 5 second and add the average RSSI value to the list
            async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
                async for result in scanner:
                    if binascii.hexlify(result.device.addr, ":").decode() == deviceAdress:
                        rssi_values.append(result.rssi)
            avg_rssi = sum(rssi_values) / len(rssi_values)
            measures.append((distance, avg_rssi))
        print("Distance: "+ distance +"m / RSSI: " + avg_rssi)
    return measures



#Calibration for the distance
async def calibration_measure(deviceAdress = deviceJulienAddress):    
    print("Déplacez-vous à 1 mètre de l'appareil")
    rssi_values = []
    char = input("Tapez 'ok' lorsque vous êtes prêt.")
    if (char != "ok"):
        print("Erreur de saisie")
        print("Veuillez recommencer la calibration")
        return None
    else:
        # Scan for 10 second and add the average RSSI value to the list
        # Getting the "measured power" at 1 meter away from the device to use in the formula
        async with aioble.scan(10000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if binascii.hexlify(result.device.addr, ":").decode() == deviceAdress:
                    rssi_values.append(result.rssi)
        measured_power = moyenne(rssi_values)
        if(measured_power !=0):
            print("La calibration a bien été effectuée")
        else:
            print("Une erreur est apparue dans la calibration. Veuillez recommencer depuis le début")
            return -1
        ### A FAIRE : CHANGER N ET COMPRENDRE LA VALEUR DE   N   
        asyncio.run(device_rssi_to_meter(deviceAdress, measured_power, 4))
             
    

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

async def device_rssi_to_meter(deviceAdress, measured_power, N):
    
    while True:
        tab = []
        t = time.time()
        while(time.time()-t<6):
            async with aioble.scan(500, interval_us=30000, window_us=30000, active=True) as scanner:
                async for result in scanner: 
                    if binascii.hexlify(result.device.addr, ":").decode() == deviceAdress:
                            tab.append(result.rssi)
        
        moyenne_rssi = moyenne(tab)
        print("Moyenne sur 3 sceondes RSSI : ")
        print("Nombre de valeurs obtenues sur 3 secondes : ", len(tab))
        print("RSSI sur 3 secondes : ", moyenne_rssi)
        # Return the distance in meters, starting from the measured power (rssi at 1 meter)
        # N ranges from 2 to 4 depending on  and the rssi (Received Signal Strength Intensity)
        print("Distance from ESP32 to object in meters :", 10**((measured_power - moyenne_rssi)/(10*N)))
        print("/////////////////")
      

def moyenne(tab):   
    res=0
    for i in tab:
          res+=i
    if(len(tab)!=0):
     return (res/len(tab))  