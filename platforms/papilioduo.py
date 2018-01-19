# Papilio Duo
# https://github.com/GadgetFactory/Papilio-DUO
# http://papilio.cc/index.php?n=Papilio.PapilioDUOHardwareGuide
# http://papilio.cc/index.php?n=Papilio.DUOStart
# http://www.papilio.cc/uploads/Papilio/Papilio_DUO.pdf?raw=true
# http://forum.gadgetfactory.net/files/file/235-papilio-duo-generic-ucf/
#
# SPI Flash:
# http://www.macronix.com/Lists/Datasheet/Attachments/6636/MX25L6445E,%203V,%2064Mb,%20v1.8.pdf
#
# Xilinx Spartan 6 FPGA _and_ Arduino compatible ATmega32U4 micro
# on same board, with many shared signals.  Several lines are 5V 
# compatible to inter-operate with the Arduino, through in-series
# resistors; see:
#
# http://papilio.cc/index.php?n=Papilio.PapilioDUOHardwareGuide#PProIO
#
# Includes 64Mbit Macronix MX25L6445 SPI Flash, and FT2232H dual 
# channel USB chip.  Appears to have 32MHz clock (31.25 ns 50% duty cycle)
#
# Available in 512KB And 2MB SRAM models (static RAM; not DRAM).
#
# Programming:
# http://papilio.cc/index.php?n=Papilio.GettingStarted#Linux
# https://github.com/GadgetFactory/Papilio-Loader/
#
# May also be possible to add to OpenOCD, eg via patch at:
# https://github.com/timvideos/conda-hdmi2usb-packages/tree/master/openocd
#
# NOTE: the many, many, pins that map tp Arduino pins not currently mapped;
# just the minimal pins to get serial working
#
# NOTE: external SRAM not currently wired either; unclear how to handle
# external SRAM, so attempting board without main ram


from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform


_io = [
    ("clk32", 0, Pins("P94"), IOStandard("LVTTL")),

    ("serial", 0,
        Subsignal("tx", Pins("P141"), IOStandard("LVTTL"),
                  Drive(8), Misc("SLEW=FAST")),
        Subsignal("rx", Pins("P46"), IOStandard("LVTTL"),
                  Drive(8), Misc("SLEW=FAST"))),

    ("spiflash", 0,
        Subsignal("cs_n", Pins("P38")),
        Subsignal("clk", Pins("P70")),
        Subsignal("mosi", Pins("P64")),
        Subsignal("miso", Pins("P65"), Misc("PULLUP")),
        IOStandard("LVTTL"), Drive(8), Misc("SLEW=FAST")),
]

_connectors = [
#   ("P6", "T3 R3 V5 U5 V4 T4 V7 U7"),
#   ("P7", "V11 U11 V13 U13 T10 R10 T11 R11"),
#   ("P8", "L16 L15 K16 K15 J18 J16 H18 H17")
]


class Platform(XilinxPlatform):
    name = "papilioduo"
    default_clk_name = "clk32"
    default_clk_period = 10

    # The Papilio Duo has a XC6SLX9 which bitstream takes up ~2.6Mbit (1484472 bytes)
    # 0x80000 offset (4Mbit) gives plenty of space
    gateware_size = 0x80000

    # Macronix MX25L6445 SPI Flash
    # 64Mb - ?? MHz clock frequency
    # FIXME: Create a "spi flash module" object in the same way we have SDRAM
    # module objects.
    #	/*             name,  erase_cmd, chip_erase_cmd, device_id, pagesize, sectorsize, size_in_bytes */
    #	FLASH_ID("st m25p16",      0xd8,           0xc7, 0x00152020,   0x100,    0x10000,      0x200000),
    spiflash_model = "mx25l6445"
    spiflash_read_dummy_bits = 8
    spiflash_clock_div = 4
    spiflash_total_size = int((64/8)*1024*1024) # 64Mbit
    spiflash_page_size = 256
    spiflash_sector_size = 0x10000              # 64kB (also 32kB / 4kB modes)

    def __init__(self):
        XilinxPlatform.__init__(self, "xc6slx9-2tqg144", _io, _connectors)

    def create_programmer(self):
        raise NotImplementedError
