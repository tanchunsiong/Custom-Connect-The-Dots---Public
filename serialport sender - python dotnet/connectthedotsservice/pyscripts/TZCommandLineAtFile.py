#!/usr/bin/python

# TZCommandLineAtFile.py
#       --copyright--                   Copyright 2007 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       February 3, 2004        bar
#       January 28, 2005        bar     do command line arg zero
#       September 17, 2005      bar     allow glob'd file names
#       November 18, 2007       bar     turn on doxygen
#       November 20, 2007       bar     comments
#       November 27, 2007       bar     insert boilerplate copyright
#       May 17, 2008            bar     email adr
#       August 31, 2008         bar     1st line path that deb package lint program, lintian, doesn't fuss about
#                                       user: expand ~/ in input file names using os.path.expanduser
#       November 28, 2010       bar     allow relative paths in cmd files - relative to the cmd file, itself, that is
#       February 15, 2011       bar     raise exceptions when the file has bad tgcmsgs
#       March 3, 2011           bar     encoding param
#       May 27, 2012            bar     doxygen namespace
#       March 14, 2013          bar     allow callers to get a list of the files found
#       --eodstamps--
##      \file
#       \namespace              tzpython.TZCommandLineAtFile
#
#
#       Expand out command line @files.
#
#       Note: This logic allows a file name to be of the form: @@file_name  to specify a file named, @file_name.
#
#       TODO:
#           allow @ file_name
#           allow file names with spaces in them?
#           stop recursion?
#
#


import  glob
import  re
import  os.path

import  tgcmsg



def expand_command_line_file(args, i, del_i, fn, encoding = None, file_list = None) :
    """ Given the arguments, insert at or replace an argument with the contents of command line parameter file of the given name. """

    xms      = tgcmsg.amp_messages_from_file(fn, encoding = encoding, safe = False)
    if  xms != None :
        if  del_i :     del args[i]
        xms.reverse()
        for xm in xms :
            expand_at_sign_command_line_files(xm, os.path.dirname(fn), encoding = encoding, file_list = file_list)
            xm.reverse()
            for f in xm :
                args.insert(i, f)
            pass

        return(True)

    return(False)



#
#
#       expand_at_sign_command_line_files(sys.argv);
#
#
def expand_at_sign_command_line_files(args, path = None, encoding = None, file_list = None) :
    """ Expand any command line argument files (command line arguments which start with '@') in the given arguments. """

    if  file_list is None :
        file_list   = []

    for i in range(len(args) - 1, -1, -1) :
        a   = args[i]
        if  re.match(r"^@@", a) :                                       # allow @file names by the command line doubling the @ signs: @@file
            args[i] = re.sub(r"^@@", "@", a)
        else        :
            g       = re.match(r"\@(\S.*)$", a)
            if  g       :
                fn      = g.group(1)
                fn      = os.path.expanduser(os.path.expandvars(fn))
                fns     = []
                if  path    :
                    fns = glob.glob(os.path.join(path, fn))             # first try file name relative to the path - the include file we're doing now's directory
                if  not fns :
                    fns = glob.glob(fn)                                 # no files found, bail out and try the current directory
                fns.sort(lambda a, b : cmp(b.lower(), a.lower()))       # since we stuff things from the files in the args in reverse order, we'll sort the files reversed
                del_i   = True
                for fn in fns :
                    afn = os.path.abspath(os.path.normpath(fn))
                    if  os.path.isfile(afn) :                           # the following code stops recursion, but also stops last instant of the file, which may have contents wanted to be read later in the args - or not, given that we are expanding backward  #    and (afn not in file_list) :
                        r       = expand_command_line_file(args, i, del_i, fn, encoding = encoding, file_list = file_list)          # keep telling him to delete the i'th arg until he does
                        if  r   :
                            file_list.append(afn)
                        del_i  &= (not r)
                    pass
                pass
            pass
        pass
    pass





#
#
#   Test code.
#
#
if __name__ == '__main__' :
    import  sys

    file_list   = []
    expand_at_sign_command_line_files(sys.argv, encoding = 'utf8', file_list = file_list)
    file_list.reverse()

    print sys.argv
    print "Filelist:"
    for fn in file_list :
        print " ", fn
    pass



##      Public things.
__ALL__ = [
            'expand_command_line_file'
            'expand_at_sign_command_line_files'
          ]

#
#
#
# eof
