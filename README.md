# Aktywny firewall 
# Spis treści
- [Snort](#snort)
  + [Instalacja Snort na Ubuntu](#instalacja-snort-na-ubuntu)
  + [Pliki konfiguracyjne dla Snort](#pliki-konfiguracyjne-dla-snort)
  + [Wyłączenie domyślnych reguł](#wyłączenie-domyślnych-reguł)
  + [Utworzenie własnych reguł](#utworzenie-własnych-reguł)
  + [Testowanie konfiguracji](#testowanie-konfiguracji)
  + [Testowanie Snort na dwóch hostach](testowanie-snort-na-dwoch-hostach)

# Snort

## Instalacja Snort na Ubuntu
Ubuntu 16.04:
```console
sudo apt-get update
# instalacja zaleznosci dla snort:
sudo apt-get install libpcap-dev bison flex
# instalacja snort:
sudo apt-get install snort
# sprawdzenie instalacji:
snort -V
```
## Pliki konfiguracyjne dla Snort
```console
cd /etc/snort
ls
# Najwazniejsze z plikow:
# konfiguracja snort:
snort.conf  
# folder z regułami dopasowania do żądań:
rules 
```
## Wyłączenie domyślnych reguł
Najpierw należy nadać dla pliku odpowiednie prawa:
```console
sudo chmod 777 snort.conf
```
Plik snort.conf najlepiej otworzyć w edytorze gedit przez interfejs graficzny (otwórz za pomocą -> gedit).
W pliku snort.conf należy wykomentować wszystkie 'include' znajdujące się w kroku 7 jak na screenie poniżej.
Dzięki temu unikniemy analizowania nieistotnych z punktu widzenia projektu zdarzeń.

![01](https://user-images.githubusercontent.com/39568472/79751141-61b31e00-8312-11ea-89d4-e6d2f3bfa71c.PNG)

## Utworzenie własnych reguł
Własne reguły umieszczamy w pliku /etc/snort/rules/local.rules

Najpierw nadejmy mu prawa:
```console
sudo chmod 777 local.rules
```
Następnie możemy wpisać do niego testową regułę np. przy użyciu edytora gedit:
```console
alert icmp any any -> any any (msg:"ICMP connection attempt"; sid:1000004; rev:1;)

alert tcp any any -> any any (msg:"TCP connection attempt"; sid:1000001; rev:1;)
```
Powyższe reguły to reguły testowe, które powodują wypisanie alarmu przy dowolnym połączeniu TCP lub ICMP.

## Testowanie konfiguracji
Sprawdzamy poprawność konfiguracji:
```console
sudo snort -T -c /etc/snort/snort.conf
```
W wyniku powinniśmy dostać komunikat 'Snort successfully validated the configuration'. Jeśli wszystko jest ok to możemy teraz uruchomić Snort:

```console
snort -d -l /var/log/snort/ -h {YOUR_HOST_IP}/24 -A console -c /etc/snort/snort.conf
# -d  -> dumps application layer data
# -l dir -> logging directory
# -h home_net 
# -A console -> log to console
# -c file -> configuration file
```
YOUR_HOST_IP to adres ip, który możemy sprawdzić korzystając z komendy ifconfig. Jeśli wejdziemy na dowolną stronę w przeglądarce to powinniśmy przy tej konfiguracji dostać alert tcp w konsoli. 

Aby uruchomić alert icmp możemy wysłać ping na ip naszej domyślnej bramy, którą możemy sprawdzić komendą ip route.  

## Testowanie Snort na dwóch hostach

Jeśli sprawdziliśmy już, że działają alerty na jednym hoście, możemy teraz przejść do próby przeprowadzenia bardziej rzeczywistego testu. Spróbujemy wysłać ping z jednego hosta na drugi i uzyskać alert na jednym z hostów. Aby to zrobić najpierw potrzebujemy mieć dwie maszyny wirtualne, np. Linux Ubuntu oraz Linux Kali (obraz Kali do pobrania: https://www.offensive-security.com/kali-linux-vm-vmware-virtualbox-image-download/#1572305786534-030ce714-cc3b)

Link do całego filmiku z instalacją Kali: https://www.youtube.com/watch?v=TGOiAsSdADs

![image](https://user-images.githubusercontent.com/39568472/79867365-896fb800-83de-11ea-9725-b315b862ed35.png)

Następnie musimy utworzyć sieć dla naszych wirtualnych maszyn, wszystko pokazane jest w tym filmiku:

https://www.youtube.com/watch?v=vReAkOq-59I

Teraz uruchamiamy obie maszyny naraz, na tej na której mamy Snorta uruchamiany go. Sprawdzamy też IP komendą ifconfig. Na drugim hoście też sprawdzamy tą komendą IP, powinny być z tej samej sieci, ale różne. Z hosta atakującego wysyłamy ping do tego na którym działa Snort. Powinien się wyświetlić Alert. 
 

