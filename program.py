#! /usr/bin/python3

import os, time, subprocess

class AtProgram:
    # os.system('notepad')
    tool = 'atmelice'

    def __init__(self, device, interface, atprogram):
        self.device = device
        self.interface = interface
        self.prefix = atprogram

        self.preprocess()

    def program(self, file):
        print("File Size: %.1fK" % (int(os.path.getsize(file))/1024))
        print("Date Motified: ", time.asctime(time.localtime(os.path.getmtime(file))))

        if True:
            self.flash(file)
        else:
            self.eeprom(file)

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
        arguments = " info " + " --signature "
        cmd = self.prefix + arguments
        self.actuator(cmd)

    def preprocess(self):
        self.prefix += " -t %s " % self.tool
        self.prefix += " -i %s " % self.interface
        self.prefix += " -d %s " % self.device

    def actuator(self, cmd):
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        ps.wait()
        if ps.returncode == 0:
            print(str(ps.stdout.read(), encoding="utf-8").split('\r\n')[1])
        else:
            pass

    def log(self):
        pass

def main():
    device = "ATA5702M322"
    interface = "ISP"
    atprogram = r'"C:\Program Files (x86)\Atmel\Studio\7.0\atbackend\atprogram.exe "'

    print("%s Program Tool using %s" % (device, interface))

    programer = AtProgram(device, interface, atprogram)
    while True:
        cmd = input("\nEnter CMD: ")
        if cmd == "erase":
            pass
        elif cmd == "signature":
            programer.signature()
        elif os.path.isfile(cmd) and os.path.exists(cmd):
            programer.program(cmd)
        else:
            print("Unrecognized CMD\n")

if __name__ == "__main__":
    main()