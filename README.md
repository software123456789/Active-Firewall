# Aktywny firewall 
# Spis treści
- [Snort](#snort)
  + [Instalacja Snort na Ubuntu](#instalacja-snort-na-ubuntu)
  + [Pliki konfiguracyjne dla Snort](#pliki-konfiguracyjne-dla-snort)

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
## Pliki konfiguracyjne dla Snort
```console
cd /etc/snort
ls
# Najwazniejsze z plikow:
# konfiguracja snort
snort.conf  
# folder z regułami dopasowania do żądań
rules 
```
