import os
from math import floor

# workloads=[f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inst/amd64-linux.gcc.pre/bin/x264 --quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads {NTHREADS} -o eledream.264 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inputs/eledream_640x360_128.y4m'
#     ,
#     f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/swaptions/inst/amd64-linux.gcc.pre/bin/swaptions -ns 64 -sm 40000 -nt {NTHREADS}'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/streamcluster/inst/amd64-linux.gcc.pre/bin/streamcluster 10 20 128 16384 16384 1000 none output.txt {NTHREADS}'


#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inst/amd64-linux.gcc.pre/bin/fluidanimate {NTHREADS} 5 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inputs/in_300K.fluid out.fluid'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/facesim/inst/amd64-linux.gcc.pre/bin/facesim -timing -threads {NTHREADS}'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inst/amd64-linux.gcc.pre/bin/dedup -c -p -t {NTHREADS} -i /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inputs/media.dat -o output.dat.ddp'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc.pre/bin/bodytrack /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inputs/sequenceB_4 4 4 4000 5 0 {NTHREADS}'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inst/amd64-linux.gcc.pre/bin/canneal {NTHREADS} 15000 2000 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inputs/400000.nets 128'

#     , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inst/amd64-linux.gcc.pre/bin/blackscholes {NTHREADS} /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inputs/in_64K.txt blackscholes.out'
#     ]

chip_area=20

bigcore_area=0.458
smallcore_area=0.186

l2_sizes=['256kB','512kB','1MB','2MB','4MB','8MB','16MB']
l2_areas=[0.401,0.596,1.09,2.23,4.49,7.67,15.46]
tag_latancys=[1,1,2,2,2,3,4]
data_latencys=[3,4,4,6,7,10,12]


for i in range(1,5):
    l2_size=l2_sizes[i]
    l2_area=l2_areas[i]
    tag=tag_latancys[i]
    data=data_latencys[i]
    num_cpu=floor(chip_area/(bigcore_area+l2_area))
    NTHREADS=num_cpu-1
    workloads = [f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inst/amd64-linux.gcc.pre/bin/x264 --quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads {NTHREADS} -o eledream.264 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inputs/eledream_640x360_8.y4m',

    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/swaptions/inst/amd64-linux.gcc.pre/bin/swaptions -ns 16 -sm 10000 -nt {NTHREADS}'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/streamcluster/inst/amd64-linux.gcc.pre/bin/streamcluster 10 20 32 4096 4096 1000 none output.txt {NTHREADS}'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inst/amd64-linux.gcc.pre/bin/fluidanimate {NTHREADS} 5 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inputs/in_300K.fluid out.fluid'


    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inst/amd64-linux.gcc.pre/bin/dedup -c -p -t {NTHREADS} -i /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inputs/media.dat -o output.dat.ddp', 
    
    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc.pre/bin/bodytrack /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inputs/sequenceB_1 4 1 1000 5 0 {NTHREADS}',

    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inst/amd64-linux.gcc.pre/bin/canneal {NTHREADS} 10000 2000 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inputs/100000.nets 32'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inst/amd64-linux.gcc.pre/bin/blackscholes {NTHREADS} /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inputs/in_4K.txt blackscholes.out'
    ]
    for wkld in workloads[5:7]:
        wkld_name=wkld.split()[0].split('/')[-1]
        cmd=f'/home/henrychang/nfs/code/gem5/build/X86/gem5.opt configs/example/henry_simplecpu.py --workload \'{wkld}\' --cpu-type \'O3\' --num-cpus {num_cpu} --l2-size \'{l2_size}\' --l2-tag {tag} --l2-data {data} >sim_logs/{wkld_name}_O3_{l2_size}_{num_cpu}.log &'
        os.system(cmd)


for i in range(4):
    l2_size=l2_sizes[i]
    l2_area=l2_areas[i]
    tag=tag_latancys[i]
    data=data_latencys[i]
    num_cpu=floor(chip_area/(smallcore_area+l2_area))
    NTHREADS=num_cpu-1
    workloads = [f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inst/amd64-linux.gcc.pre/bin/x264 --quiet --qp 20 --partitions b8x8,i4x4 --ref 5 --direct auto --b-pyramid --weightb --mixed-refs --no-fast-pskip --me umh --subme 7 --analyse b8x8,i4x4 --threads {NTHREADS} -o eledream.264 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/x264/inputs/eledream_640x360_8.y4m',

    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/swaptions/inst/amd64-linux.gcc.pre/bin/swaptions -ns 16 -sm 10000 -nt {NTHREADS}'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/streamcluster/inst/amd64-linux.gcc.pre/bin/streamcluster 10 20 32 4096 4096 1000 none output.txt {NTHREADS}'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inst/amd64-linux.gcc.pre/bin/fluidanimate {NTHREADS} 5 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/fluidanimate/inputs/in_300K.fluid out.fluid'


    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inst/amd64-linux.gcc.pre/bin/dedup -c -p -t {NTHREADS} -i /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/dedup/inputs/media.dat -o output.dat.ddp', 
    
    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inst/amd64-linux.gcc.pre/bin/bodytrack /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/bodytrack/inputs/sequenceB_1 4 1 1000 5 0 {NTHREADS}',

    f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inst/amd64-linux.gcc.pre/bin/canneal {NTHREADS} 10000 2000 /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/kernels/canneal/inputs/100000.nets 32'

    , f'/home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inst/amd64-linux.gcc.pre/bin/blackscholes {NTHREADS} /home/henrychang/nfs/code/gem5/henry/benchmarks/parsec-3.0/pkgs/apps/blackscholes/inputs/in_4K.txt blackscholes.out'
    ]
    for wkld in workloads[5:7]:
        wkld_name=wkld.split()[0].split('/')[-1]    
        cmd=f'/home/henrychang/nfs/code/gem5/build/X86/gem5.opt configs/example/henry_simplecpu.py --workload \'{wkld}\' --cpu-type \'Simple\' --num-cpus {num_cpu} --l2-size \'{l2_size}\' --l2-tag {tag} --l2-data {data} >sim_logs/{wkld_name}_Simple_{l2_size}_{num_cpu}.log &'
        os.system(cmd)
