build/X86/gem5.opt configs/example/henry_simplecpu.py --workload /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inst/amd64-linux.gcc/bin/blackscholes --option '4 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inputs/in_4K.txt temp.out' --num-cpus 5

# build/X86/gem5.opt configs/example/henry_simplecpu.py --workload /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/bin/parsecmgmt --option '-a run -p blackscholes -n 4' --num-cpus 5