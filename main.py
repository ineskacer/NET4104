import aioble
import uasyncio as asyncio
import binascii
import time

async def main():
    print("$ Bienvenue dans le Projet NET4104 ")
    print("$ Pour afficher les objets BLE autour, tapez 'scan'")
    print("$ Pour mesurer la distance à un appareil, tapez 'measure'")
    print("$ Choisissez un mode : ")
    char = input("$ ")
    if(char=="scan"):
        asyncio.run(scan_around())
        return None
    elif(char=="measure"):
        print("$ Tapez l'adresse de l'appareil dont vous voulez connaitre la distance")
        while True:
            addr = input("$ ")
            if(len(addr) == 17):
                break
            print("Veuillez entrer une adresse valide")
       
        asyncio.run(calibration_measure(addr))   
        return None
    return None


#Calibration for the distance
async def calibration_measure(deviceAdress):    
    print("$ Déplacez-vous à 1 mètre de l'appareil")
    rssi_values = []
    print("$ Tapez 'ok' lorsque vous êtes prêt.")
    print("$ Après avoir tapé ok, veuillez laisser le device immobile pendant 10 secondes")
    char = input("$ ")
    if (char != "ok"):
        print("Erreur de saisie")
        print("Veuillez recommencer la calibration depuis le début")
        return None
    else:
        # Scan for 10 second and add the average RSSI value to the list
        # Getting the "measured power" at 1 meter away from the device to use in the formula
        async with aioble.scan(10000, interval_us=30000, window_us=30000, active=True) as scanner:
            async for result in scanner:
                if binascii.hexlify(result.device.addr, ":").decode() == deviceAdress:
                    rssi_values.append(result.rssi)
        measured_power = moyenne(rssi_values)
        if(measured_power is not None):
            print("$ La calibration a bien été effectuée")
            print("$ Vous pouvez bougez librement le device")
        else:
            print("$ Une erreur est apparue dans la calibration. Veuillez recommencer depuis le début")
            return -1
        print("$ Indiquez la puissance relative de votre émetteur Bluetooth : faible, moyen ou fort")
        puissance = input("$ ")
        if(puissance== "faible"):
             asyncio.run(device_rssi_to_meter(deviceAdress, measured_power, 2))
        elif(puissance== "moyen"):
             asyncio.run(device_rssi_to_meter(deviceAdress, measured_power, 3))
        elif(puissance== "fort"):
             asyncio.run(device_rssi_to_meter(deviceAdress, measured_power, 4))
    

#Scan BLE devices around         
async def scan_around():
    while True: 
        async with aioble.scan(duration_ms=5000) as scanner:
            async for result in scanner:
                print("////////////////////////////\n")
                #Obtenu avec doc github class Device.py, Addr MAC au format str
                print("Addresse du device: ", binascii.hexlify(result.device.addr, ":").decode())
                print("Nom du device:      ", result.name())
                #print("Services du device: ", result.services())
                print("RSSI:               ", result.rssi)

        
        
#Cette fonction scan et retourne uniquement le device que vous voulez détecter et s'arrête après détection
async def device_to_detect(deviceAddress):
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
 

 