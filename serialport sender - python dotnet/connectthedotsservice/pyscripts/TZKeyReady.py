#!/usr/bin/python

# TZKeyReady.py
#       --copyright--                   Copyright 2007 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       December 19, 2003       bar
#       August 5, 2004          bar     take some white space off the end of the source file
#       June 25, 2006           bar     hey, python doesn't have name space problems, make the routine's name friendlier
#       November 4, 2007        bar     no need of tz_ in front of the name
#       November 18, 2007       bar     turn on doxygen
#       November 20, 2007       bar     comments
#       November 27, 2007       bar     insert boilerplate copyright
#       May 17, 2008            bar     email adr
#       February 2, 2010        bar     unichr the key if needed
#       February 25, 2010       bar     wrap unix stdin in protection
#       May 27, 2012            bar     doxygen namespace
#       June 2, 2013            bar     fix interpretor name
#       August 19, 2015         bar     pyflakes
#       --eodstamps--
##      \file
#       \namespace              tzpython.TZKeyReady
#
#
#
#
#####
#
#   From the Python docs:
#
#       import termios, fcntl, sys, os
#       fd = sys.stdin.fileno()
#
#       oldterm = termios.tcgetattr(fd)
#       newattr = termios.tcgetattr(fd)
#       newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
#       termios.tcsetattr(fd, termios.TCSANOW, newattr)
#
#       oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
#       fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
#
#       try:
#           while 1:
#               try:
#                   c = sys.stdin.read(1)
#                   print "Got character", `c`
#               except IOError: pass
#       finally:
#           termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
#           fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
#
#####
#
#       import termios, sys, os
#       fd = sys.stdin.fileno()
#       old = termios.tcgetattr(fd)
#       new = termios.tcgetattr(fd)
#       new[3] = new[3] & ~termios.ICANON & ~termios.ECHO
#       new[6][termios.VMIN] = 1
#       new[6][termios.VTIME] = 0
#       termios.tcsetattr(fd, termios.TCSANOW, new)
#       s = ''    # We'll save the characters typed and add them to the pool.
#       try:
#           while 1:
#               c = os.read(fd, 1)
#               print "Got character", `c`
#               s = s+c
#       finally:
#           termios.tcsetattr(fd, termios.TCSAFLUSH, old)
#
#####
#
#


import  sys



def tz_key_ready() :
    """ Return a keyboard key if one has been hit. """

    k   = None


    if  sys.platform == 'win32' :

        import  msvcrt

        if  msvcrt.kbhit() :

            k = msvcrt.getch()
            if  ord(k) == 0 :
                k   = ord(msvcrt.getch())
                if  k  >= 128 :
                    k   = unichr(k)
                else    :
                    k   = chr(k)
                pass
            pass

        pass

    else :

        stdin           = sys.stdin

        import          termios, fcntl, os


        fd              = sys.stdin.fileno()

        try             :
            oldterm     = termios.tcgetattr(fd)
            newattr     = termios.tcgetattr(fd)
            newattr[3]  = newattr[3] & ~termios.ICANON & ~termios.ECHO
            termios.tcsetattr(fd, termios.TCSANOW, newattr)

            oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

            try         :
                try     :
                    k   = stdin.read(1)
                except IOError:
                    k   = None
                    pass
            finally:
                termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
                fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
            pass
        except termios.error :
            pass

        pass


    return(k)


# def key_ready() :
#     """ Return a keyboard key if one has been hit. """
#
#     return(tz_key_ready())


key_ready   = tz_key_ready
get_key     = tz_key_ready


#
#
#
# eof
