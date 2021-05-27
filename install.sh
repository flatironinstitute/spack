#!/usr/bin/env bash

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

for compiler in "${compilers[@]}"
do
    # Serial installs
    spack install boost@1.74.0                     $compiler
    spack install cuda@11.1.0                      $compiler
    spack install cudnn@8.0.4.30-11.1-linux-x64    $compiler
    spack install cmake@3.18.4                     $compiler
    spack install eigen@3.3.8                      $compiler
    spack install fftw@2.1.5 mpi=false \
          precision=float,double                   $compiler
    spack install fftw@3.3.8 mpi=false \
          precision=float,double,quad,long_double  $compiler
    spack install git@2.29.0                       $compiler
    spack install hdf5@1.10.7 mpi=false            $compiler
    spack install intel@20.0.2                     $compiler
    spack install intel-mkl@2020.3.279             $compiler
    spack install intel-oneapi-mkl@2021.1.1        $compiler
    spack install openblas@0.3.12 threads=none     $compiler
    spack install openblas@0.3.12 threads=openmp   $compiler
    spack install openblas@0.3.12 threads=pthreads $compiler
    spack install python@3.8.6                     $compiler
    spack install python-blas-backend@3.8.6        $compiler ^openblas@0.3.12 threads=pthreads
    spack install python-blas-backend@3.8.6        $compiler ^intel-mkl@2020.3.279

    spack install py-pandas@1.1.4                  $compiler ^openblas@0.3.12 threads=pthreads
    spack install py-scikit-learn@0.23.2           $compiler ^openblas@0.3.12 threads=pthreads
    spack install py-numba@0.50.1                  $compiler ^openblas@0.3.12 threads=pthreads

    spack install py-pip@20.2                      $compiler
    spack install py-pyqt5@5.13.1                  $compiler
    spack install py-ipython@7.18.1                $compiler
    spack install py-jupyter@1.0.0                 $compiler

    # Installed via the python-blas-backend bundle package
    spack activate py-numpy                        $compiler ^openblas@0.3.12 threads=pthreads
    spack activate py-scipy                        $compiler ^openblas@0.3.12 threads=pthreads

    # need to have py-pyqt5 as external module for now, because there is a conflict with py-sip
    # on the merge, so we activate py-sip, and then load py-pyqt5 via module
    spack activate py-sip                          $compiler

    spack activate py-ipython                      $compiler
    spack activate py-jupyter                      $compiler
    spack activate py-numba                        $compiler
    spack activate py-pandas                       $compiler
    spack activate py-pip                          $compiler
    spack activate py-scikit-learn                 $compiler

    # Parallel installs
    for mpi in "${mpis[@]}"
    do
        spack install $mpi                         $compiler

        spack install boost@1.74.0 mpi=true        $compiler ^$mpi
        spack install hdf5@1.10.7                  $compiler ^$mpi
        spack install fftw@2.1.5                   $compiler ^$mpi
        spack install fftw@3.3.8                   $compiler ^$mpi
        spack install py-mpi4py@3.0.3              $compiler ^$mpi
        spack install py-h5py@2.10.0               $compiler ^$mpi ^openblas@0.3.12 threads=pthreads
    done
done
