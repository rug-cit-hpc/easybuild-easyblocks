# -*- coding: utf-8 -*-
"""
EasyBuild support for MAKER, implemented as an easyblock

@author: Bob Dröge (University of Groningen)
"""
import os
import shutil

from easybuild.easyblocks.generic.bundle import Bundle
from easybuild.easyblocks.generic.tarball import Tarball
from easybuild.tools.run import run_cmd

class EB_MAKER(Tarball, Bundle):
    """
    Support for building MAKER
    """

    def post_install_step(self):

        # load fake module
        fake_mod_data = None
        if not self.dry_run:
            fake_mod_data = self.load_fake_module(purge=True)

            # also load modules for build dependencies again, since those are not loaded by the fake module
            #self.modules_tool.load(dep['short_mod_name'] for dep in self.cfg['builddependencies'])
        
        source_dir = os.path.join(self.installdir, 'src')
        os.chdir(source_dir)
        
        # generate input for interactive build script
        # "Y" or "N" for MPI support
        # "Y" needs to be followed by the path to mpicc and, subsequently, the path to mpi.h
        if self.toolchain.options.get('usempi', True):
            mpi_support = 'Y'
            mpi_inc_dir = self.toolchain.get_variable('MPI_INC_DIR')
            mpicc = os.path.join(mpi_inc_dir, '..', 'bin', 'mpicc')
            mpih = os.path.join(mpi_inc_dir, 'mpi.h')
            input = '\n'.join([mpi_support, mpicc, mpih])
        else:
            input = 'N'

        input += '\n'
        run_cmd('perl Build.PL', inp=input)
        run_cmd('perl Build install')
                                                        
        # cleanup (unload fake module, remove fake module dir)
        if fake_mod_data:
            self.clean_up_fake_module(fake_mod_data)
                            
