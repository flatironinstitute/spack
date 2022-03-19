# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""LinkTree class for setting up trees of symbolic links."""

from __future__ import print_function

import filecmp
import os
import stat
import shutil

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, touch, traverse_tree
from llnl.util.symlink import islink, symlink

__all__ = ['LinkTree']

empty_file_name = '.spack-empty'


def remove_link(src, dest):
    if not islink(dest):
        raise ValueError("%s is not a link tree!" % dest)
    # remove if dest is a hardlink/symlink to src; this will only
    # be false if two packages are merged into a prefix and have a
    # conflicting file
    if filecmp.cmp(src, dest, shallow=True):
        os.remove(dest)


class LinkTree(object):
    """Class to create trees of symbolic links from a source directory.

    LinkTree objects are constructed with a source root.  Their
    methods allow you to create and delete trees of symbolic links
    back to the source tree in specific destination directories.
    Trees comprise symlinks only to files; directries are never
    symlinked to, to prevent the source directory from ever being
    modified.
    """
    def __init__(self, source_root):
        if not os.path.exists(source_root):
            raise IOError("No such file or directory: '%s'", source_root)

        self._root = source_root

    def find_dir_conflicts(self, dest_root, ignore):
        """Returns conflict descritions for all files/directories in dest incompatible with src."""
        conflicts = []
        kwargs = {'follow_nonexisting': False, 'ignore': ignore, 'with_stat': True}
        for src, dest, src_stat in traverse_tree(self._root, dest_root, **kwargs):
            if stat.S_ISDIR(src_stat.st_mode):
                if not os.path.isdir(dest):
                    conflicts.append("File blocks directory: %s" % dest)
            elif os.path.isdir(dest):
                conflicts.append("Directory blocks non-directory: %s" % dest)
        return conflicts

    def get_file_map(self, dest_root, ignore):
        merge_map = {}
        kwargs = {'follow_nonexisting': True, 'ignore': ignore, 'with_stat': True}
        for src, dest, src_stat in traverse_tree(self._root, dest_root, **kwargs):
            if not stat.S_ISDIR(src_stat.st_mode):
                merge_map[src] = dest
        return merge_map

    def merge_directories(self, dest_root, ignore):
        """Create any missing directories in dest for all those in src."""
        for src, dest, src_stat in traverse_tree(self._root, dest_root, ignore=ignore, with_stat=True):
            if stat.S_ISDIR(src_stat.st_mode): # was this supposed to follow symlinks? (it did before)
                if not os.path.exists(dest):
                    mkdirp(dest)
                    continue

                if not os.path.isdir(dest):
                    raise ValueError("File blocks directory: %s" % dest)

                # mark empty directories so they aren't removed on unmerge.
                # (this only happens if it already exists because continue above!)
                if not os.listdir(dest):
                    marker = os.path.join(dest, empty_file_name)
                    touch(marker)

    def unmerge_directories(self, dest_root, ignore):
        for src, dest, src_stat in traverse_tree(
                self._root, dest_root, ignore=ignore, order='post', with_stat=True, follow_nonexisting=False):
            if stat.S_ISDIR(src_stat.st_mode): # was this supposed to follow symlinks? (it did before)
                # remove empty dir marker if present.
                marker = os.path.join(dest, empty_file_name)
                try:
                    os.remove(marker)
                except FileNotFoundError:
                    pass
                except NotADirectoryError:
                    raise ValueError("File blocks directory: %s" % dest)

                # remove directory if it is empty.
                try:
                    os.rmdir(dest)
                except OSError:
                    pass


    def merge(self, dest_root, ignore_conflicts=False, ignore=None,
              link=symlink, relative=False):
        """Link all files in src into dest, creating directories
           if necessary.

        Keyword Args:

        ignore_conflicts (bool): if True, do not break when the target exists;
            return a list of files that could not be linked

        ignore (callable): callable that returns True if a file is to be
            ignored in the merge (by default ignore nothing)

        link (callable): function to create links with (defaults to llnl.util.symlink)

        relative (bool): create all symlinks relative to the target
            (default False)

        """
        if relative:
            # needed absolute path to determine relative links
            src_root = os.path.abspath(self._root)
            dest_root = os.path.abspath(dest_root)
        else:
            src_root = self._root

        mkdirs = []
        links = []
        existing = []
        for src, dst, src_stat in traverse_tree(src_root, dest_root, ignore=ignore, with_stat=True):
            try:
                dst_stat = os.lstat(dst)
            except FileNotFoundError:
                dst_stat = None

            if stat.S_ISDIR(src_stat.st_mode):
                if not dst_stat:
                    mkdirs.append(dst)
                elif not stat.S_ISDIR(dst_stat.st_mode):
                    raise MergeConflictError("File blocks directory: %s" % dst)
            elif not dst_stat:
                links.append((src, dst))
            elif stat.S_ISDIR(dst_stat.st_mode):
                raise MergeConflictError("Directory blocks non-directory: %s" % dst)
            elif ignore_conflicts:
                existing.append(dst)
            else:
                raise MergeConflictError(dst)

        os.makedirs(dest_root, exist_ok=True)
        for d in mkdirs:
            try:
                os.mkdir(d)
            except FileExistsError:
                pass
        # TODO: do we want empty_file_name markers for empty directories?
        # they're not happening in most cases now anyway.

        for src, dst in links:
            if relative:
                src = os.path.relpath(src, os.path.dirname(dst))
            link(src, dst)

        for c in existing:
            tty.warn("Could not merge: %s" % c)

    def unmerge(self, dest_root, ignore=None, remove_file=remove_link):
        """Unlink all files in dest that exist in src.

        Unlinks directories in dest if they are empty.
        """
        for src, dest, src_stat in traverse_tree(
                self._root, dest_root, ignore=ignore, order='post', with_stat=True, follow_nonexisting=False):
            if stat.S_ISDIR(src_stat.st_mode):
                # remove empty dir marker if present.
                marker = os.path.join(dest, empty_file_name)
                try:
                    os.remove(marker)
                except FileNotFoundError:
                    pass
                except NotADirectoryError:
                    raise ValueError("File blocks directory: %s" % dest)

                # remove directory if it is empty.
                try:
                    os.rmdir(dest)
                except OSError:
                    pass
            else:
                remove_file(src, dst)

class MergeConflictError(Exception):

    def __init__(self, path):
        super(MergeConflictError, self).__init__(
            "Package merge blocked by file: %s" % path)
