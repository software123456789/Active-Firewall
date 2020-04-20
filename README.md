# Aktywny firewall 
# Spis treści
- [Snort](#snort)
  + [Instalacja Snort na Ubuntu](#instalacja-snort-na-ubuntu)
  + [Pliki konfiguracyjne dla Snort](#pliki-konfiguracyjne-dla-snort)
  + [Wyłączenie domyślnych reguł](#wyłączenie-domyślnych-reguł)
  + [Utworzenie własnych reguł](#utworzenie-własnych-reguł)
  + [Testowanie konfiguracji](#testowanie-konfiguracji)

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
YOUR_HOST_IP to adres, który możemy sprawdzić korzystając z komendy ifconfig. Jeśli wejdziemy na dowolną stronę w przeglądarce to powinniśmy przy tej konfiguracji dostać alert tcp w konsoli. Aby uruchomić alerr icmp możemy wysłać ping na naszą domyślną bramę, którą możemy sprawdzić komendą ip route.  


