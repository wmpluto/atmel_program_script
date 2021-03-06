#! /usr/bin/python3

import os, time, subprocess

class AtProgram:
    # os.system('notepad')
    tool = 'atmelice'
    fuses_expected = 'E299FF'
    fuses_SPI_bit = 15 - 1
    eeprom_start = '0000'
    flash_start = '0000'

    def __init__(self, device, interface, atprogram):
        self.device = device
        self.interface = interface
        self.prefix = atprogram

        self.preprocess()

    def program(self, file):
        size = int(os.path.getsize(file))/1024
        print("File Size: %.1fK" % size)
        print("Date Motified: ", time.asctime(time.localtime(os.path.getmtime(file))))

        with open(file, mode='rb') as f:
            line = f.readline()
            try:
                address = line[3:7]
                if address == self.flash_start.encode('ansi') and size > 4:
                    self.flash(file)
                elif address == self.eeprom_start.encode('ansi'):
                    self.eeprom(file)
                else:
                    print("start address not detected")
            except Exception as e:
                print("start address not detected")

    def flash(self, file):
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 -xr -cl 2mhz program -c --verify -f foo61.hex
        print("programing flash...")
        arguments = " program " + " -c " + " --verify " + " --format hex " + " -f " + file
        self.actuator(arguments)

    def eeprom(self, file):
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 program -ee --format hex -f fooEEPROM.eep
        print("programing eeprom...")
        arguments = " program " + " -ee " + " --verify " + " --format hex " + " -f " + file
        self.actuator(arguments)

    def erase(self):
        # atprogram -t atmelice -i ISP -d ATA5702M322 chiperase
        arguments = " chiperase "
        self.actuator(arguments)
        pass

    def fuses(self, values = 0):
        # atprogram -t atmelice -i ISP -d ATA5702M322 read -fs
        # atprogram -t avrispmk2 -i ISP -d atmega128rfr2 -cl 65khz write -fs --values e6d7f8
        if values:
            if (1 << self.fuses_SPI_bit) & int(values, 16):
                print("SPI_ENABLE bit must set to 0")
            else:
                print("writing %s to fuses" % values)
                arguments = " write " + " -fs " + " --values " + values
                self.actuator(arguments)
        else:
            arguments = " read " + " -fs "
            act = self.actuator(arguments)
            if act['returncode'] == 0 and act['output'][0] == ':':
                l = int(act['output'][1:3], 16)
                fs = act['output'][(-2-l*2):-2]
                if fs.lower() != self.fuses_expected.lower():
                    c = input("fuses is not equal as expected, update it?(y/n) ")
                    if c == 'y':
                        self.fuses(self.fuses_expected)

    def signature(self):
        # atprogram.exe -t atmelice -i ISP -d ATA5702M322 info --signature
        arguments = " info " + " --signature "
        self.actuator(arguments)

    def preprocess(self):
        self.prefix += " -t %s " % self.tool
        self.prefix += " -i %s " % self.interface
        self.prefix += " -d %s " % self.device

    def actuator(self, arguments):
        cmd = self.prefix + arguments
        ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        ps.wait()
        output = ""
        if ps.returncode == 0:
            output = str(ps.stdout.read(), encoding="utf-8").split('\r\n')[1]
            print(output)
        else:
            pass
        return {"returncode": ps.returncode, "output": output}

    def log(self):
        pass

def main():
    device = "ATmega2560"
    interface = "JTAG"
    atprogram = r'"C:\Program Files (x86)\Atmel\Studio\7.0\atbackend\atprogram.exe "'

    print("%s Tool using %s" % (device, interface))

    programer = AtProgram(device, interface, atprogram)
    programer.fuses()
    last_cmd = ''
    while True:
        print("\n%s Tool using %s" % (device, interface))
        cmd = input("Enter CMD: ")
        if cmd == '':
            cmd = last_cmd
            print("Repeat last command:", cmd)
        if cmd == "erase":
            programer.erase()
        elif "fuses" in cmd:
            cmds = cmd.split()
            if len(cmds) == 2:
                programer.fuses(cmds[1])
            else:
                programer.fuses()
        elif cmd == "signature":
            programer.signature()
        elif os.path.isfile(cmd) and os.path.exists(cmd):
            programer.program(cmd)
        else:
            print("Unrecognized CMD")

        last_cmd = cmd

if __name__ == "__main__":
    main()