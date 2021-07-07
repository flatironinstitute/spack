import os
from spack import *
import spack.pkg.builtin.openmpi

class Openmpi(spack.pkg.builtin.openmpi.Openmpi):
    # Add custom patches from Andras for IB and other things
    patch('openmpi-1.10.7.PATCH', when='@1.10.7')
    patch('openmpi-1.10-gcc.PATCH', when='@:1.10')
    patch('openmpi-2.1.6.PATCH', when='@2.1.6')

    @run_after('install')
    def update_conf_for_bnl(self):
        mca_conf_path = os.path.join(self.prefix.etc, "openmpi-mca-params.conf")
        with open(mca_conf_path, 'a') as f:
            f.write("\n")
            f.write("oob_tcp_if_exclude = idrac,lo,ib0\n")
            f.write("btl_tcp_if_exclude = idrac,lo,ib0\n")
