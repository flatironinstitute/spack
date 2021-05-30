#!/bin/bash

source share/spack/setup-env.sh
export INTEL_LICENSE_FILE=28518@lic1.flatironinstitute.org

compilers=(
    %gcc@7.4.0
    %gcc@10.2.0
    # %intel
)

mpis=(
    openmpi@1.10.7
    openmpi@2.1.6
    openmpi@4.0.5
)


in_list() {
    checkval=$1
    shift
    list=("$@")
    for val in "${list[@]}"; do
        if [ "$val" == "$checkval" ]; then
            return 0
        fi
    done
    return 1
}

declare -a python_blas_packages=(
    "py-pandas@1.1.4"
    "py-scikit-learn@0.23.2"
    "py-numba@0.50.1"
    "py-emcee@2.2.1"
    "py-astropy@4.0.1.post1"
    "py-dask@2.16.0"
    "py-seaborn@0.9.0"
    "py-matplotlib@3.3.3"
)
declare -a python_packages=(
    "py-cherrypy@18.1.1"
    "py-flask@1.1.2"
    "py-pip@20.2"
    "py-ipython@7.18.1"
    "py-pyyaml@5.3.1"
    "py-pylint@2.3.1"
    "py-autopep8@1.4.4"
    "py-sqlalchemy@1.3.19"
    "py-nose@1.3.7"
    "py-mako@1.0.4"
    "py-pkgconfig@1.5.1"
    "py-virtualenv@16.7.6"
    "py-sympy@1.4"
    "py-pycairo@1.18.1"
    "py-sphinx@3.2.0"
)

for compiler in "${compilers[@]}"; do
    # Core installs
    spack install boost@1.74.0                     $compiler
    spack install cuda@11.1.0                      $compiler
    spack install cudnn@8.0.4.30-11.1-linux-x64    $compiler
    spack install cmake@3.18.4                     $compiler
    spack install eigen@3.3.8                      $compiler
    spack install fftw@2.1.5 mpi=false \
          precision=float,double                   $compiler
    spack install fftw@3.3.8 mpi=false \
          precision=float,double,quad,long_double  $compiler
    spack install gdb@9.2                          $compiler
    spack install git@2.29.0                       $compiler
    spack install hdf5@1.10.7+fortran~mpi+cxx      $compiler
    spack install intel-mkl@2020.3.279             $compiler
    spack install intel-oneapi-mkl@2021.1.1        $compiler
    spack install llvm@10.0.1                      $compiler
    spack install llvm@11.0.1                      $compiler
    spack install openblas@0.3.12 threads=none     $compiler
    spack install openblas@0.3.12 threads=openmp   $compiler
    spack install openblas@0.3.12 threads=pthreads $compiler
    spack install openmpi-opa@4.0.5                $compiler
    spack install slurm                            $compiler

    # python time!
    # python default to multithreaded openblas
    # python-blas-backend is a custom package that includes scipy/numpy
    spack install python@3.8.6                     $compiler
    spack install python-blas-backend@3.8.6        $compiler ^openblas@0.3.12 threads=pthreads
    spack install python-blas-backend@3.8.6        $compiler ^intel-mkl@2020.3.279

    # I cache the active extensions, because each "activate" alone takes forever, even if it's
    # already activated.
    active_python_extensions=$(spack extensions -s activated python$compiler | tail -n+3)

    # blas stuff requires a blas spec
    for package in ${python_blas_packages[@]}; do
        spack install  $package                    $compiler ^openblas@0.3.12 threads=pthreads

        if ! in_list $package $active_python_extensions; then
            spack activate $package                $compiler ^openblas@0.3.12 threads=pthreads
        fi
    done

    # all non-blas python packages
    for package in ${python_packages[@]}; do
        spack install $package                     $compiler

        if ! in_list $package $active_python_extensions; then
            spack activate $package                $compiler
        fi
    done

    # Non-default or otherwise special python modules

    # need to have py-pyqt5 as external module for now, because there is a conflict with py-sip
    # on the merge, so we activate py-sip, and then load py-pyqt5 via module if needed
    spack install py-pyqt5@5.13.1                  $compiler
    spack activate py-sip                          $compiler

    spack install py-jupyter@1.0.0                 $compiler

    # h5py, since it uses a variant, needs its own install
    spack install py-h5py@2.10.0 mpi=false         $compiler ^openblas@0.3.12 threads=pthreads ^hdf5+fortran~mpi+cxx
    spack activate py-h5py@2.10.0 mpi=false        $compiler ^openblas@0.3.12 threads=pthreads ^hdf5+fortran~mpi+cxx

    # requires git > 2
    spack load git                                 $compiler
    spack install py-torch@1.7.0 cuda_arch=35,60,70,80 \
          $compiler ^openblas@0.3.12 threads=pthreads ^cudnn@8.0.4.30-11.1-linux-x64
    spack install py-torch@1.7.0 cuda_arch=35,60,70,80 \
          $compiler ^intel-mkl@2020.3.279 ^cudnn@8.0.4.30-11.1-linux-x64
    spack unload git                               $compiler

    # ipython requires 7.18.1 requires py-prompt-toolkit@2, so ipdb needs this constraint since it tries for v3
    spack install py-ipdb                          $compiler ^py-prompt-toolkit@2:2
    spack activate py-ipdb                         $compiler ^py-prompt-toolkit@2:2

    # Anything dependent on MPI
    for mpi in "${mpis[@]}"; do
        spack install $mpi                         $compiler

        spack install boost@1.74.0 mpi=true        $compiler ^$mpi
        spack install hdf5@1.10.7                  $compiler ^$mpi
        spack install fftw@2.1.5                   $compiler ^$mpi
        spack install fftw@3.3.8                   $compiler ^$mpi
        spack install py-mpi4py@3.0.3              $compiler ^$mpi

        # openmpi was compiled with gcc@7, so we can't compile hdf5 with fortran, because of
        # binary incompability with the openmpi fortran bindings in our external module
        if [ "$compiler" == "%gcc@10.2.0" ]; then
            spack install py-h5py@2.10.0           $compiler ^$mpi ^openblas@0.3.12 threads=pthreads ^hdf5~fortran
        else
            spack install py-h5py@2.10.0           $compiler ^$mpi ^openblas@0.3.12 threads=pthreads ^hdf5+fortran
        fi
    done
done
