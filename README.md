# Aktywny firewall 
# Spis treści
- [Snort](#snort)
  + [Instalacja Snort na Ubuntu](#instalacja-snort-na-ubuntu)
  + [Pliki konfiguracyjne](#pliki-konfiguracyjne)

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
man snort
```
## Pliki konfiguracyjne
Snort 

```console
cd /etc/snort
ls
# Najwazniejsze z plikow:
snort.conf -> konfiguracja snort
rules -> folder z regułami dopasowania do żądań
```
