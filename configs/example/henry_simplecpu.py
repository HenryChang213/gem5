# Copyright (c) 2012-2013 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright (c) 2006-2008 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Simple test script
#
# "m5 test.py"

import argparse
import sys
import os

import m5
from m5.defines import buildEnv
from m5.objects import *
from m5.params import NULL
from m5.util import addToPath, fatal, warn

addToPath('../')

from ruby import Ruby

from common import Options
from common import Simulation
from common import CacheConfig
from common import CpuConfig
from common import ObjectList
from common import MemConfig
from common.FileSystemConfig import config_filesystem
from common.Caches import *
from common.cpu2000 import *

# from XBar import L3XBar

class L1Cache_henry(Cache):
    assoc = 2
    tag_latency = 1
    data_latency = 1 
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20
    def __init__(self):
        super(L1Cache_henry, self).__init__()
        pass
    def connectBus(self, bus):
        """Connect this cache to a memory-side bus"""
        self.mem_side = bus.cpu_side_ports
    def connectCPU(self, cpu):
        """Connect this cache's port to a CPU-side port
           This must be defined in a subclass"""
        raise NotImplementedError

class L1DCache_henry(L1Cache_henry):
    size='32kB'      
    def __init__(self,l1i_size):
        super(L1DCache_henry,self).__init__()
        self.size=l1i_size
    def connectCPU(self,cpu):
        self.cpu_side=cpu.icache_port

class L1ICache_henry(L1Cache_henry):
    size='16kB'
    def __init__(self,l1d_size):
        super(L1ICache_henry,self).__init__()
        self.size=l1d_size
    def connectCPU(self,cpu):
        self.cpu_side=cpu.dcache_port

class L2Cache_henry(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 20
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    def __init__(self, l2_size,tag_latency=1,data_latency=1):
        super(L2Cache_henry, self).__init__()
        self.size = l2_size
        self.tag_latency=tag_latency
        self.data_latency=data_latency
        self.response_latency=data_latency
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L3Cache_henry(Cache):
    size = '1024kB'
    assoc = 64
    tag_latency = 200
    data_latency = 200
    response_latency = 200
    mshrs = 32
    tgts_per_mshr = 24
    def __init__(self, l3_size):
        super(L3Cache_henry, self).__init__()
        self.size = l3_size
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.mem_side_ports
    def connectMemSideBus(self, bus):
        self.mem_side = bus.cpu_side_ports

class L3XBar(CoherentXBar):
# 256-bit crossbar by default
    width = 32
    frontend_latency = 1
    forward_latency = 0
    response_latency = 1
    snoop_response_latency = 1
    snoop_filter = SnoopFilter(lookup_latency = 0)

def get_process(args):
    """Interprets provided args and returns a list of processes"""

    multiprocesses = []

    workload=args.workload
    process = Process(pid = 100)
    process.executable = workload.split()[0]
    process.cwd = os.getcwd()
    process.gid = os.getgid()
    process.cmd = workload.split()

    return process

parser=argparse.ArgumentParser(description='simple cpu')
parser.add_argument('--workload',type=str,default='')
# parser.add_argument('--option',type=str)
parser.add_argument('--cpu-type',type=str,default='O3')
parser.add_argument('--num-cpus',type=int,default=1)
# parser.add_argument('--l1i_size',type=str,default='64kB')
# parser.add_argument('--l1d_size',type=str,default='64kB')
parser.add_argument('--l2-size',type=str,default='512kB')
parser.add_argument('--l2-tag',type=int,default=10)
parser.add_argument('--l2-data',type=int,default=10)


args=parser.parse_args()


# create the system we are going to simulate
system = System(cache_line_size = 64)

# Set the clock frequency of the system (and all of its children)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '3GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up the system
system.mem_mode = 'timing'               # Use timing accesses
system.mem_ranges = [AddrRange('8GB')] # Create an address range

# Create a pair of simple CPUs
if args.cpu_type=='O3':
    system.cpu = [O3CPU() for i in range(args.num_cpus)]
else:
    system.cpu = [TimingSimpleCPU() for i in range(args.num_cpus)]



for i in range(args.num_cpus):
    if args.cpu_type=='O3':
        system.cpu[i].icache=L1ICache_henry('64kB')
        system.cpu[i].dcache=L1DCache_henry('64kB')
    else:
        system.cpu[i].icache=L1ICache_henry('32kB')
        system.cpu[i].dcache=L1DCache_henry('32kB')
    system.cpu[i].clk_domain=system.clk_domain

for i in range(args.num_cpus):
    system.cpu[i].icache.connectCPU(system.cpu[i])
    system.cpu[i].dcache.connectCPU(system.cpu[i])

system.l2bus=[L2XBar() for i in range(args.num_cpus)]

for i in range(args.num_cpus):
    system.cpu[i].icache.connectBus(system.l2bus[i])
    system.cpu[i].dcache.connectBus(system.l2bus[i])

system.l2cache=[L2Cache_henry(args.l2_size,args.l2_tag,args.l2_data) for i in range(args.num_cpus)]
for i in range(args.num_cpus):
    system.l2cache[i].connectCPUSideBus(system.l2bus[i])

# system.l3bus=L3XBar()
system.membus=SystemXBar()
for i in range(args.num_cpus):
    system.l2cache[i].connectMemSideBus(system.membus)

# system.l3cache=L3Cache_henry('32MB')
# system.l3cache.connectCPUSideBus(system.l3bus)

# system.l3cache.connectMemSideBus(system.membus)

for cpu in system.cpu:
    cpu.createInterruptController()
    cpu.interrupts[0].pio = system.membus.mem_side_ports
    cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    cpu.interrupts[0].int_responder = system.membus.mem_side_ports

system.system_port=system.membus.cpu_side_ports

# Create a DDR3 memory controller and connect it to the membus
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port=system.membus.mem_side_ports
    
process=get_process(args)
mp0_path = process.executable
for i in range(args.num_cpus):
    system.cpu[i].workload=process
    system.cpu[i].createThreads()


system.workload = SEWorkload.init_compatible(mp0_path)

root = Root(full_system = False, system = system)
m5.instantiate()

with open('henry/results/sim_result_log_large.csv','a') as f:
    print("{},{},{},{},{}".format(args.workload.split()[0].split('/')[-1],args.l2_size,args.cpu_type,args.num_cpus,args.workload),file=f)

print("Beginning simulation!")
exit_event = m5.simulate()
print('Exiting @ tick %i because %s' % (m5.curTick(), exit_event.getCause()))

with open('henry/results/sim_result_large.csv','a') as f:
    print("{},{},{},{},{}".format(args.workload.split()[0].split('/')[-1],args.l2_size,args.cpu_type,args.num_cpus,m5.curTick()/3e9),file=f)