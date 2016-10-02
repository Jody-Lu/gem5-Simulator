import m5
from m5.objects import *
from cache import *

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

# Create the L1 caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()

# Connect icahe and dcache port to CPU
system.cpu.icache.connectCPU(system.cpu)
system.cpu.dcache.connectCPU(system.cpu)

# Create L2 cache bus
system,l2bus = CoherentXBar()
system.cpu.icache.connectBus(system.l2bus)
system.cpu.dcache.connectBus(system.l2bus)

# Create L2 cache and connect it to L2 bus
system.l2cache = L2Cache()
system.l2cache.connectCPUSideBus(system.l2bus)
system.l2cache.connectMemSideBus(system.membus)

# create the interrupt controller for the CPU and connect to the membus
system.cpu.createInterruptController()
system.cpu.interrupts.pio = system.membus.master
system.cpu.interrupts.int_master = system.membus.slave
system.cpu.interrupts.int_slave = system.membus.master

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = DDR3_1600_x64()
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# Connect the system up to the membus
system.system_port = system.membus.slave

# Create a process for a simple "Hello World" application
process = LiveProcess()
# Set the command
# cmd is a list which begins with the executable (like argv)
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
# Set the cpu to use the process as its workload and create thread contexts
system.cpu.workload = process
system.cpu.createThreads()

# set up the root SimObject and start the simulation
root = Root(full_system = False, system = system)
# instantiate all of the objects we've created above
m5.instantiate()

print "Beginning simulation!"
exit_event = m5.simulate()
print 'Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause())

