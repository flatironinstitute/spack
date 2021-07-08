import os
from spack import *
import spack.pkg.builtin.openmpi

class Openmpi(spack.pkg.builtin.openmpi.Openmpi):
    # Add custom patches from Andras for IB and other things
    patch('openmpi-1.10.7.PATCH', when='@1.10.7')
    patch('openmpi-1.10-gcc.PATCH', when='@:1.10')
    patch('openmpi-2.1.6.PATCH', when='@2.1.6')

    @run_after('install')
    def update_conf(self):
        mca_conf_path = os.path.join(self.prefix.etc, "openmpi-mca-params.conf")
        with open(mca_conf_path, 'a') as f:
            f.write("\n")
            f.write("oob_tcp_if_exclude = idrac,lo,ib0\n")
            f.write("btl_tcp_if_exclude = idrac,lo,ib0\n")
            f.write("\n")
            f.write("btl_openib_if_exclude = i40iw0,i40iw1,mlx5_1\n")
            f.write("btl_openib_warn_nonexistent_if = 0\n")
            if self.spec.satisfies("@4.0:"):
                f.write("\n")
                #f.write("btl_openib_receive_queues=P,128,2048,1024,32:S,2048,2048,1024,64:S,12288,2048,1024,64:S,65536,2048,1024,64\n")
                f.write("btl=^openib,usnix\n")
                f.write("mtl=^psm,ofi\n")
                f.write("pml=ucx\n")
