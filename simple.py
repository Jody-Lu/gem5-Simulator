import m5
from m5.objects import *

# Create system object
system = System()

# Set the clock on the system
system.clk_domain = srcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set memory
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# Create CPU
system.cpu = TimingSimpleCPU()

# Create the system-wide memory bus
system.membus = CoherentXBar()

# Connect the I-cache and D-cache ports directly to the membus
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

