import os
import json
from spack import *

class JupyterKernelLabel(Package):
    """Rename/label an exsisting jupyter kernel."""
    version('1')
    depends_on('jupyter-kernel')
    variant('language', default='python', values=('python','r','julia'), multi=False)
    has_code = False
    kerneldir = os.path.join('share','jupyter','kernels')

    def install(self, spec, prefix):
        pkg = spec['jupyter-kernel']
        srcdir = os.path.join(pkg.prefix, self.kerneldir)
        dstdir = os.path.join(    prefix, self.kerneldir)
        kernels = os.listdir(srcdir)
        if not kernels:
            raise InstallError('No kernels found in {0}'.format(pkg))
        os.makedirs(dstdir)
        lang = spec.variants['language'].value
        label = pkg.format('{^'+lang+'.name}@{^'+lang+'.version}-{name}@{version}%{compiler}')

        for sname in kernels:
            dname = sname+"-"+label
            sdir = os.path.join(srcdir, sname)
            ddir = os.path.join(dstdir, dname)
            if not os.path.exists(os.path.join(sdir, 'kernel.json')):
                raise InstallError('Missing {0}/kernel.json in {1}'.format(s, pkg))
            os.mkdir(ddir)
            for f in os.listdir(sdir):
                sf = os.path.join(sdir, f)
                df = os.path.join(ddir, f)
                if f == 'kernel.json':
                    with open(sf, 'r') as kjf:
                        kj = json.load(kjf)
                    kj['display_name'] += " ("+label +")"
                    with open(df, 'w') as kjf:
                        json.dump(kj, kjf)
                else:
                    os.symlink(sf, df)
