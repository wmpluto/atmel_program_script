#! /usr/bin/python3

import os

class AtProgram:
    # os.system('notepad')
    atprogram = r'"C:Program Files (x86)\Atmel\Studio\7.0\atbackend\atprogram.exe"'
    device = "ATA5702M322"

    def __init__(self, device, interface):
        self.device = device
        self.interface = interfaces

    def flash(self, file):
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 -xr -cl 2mhz program -c --verify -f foo61.hex
        pass

    def eeprom(self, file):
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 program -ee --format hex -f fooEEPROM.eep
        pass

    def erase(self):
        # atprogram -t atmelice -i ISP -d ATA5702M322 chiperase
        pass

    def fuses(self, values):
        # atprogram -t atmelice -i ISP -d ATA5702M322 read -fs
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 -cl 65khz write -fs --values e6d7f8
        pass

    def signature(self):
        # atprogram.exe -t atmelice -i ISP -d ATA5702M322 info --signature
        pass
        
def main():
    print("ATA5702 Program Tool")

    while True:
        cmd = input("Enter CMD: ")
        if cmd == "erase":
            pass
        elif os.path.exists(cmd):
            print(cmd)
        else:
            print("Unrecognized CMD\n")

if __name__ == "__main__":
    main()