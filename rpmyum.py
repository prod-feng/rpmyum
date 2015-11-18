#!/usr/bin/python
# Licensed under the GNU General Public License Version 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

# Developed on Fedora 10. May not be able to work on other system. July 2010.

import sys
sys.path.insert(0, '/usr/share/PackageKit/helpers/yum/')

from yumBackend import *
from optparse import OptionParser

def _get_package_ver(po):
    ''' return the a ver as epoch:version-release or version-release, if epoch=0'''
    if po.epoch != '0':
        ver = "%s:%s-%s" % (po.epoch, po.version, po.release)
    else:
        ver = "%s-%s" % (po.version, po.release)
    return ver

def _text_to_boolean(text):
    '''
    Parses true and false
    '''
    if text == 'true':
        return True
    if text == 'TRUE':
        return True
    if text == 'yes':
        return True
    if text == 'YES':
        return True
    return False


class rpmyum(PackageKitYumBackend):

    def __init__(self, args, lock=True):
        PackageKitYumBackend.__init__(self, args, lock)

######Override these functions to clear unnecessary printing messages######
######see packagekit/backend.py                                      ######
    def allow_cancel(self, allow):
        if allow:
            data = 'true'
        else:
            data = 'false'
        #do nothing here!
        sys.stdout.flush()

    def percentage(self, percent=None):
        #do nothing here!
        sys.stdout.flush()

    def finished(self):
        print "\n Done!"
        sys.stdout.flush()


    def status(self, state):
        #do nothing here!
        sys.stdout.flush()

    def package(self, package_id, status, summary):
        summary = _to_unicode(summary)

        # maintain a dictionary of the summary text so we can use it when rpm
        # is giving up package names without summaries
        (name, idver, a, repo) = self.get_package_from_id(package_id)
        if len(summary) > 0:
            self.package_summary_cache[name] = summary
        else:
            if self.package_summary_cache.has_key(name):
                summary = self.package_summary_cache[name]
        print >> sys.stdout, "package\t%s\t%s\t%s" % (status, package_id, summary)
        sys.stdout.flush()


######                                                             ######
######                                                             ######
    def category(self, parent_id, cat_id, name, summary, icon):
        '''
        Send 'category' signal
        parent_id : A parent id, e.g. "admin" or "" if there is no parent
        cat_id    : a unique category id, e.g. "admin;network"
        name      : a verbose category name in current locale.
        summery   : a summary of the category in current locale.
        icon      : an icon name to represent the category
        '''
        name = _to_unicode(name)
        summary = _to_unicode(summary)
        PackageKitBaseBackend.category(self, parent_id, cat_id, name, summary, icon)


    def get_requires(self, filters, package_ids, recursive_text):
        '''
        Print a list of requires for a given package
        '''
        self._check_init(lazy_cache=True)
        self.yumbase.conf.cache = 0 # Allow new files
        self.allow_cancel(True)
        self.percentage(None)
#        self.status(STATUS_INFO)

        percentage = 0
        bump = 100 / len(package_ids)
        deps_list = []
        resolve_list = []
        recursive = _text_to_boolean(recursive_text)

        for package in package_ids:
            self.percentage(percentage)
            pkg, inst = self._findPackage(package)
            print "\nRetrieving the requires of package: %s\n"%pkg.name
              # This simulates the removal of the package
            if inst and pkg:
               resolve_list.append(pkg)
               txmbrs = self.yumbase.remove(po=pkg)
            percentage += bump

        # do the depsolve to pull in deps
        if len(self.yumbase.tsInfo) > 0  and recursive:
            rc, msgs =  self.yumbase.buildTransaction()
            if rc != 2:
                self.error(ERROR_DEP_RESOLUTION_FAILED, _format_msgs(msgs))
            else:
                for txmbr in self.yumbase.tsInfo:
                    if txmbr.po not in deps_list:
                        deps_list.append(txmbr.po)

        # remove any of the original names
        for pkg in resolve_list:
            if pkg in deps_list:
                deps_list.remove(pkg)
        print "   #\tName\tSummary"
        # each unique name, emit
        ifile=0
        for pkg in deps_list:
            package_id = self._pkg_to_id(pkg)
            ifile=ifile+1
            print "%4d\t%s\t%s" % (ifile, package_id, pkg.summary)
            #self.package(package_id, INFO_INSTALLED, pkg.summary)
        self.percentage(100)




    def get_details(self, package_ids):
        '''
        Print a detailed details for a given package
        '''
        self._check_init(lazy_cache=True)
        self.yumbase.conf.cache = 0 # Allow new files
        self.allow_cancel(True)
        #self.percentage(None)
        #self.status(STATUS_INFO)

        for package in package_ids:
          pkg, inst = self._findPackage(package)
          if pkg:
            print "\nRetrieving the detailed information of package: %s\n"%pkg.name
            self._show_details_pkg(pkg)
          else:
            self.error(ERROR_PACKAGE_NOT_FOUND, 'Package %s was not found' % package)

    def _show_details_pkg(self, pkg):

        pkgver = _get_package_ver(pkg)
        package_id = self.get_package_id(pkg.name, pkgver, pkg.arch, pkg.repo)
        desc = pkg.description
        desc = desc.replace('\n\n', ';')
        desc = desc.replace('\n', ' ')
        group = self.comps.get_group(pkg.name)
        files = pkg.returnFileEntries('dir')
        files.extend(pkg.returnFileEntries())
        print "Package ID  : ",package_id
        print "Group       : ",group
        print "Description : ",desc
        print "Size        : ",pkg.size/1000," KB"
        print "Files       : "
        ifile=0
        for file in files:
          if os.path.isfile(file):
            ifile=ifile+1
            print "%4d  :"%ifile,file
 


def main(args):

    errcode = None
    rpmq = rpmyum('', lock=True)
    errcode = rpmq.dispatch_command(args[0], args[1:])
    sys.exit(errcode)
    return errcode
    
if __name__ == "__main__":

    argvv=[]
    usagemsg = "usage: %prog [options] package"
    parser = OptionParser(usage=usagemsg)
    parser.add_option("-d", "--details",help="Quey detailed information of a package")
    parser.add_option("-r", "--requires",help="Query the what-requires of a package recursively")

  
    (options, args) = parser.parse_args()
    if(len(sys.argv)<3):# and options.help):
        parser.error("Incorrect number of arguments")

    if options.details and options.requires:
        parser.error("You can only use -d or -r at one time")
    if(options.details!=None):
        argvv.append('get-details')
        argvv.append(options.details)
    if(options.requires!=None):
        argvv.append('get-requires')
        argvv.append(' ')    #no filter
        argvv.append(options.requires)
        argvv.append('yes')
    try:
      main(argvv) 
    except KeyboardInterrupt, e:
      print >> sys.stderr, "\n\nExiting on user cancel."
      sys.exit(1)
