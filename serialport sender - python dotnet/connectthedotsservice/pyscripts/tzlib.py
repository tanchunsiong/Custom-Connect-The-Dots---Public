#!/usr/bin/python

# tzlib.py
#       --copyright--                   Copyright 2007 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       July 22, 2003           bar
#       October 7, 2003         bar     ambiguous_file_list
#       January 31, 2004        bar     find_in_array
#       September 28, 2004      bar     define False and True
#       October 25, 2004        bar     hash sort routines (built in already?)
#       January 12, 2005        bar     array_find
#       January 13, 2005        bar     file_name_able and ascii and crc32 routines moved to here
#       January 17, 2005        bar     add <>+'" to the characters changed by file_name_able
#                                       fix __ALL__'s file_name_able name
#       January 30, 2005        bar     _ascii() call -> ascii() - and make it right and import re
#       February 9, 2005        bar     tz_vector_cosine
#       February 17, 2005       bar     html character entities
#       February 25, 2005       bar     safe_html
#       March 1, 2005           bar     option to translate &nbsp; to space or whatever
#       March 19, 2005          bar     typo in ascii - StringType's
#       June 27, 2005           bar     collapse array_find in to find_in_array
#                                       without_dupes
#       July 12, 2005           bar     check crc
#       August 24, 2005         bar     more fooling with the new python warnings about 32 bit ints in crc logic
#       September 5, 2005       bar     look up any of an array of strings in find_in_array / array_find
#       March 25, 2006          bar     try to avoid a latin1 to ascii fuss
#       April 26, 2006          bar     strrev
#       June 14, 2006           bar     string_pairs and flat_positional_strings
#       June 16, 2006           bar     de_html_str
#       June 21, 2006           bar     pull scripts out in de_html_str
#       May 5, 2007             bar     linear_regression
#       May 16, 2007            bar     zlib crc
#       May 17, 2007            bar     printable
#       June 22, 2007           bar     comment
#       July 1, 2007            bar     longitudinal parity (xor sum)
#       October 12, 2007        bar     distance / direction routines (here so I don't need to look 'em up again)
#       November 18, 2007       bar     turn on doxygen
#       November 20, 2007       bar     move lf_only() and no_blank_lines() from strip_files.py
#                                       lf_only() fixes \r\r\n to be one \n
#                                       as does safe_html() make \r\r\n one <BR>
#                                       c_string()
#                                       read_whole_text_file() (finally)
#                                       read_whole_binary_file() (ditto)
#       November 27, 2007       bar     lf_only_with_no_trailing_white_space()
#       November 27, 2007       bar     insert boilerplate copyright
#       December 1, 2007        bar     elapsed_time()
#       December 14, 2007       bar     write the file in write_whole_...
#       December 15, 2007       bar     multiline_strip
#       December 21, 2007       bar     maybe_wrap_with_cdata
#       January 1, 2008         bar     s_except_1()
#       January 18, 2008        bar     unicode_byte_string()
#                                       and auto-convert unicode to utf-16 or utf-8 when writing whole files
#       January 20, 2008        bar     same_object() (for doc purposes)
#       January 21, 2008        bar     s_except_1 takes lists and dictionarys
#       January 29, 2008        bar     sys_err_file_line()
#       February 8, 2008        bar     finally, a binary_search() i can remember
#                                       fix blkcrc32() under python 2.2 (zlib's crc isn't right, apparently)
#                                       add start/end indices to find_in_array and array_find
#       March 9, 2008           bar     temp_file_name
#       March 12, 2008          bar     allow arrays to de_html_str()
#       March 13, 2008          bar     comment
#       May 17, 2008            bar     email adr
#       August 13, 2008         bar     make_dictionary works for strings
#       August 18, 2008         bar     use basestring
#       August 29, 2008         bar     basestring instead of StringType because of unicode strings and others
#       October 28, 2008        bar     float_regx_str
#       November 6, 2008        bar     bool_to_0_or_1()
#       November 15, 2008       bar     egad! I've been making default params as [] and {}
#       November 28, 2008       bar     decode_html_entities latin1/unicode fixes
#                                       print_exception()
#       December 20, 2008       bar     INITIAL_CRC32_VALUE
#       December 28, 2008       bar     ooops, it should be zero, not -1
#       January 7, 2009         bar     excel_column_name
#       January 9, 2009         bar     list_lstrip()
#       February 20, 2009       bar     golden_smaller()
#       March 27, 2009          bar     python 2.6
#       April 1, 2009           bar     printable_str()
#       April 11, 2009          bar     run test ok under python 2.5
#       April 15, 2009          bar     max_index() and min_index()
#       June 2, 2009            bar     find_upper_dir()
#       September 2, 2009       bar     fix find_upper_dir for when the dir is not found (unix needs testing)
#       September 9, 2009       bar     radian_angle_difference()
#       September 16, 2009      bar     find_upper_file_or_dir
#       November 13, 2009       bar     crc16
#       November 28, 2009       bar     file_signature()
#       January 24, 2010        bar     force 16 bit crc to be 16 bits
#       February 10, 2010       bar     get_tid() for linux
#       February 11, 2010       bar     value_array_for_key()
#                                       replace_value_array_for_key()
#       February 20, 2010       bar     windows version of get_tid
#       March 14, 2010          bar     pickle file by file name routines
#       July 22, 2010           bar     keep replace_file inside the only place it's used (and shouldn't be here, anyway)
#       September 23, 2010      bar     make_index_dictionary() and update_all_case_keys()
#       September 26, 2010      bar     print_stack()
#       September 28, 2010      bar     c_ctrl_esc()
#       October 1, 2010         bar     C, C++ comment remover
#       October 2, 2010         bar     safe whole file read/write
#                                       safe_relpath()
#       October 10, 2010        bar     base 36
#       October 19, 2010        bar     best_ascii()
#       October 24, 2010        bar     de_dupe_str()
#       October 27, 2010        bar     find_arg()
#       November 2, 2010        bar     allow update_all_case_keys() to accept int and other keys
#       November 5, 2010        bar     flatten_array()
#       November 7, 2010        bar     expand user and vars in ambiguous file name finder
#       November 9, 2010        bar     c_string changes \ to \134 rather than \\ so that there are no doubled slashes
#       November 16, 2010       bar     same_file()
#                                       reroute_stdout_err()
#       December 5, 2010        bar     multiline_flush_left()
#                                       invert_dictionary()
#       December 27, 2010       bar     safer pickling
#                                       allow printable to zap bad chars
#       February 8, 2011        bar     make unpickle safer ('module' object has no attribute '---class---')
#       March 21, 2011          bar     line intersections
#       March 27, 2011          bar     allow smart proto to pickle_file
#       April 14, 2011          bar     under non-win32, put the .cfg file in get_ini_or_cfg_file_name() in an app directory, not at the user's home dir
#       June 15, 2011           bar     faster max_index and min_index
#       August 9, 2011          bar     let those faster _index routines work with numpy arrays
#       November 5, 2011        bar     can_run_program()
#       November 6, 2011        bar     whack_file()
#       November 13, 2011       bar     q_get()
#       November 29, 2011       bar     pyflake cleanup
#                                       allow make_dictionary to take a dictionary (it's shallow duped, effectively)
#       November 30, 2011       bar     uh. test it
#       December 14, 2011       bar     kalman filter
#                                       get rid of ALL
#       December 23, 2011       bar     cmp_str_with_ints()
#       January 18, 2012        bar     left_valley(), rite_valley()
#       February 4, 2012        bar     run_program() and in_screen_saver()
#       February 7, 2012        bar     add stderr to the output string in run_program
#       February 11, 2012       bar     wdhms_str()
#       March 8, 2012           bar     buples_to_dictionary()
#       March 11, 2012          bar     weighted_choice()
#       March 15, 2012          bar     make ambiguous_file_list() safer
#       May 1, 2012             bar     file_name_able() uses best_ascio to turn latin 1 characters in to ascii (but really should leave them for modern OS's)
#       May 25, 2012            bar     fix a comment
#       May 27, 2012            bar     doxygen namespace
#       July 8, 2012            bar     same_time_ish()
#       August 19, 2012         bar     do line segments intersect using a trick
#       September 1, 2012       bar     ext_ambiguous_file_list()
#                                       kmeans clustering
#       September 19, 2012      bar     restricted_eval()
#       October 28, 2012        bar     regression rtn can handle missing data
#       November 14, 2012       bar     get rid of too-generic command line args for re-routing std out/err
#       December 2, 2012        bar     a_pickleable_pil_image
#       December 19, 2012       bar     "Doing gravity right"
#       January 26, 2013        bar     get_full_user_name()
#       May 19, 2013            bar     rotate 2d array
#       May 21, 2013            bar     catch more (all) errors in the unpickle routine
#       July 8, 2013            bar     stdin input parameter to run_program()
#       July 25, 2013           bar     pil_tostring() and pil_fromstring() to avoid pillow's deprecation warnings in most code
#                                       best_w_h_fit_scale()
#       September 6, 2013       bar     way for caller to get to the proc in run_program
#       September 17, 2013      bar     comment
#       September 23, 2013      bar     correct namespace
#                                       triangle rtns
#       September 30, 2013      bar     make_q_empty()
#                                       handle more exceptions in q_get()
#       October 1, 2013         bar     fix cmp_str_with_ints
#       October 9, 2013         bar     find_argi()
#       October 17, 2013        bar     make reroute_stdout_err more robust
#       October 20, 2013        bar     best_line_fit()
#       October 22, 2013        bar     area_of_irregular_polygon()
#       November 24, 2013       bar     raise value error for vertical linear regression lines
#       November 27, 2013       bar     better angle difference code
#                                       radian_angle_from_horizontal()
#       November 29, 2013       bar     a_min_max()
#                                       return value from whack_file()
#       December 3, 2013        bar     golden_rectangle() and ilk
#       February 24, 2014       bar     make a_min_max robust in the face of no file name and None being attempted to be counted
#       February 25, 2014       bar     make_thread_listing()
#       March 1, 2014           bar     move the Windows .ini file dir to .app in C:\users\USER_NAME or, under XP to C:\Documents and Settings\USER_NAME
#                                       that is, move it to where it can be found, but put a dot in front of the name
#                                       change the Linux .ini file name to .ini from .cfg
#       April 13, 2014          bar     dink with close_fds in run_program()
#                                       cache the full user name
#                                       run_shell_program()
#                                       by default, in the run_program routines, route stderr to stdout
#       April 25, 2014          bar     allow caller to pass allowed things to the restricted eval and exec routines
#                                       allow enumerate() and sum() in restricted eval and exec
#       May 11, 2014            bar     create_*_id rtns
#       May 18, 2014            bar     get_system_wide_lock()
#       May 28, 2014            bar     show tid (htop's PID) in thread listing
#       May 29, 2014            bar     can_run_program can now handle None or ""
#       June 13, 2014           bar     decode latin1 in de_html_str
#       June 14, 2014           bar     undotted_file_name_able()
#                                       allow z to distance_from_x_y
#                                       put the short-form thread listing at the bottom of the printout, not the top
#       June 26, 2014           bar     release_system_wide_lock()
#       July 1, 2014            bar     whack_dir() and whack_full_dir()
#       July 2, 2014            bar     average angle and modulo - but they don't work
#       July 3, 2014            bar     file_name_able won't allow file names starting with dashes
#                                       satisfy myself about the average angle logic - I still don't like it when the angles are "local" to each other. In a small area on Earth, the land appears flat and average location is different on flatland than on curve-land
#                                       expand_user_vars(), finally
#       July 16, 2014           bar     drives and sizes
#       July 17, 2014           bar     get_mount_point()
#       July 29, 2014           bar     sha_directory() and sha_dir_compare()
#       July 30, 2014           bar     str_base()
#       August 19, 2014         bar     reverse tick turned to underline in file_name_able()
#       August 28, 2014         bar     safe_file_datetime
#       September 2, 2014       bar     option to not strip blank lines from run_program()
#                                       don't allow pipe | in file_name_able()
#       September 3, 2014       bar     convert_to_unicode()
#                                       sort_numerically() and its ilk
#       September 18, 2014      bar     whack_dir_contents()
#       October 3, 2014         bar     rename a dir to be whacked. and try to get rid of as much of it as can be gotten rid of.
#       October 14, 2014        bar     put the whack full dir tmp name in a variable so it can be changed by outsiders
#       October 21, 2014        bar     not_in()
#       October 28, 2014        bar     best_ascii() comment
#       November 13, 2014       bar     pop_slice()
#       January 18, 2015        bar     disappear_window()
#       January 20, 2015        bar     protect get_disk_space() against bad Windows drives.
#       January 27, 2015        bar     read_whole rtns take optional how_many param
#       April 10, 2015          bar     point_in_polygon(), but not finished
#       April 11, 2015          bar     go with calling the right/bottom edges outside the polygon (with an exception or two when they are angled)
#                                       relatively untested clip_polygon()
#                                       rotate_point()
#       May 2, 2015             bar     compass_angle()
#       May 4, 2015             bar     sort_kmeans_clusters and fix a bug for None values in kmeans logic
#       May 10, 2015            bar     torus_distance()
#       May 16, 2015            bar     square hilbert curver rtns
#                                       bit routines
#                                       make_color_gradient and make_color_wheel
#       May 17, 2015            bar     gray_code and make un_gray_code more powerful
#                                       balanced_8_bit_gray_code8
#       May 24, 2015            bar     median()
#                                       min_array() and max_array() return -1 for empty arrays rather than zero and use argmin/max for numpy arrays
#                                       as_integer_ratio()
#       May 25, 2015            bar     table lookup bit_count
#       June 1, 2015            bar     couple of special cases in median weren't handled right
#                                       flatten arrays for median
#                                       flatten numpy arrays in flatten_array()
#       June 21, 2015           bar     cumsum_sum() and cumsum_average()
#                                       cleaner handling of array copy in median
#       June 23, 2015           bar     sense numpy arrays in cumsum()
#       July 28, 2015           bar     comment
#       July 29, 2015           bar     fix a special case in cumsum()
#       August 4, 2015          bar     make median work for numpy arrays
#                                       is_pil_image() and is_numpy_array()
#       August 6, 2015          bar     find_argi_and_del()
#       August 7, 2015          bar     de_bruijn()
#       --eodstamps--
##      \file
#       \namespace              tzpython.tzlib
#
#
#       Buncha things.
#
#

import  cPickle

import  copy
import  getpass
import  glob
import  htmlentitydefs
import  math
import  os
import  Queue
import  random
import  re
import  shutil
import  string
import  subprocess
import  sys
import  threading
import  time
import  traceback
import  unicodedata
import  zlib
from    types                   import ListType, TupleType, UnicodeType, DictionaryType

try :
    import  hashlib
except      ImportError       :
    import  md5
    import  sha
    class   a_hashlib(object) :
        def md5(me, s  = "")  :
            return(md5.new(s))
        def sha1(me, s = "")  :
            return(sha.new(s))
        pass
    hashlib = a_hashlib()

try :
    import  ctypes
except      ImportError :
    cypes   = None

try     :
    import  win32api
except  ImportError :
    win32api    = None

try     :
    import  pywintypes
except      ImportError :
    class   pywintypes_type(object) :
        pass
    pywintypes          = pywintypes_type()
    pywintypes.error    = Exception                                     # this keeps python from crashing to hide an exception we don't handle, sort of


##  Run under older Pythons
try:
    True, False
except NameError:
    True    = 1
    False   = 0



float_regx_str      = r"(?:[\+\-]?(?:\d+(?:\.\d*)?|\.\d+))"             # but not scientifc e numbers because for no real reason, probably
FLOAT_regx_str      = r"(?:[\+\-]?(?:\.\d+|\d+\.\d*))"                  # number with a decimal point, for sure



def print_exception() :
    e       = sys.exc_info()
    traceback.print_exception(e[0], e[1], e[2])


def print_stack() :
    traceback.print_stack()


def make_thread_listing(force_show_frames = False) :
    """ Return a string with an informative thread listing. """
    tnms    = [ "Thread: " + th.name + " " + str(getattr(th, 'tid', 'NoTID')) for th in threading.enumerate() ]
    tnms.sort(lambda a, b : cmp(a.lower(), b.lower()))
    s       = ""
    for th in threading.enumerate() :
        if  force_show_frames or th.name.startswith('Thread-') :
            fr      = sys._current_frames().get(th.ident, None)
            if  fr  :
                s  += "\n"
                s  += "------ %s %s ------\n" % ( th.name, str(getattr(th, 'tid', 'NoTID')), )
                s  += "".join(traceback.format_stack(fr))                   # traceback.print_stack() by another name
            pass
        pass
    if  s   :
        s  += "\n"
    s      += "\n".join(tnms)
    if  s and (s[-1] != '\n') :
        s  += '\n'

    return(s)






def get_tid() :
    tid             = -2
    if win32api     :
        tid         = win32api.GetCurrentThreadId()
    elif sys.platform.find('linux') >= 0 :                                      # we could try to find the syscall.h or unistd.d file with the SYS_gettid in it
        if  ctypes  :
            tid         = int(str(ctypes.CDLL('libc.so.6').syscall(224)))       # does not work on 64-bit OS (that's probably the reason it returns -1 on spring)
            if  tid < 0 :                                                       # note: "pstree -p -H " + str(os.getpid) is ambiguous at best, and would need a system lock around it, too, if more that 1 thread were using it for this purpose
                tid     = int(str(ctypes.CDLL('libc.so.6').syscall(186)))       # found with " #include <syscall.h> printf("%u\n", SYS_gettid) "
            pass
        pass

    return(tid)



BIT_BUCKET  = [ None ]
def disappear_window(hide) :
    """ If told to, disappear our window. Or, at least, send stdout and stderr to the bit bucket. """
    if  hide :
        BIT_BUCKET[0]   = open(os.devnull, 'w')
        sys.stdout      = BIT_BUCKET[0]
        sys.stderr      = BIT_BUCKET[0]
        if  (sys.platform == 'win32') and hasattr(ctypes, 'windll') and ctypes :
            ctypes.windll.kernel32.FreeConsole()
        pass
    pass



def run_shell_program(cmd, stdin = None, stdout = None, stderr = None) :
    """
        Run the given command line program (full path needed for the executable's name).
        Return the process.
    """
    close_fds   = not not (stdin or stdout or stderr)           # note: I could not repro the reason this was always True before April 13, 2014, but this is an attempt to stop an "Err:[Errno 12] Cannot allocate memory on line NNNN" when failing to fork inside subprocess here
    stdin       = stdin  or subprocess.PIPE
    stdout      = stdout or subprocess.PIPE
    stderr      = stderr or subprocess.STDOUT

    if  sys.platform == 'win32' :
        p       = subprocess.Popen(cmd, shell = True, stdin = stdin, stdout = stdout, stderr = stderr)
    else        :
        p       = subprocess.Popen(cmd, shell = True, stdin = stdin, stdout = stdout, stderr = stderr, close_fds = close_fds)
    return(p)


def run_program(cmd, stdin = None, stdout = None, stderr = None, input = None, proc_a = None, strip_blank_lines = True) :
    """
        Run the given command line program (full path needed for the executable's name).
        Return the exit code int and the stdout/stderr output stripped and CRLFCRLF...LFLF... -> LF converted.
        This is a blocking function and does not return until the program finishes. So you can't monitor the output as it runs.

    """
    if  proc_a     is None :
        proc_a      = []
    try             :
        p           = run_shell_program(cmd, stdin = stdin, stdout = stdout, stderr = stderr)
        proc_a.append(p)
        ( rs, se )  = p.communicate(input = input or None)          # note: this input won't work as input to sudo for the password
        proc_a.pop()
        r           = p.returncode
        rs          = (rs or "").strip() + (se or "").strip()
        rs          = re.sub(r"(?:\r?\n)" + ((strip_blank_lines and "+") or ''), "\n", rs).strip() + "\n"
    except          :
        raise

    return(r, rs)



def in_screen_saver() :
    """ Is the screen saver running? (Only works under Gnome !!!! ) """

    if  sys.platform.find('linux') < 0 :
        return(False)

    ( r, rs )   = run_program("gnome-screensaver-command -q")
    if  (not r) and (rs.find(" active") >= 0) :
        return(True)

    return(False)



def can_run_program(program_file_name) :
    """ Return True if it appears that this program is runnable. """
    return(program_file_name and os.path.exists(program_file_name) and os.path.isfile(program_file_name) and os.access(program_file_name, os.R_OK) and os.access(program_file_name, os.X_OK))



def expand_user_vars(fn) :
    """ Expand ~/ and ${HOME}/, etc. """
    return(os.path.expanduser(os.path.expandvars(fn)))




def ambiguous_file_list(ambiguous_name, do_sub_dirs = False) :
    """
        Return an array with the names of the files that match the given ambiguous file name.
    """

    abn     = expand_user_vars(ambiguous_name)
    files   = glob.glob(abn)

    if  do_sub_dirs :
        (dir_name, amb_name) = os.path.split(abn)
        if  not len(dir_name) :
            dir_name         = "./"

        try         :
            abn     = os.path.join(os.path.normpath(dir_name), os.path.normpath(amb_name))          # note: not sure why this is here. it's not what we want for listdir, but would work for glob, though they both have weirdnesses

            for fn in os.listdir(dir_name) :
                ffn = os.path.join(os.path.normpath(dir_name), fn)
                if  os.path.isdir(ffn) :
                    fls = ambiguous_file_list(os.path.join(ffn, amb_name), do_sub_dirs)
                    for fln in fls :
                        files.append(fln)
                    pass
                pass
            pass
        except ( OSError, IOError, ValueError ) :
            pass
        pass

    return(files)


def ext_ambiguous_file_list(fn, ext, do_sub_dirs = None) :
    """ Return an array with the names of the files that match the given ambiguous file name - looking for those that have the given extension when needed. """

    ext     = ext or ""
    if  ext and (ext[0] != '.') :
        ext = '.' + ext

    if  os.path.isdir(fn) :
        fn  = os.path.join(fn, '*' + ext)
    else    :
        fns = ambiguous_file_list(fn, do_sub_dirs = do_sub_dirs)
        if  not len(fns) :                                          # if there are no ambiguous files to find,
            fn += '*' + ext                                         #    then add the extension in case it's not there.
        pass
    fns     = ambiguous_file_list(fn, do_sub_dirs = do_sub_dirs)    # find the files

    return(fns)



def is_numpy_array(a) :
    """ Return if the given object is a numpy array. """
    return(hasattr(a, 'flatten') and hasattr(a, 'shape'))


def is_pil_image(image) :
    """ Return if the given object is a PIL image. """
    return(hasattr(image, 'convert') and hasattr(image, 'getdata') and hasattr(image, 'getpixel') and hasattr(image, 'crop'))






class   a_min_max(object) :
    """ Track a minimum, maximum, average, etc. """

    def __init__(me) :
        """ Make a new object. """
        me.mn   =   sys.maxint
        me.mnfn = ""
        me.mx   = -(sys.maxint - 1)
        me.mxfn = ""
        me.sm   = 0.0
        me.cnt  = 0

    def mean(me) :
        """ Return the average value so far. (0.0 if none) """
        return(me.sm / float(me.cnt or 1))

    def min(me) :
        """ Return the minimum value so far. """
        return(me.mn)

    def min_info(me) :
        """ Return the minimum value's info so far. """
        return(me.mnfn)

    def max(me) :
        """ Return the maximum value so far. """
        return(me.mx)

    def max_info(me) :
        """ Return the maximum value's info so far. """
        return(me.mxfn)

    def len(me) :
        """ Return the number of values known so far. """
        return(me.cnt)

    def sum(me) :
        """ Return the number of values known so far. """
        return(me.sm)

    def append(me, v, info = None) :
        """ Check out this new value, dude. """
        if  v != None   :
            if  me.mn   > v :
                me.mn   = v
                me.mnfn = info or ""
            if  me.mx   < v :
                me.mx   = v
                me.mxfn = info or ""
            me.sm      += v
            me.cnt     += 1
        pass

    #   a_min_max



def binary_search(a, item, cmp_rtn = None, si = None, ei = None, cmp_obj = None) :
    """
        Binary search the sorted array, 'a' looking for 'item' or the first index in the array that has a value greater than or equal to 'item'.
        Use the given 'cmp_rtn', which looks like the default, direct_cmp(), below.
        Return the found index (or len(a) if all the array's items are below 'item').
    """


    def direct_cmp(a, i, item, cmp_obj) :
        return(cmp(a[i], item))


    si      = si or 0
    if  ei == None  :
        ei  = len(a)

    if  cmp_rtn == None :
        cmp_rtn = direct_cmp

    lo      = si
    hi      = ei
    mid     = (lo + hi) / 2
    while lo < hi :
        mid = (lo + hi) / 2

        if  cmp_rtn(a, mid, item, cmp_obj) < 0 :        # note: it appears that this could be <= and we'd find the firt index with a value greater than 'item'
            mid    += 1
            lo      = mid
        else :
            hi      = mid
        pass

    # let the caller do mid=max(0, min(len(a), mid)) if he wants

    return(mid)





def find_in_array(a, s, bi = None, ei = None) :
    """
        Find an item in an array, 'a' - or the first of an array of items, 's', in the array..
        Return -1 if not found.
        Otherwise return the found array index.
    """

    if  not isinstance(a, ListType) and not isinstance(a, TupleType) :
        a = [ a ]

    if  not isinstance(s, ListType) and not isinstance(s, TupleType) :
        s = [ s ]

    bi  = bi or 0
    if  ei == None :
        ei  = len(a)

    for ss in s :
        try :
            i = a.index(ss, bi, ei)
            return(i)

        except TypeError :                  # catch python 2.2 or whatever
            try :
                i = a[bi:ei].index(ss)
                return(i)

            except IndexError :
                pass
            except ValueError :
                pass
            pass
        except IndexError :
            pass
        except ValueError :
            pass
        pass

    return(-1)


#
#   http://stackoverflow.com/questions/42519/how-do-you-rotate-a-two-dimensional-array
#

def rotate_2d_array_clockwise(a) :
    """ Rotate a 2D array clockwise. """
    return(zip(*a[::-1]))

def rotate_2d_array_counter_clockwise(a) :
    """ Rotate a 2D array counter clockwise. """
    return(zip(*a)[::-1])



def max_index(a) :
    """
        Return the index in to the given array of the maximum value in the array.
    """

    if  len(a) == 0 :
        return(-1)

    if  hasattr(a, 'argmax') :
        return(a.argmax())          # numpy

    if  hasattr(a, 'index') :       # numpy arrays don't have this, apparently
        return(a.index(max(a)))     # benchmark says this is faster (than enumerate, too)

    bi  = 0
    bv  = a[0]
    for i in xrange(1, len(a)) :
        v       = a[i]
        if  bv  < v :
            bv  = v
            bi  = i
        pass

    return(bi)



def min_index(a) :
    """
        Return the index in to the given array of the minimum value in the array.
    """

    if  len(a) == 0 :
        return(-1)

    if  hasattr(a, 'argmin') :
        return(a.argmin())          # numpy

    if  hasattr(a, 'index') :
        return(a.index(min(a)))     # benchmark says this is faster (than enumerate, too)

    bi  = 0
    bv  = a[0]
    for i in xrange(1, len(a)) :
        v       = a[i]
        if  bv  > v :
            bv  = v
            bi  = i
        pass

    return(bi)


def as_integer_ratio(v, cutoff = 0.000000001) :
    """ Find a good fraction for the given real number. """
    cr  = 1.0 / cutoff
    x   = float(v)
    n   = 0
    d   = 1
    tn  = 1
    td  = 0
    while (tn < cr) and (td < cr) :
        f   = math.floor(x)
        n, tn   = tn, f * tn + n
        d, td   = td, f * td + d
        if  (f == x) or (abs(tn / td - v) < cutoff) :
            if  (tn < cr) and (td < cr) :
                n   = tn
                d   = td
            break
        x   = 1 / (x - f)

    return(n, d)



def median(a, middle = None) :
    """
        Return the float median or some kinda of median-esque value from the given array.

        middle can be from 0.0 to 1.0

        ????
            Should the 1/3rd-ian of [ 1, 2, 3 ] be 1? and the 2/3rd-ian be 3?

            That is, at the ends, shouldn't a sufficiently close to zero or 1 -ian value pick the end values in the array?

            If the floor and ceil operations are given tweaked values and the special li==hi return value is done for li>=hi, then this sort of thing might be handled in a way that makes a different sense.

            This is all leaving aside the issue of whether the proper model of a median should be a linear interpolation between two array values, and whether the model should effectively fill in
            the array value with many microscopic values between the array values, but not, say, filling in half way past the end values.

                In other words, should the model of [ 1, 2, 3 ] by [ 1, 1.1, 1.2.... 2.7, 2.8, 2.9, 3 ] or [ .5, .6, .7, .8, .9, 1.0, 1.1 ... 2.9, 3, 3.1 ... 3.5, ]?

                Current thinking

                    It makes sense that it would be the former, as the code does it, but not perfect sense.

                    An -ian value outside the array values? Ugh. And some particular normal median case doesn't work right if the boundaries are extended. I forget what it is.

    """
    if  a  is None :
        return(None)

    if  is_pil_image(a) :
        a   = a.getdata()

    if  hasattr(a, 'flatten') :
        a   = a.flatten()               # numpy array
        a   = list(a)
    elif len(a) and isinstance(a[0], (list, tuple)) :
        a   = flatten_array(a)
    else    :
        a   = list(a)
    a.sort()

    if  not len(a) :
        return(None)
    if  len(a) == 1 :
        return(a[0])

    if  middle is None :
        middle  = 0.5

    if  not middle :
        return(a[0])
    if  middle == 1.0 :
        return(a[-1])

    li  = int(math.floor((len(a) - 1) * middle))
    hi  = int(math.ceil( (len(a) - 1) * middle))

    if  li == hi :
        return(a[li])

    lv      = a[li]
    hv      = a[hi]

    try         :
        n, d    = float(middle).as_integer_ratio()
    except      :
        n, d    = as_integer_ratio(middle)

    fr      = float(n) * ((len(a) - 1) % float(d)) / float(d)
    fr      = fr - math.floor(fr)

    return(lv + ((hv - lv) * fr))




def left_valley(a, i, bump = 0) :
    """ Return the lowest spot in the given array to the left/west of the given index. """

    bump    = bump or 0
    while i > 0 :
        if  a[i - 1] > a[i] + bump :        # find the spot to the left/west of a flat valley
            break
        i -= 1

    return(i)
west_valley     = left_valley


def rite_valley(a, i, bump = 0) :
    """ Return the lowest spot in the given array to the rite/east of the given index. """

    bump    = bump or 0
    while i < len(a) - 1 :
        if  a[i + 1] > a[i] + bump :        # find the spot to the rite/east of a flat valley
            break
        i  += 1

    return(i)
east_valley     = rite_valley
right_valley    = rite_valley


#
#   Snagged from: http://rightfootin.blogspot.com/2006/09/more-on-python-flatten.html
#
def flatten_array(l, ltypes = (list, tuple)) :
    """
        Flatten an array (of arrays).
    """

    if  hasattr(l, 'flatten') :
        return(l.flatten())             # numpy array

    ltype   = type(l)
    l       = list(l)
    i       = 0
    while i < len(l) :
        while isinstance(l[i], ltypes) :
            if  not l[i] :
                l.pop(i)
                i  -= 1
                break
            else :
                l[i:i + 1]  = l[i]
            pass
        i  += 1

    return(ltype(l))



def cumsum(a) :
    """
        Return a 2D array that's a cumulative sum of the given array.

    """
    if      hasattr(a,    'cumsum') :
        if  hasattr(a[0], 'cumsum') :                           # TODO: should be able to handle N axises

            return(a.cumsum(axis = 1).cumsum(axis = 0))

        return(a.cumsum())                                      # 1D

    a   = copy.deepcopy(a)

    try :
        for y in xrange(len(a)) :
            for x in xrange(1, len(a[0])) :
                a[y][x]    += a[y][x - 1]
            pass
        for x in xrange(len(a[0])) :                            # note: requires each row be the same length
            for y in xrange(1, len(a)) :
                a[y][x]    += a[y - 1][x]
            pass
        pass
    except AttributeError :
        pass

    return(a)


def cumsum_sum(a, x, y, w, h) :
    """
        Return the sum of the original array values in a given rectangle from the cumulative sum array of the original array.

        The cumulative sum array can be computed using numpy like this:
            a   = numpy.cumsum(numpy.cumsum(original_a, axis = 0), axis = 1)

    """
    w   = max(0, min(w, len(a[0]) - x))
    h   = max(0, min(h, len(a   ) - y))
    if  w and h :
        return(                a[y + h - 1][x + w - 1]
               - ((      y and a[y     - 1][x + w - 1]) or 0)
               - ((x and       a[y + h - 1][x     - 1]) or 0)
               + ((x and y and a[y     - 1][x     - 1]) or 0)
              )
    return(0)


def cumsum_average(a, x, y, w, h) :
    """ Return the average original array float value of the given rectangle's values from the cumulative sum array of the original array. """
    w   = max(0, min(w, len(a[0]) - x))
    h   = max(0, min(h, len(a   ) - y))
    if  w and h :
        s   = cumsum_sum(a, x, y, w, h)
        return(float(s) / (w * h))
    return(None)






def pop_slice(a, frm = None, to = None) :
    """ pop() the given slice of the array. """
    r   = a[frm:to]
    del(  a[frm:to])
    return(r)




def invert_dictionary(d, dupable_values = {}) :
    """
        Invert the given dictionary.
        The result is updated with force_dict.
    """

    dupable_values  = dupable_values or {}
    rd              = dict((v, k) for k, v in d.iteritems())
    if  len(rd)    != len(d) :
        rrd         = make_dictionary(rd.values())
        va          = [ { k : v } for k, v in d.iteritems() if (k not in rrd) and (v not in dupable_values) ]
        if  va      :
            raise IndexError("invert_dictionary(): %d duped value%s %s" % ( len(d) - len(rd), s_except_1(va), repr(va) ) )
        rd.update(dupable_values)

    return(rd)


def make_dictionary(a, val = True) :
    """
        Make a dictionary from a list/tuple.

        If python is 2.3+, then this is fromkeys().
    """

    retval  = {}
    try     :
        retval.update(a)
        return(retval)

    except ( ValueError, AttributeError, TypeError ) :
        pass

    if  a  != None :

        if  not isinstance(a, ListType) and not isinstance(a, TupleType) and not isinstance(a, basestring) :
            a = [ a ]

        for k in a :
            retval[k] = val
        pass

    return(retval)


def buples_to_dictionary(a) :
    """
        Given an array of [ key, value ] items return a dictionary. (dict() function does this.)
    """

    d   = {}
    for i in a :
        d[i[0]] = i[1]

    return(d)



def make_index_dictionary(a) :
    """
        Make a dictionary from a list/tuple where the keys are the list/tuple's values and the values are the list/tuple indices.

    """

    retval = {}

    if  a != None :

        if  not isinstance(a, ListType) and not isinstance(a, TupleType) and not isinstance(a, basestring) :
            a = [ a ]

        for i, k in enumerate(a) :
            retval[k] = i
        pass

    return(retval)


def update_all_case_keys(d) :
    """
        Update a dictionary, adding key/values for all upper() or lower() versions of existing keys where there are none now.
    """

    for k in d.keys() :
        try :
            nk  = k.lower()
            if  nk not in d :
                d[nk]   = d[k]
            nk  = k.upper()
            if  nk not in d :
                d[nk]   = d[k]
            pass
        except AttributeError :
            pass                    # the key is and int or something
        pass
    pass



def list_lstrip(a, va) :
    """
        Return an array subjected to the logical equivalent of string.lstrip().
    """

    if  not isinstance(va, (ListType, TupleType)) :
        va  = [ va ]
    va  = make_dictionary(va)

    for i in xrange(len(a)) :
        if  a[i] not in va :

            return(a[i:])

        pass

    return([])







def fromkeys(a, val = True) :
    """
        Synonym for make_dictionary.
    """

    return(make_dictionary(a, val))



def without_dupes(a) :
    """
        Return a copy of the given array with dupes removed.
        The item order will probably be changed.
    """

    return(make_dictionary(a).keys())


def de_dupe_str(s) :
    """
        Return the given string without duplicate characters (after the 1st instance of each unique character).
    """

    cnts    = {}
    so      = ""
    if  type(s) == type(u"") :
        so  = u""
    for c in s :
        cnts[c] = cnts.get(c, 0) + 1
        if  cnts[c] < 2 :
            so += c
        pass

    return(so)



def not_in(d, a) :
    """ Return an array of the keys in dictionary, d (or values in array, d) that are not in array a (or dictinonary a's keys). """
    if  hasattr(d, 'keys') :
        d   = make_dictionary(d.keys())         # make copy of 'd's keys
    else    :
        d   = make_dictionary(d)                # or make a dictionary of 'a'
    if  hasattr(a, 'keys') :
        a   = a.keys()                          # make an array of values we'll look for
    for v in a :
        if  v in d :
            del(d[v])                           # get rid of values that are in 'a'
        pass
    return(d.keys())                            # leaving only the keys that aren't in 'a'




def keys_sorted_by_values_keys(hash_dict) :
    """
        Return an array of the keys from a dictionary, sorted by value/key.
    """

    def _vkcmp(k1, k2) :
        c      = cmp(hash_dict[k1], hash_dict[k2])
        if  c != 0 :
            return(c)
        return(cmp(k1, k2))

    v = hash_dict.keys()

    v.sort(_vkcmp)

    return(v)


def values_sorted_by_values_keys(hash_dict) :
    """
        Return an array of the values from a dictionary, sorted by value/key.
    """

    kys = keys_sorted_by_values_keys(hash_dict)

    return(map(lambda k : hash_dict[k], kys))



def keys_sorted_by_keys_values(hash_dict) :
    """
        Return an array of the keys from a dictionary, sorted by key/value.
    """

    def _vkcmp(k1, k2) :
        c      = cmp(k1, k2)
        if  c != 0 :
            return(c)
        return(cmp(hash_dict[k1], hash_dict[k2]))

    v = hash_dict.keys()

    v.sort(_vkcmp)

    return(v)


def values_sorted_by_keys_values(hash_dict) :
    """
        Return an array of the values from a dictionary, sorted by key/value.
    """

    kys = keys_sorted_by_keys_values(hash_dict)

    return(map(lambda k : hash_dict[k], kys))


def value_array_for_key(array_of_dicts, k, dflt = None) :
    """
        Return an array of values for the given key in each dict in an array of dicts.

        If dflt is None :
            Skip any dict that doesn't have the key, returning an array shorter than the input array.
        else            :
            Return dflt for any missing value.
    """

    if  dflt == None :
        return([ d[k]           for d in array_of_dicts if k in d ])

    return(    [ d.get(k, dflt) for d in array_of_dicts           ])



def replace_value_array_for_key(array_of_dicts, k, a) :
    """
        Put the given array of values in each dict in an array of dicts - each value under the given key.

        Raise an IndexError exception if the length of 'a' is not the same as 'array_of_dicts'.
    """

    if  len(array_of_dicts) != len(a) :
        raise IndexError("Wrong length %u in to %u" % ( len(a), len(array_of_dicts) ))

    for di in xrange(len(array_of_dicts)) :
        array_of_dicts[di][k]   = a[di]
    pass



def numerically_sortable(s) :
    """
        Return a string converted to one appropriate for sorting numerically. That is, "a9" sorts lower than "a10".

        Notice that negative numbers aren't handled, as the integer parts of them are a problem.

        Also, notice that dots make floats. That may not be what you want.

        There are better ways to do this - creating a list of strings and numbers for each item in the list and sorting on those lists, for instance.
        But, it happened, I wanted this routine, not the actual sort routines. And dashes before the numbers are as often dashes, not minus signs, that, ... well ...

    """

    #
    #   import  natsort     is a heavy-weight solution for this kind of thing
    #

    def _float_sub(g) :
        """ Replace ints. """
        f   = float(g.group(1))
        return("%065.32f" % f)

    def _int_sub(g) :
        """ Replace ints. """
        s   = g.group(1)
        if  s.startswith('.') :
            return(s)
        return("%032i" % int(s, 10))

    s   = re.sub(r'(\.\d+|\d+\.\d*)',   _float_sub, s)         # note: the digits after the dot can be of various lengths. numericizing them makes .11 the same as .110 and makes .11 less than .111
    s   = re.sub(r'(\.?\d+)',           _int_sub,   s)

    return(s)


def sort_numerically(a) :
    """ Sort the given list numerically. That is, "9" comes before "10". """
    a.sort(lambda a, b : cmp(numerically_sortable(a), numerically_sortable(b)))

def sorted_numerically(a) :
    """ Sort the given list numerically. That is, "9" comes before "10". """
    return(sorted(a, lambda a, b : cmp(numerically_sortable(a), numerically_sortable(b))))





def array_find(a, s, si = None, ei = None) :
    """
        Return the index of the item in an array or negative 1 if it's not there.
    """

    return(find_in_array(a, s, si, ei))



def find_arg(args, a) :
    """
        Return the index in to args of 'a' (or any string in 'a') or -1 if not found.
        Underscores are ignored and/or match dashes.

        DO NOT USE THIS! Use the next one.
    """

    if  not isinstance(args, ListType) and not isinstance(args, TupleType) :
        args    = [ args ]
    adn         = make_index_dictionary([ s.replace('_', '' ) for s in args ])
    add         = make_index_dictionary([ s.replace('_', '-') for s in args ])

    if  not isinstance(a, ListType) and not isinstance(a, TupleType) :
        a       = [ a ]

    for s in a  :
        i       = adn.get(s.replace('_', '' ), -1)
        if  i  >= 0 :
            return(i)
        i       = add.get(s.replace('_', '-'), -1)
        if  i  >= 0 :
            return(i)
        pass

    return(-1)


def find_argi(sys_args, to_find_a) :
    """
        Return the index in to 'sys_args' of 'to_find_a' (or any string in 'to_find_a') or -1 if not found.
        If 'to_find_a' has args with underscores or non-leading dashes, they are converted to being eqivalent to each other and to nothing.
    """

    if  not isinstance(sys_args,  ListType) and not isinstance(sys_args,  TupleType) :
        sys_args    = [ sys_args  ]
    if  not isinstance(to_find_a, ListType) and not isinstance(to_find_a, TupleType) :
        to_find_a   = [ to_find_a ]

    to_find_a       = make_dictionary(to_find_a)
    for k in to_find_a.keys() :
        to_find_a[k.replace('_', '-')]  = True                                                      # sense args with dashes between the words in case
        to_find_a[k.replace('_', '' )]  = True                                                      # sense args with runonwords
        to_find_a[re.sub(r'(^-+).*', r'\1', k) + re.sub(r'^-+', '', k).replace('-', '_')] = True    # sense args with dashes as having underscored words
        to_find_a[re.sub(r'(^-+).*', r'\1', k) + re.sub(r'^-+', '', k).replace('-', '' )] = True    # sense args with dashes as begin runonwords

    for ai, a in enumerate(sys_args) :
        if  a in to_find_a :
            return(ai)
        pass

    return(-1)


def find_argi_and_del(sys_args, to_find_a) :
    """ Call find_argi() and delete the argument from 'sys_args' if it's found, returning -1 or the index of the arg that was deleted. """
    ai  = find_argi(sys_args, to_find_a)
    if  ai >= 0 :
        del(sys_args[ai])
    return(ai)




def strrev(s) :
    """
        Reverse a string.

        Or post or 2.2 (2.3?) return(s[::-1])
    """

    a = list(s)
    a.reverse()
    return(string.join(a, ""))


def strip_c_comments(text) :
    """
        Strip C and C++ comments from a string.
        From:   http://stackoverflow.com/questions/241327/python-snippet-to-remove-c-and-c-comments
    """

    def replacer(match) :
        s   = match.group(0)
        if  s.startswith('/') :
            return("")
        return(s)

    pattern = re.compile(r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"', re.DOTALL | re.MULTILINE)

    return(re.sub(pattern, replacer, text))



def c_string(s) :
    """
        Escape a string back to C string form.
        Or, anyway, get the normal escaped characters back to their C string form.

        This *must* be a built in function somewhere! (repr(), sort of)
    """

    s   =   s.replace("\\", r"\134")                # this way there are no doubled slashes
    s   =   s.replace("\'", r"\'")
    s   =   s.replace("\"", r"\"")
    s   =   s.replace("\a", r"\a")
    s   =   s.replace("\b", r"\b")
    s   =   s.replace("\f", r"\f")
    s   =   s.replace("\n", r"\n")
    s   =   s.replace("\r", r"\r")
    s   =   s.replace("\t", r"\t")
    s   =   s.replace("\v", r"\v")

    return(s)


def c_ctrl_esc(s) :
    """
        Escape a string back to C string form with all control characters and Perl smarties escaped.
    """

    def _esc(s) :
        return(r"\%03o" % ord(s.group(0)))

    s   = c_string(s)
    s   = re.sub(r"[\0-\x1f$@%]", _esc, s)              # escape control characters and Perl smarties

    return(s)



def unicode_byte_string(s) :
    """
        Return a Unicode string as a byte string.

        Note: encode puts 2 bytes (converted codecs.BOM_LE), at the start of the string (under Windows or maybe x86).
    """

    return(s.encode('utf-16'))



def ascii(s, ac = '_') :
    """
        Return the given string after converting all characters over 127 to _ or the given character.
    """

    if  ac == None :
        ac  = '_'

    astr    = ""

    if  not isinstance(s, basestring) :
        s = str(s)

    for i in range(0, len(s)) :
        c = s[i:i+1]
        if  ord(c) >= 128 :
            c = ac

        astr += c

    return(astr)


def convert_to_unicode(s) :
    """ Try to convert the given string to unicode as best we can guess. """
    if  not isinstance(s, unicode) :
        try :
            s   = unicode(s.decode('utf8'))     # this blows up on most latin1 chars - so we hope such is the case if the string is latin 1
        except UnicodeDecodeError :
            s   = unicode(s.decode('latin1'))   # bail out
        pass
    return(s)



def best_ascii(unicode_s) :
    """
        Return the best guess as to ASCII characters that could be used for the given string.
    """

    unicode_s   = convert_to_unicode(unicode_s)

    #
    #   NFKD doesn't work for a lot of characters \u0189, for instance, should be a D
    #   http://www.unicode.org/reports/tr36/confusables.txt is a tiny attempt at look-alikes.
    #   Best to do something to actually render characters in various fonts and compare them to ASCII chars in the same font.
    #   And this logic could be used to compare fonts and put them in family/groups.
    #
    #   Another way of dealing with this is to get the descriptions of the characters, unicodedata.name(c), from http://www.unicode.org/Public/UNIDATA/UnicodeData.txt, and do a least-differencs string thing against the ascii characters' names
    #   Some of the non-Roman names could be table-translated going in to such a thing.
    #
    #   Another thing to do would be to convert Chinese characters to Pingyen. And do similar to other appropriate languages.
    #
    s   = "".join([ unicodedata.normalize("NFKD", c)[0] for c in unicode_s ])

    return(s)





def file_name_able(fn) :
    """
        Return the given file name with the illegal file name characters stripped from it.
    """

    if  isinstance(fn, UnicodeType) :
        fn  = best_ascii(fn).encode('ascii', 'replace')

    fn      = ascii(fn)

    fn      = re.sub(r"[\"]", "", fn)
    fn      = re.sub(r"[\\\/\:\&\^\*\?\<\>\|\"\'\`\+]", "_", fn)
    fn      = re.sub(r"^-", "_", fn)                                                    # don't allow leading dashes - so they can't be confused with Unix command line arguments

    return(fn.strip())


def undotted_file_name_able(base_name_no_ext) :
    """
        Return the given file name with the illegal file name characters stripped from it, including dots.
    """
    return(file_name_able(base_name_no_ext).replace('.', '_'))



printable_re    =   re.compile(r"[^" + re.escape(string.printable) + r"]")
def printable(s, tochr = "_") :
    """
        Return a printable string with non-printable characters converted to underscores or whatever.
    """

    tochr   = "" if tochr == "" else (tochr or "_")

    s   = printable_re.sub(tochr, s)

    return(s)



def printable_str(s) :
    """ Return a string that's printable. """

    try :
        rs  = unicode(s).encode('unicode_escape')
    except UnicodeDecodeError :
        try :
            rs  = unicode(s.decode('utf8')).encode('unicode_escape')
        except UnicodeDecodeError :
            try :
                rs  = unicode(s.decode('latin1')).encode('unicode_escape')
            except UnicodeDecodeError :
                rs  = repr(s)
            pass
        pass

    return(rs)



def lf_only(fs) :
    """ Convert all variants of line breaks to '\n' in a string with multiple text lines. """

    fs  = re.sub(r"\r+\n", "\n", fs)
    fs  = re.sub(r"\r",    "\n", fs)

    return(fs)




##  Get rid of leading line feeds (amounts to s.strip("\n"))
strip_first_lines_re            =   re.compile(r"^\n+",                 re.DOTALL)

##  Get rid of white-space that is at the ends of text lines inside a string.
strip_eol_spaces_re             =   re.compile(r"\s+$",                 re.MULTILINE)


def lf_only_with_no_trailing_white_space(fs) :
    """ Run a string through lf_only() and strip trailing white space from the lines, too. Insure last lines ends with LF. """

    fs  = lf_only(fs)
    fs  = strip_eol_spaces_re.sub("", fs)
    fs += "\n"

    return(fs)



def no_blank_lines(fs) :
    """
        Get rid of any blank or white-space-only lines in a string containing multiple text lines.

        Gets rid of white space at the ends of all text lines as a side effect.
        The last line is forced to end with an LF.
    """

    fs  = lf_only(fs)
    fs  = strip_eol_spaces_re.sub("", fs)
    fs += "\n"
    fs  = re.sub("\n(\s*\n)+", "\n", fs)
    fs  = strip_first_lines_re.sub("", fs)

    return(fs)



def multiline_strip(fs, chrs = None) :
    """
        Do a strip on a string with multiple text lines.
        If no \n is at the end of 'fs', there will be none at the end of the return value.
        CRLF, LF and CR all are considered to be an EOL.
    """

    fs  = "\n".join( [ s.strip(chrs) for s in re.split(r"\r?\n|\r", fs) ] )
    return(fs)
    if  chrs :
        rs  = re.escape(chrs)
    else :
        rs  = r"\s"

    fs  = lf_only(fs)

    fs  = re.sub(r"(?m)^[" + rs + "]+",  "", fs)
    fs  = re.sub(r"(?m)["  + rs + "]+$", "", fs)
    fs  = re.sub(r"^[" + rs + "]+",  "", fs)
    fs  = re.sub(r"["  + rs + "]+$", "", fs)

    return(fs)


def multiline_flush_left(s) :
    """
        Whack left-side spaces shared for all non-blank lines in the given multiline string.
        Also whacks right-side white-space.
        Also, converts to \n separated lines. No CRs.
    """

    if  isinstance(s, basestring) :
        s   = re.split(r"\r*\n", s)

    la      = [ len(ln) - len(ln.lstrip(' ')) for ln in s if ln.strip() ]
    if  la  :
        lc  = min(la)
        s   = [ ln[lc:] if ln.strip() else ln for ln in s ]
        s   = [ ln.rstrip() for ln in s ]
    return("\n".join(s))



_crc32_table = (
        0x4dbdf21c,
        0x500ae278,
        0x76d3d2d4,
        0x6b64c2b0,
        0x3b61b38c,
        0x26d6a3e8,
        0x000f9344,
        0x1db88320,
        -1610256068,        # 0xa005713c,
        -1112383144,        # 0xbdb26158,
        -1687465484,        # 0x9b6b51f4,
        -2032385648,        # 0x86dc4190,
         -690409300,        # 0xd6d930ac,
         -881975096,        # 0xcb6e20c8,
         -306769820,        # 0xedb71064,
         -268435456,        # 0xf0000000
        )

_TEST_CRC_VALUE     = -1737075662           # 0x98765432
_CRC32_MASK         = 0xFFFFffffl
try :
    _CRC32_MASK     = int(_CRC32_MASK)
except OverflowError :
    _CRC32_MASK     = -1




INITIAL_CRC32_VALUE = 0     # 0xFFFFffffl



#
#       Compute a 32-bit (PKZIP) crc of a string or array.
#
#       REMEMBER! The value could easily be construed to be a signed int. Odd things might happen in future versions of python.
#       To be "correct" about it, the value should be massaged like "crc = long(crc) & 0xFFFFffffL", yeilding a long value.
#
#


def crc32(current_crc, c) :
    c            = int(c)
    current_crc  = (((current_crc >> 4) & 0x0FFFffff) ^ _crc32_table[(current_crc ^  c      ) & 0xf]) & _CRC32_MASK
    current_crc  = (((current_crc >> 4) & 0x0FFFffff) ^ _crc32_table[(current_crc ^ (c >> 4)) & 0xf]) & _CRC32_MASK

    return(current_crc)


def pure_python_crc32(current_crc, xmem) :
    # print "crclen", len(xmem)
    for i in range(0, len(xmem)) :
        cv = ord(xmem[i:i+1])
        current_crc = crc32(current_crc, cv)
        # print "%u %08x %02x %s\n" % ( i, current_crc, cv, chr(cv) )
    return(current_crc)



def blkcrc32(current_crc, xmem) :

    if  sys.version < "2.4" :
        return(pure_python_crc32(current_crc, xmem))                # maybe 2.3 is ok. I don't know. But 2.4 is ok and 2.2 is not.

    current_crc = long(current_crc)
    if  current_crc & 0x80000000L :
        current_crc = (~current_crc + 1) & 0xFFFFffffL
        current_crc = -current_crc

    return(long(zlib.crc32(xmem, int(current_crc))) & 0xFFFFffffL)




xmcrctab    = (
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
        0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
        0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
        0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
        0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
        0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
        0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
        0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
        0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
        0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
        0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
        0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
        0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
        0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
        0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
        0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
        0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
        0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
        0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
        0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
        0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
        0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
        0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
        )



def crc16(current_crc, c) :
    c            = int(c)
    #                               Note: Not Xmodem CRC. Xmodem has post processing. We do the Palm CRC: "dcrc /i -1 /Wp"
    return((((current_crc) << 8) ^ xmcrctab[(((current_crc) >> 8) ^ c) & 0xff]) & 0xffff)


def pure_python_crc16(current_crc, xmem) :
    # print "crclen", len(xmem)
    for i in range(0, len(xmem)) :
        cv          = ord(xmem[i:i+1])
        current_crc = crc16(current_crc, cv)
        # print "%u %08x %02x %s\n" % ( i, current_crc, cv, chr(cv) )
    return(current_crc & 0xffff)



def blkcrc16(current_crc, xmem) :
    return(pure_python_crc16(current_crc, xmem))






def xorsum(s) :
    """
        Compute the longitudinal parity (the XOR sum) of a string.
    """

    cs      = 0
    for c in s :
        cs ^= ord(c)

    return(cs)







def str_base(n, base = 10) :
    """ Convert a number to a lower case string like str(), but with a given base from 2 to 36. """
    if  n < 0 :
        return('-' + str_base(-n, base))

    (d, m)  = divmod(n, base)

    return(((d and str_base(d, base)) or "") + chr((((m < 10) and 48) or 87) + m))


#
#
#   Find the "cosine" of the angle between two vectors.
#
#       If either vector is None, then the return value is None.
#       If all elements of either of the arrays are zero (or None), then the return value is None.
#
#       Undef'd values in the arrays are ignored - that "dimension" is ignored, that is.
#
#       cosine = tz_vector_cosine( [ 1, 2, 3 ], [ 4, -5, 6 ])
#
#       If the vectors are the same, then the return value is 1.
#       If the vectors are exactly opposite in direction and magnitude, then the return value is -1.
#       If the vectors are exactly at "right angles", then the return value is 0.
#
#
def tz_vector_cosine(v1, v2) :
    """
        Return the hyperspace cosine of two vectors.
    """

    if  (v1 == None) or (v2 == None) :    return(None)

    sum      = 0.0
    ss1      = 0.0
    ss2      = 0.0

    for i in range(0, min(len(v1), len(v2))) :

        i1   = v1[i]
        if  i1 == None :    continue

        i2   = v2[i]
        if  i2 == None :    continue

        i1   = float(i1)
        i2   = float(i2)

        sum += (i1 * i2)
        ss1 += (i1 * i1)
        ss2 += (i2 * i2)

    if  (ss1 == 0.0) or (ss2 == 0.0) :
        return(None)

    return(sum / math.sqrt(ss1 * ss2))




#
#
#       Decode HTML character entities in a string.
#
#
html_entity_re  = re.compile(r"\&[^;\r\n\s]+;", re.DOTALL)

def decode_html_entities(s, nbsp_chr = None) :
    """
        Decode any HTML character entities in the string to their character counterparts.

        The string given to this routine should be unicode.
        If it isn't then unicode (> Latin 1) characters will
        cause python fusses of

        "TypeError: function takes exactly 5 arguments (1 given)"

        or other bad things to happen.

    """

    if  nbsp_chr == None :
        nbsp_chr  = htmlentitydefs.entitydefs['nbsp']

    def _entity_2_chr(g) :
        try :
            w = g.group(0)[1:-1]

            if htmlentitydefs.entitydefs.has_key(w) :
                if  w == 'nbsp' :
                    w = nbsp_chr
                else :
                    w = htmlentitydefs.entitydefs[w]
                pass

            if  (w[0:2] == '&#') and (w[-1:] == ';') :          # handles ints from htmlentitydefs
                w   = w[2:-1]
                try :
                    w = chr(int(w))
                except ValueError :
                    w = unichr(int(w))
                pass
            elif w[0:1] == '#' :                                # handles normal int values from the passed string
                w   = w[1:]
                try :
                    w = chr(int(w))
                except ValueError :
                    w = unichr(int(w))
                pass

            pass

        except ValueError :
            w = g.group(0)

        if  len(w) == 1 :
            if  128  <= ord(w) < 256 :
                w   = w.decode('latin1')
            elif 256 <= ord(w) :
                pass
            pass

        return(w)


    return(html_entity_re.sub(_entity_2_chr, s))




def safe_html(txt) :
    """
        Convert the given string in to text that can be put out in an HTML page without worry of it being interpreted as anything but text.
    """

    def _decimalfy(s) :
        return("&#" + str(ord(s.group(0))) + ";")

    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    txt = lf_only(txt)
    txt = re.sub(r"[\r\n]", "<BR>", txt)
    txt = re.sub(r"-{6,}", "<HR>", txt)
    txt = re.sub(r"[^ -\176]", _decimalfy, txt)             # escape all characters outside of space-to-tilde

    return(txt)



cdata_string_re = re.compile(r"^<\!\[CDATA\[.*\]\]>$")

def maybe_wrap_with_cdata(s) :
    """ If needed, and if it's not already wrapped with a CDATA tag, wrap this string with <[!CDATA[...]]> """

    if  not cdata_string_re.match(s) :
        ns  = safe_html(s)
        if  ns != s :
            s   = "<![CDATA[%s]]>"  % ( s.replace("]]>", "&#93;&#93;&gt;") )
        pass

    return(s)





de_br_re        = re.compile(r"</?br\b[^>]{0,200}>",                    re.DOTALL + re.IGNORECASE)
de_p_re         = re.compile(r"</?p\b[^>]{0,200}>",                     re.DOTALL + re.IGNORECASE)
de_hr_re        = re.compile(r"<hr\b[^>]{0,200}>",                      re.DOTALL + re.IGNORECASE)
de_lfs_re       = re.compile(r"<(/?(?:table|tr|dir|li|ol|ul|dt|dl))\b", re.DOTALL + re.IGNORECASE)

de_tab_re       = re.compile(r"\t",                                     re.DOTALL + re.IGNORECASE)
de_space_re     = re.compile(r" +",                                     re.DOTALL + re.IGNORECASE)

de_lf_re        = re.compile(r"\n *\n *(?:\n *)+",                      re.DOTALL + re.IGNORECASE)
de_lfsp_re      = re.compile(r"\n +",                                   re.DOTALL + re.IGNORECASE)
de_splf_re      = re.compile(r" +\n",                                   re.MULTILINE)
de_multlf_re    = re.compile(r"\n+",                                    re.DOTALL + re.IGNORECASE)

de_script_re    = re.compile(r"<script\b[^>]*>.*?</script\b[^>]*>",     re.DOTALL + re.IGNORECASE)

de_html_re      = re.compile(r"<[^>]+>",                                re.DOTALL + re.IGNORECASE)


def de_html_str(s) :
    """
        Do cheaply what something like lynx could do from the command line:
          Convert a string that contains HTML in to a text string with no HTML markup, but
          with the text looking kind of like the HTML would look if rendered as text.
    """
    if  isinstance(s, ListType) or isinstance(s, TupleType) :
        s       = "\n".join(s)

    s = de_tab_re.sub(" ", s)
    s = de_space_re.sub(" ", s)

    s = s.replace("\r\n", "\n")
    s = s.replace("\r",   "\n")
    s = de_lf_re.sub("\n\n", s)
    s = de_lfsp_re.sub("\n", s)
    s = de_splf_re.sub("\n", s)
    s = de_multlf_re.sub("\n", s)

    s = de_br_re.sub("\n", s)
    s = de_p_re.sub("\n\n", s)
    s = de_hr_re.sub("\n----------------------------------------\n", s)
    s = de_lfs_re.sub(r"\n<\1", s)

    s = de_script_re.sub("", s)

    s = de_html_re.sub("", s)                                   # remove all HTML tags

    s = decode_html_entities(s, nbsp_chr = ' ')

    s = s.replace(unicode("\x93", 'latin1'), '"')               # left  double quote
    s = s.replace(unicode("\x91", 'latin1'), '`')               # left  single quote
    s = s.replace(unicode("\x94", 'latin1'), '"')               # right double quote
    s = s.replace(unicode("\x92", 'latin1'), "'")               # right single quote
    s = s.replace(unicode("\x9c", 'latin1'), "oe")
    s = s.replace(unicode("\x96", 'latin1'), "-")               # n-dash

    s = s.replace(unicode("\x8b", 'latin1'), "<")
    s = s.replace(unicode("\x9b", 'latin1'), ">")
    s = s.replace(unicode("\x8c", 'latin1'), "OE")


    s = s.replace(unicode("\xa0", 'latin1'), ' ')               # non-break space
    s = s.replace(        "\x7f",            ' ')               # rubout

    s = s.replace(unicode("\xad", 'latin1'), "-")               # soft hyphen
    s = s.replace(unicode("\xaf", 'latin1'), "-")               # macron mark
    s = s.replace(unicode("\xab", 'latin1'), "<<")
    s = s.replace(unicode("\xbb", 'latin1'), ">>")

    s = de_tab_re.sub(" ", s)
    s = de_space_re.sub(" ", s)

    s = de_lf_re.sub("\n\n", s)
    s = de_lfsp_re.sub("\n", s)
    s = de_splf_re.sub("\n", s)

    return(s)




def string_pairs(a, skip = 1, connector_str = "\x80_Pr_") :
    """
        Return an array of strings composed of each sequential pair in the given array of strings.
    """
    if  False :

        t2  = [ 0 ] * (len(a) - skip)

        for i in xrange(len(t2)) :
            t2[i]   =   a[i] + connector_str + a[i + skip]
        pass

    else :
        t2          = [ a[i] + connector_str + a[i + skip] for i in xrange(len(a) - skip) ]

    return(t2)




def flat_positional_strings(strings, buckets = 3, ident_str = "\x80_Pf%u_%s") :
    """
        Given an array of strings, return an array of the strings with their positions in the array concatenated with them.
        For each string, there are two positions so that equal strings in similar positions in two arrays will yield at least one equal position string.
        The 'buckets' refers to how many sections of the array are used. Each identical string inside a particular bucket/section will yield at least one positional string that's the same.
            The first positional  string will identify the bucket the string is in.
            The second positional string will identify which pair of buckets the string is in and nearest.
        The 'ident_str' must contain a %u and a %s in that order.
            The %u will be filled in with the bucket or half-bucket number.
            The %s will be filled in with the string.
    """

    if  len(strings) == 0 :
        return( [] )


    pstrs   = [ 0 ] * (len(strings) * 2)


    def _fill(pi, ni, ne, n) :
        # print pi, ni, ne, n
        for i in xrange(ni, min(ne, len(strings))) :
            pstrs[pi]   = ident_str % ( n, strings[i] )
            pi         += 1

        return( ( pi, ne ) )

    d   = min((len(strings) + buckets - 1) / buckets, 2)
    d2  = (d + 1) / 2
    i   = pi = 0
    ni  = 0
    while ni < len(strings) :
        (pi, ni)    = _fill(pi, ni, ni + d2,  i)
        d2          = d
        i          += 1

    ni  = 0
    while ni < len(strings) :
        (pi, ni)    = _fill(pi, ni, ni + d2,  i)
        i          += 1

    return(pstrs)



phi = 1.618033988749894848204586834

def golden_smaller(v) :
    return(v * (1.0 / phi))


def golden_portrait_rectangle(w, h) :
    """ Given a width and hite, return the width and hite of a possibly-larger, golden-ratio-sized, portrait-aspect-ratio rectangle that encompasses the given one. """
    if  h   > w * phi :
        w   = h / phi
    else    :
        h   = w * phi
    return(w, h)


def golden_landscape_rectangle(w, h) :
    """ Given a width and hite, return the width and hite of a possibly-larger, golden-ratio-sized, landscape-aspect-ratio rectangle that encompasses the given one. """
    if  w   > h * phi :
        h   = w / phi
    else    :
        w   = h * phi
    return(w, h)


def golden_rectangle(w, h) :
    """ Given a width and hite, return the width and hite of a possibly-larger, golden-ratio-sized rectangle that encompasses the given one. """
    if  w < h   :
        return(golden_portrait_rectangle(w, h))
    return(golden_landscape_rectangle(w, h))




def log_positional_strings(strings, log_mult = 2.0, ident_str = "\x80_Pl_%u_%s") :
    """
        Given an array of strings, return an array of the strings with their positions in the array concatenated with them.
        For each string, create a string concatenated with the log of the position of the string in 'strings' multiplied by 'log_mult'.
        The 'ident_str' must contain a %u and a %s in that order.
            The %u will be filled in with the string's position in 'strings'
            The %s will be filled in with the string.
    """

    sa  = [ ident_str % ( int(math.log(i + 1) * log_mult), strings[i] ) for i in xrange(len(strings)) ]

    return(sa)



def lower_left_bit(n) :
    """ Make 0 the left-most 1 bit of the given number. E.g. 0b0100->0b0000 or 0b0101->0b0100 or 0b0111->0b0110 or 0b0110->0b0100. """
    return(n & (n - 1))


def raise_left_zero_bit(n) :
    """ Make 1 the left-most 0 bit of the given number. E.g. 0b0100->0b0101 or 0b0101->0b0111 or 0b0111->0b1111. """
    return(n | (n + 1))


def only_right_zero_bit(n) :
    """ Return a number with only the given number's right most 0 bit a 1. E.g. 0b1001->0b0010 or 0b0111->0b1000. """
    return(~n & (n + 1))

def raise_all_right_xero_bits(n) :
    """ Return the given number with all far right-side 0 bits set to 1.   E.g. 0b0100->0b0111   or 0x0101->0b0101. """
    return(n | (n - 1))


def bit_length(n) :
    """
        Return the bit number of the left-most bit in the given number.

        In the case of 0, return 0.

        Compatible with 2.7 and 3.1+ int.bit_length().

        Another approach is int(math.log(abs(n),2))+1
        Rounding might be a problem with really big numbers.
        No timing test done with either the log or a simple loop or this cute method.

    """
    if  not n:
        return(0)
    return(len(bin(abs(n))) - 2)


#
#   http://graphics.stanford.edu/~seander/bithacks.html#CountBitsSetTable
#
bit_count_table = [0] * 0x10000
for i in range(len(bit_count_table)) :
    bit_count_table[i]  = (i & 1) + bit_count_table[i >> 1]
del(i)

def _bit_count(v) :
    c   = 0
    while v :
        c  += (
                  bit_count_table[ v        & 0xffff]
                + bit_count_table[(v >> 16) & 0xffff]
                + bit_count_table[(v >> 32) & 0xffff]
                + bit_count_table[(v >> 48) & 0xffff]
              )
        v >>= 64
    return(c)

def _loop_bit_count(n) :
    """ Return the number of 1 bits in the given number. """
    c   = 0
    while n :
        n  &= (n - 1)
        c  += 1
    return(c)

bit_count   = _bit_count            # table lookup is twice as fast with lots of bits, can be a hair slower with values in 0..15



def un_gray_code(g) :
    """ Convert from grey code (gray code) back to binary """
    g ^= (g >>  1)
    g ^= (g >>  2)
    g ^= (g >>  4)
    g ^= (g >>  8)
    g ^= (g >> 16)
    g ^= (g >> 32)
    if  g   > 0x0fffFFFF :
        g  ^= (g >> 64)
        g  ^= (g >> 128)
        g  ^= (g >> 256)
        b   = 512
        while g >= (1 << b) :
            g  ^= (g >> b)
            b <<= 1
        pass
    return(g)
un_grey_code    = un_gray_code


def gray_code(n) :
    """ Convert a binary number to gray code. """
    return(n ^ (n >> 1))
grey_code       = gray_code


_balanced_8_bit_gray_code_table = [
                                    0x00, 0x01, 0x03, 0x02, 0x06, 0x0E, 0x0A, 0x0B, 0x09, 0x0D, 0x0F, 0x07, 0x05, 0x04, 0x0C, 0x08,
                                    0x18, 0x1C, 0x14, 0x15, 0x17, 0x1F, 0x3F, 0x37, 0x35, 0x34, 0x3C, 0x38, 0x28, 0x2C, 0x24, 0x25,
                                    0x27, 0x2F, 0x2D, 0x29, 0x39, 0x3D, 0x1D, 0x19, 0x1B, 0x3B, 0x2B, 0x2A, 0x3A, 0x1A, 0x1E, 0x16,
                                    0x36, 0x3E, 0x2E, 0x26, 0x22, 0x32, 0x12, 0x13, 0x33, 0x23, 0x21, 0x31, 0x11, 0x10, 0x30, 0x20,
                                    0x60, 0x70, 0x50, 0x51, 0x71, 0x61, 0x63, 0x73, 0x53, 0x52, 0x72, 0x62, 0x66, 0x6E, 0x7E, 0x76,
                                    0x56, 0x5E, 0x5A, 0x7A, 0x6A, 0x6B, 0xEB, 0xEA, 0xFA, 0xDA, 0xDE, 0xD6, 0xF6, 0xFE, 0xEE, 0xE6,
                                    0xE2, 0xF2, 0xD2, 0xD3, 0xF3, 0xE3, 0xE1, 0xF1, 0xD1, 0xD0, 0xF0, 0xE0, 0xA0, 0xB0, 0x90, 0x91,
                                    0xB1, 0xA1, 0xA3, 0xB3, 0x93, 0x92, 0xB2, 0xA2, 0xA6, 0xAE, 0xBE, 0xB6, 0x96, 0x9E, 0x9A, 0xBA,
                                    0xAA, 0xAB, 0xBB, 0x9B, 0x99, 0x9D, 0xDD, 0xD9, 0xDB, 0xFB, 0x7B, 0x5B, 0x59, 0x5D, 0x7D, 0x79,
                                    0xF9, 0xFD, 0xBD, 0xB9, 0xA9, 0xE9, 0x69, 0x6D, 0x6F, 0x67, 0x65, 0x64, 0xE4, 0xE5, 0xE7, 0xEF,
                                    0xED, 0xAD, 0xAF, 0xA7, 0xA5, 0xA4, 0xAC, 0xEC, 0x6C, 0x68, 0xE8, 0xA8, 0xB8, 0xF8, 0x78, 0x7C,
                                    0xFC, 0xBC, 0xB4, 0xB5, 0xB7, 0xF7, 0xF5, 0xF4, 0x74, 0x75, 0x77, 0x7F, 0xFF, 0xBF, 0x9F, 0xDF,
                                    0x5F, 0x57, 0x55, 0x54, 0xD4, 0xD5, 0xD7, 0x97, 0x95, 0x94, 0x9C, 0xDC, 0x5C, 0x58, 0xD8, 0x98,
                                    0x88, 0xC8, 0x48, 0x4C, 0xCC, 0x8C, 0x84, 0xC4, 0x44, 0x45, 0xC5, 0x85, 0x87, 0xC7, 0x47, 0x4F,
                                    0xCF, 0x8F, 0x8D, 0xCD, 0x4D, 0x49, 0xC9, 0x89, 0x8B, 0xCB, 0x4B, 0x4A, 0xCA, 0x8A, 0x8E, 0xCE,
                                    0x4E, 0x46, 0xC6, 0x86, 0x82, 0xC2, 0x42, 0x43, 0xC3, 0x83, 0x81, 0xC1, 0x41, 0x40, 0xC0, 0x80,
                                  ]

def balanced_8_bit_gray_code(n) :
    """ Return a balanced gray code for the given number 0..255. """
    return(_balanced_8_bit_gray_code_table[n])


_balanced_8_bit_un_gray_code_table  = [ 0 ] * 256
for i in xrange(len(_balanced_8_bit_un_gray_code_table)) :
    _balanced_8_bit_un_gray_code_table[_balanced_8_bit_gray_code_table[i]]  = i
del(i)

def balanced_8_bit_un_gray_code(g) :
    return(_balanced_8_bit_un_gray_code_table[g])





def de_bruijn(alphabet_or_number_of_symbols, n):
    """
        Get a De Bruijn sequence for subsequences of length 'n' taken from 'alphabet'.

        The returned value contains all possible unique sequences of length 'n'
        of values from 'alphabet'.

        Rememeber that to get all sequences, you must wrap around such that the last sequence
        will start with the last item in the returned value.

        Return a string if given 'alphabet' as a string. Otherwise, return a list.

        Code is modified from https://en.wikipedia.org/wiki/De_Bruijn_sequence

    """

    try:
        alphabet    = range(int(alphabet_or_number_of_symbols))     # make a list if given a symbol count
    except ( ValueError, TypeError, ) :
        alphabet    = alphabet_or_number_of_symbols                 # otherwise

    k           = len(alphabet)
    a           = [0] * k * n
    sequence    = []


    def db(t, p) :
        if t > n :
            if n % p == 0 :
                sequence.extend(a[1:p + 1])
            pass
        else            :
            a[t]        = a[t - p]
            db(t + 1, p)
            for j in xrange(a[t - p] + 1, k) :
                a[t]    = j
                db(t + 1, t)
            pass
        pass


    db(1, 1)
    if  isinstance(alphabet_or_number_of_symbols, basestring) :
        sequence    = "".join(alphabet[i] for i in sequence)

    return(sequence)




#
#
#   From Wikipedia      http://en.wikipedia.org/wiki/Hilbert_curve
#
#

def _sqhilbert_rot(n, x, y, rx, ry) :
    """ Rotate the situation. """
    if  not ry :
        if  rx == 1 :
            x = n - 1 - x
            y = n - 1 - y
        x, y    = y, x
    return(x, y)


def square_hilbert_xy_to_i(n, x, y) :
    """
        Convert a 2D location in a square to the appropriate location on a Hilbert curve.

        n   is the width/hite - must be a power of 2.
        x   is the current X location.
        y   is the current Y location.

        The curve will go from upper left to upper right, assuming X increases to the right and Y increases going down.

        Returns a new curve index [0 ... (max(x) + 1) * (max(y) + 1)).
    """
    i   = 0
    s   = n / 2
    while s > 0 :
        rx      = ((x & s) > 0)
        ry      = ((y & s) > 0)
        i      += s * s * ((3 * rx) ^ ry)
        x, y    = _sqhilbert_rot(s, x, y, rx, ry)
        s      /= 2
    return(i)


def square_hilbert_i_to_xy(n, i)  :
    """
        Convert a location on a Hilbert curve to a 2D location on a square.

        n   is the width/hite - must be a power of 2.
        i   is the index/location on the Hilbert curve.  [0 ... n * n)

        The curve will go from upper left to upper right, assuming X increases to the right and Y increases going down.

        Returns the X and Y location.

    """
    x   = 0
    y   = 0
    s   = 1
    while s < n :
        rx      = 1 & (i/2)
        ry      = 1 & (i ^ rx)
        x, y    = _sqhilbert_rot(s, x, y, rx, ry)
        x      += s * rx
        y      += s * ry
        i      /= 4
        s      *= 2
    return(x, y)




def linear_regression(ax = None, ay = None):
    """
        Given an array of ax and ay values,
        return the values that make a linear regression line,
        (m * ax[i]) + a = ay[i]
    """

    ay  = ay or []

    if  not ax :
        ax  = range(len(ay))

    if  (not isinstance(ax, ListType)) and (not isinstance(ax, TupleType)) :
        ax  = [ x + ax for x in xrange(len(ay)) ]

    if  len(ax) != len(ay) :
        raise ValueError('Different length of ax and ay array')

    sx      = sy    =   sxx =   syy =   sxy =   0.0
    c       = 0
    for i   in xrange(len(ax)) :
        x   = ax[i]
        y   = ay[i]
        if  (x != None) and (y != None) :
            c  += 1
            sx  = sx + x
            sy  = sy + y

            sxx = sxx + (x * x)
            syy = syy + (y * y)
            sxy = sxy + (x * y)
        pass

    d       =  (sxx *  c) - (sx * sx)

    if  not d :
        raise ValueError('Vertical line')
        m   = sum(ay + [ 0.0 ]) / (len(ay) or 1.0)      # special case a vertical line for no real reason other than to stop the crash
        a   = 0.0
    else    :
        m   = ((sxy *  c) - (sy * sx )) / d
        a   = ((sxx * sy) - (sx * sxy)) / d

    return( ( m, a ) )



def torus_distance(a, b, w) :
    """
        How far apart are a and b on a torus (a loop, really) of width w?

        Returns a value from [0 to w / 2).

    """
    w2  = w / 2
    return(abs((((a - b) + w2) % w) - w2))






def y_from_distance_direction(dist, direction) :
    """
        Get the Y value from a distance and a direction (direction is -pi..pi, where both pi's are at y<0:x=0 and 0 direction is y=0:x>=0)
    """

    return(dist * math.sin(direction))


def x_from_distance_direction(dist, direction) :
    """
        Get the X value from a distance and a direction (direction is -pi..pi, where both pi's are at y<0:x=0 and 0 direction is y=0:x>=0)
    """

    return(dist * math.cos(direction))


def distance_from_x_y(x, y, z = None) :
    """
        Get the distance from an X and Y value.
        This routine is here for documentation purposes, folks.
    """
    if  z != None :
        return(math.sqrt((x * x) + (y * y) + (z * z)))
    return(math.hypot(y, x))


def direction_from_x_y(x, y) :
    """
        Get the direction from an X and Y value.
        This routine is here for documentation purposes, folks.
    """

    return(math.atan2(y, x))


def compass_angle(radians) :
    """ Return the compass angle of the given angle. 0..360. And 0 is north. """
    return((math.degrees(-(radians - (math.pi / 2.0))) + 720.0) % 360.0)



p2  = math.pi * 2.0

def radian_angle_difference(a, b) :
    """
        What's the angle between these two angles (in radians. that is, += 0..pi - to get degrees, math.degrees(a))?
    """
    return((((a - b) + math.pi) % p2) - math.pi)        # 12% quicker, ballpark, than the original code

    #
    #   Original code: closer than 0.00000000000001 to the above.
    #
    #   Slower is:  math.atan2(math.sin(a - b), math.cos(a - b))
    #
    a       = (a - b) % p2

    if  a   >  math.pi :
        a  -=  p2

    if  a   < -math.pi :
        a  +=  p2

    return(a)


def radian_angle_from_horizontal(a) :
    """ Return the absolute angle the given angle is from horizontal. """
    a  %= math.pi
    return(min(abs(a), abs(math.pi - a)))



def angle_from_triangle_sides(side1, side2, opp_side) :
    """ Given 3 side lengths of a triangle, return the angle between the first two sides. """
    side1       = float(side1)
    side2       = float(side2)
    opp_side    = float(opp_side)
    return(math.acos((side1*side1 + side2*side2 - opp_side*opp_side) / (2 * side1 * side2)))


def rite_triangle_hite_from_angle_and_hypotenuse(a, hypot) :
    """ Return one of the sides of a right triangle, given an angle and hypotenuse. """
    return(hypot * math.sin(a))                             # watch out for extreme angles - loss of precision situation


def area_of_triangle_given_sides(a, b, c) :
    """ Return the area of a triangle given the lengths of the 3 sides. """
    p   = (a + b + c) / 2.0
    return(math.sqrt(p * (p - a) * (p - b) * (p -c)))       # Heron's formula


def average_angle(radian_angles) :
    """
        Return the average angles of the given radian angles. Return value is [0..2*pi).

        Note: This routine won't necessarily return the simple
        average of some angles even though they are all within
        180 degrees of each other. The idea is that the space
        angles reside in isn't really linear with respect to the
        angle, itself.

    """
    if  radian_angles is None :
        return(None)
    if  not len(radian_angles) :
        return(0.0)
    y   = sum([ math.sin(a) for a in radian_angles ]) / float(len(radian_angles))
    x   = sum([ math.cos(a) for a in radian_angles ]) / float(len(radian_angles))
    if  abs(y) < 0.00000000001 :
        y   = 0.0                                                       # this keeps us from figuring the angle of a very, very, very short vector, instead of calling it 0 degrees
    if  abs(x) < 0.00000000001 :
        x   = 0.0
    return(math.atan2(y, x) % p2)


def average_modulo(numbers, modulo) :
    """
        Return the average of the given numbers modulo the modulo.

        See the note in average_angle() for why the average of these numbers isn't the straight average of the numbers.
        Modulo space implies a world that's not linear.

    """
    if  (numbers is None) or (modulo is None) :
        return(None)

    modulo  = abs(float(modulo))
    numbers = [ (p2 * ((n % modulo) / modulo)) for n in numbers ]
    a       = average_angle(numbers)
    return(modulo * a / p2)



#
#
#   Notes from:
#       http://www.wikihow.com/Calculate-the-Area-of-a-Polygon
#
#       Going clockwise, the area is negated, which can be used to "identify a cyclic path or sequence of a set of points forming a polygon".
#       "If you use it on a shape where two of the lines cross like a figure eight, you will get the area surrounded counterclockwise minus the area surrounded clockwise."
#
#
def area_of_irregular_polygon(counter_clockwise_vertices) :
    """ Give a list of corners [ [ x, y ] ... ] in counter clockwise order, return the area of the polygon they describe. """
    if  len(counter_clockwise_vertices) <= 1 :
        return(0.0)

    va  = list(counter_clockwise_vertices)
    va.append(counter_clockwise_vertices[0])

    psm = sum([ va[vi][0] * va[vi + 1][1] for vi in xrange(len(va) - 1) ])
    nsm = sum([ va[vi][1] * va[vi + 1][0] for vi in xrange(len(va) - 1) ])
    return((psm - nsm) / 2.0)




def poly_from_xy_list(xyl) :
    """ Given a list list of XY values in X, Y, X, Y, ... form, return a list of [ X, Y, ], [ X, Y, ] ... """
    return([ [ xyl[i], xyl[i + 1], ] for i in xrange(0, len(xyl), 2) ])


#
#
#       Notes:
#           Look for Weiler-Atherton clipping algorithm.
#
#           Also:
#               http://math.stackexchange.com/questions/141798/two-quadrilaterals-intersection-area-special-case
#               http://www.cplusplus.com/forum/lounge/30271/
#               http://sourceforge.net/projects/polyclipping/
#
#
def clip_polygon(subjectPolygon, clipPolygon) :
    """
        Finds the intersection of two polygons using Sutherland-Hodgman algorithm.

        The polygons are in [ X, Y, ], [ X, Y, ] ... form. Untested whether both clockwise and counter-clockwise winding work.

        From    http://rosettacode.org/wiki/Sutherland-Hodgman_polygon_clipping

        Modified to return the list in the winding order of subjectPolygon

        Clip rectangle seems to need to be a rectangle - maybe even orthogonal. Jury is out on the latter, but sensing clip vertices inside subject using point_in_polygon() finds overlap where there was none from this routine..

    """

    if  (area_of_irregular_polygon(subjectPolygon) < 0) != (area_of_irregular_polygon(clipPolygon) < 0) :       # if the winding orders are different, reverse the clipPolygon.  http://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order
        clipPolygon = list(clipPolygon)
        clipPolygon.reverse()

    def inside(p) :
        return((cp2[0]-cp1[0])*(p[1]-cp1[1]) > (cp2[1]-cp1[1])*(p[0]-cp1[0]))

    def computeIntersection() :
        dc = [ cp1[0] - cp2[0],  cp1[1] - cp2[1] ]
        dp = [   s[0] -   e[0],    s[1] -   e[1] ]
        n1 =   cp1[0] * cp2[1] - cp1[1] * cp2[0]
        n2 =     s[0] *   e[1] -   s[1] *   e[0]
        n3 =   1.0 / ((dc[0] * dp[1]) - (dc[1] * dp[0]))
        return([(n1*dp[0] - n2*dc[0]) * n3, (n1*dp[1] - n2*dc[1]) * n3])

    outputList  = subjectPolygon
    cp1         = clipPolygon[-1]

    for clipVertex in clipPolygon :
        if  not len(outputList) :
            break

        cp2         = clipVertex
        inputList   = outputList
        outputList  = []
        s           = inputList[-1]

        for subjectVertex in inputList :
            e   = subjectVertex
            if  inside(e) :
                if not inside(s) :
                    outputList.append(computeIntersection())
                outputList.append(e)
            elif inside(s) :
                outputList.append(computeIntersection())
            s   = e
        cp1     = cp2

    return(outputList)



class   a_point(object) :
    def __init__(me, x, y) :
        me.x        = x
        me.y        = y
    def rotate(me) :
        """ Rotate the point 90 degrees counter-clockwise around 0,0. """
        me.x, me.y  = -me.y, me.x
    def __str__(me) :
        return("%f:%f" % ( me.x, me.y, ))
    #   a_point


#
#   Some thought should be given to the code at http://totologic.blogspot.fr/2014/01/accurate-point-in-triangle-test.html
#
def point_in_polygon(poly, p) :
    """
        Given a list of a_point() vertices of a polygon, and an a_point() 'p' , return True if the point is inside the polygon.

        Points on left/top are inside. Points on right/bottom edges are outside.
        But when the edges are at angles, return values can be not what one might expect - or want.

    """
    mnx     = poly[0].x
    mxx     = poly[0].x
    mny     = poly[0].y
    mxy     = poly[0].y
    for v  in poly[1:] :
        mnx = min(v.x, mnx)
        mxx = max(v.x, mxx)
        mny = min(v.y, mny)
        mxy = max(v.y, mxy)

    if  not ((mnx <= p.x < mxx) and (mny <= p.y < mxy)) :         # note: allow high on the line to be inside
        return(False)

    inside  = False
    j       = len(poly) - 1
    i       = 0
    while i < len(poly) :
        # if  (poly[i].x == p.x) and (poly[i].y == p.y) :
        #     return(True)                # on a vertex
        if  poly[i].y == poly[j].y :
            return((poly[i].x <= p.x < poly[j].x) or (poly[j].x < p.x <= poly[i].x))  # on a horizontal line
        if  (poly[i].x == p.x) and (poly[j].x == p.x) and ((poly[i].y <= p.y < poly[j].y) or (poly[j].y <= p.y < poly[i].y)) :
            return(True)                # on a vertical line
        if  (
                ((poly[i].y > p.y ) != (poly[j].y > p.y))
             and
                (p.x < poly[i].x + ((p.y - poly[i].y) * ((poly[j].x - poly[i].x) / float(poly[j].y - poly[i].y))))
            ) :
            inside  = not inside
        j   = i
        i  += 1

    return(inside)



def point_on_line(xy, xyxy, fudge = None) :
    """ Is the given (x, y) on infinite ( (x1,y1), (x2,y2) ) or finite line if 'fudge' is non-None? """

    x   = xy[0]
    y   = xy[1]

    x1  = xyxy[0][0]
    y1  = xyxy[0][1]
    x2  = xyxy[1][0]
    y2  = xyxy[1][1]

    if  fudge != None :
        if  (    False
             or (not (min(x1, x2) - fudge <= x <= max(x1, x2) + fudge))
             or (not (min(y1, y2) - fudge <= y <= max(y1, y2) + fudge))
            ) :

            return(False)

        pass

    if  x2 == x1 :                                              # special case vertical line
        return(abs(x - x1) <= (fudge or 0.0))

    sl  = float(y2 - y1) / float(x2 - x1)
    zy  = y1 - (sl * x1)

    return(abs((sl * x) + zy - y) <= (fudge or 0.0))

#
#   From:       http://www.topcoder.com/tc?module=Static&d1=tutorials&d2=geometry2
#   See also:   http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
#   And:        http://en.wikipedia.org/wiki/Bentley%E2%80%93Ottmann_algorithm
#   And         http://www.pygame.org/wiki/IntersectingLineDetection
#
def convert_two_points_to_ABC(x1, y1, x2, y2) :
    """ Find the values of ABC in "A*x1 + B*y1 = C" given two points. """

    A   = float(y2 - y1)
    B   = float(x1 - x2)
    C   = float((A * x1) + (B * y1))

    return(A, B, C)


def get_line_intersection(xy1, xy2, fudge = None) :
    """
        Find the intersection point between two lines. Return (None,None) if lines are parallel.

        If 'fudge' is non-None, then do strict comparison (subject to 'fudge' slop).
           That is, the intersection must be between the points
           on the lines that go from point to point, not-infinite length.
           And, if the lines are parallel find an intersection point
                if the lines overlap, 'fudge' logic accounted for.
    """

    ( A1, B1, C1 )  = convert_two_points_to_ABC(xy1[0][0], xy1[0][1], xy1[1][0], xy1[1][1])
    ( A2, B2, C2 )  = convert_two_points_to_ABC(xy2[0][0], xy2[0][1], xy2[1][0], xy2[1][1])
    det             = (A1 * B2) - (A2 * B1)
    if  not det     :
        if  point_on_line(xy1[0], xy2, fudge) : return(float(xy1[0][0]), float(xy1[0][1]))
        if  point_on_line(xy1[1], xy2, fudge) : return(float(xy1[1][0]), float(xy1[1][1]))
        if  point_on_line(xy2[0], xy1, fudge) : return(float(xy2[0][0]), float(xy2[0][1]))
        if  point_on_line(xy2[1], xy1, fudge) : return(float(xy2[1][0]), float(xy2[1][1]))

        return(None, None)

    x               = ((B2 * C1) - (B1 * C2)) / det
    y               = ((A1 * C2) - (A2 * C1)) / det

    if  fudge != None :
        if  (    False
             or (not (min(xy1[0][0], xy1[1][0]) - fudge <= x <= max(xy1[0][0], xy1[1][0]) + fudge))
             or (not (min(xy1[0][1], xy1[1][1]) - fudge <= y <= max(xy1[0][1], xy1[1][1]) + fudge))
             or (not (min(xy2[0][0], xy2[1][0]) - fudge <= x <= max(xy2[0][0], xy2[1][0]) + fudge))
             or (not (min(xy2[0][1], xy2[1][1]) - fudge <= y <= max(xy2[0][1], xy2[1][1]) + fudge))
            ) :

            return(None, None)

        pass

    return(x, y)



#
#   From http://www.bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
#
def _ccw(A,B,C):
    return((C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0]))

def do_line_segments_intersect(xy1, xy2):
    """ Return True if these line segments intersect. """
    return((_ccw(xy1[0], xy2[0], xy2[1]) != _ccw(xy1[1], xy2[0], xy2[1])) and (_ccw(xy1[0], xy1[1], xy2[0]) != _ccw(xy1[0], xy1[1], xy2[1])))




def apply_gravity(position = 0.0, speed = 0.0, gravity = 1.0, delta_time = 1.0) :
    """ Move an accelerated position by applying 'gravity' to its position and speed. From: http://www.niksula.hut.fi/~hkankaan/Homepages/gravity.html """
    d           = (gravity  * delta_time / 2.0)
    speed       = speed     + d
    position    = position  + (speed * delta_time)
    speed       = speed     + d

    return(position, speed)



def make_color_gradient(freq1, freq2, freq3, phase1, phase2, phase3, center = 128, width = 127, count = 256) :
    """ Return an array of colors that go around the wheel so that all neighboring colors are close to each other, as are the two end colors. """
    colors  = []
    for i in xrange(count) :
        red = int(math.sin(freq1 * i + phase1) * width + center)
        grn = int(math.sin(freq2 * i + phase2) * width + center)
        blu = int(math.sin(freq3 * i + phase3) * width + center)
        colors.append(( red, grn, blu ))
    return(colors)
make_color_gradiant = make_color_gradient


def make_color_wheel(count = 256) :
    """ Make a color wheel with the given number of colors. """
    count   = int(count)
    freq    = 2 * math.pi / count
    return(make_color_gradient(freq, freq, freq, 0.0, 2 * math.pi / 3, 4 * math.pi / 3, count = count))




def safe_relpath(fn) :
    """
        os.path.relpath(), returning the given file name if there is a problem with it (if it's "" or None).
    """

    try :
        fn  = os.path.relpath(fn)
    except ValueError :                                 # happens if the file name is "" or None
        pass
    return(fn)



def same_file(f1, f2) :
    """
        Are these the same files?
    """

    try :
        return(os.path.samefile(f1, f2))

    except ( AttributeError, OSError, IOError ) :               # attrib? samefile() does not exist under Unix. OS/IO? File doesn't exist.
        f1  = os.path.abspath(f1)
        f2  = os.path.abspath(f2)
        if  f1 == f2 :
            return(True)
        pass

    return(False)




def _read_whole_file(fname, how = "t", how_many = None) :
    """ Read a whole file. """

    fi      = open(fname, "r" + how)
    if  how_many is None :
        fs  = fi.read()
    else    :
        fs  = fi.read(how_many)
    fi.close()

    return(fs)


def read_whole_text_file(fname, how_many = None) :
    """ Read a whole text file. """

    return(_read_whole_file(fname, how = "t", how_many = how_many))


def read_whole_binary_file(fname, how_many = None) :
    """ Read a whole binary file. """

    return(_read_whole_file(fname, how = "b", how_many = how_many))


def _safe_read_whole_file(fn, rtn) :
    try :
        return(rtn(fn))
    except ( OSError, IOError ) :
        pass
    return(None)

def safe_read_whole_text_file(fn)   :
    return(_safe_read_whole_file(fn, read_whole_text_file))

def safe_read_whole_binary_file(fn) :
    return(_safe_read_whole_file(fn, read_whole_binary_file))



def _write_whole_file(fname, how, s) :
    """ Write a whole file. """

    if  isinstance(s, UnicodeType) :
        s   = unicode_byte_string(s)

    fi  = open(fname, "w" + how)
    fi.write(s)
    fi.close()

    del(fi)



def write_whole_text_file(fname, s) :
    """ Write a whole text file. """

    if  isinstance(s, UnicodeType) :
        s   = s.encode('utf-8')

    return(_write_whole_file(fname, "t", s))


def write_whole_binary_file(fname, s) :
    """ Write a whole binary file. """

    return(_write_whole_file(fname, "b", s))



def _safe_write_whole_file(fn, fd, rtn) :
    try :
        import  replace_file
    except ImportError  :
        replace_file    = None

    tfn = fn + ".tmp"
    try :
        rtn(tfn, fd)
    except ( OSError, IOError ) :
        return(False)

    bfn = fn + ".bak"
    if  replace_file  and None :
        try :
            replace_file.replace_file(fn, tfn, bfn)
        except ( OSError, IOError ) :
            return(False)
        pass
    else    :
        try :
            if  os.path.exists(bfn) :
                os.unlink(bfn)
            if  os.path.exists(fn)   :
                os.rename(fn, bfn)
            os.rename(tfn, fn)
        except ( OSError, IOError ) :
            return(False)
        pass

    return(True)

def safe_write_whole_text_file(fn, fd) :
    return(_safe_write_whole_file(fn, fd, write_whole_text_file))

def safe_write_whole_binary_file(fn, fd) :
    return(_safe_write_whole_file(fn, fd, write_whole_binary_file))



def safe_file_datetime(fn) :
    """ Get the given file's date/time or None. """
    try :
        t   = os.path.getmtime(fn)
    except ( OSError, IOError, ValueError ) :
        t   = None
    return(t)



def whack_file(fn) :
    """ Safely make sure the given file is no longer with us. Return True if file existed and was successfully unlinked. """

    try :
        os.unlink(fn)               # note: unlink, not remove, so symlinks get whacked instead of their target
        return(True)
    except ( OSError, IOError ) :
        pass
    return(False)


def whack_dir(dn) :
    """ Safely make sure the given empty directory is no longer with us. Return True if dir existed and was successfully removed. """

    if  whack_file(dn) :
        return(True)

    try :
        os.rmdir(dn)
        return(True)
    except ( OSError, IOError ) :
        pass
    return(False)


WHACK_DIR_TMP_DIR_NAME  = "tmpd2del.tmp"                        #: temporary name to rename a directory we want to whack to


def whack_full_dir(dn, tmp_dir_base_name = None) :
    """ Safely fully make sure the given symlink or directory is no longer with us. Return True if dir existed and was successfully removed. """

    if  (not dn) or dn.endswith(os.path.normpath("/")) :
        return(False)                                           # don't wipe the poor machine when there's a bug if we can help it

    if  whack_dir(dn) :
        return(True)

    tdn = os.path.join(os.path.dirname(os.path.abspath(dn)), os.path.basename(tmp_dir_base_name or WHACK_DIR_TMP_DIR_NAME))
    if  tdn != dn :
        whack_full_dir(tdn)                                     # get rid of any lagacy staging directory we'll rename to before whacking the dir we want to whack
        try :
            os.rename(dn, tdn)
            dn  = tdn
        except ( OSError, IOError ) :
            pass
        pass

    if  not os.path.exists(dn) :
        return(False)                                           # note: I really wonder whether this thing with returning False if the dir (and file in whack_file) did not exist is the right thing to do.

    shutil.rmtree(dn, ignore_errors = True)                     # get rid of whatever is get-riddable

    if  os.path.exists(dn) :
        try :
            shutil.rmtree(dn)                                   # otherwise, try again, but this time we'll excaption out and return False
        except ( OSError, IOError ) :
            return(False)
        pass

    return(True)


def whack_dir_contents(dn) :
    """ Safely make sure the contents of a given directory is no longer with us. Return True if dir existed and was successfully removed. """
    if  whack_file(dn) :            # in case it's just a file or a symlink
        return(True)

    retval      = os.path.isdir(dn)
    for fn     in glob.glob(os.path.join(dn, '*')) :
        retval |= whack_full_dir(fn)                    # make this thing go away
    return(retval)



def elapsed_time() :
    """ Return a running clock value based on some arbitrary "zero". """

    if  sys.platform == 'win32' :
        return(time.clock())        # as an alternate: win32api.GetTickCount()

    #       Mac could use MacOS.GetTicks() / 60.0, I suppose.

    return(os.times()[4])           # under windows this value stays at zero


def wdhms_str(t, weeks = False) :
    """ Return a string that represents the shortest weeks:days:hours:minutes:seconds.fraction for the given time. """

    def _nxt(s, t, d, fm = '%02u:') :
        tt  = t / d
        if  tt or s :
            s  += (fm % tt)
        return(s, t - (int(tt) * d))

    t               = float(t)
    s               = ""
    if  weeks       :
        ( s, t )    = _nxt(s, t, 60 * 60 * 24 * 7, fm = "%u:"   )
    ( s, t )        = _nxt(s, t, 60 * 60 * 24    , fm = "%1u:"  )
    ( s, t )        = _nxt(s, t, 60 * 60                        )
    ( s, t )        = _nxt(s, t, 60                             )
    if  t          == int(t)  :
        ( s, t )    = _nxt(s, t, 1               , fm = "%02u"  )
    else            :
        ( s, t )    = _nxt(s, t, 1               , fm = "%09.6f")

    s               = re.sub(r"^[0\:]+", "", s)
    s               = re.sub(r"[0\.]+$", "", s)
    if  s.endswith(':') :
        s          += "00"
    if  re.search(r":\d$", s) :
        s          += "0"

    return(s)




def same_time_ish(now, then, yday = None, same_day_hours = 14, diff_day_hours = 8) :
    """ Is Unix time 'then' likely to be the same "day" - session as 'now' in localtime? """

    yday    = yday or time.localtime(now).tm_yday
    d       = ((time.localtime(then).tm_yday == yday) and same_day_hours) or diff_day_hours             # same local day of year, allow the times to be 14 hours away from each other. Different days: must be within 8 hours of each other.
    d      *= 60 * 60                                                                                   # convert to seconds

    return(abs(now - then) <= d)







def get_ini_or_cfg_file_name(base_name, app_name = None) :
    """ Return a file name of config_directory/base_name.ini or .cfg, appropriate to the OS. And make the config directory for the app. """

    base_name       = base_name or "tzlibpy"
    app_name        = "." + os.path.splitext(os.path.basename(app_name or base_name))[0]

    if  sys.platform   == 'win32' :
        app_path        = os.path.join("C:\\", app_name)
        if  os.path.expandvars("${homedrive}") and os.path.expandvars("${homepath}") :
            app_path    = os.path.normpath(os.path.join(os.path.expandvars("${homedrive}${homepath}"), app_name))   # on modern machines this is C: and \Users\USER_NAME - on XP it's C: and \Documents and Settings\USER_NAME
        if  os.path.expandvars("${userprofile}") :
            app_path    = os.path.normpath(os.path.join(os.path.expandvars("${userprofile}"),          app_name))   # same thing by a different, single name
        if  not os.path.isdir(app_path) :
            os.makedirs(app_path)
        return(os.path.join(app_path, base_name + ".ini"))

    app_path    = os.path.join(os.path.expanduser("~"), app_name)
    if  not os.path.isdir(app_path) :
        os.makedirs(app_path)

    return(os.path.join(app_path, base_name + ".ini"))



def temp_file_name(base_name = None, app_name = None, ext = None) :
    ext = ext or ".tmp"

    if  (not app_name) or (not base_name) :
        td  =       os.environ.get("TEMP", None)
        td  = td or os.environ.get("TMP", None)
        td  = td or "."
        fn  = os.path.join(td, "tmp_tzlibpy" + ext)
    else :
        fn  = get_ini_or_cfg_file_name(base_name, app_name)

    while True :
        rs  = "_%08x" % ( random.randint(0, 2000000000) )
        rfn = os.path.splitext(fn)[0] + rs + ext
        if  not os.path.isfile(rfn) :
            break
        pass

    return(rfn)




def s_except_1(v) :
    """ Return an "s" if the 'v' is not 1. """

    if  isinstance(v, (TupleType, ListType, DictionaryType ) ) :
        v   = len(v)

    if  v != 1 :
        return("s")
    return("")





def same_object(o1, o2) :
    """ Return whether these two things are the same, exact thing (in memory). """

    return(id(o1) == id(o2))



def sys_err_file_line(sys_exc_info_2 = None) :
    """ Return a simple, one-line string with the bottom line about where the latest except failure has been. """

    sys_exc_info_2  = sys_exc_info_2 or sys.exc_info()[2]

    lns = traceback.format_tb(sys_exc_info_2)[-1].strip()
    lns = re.sub(r"[\r\n]+", " ---- ", lns)

    return(lns)



def bool_to_0_or_1(b) :
    """ Return 0 or 1 depending upon the given bool's value. """

    return((b or 0) and 1)



def excel_column_name(c) :
    if  c < 0 :
        raise ValueError("%d<0"   % c)
    if  c >= 26 * 27 :
        raise ValueError("%d>max" % c)

    cc  = chr(ord('a') + c % 26)
    if  c >= 26 :
        cc  = chr(ord('a') + (c / 26) - 1) + cc

    return(cc)



def find_upper_dir(to_find_dir, our_dir = None) :
    our_dir = our_dir or "."
    our_dir = os.path.abspath(our_dir)

    sd      = our_dir
    while sd and (not sd.endswith(os.path.normpath("/"))) :
        ( p, dn )   = os.path.split(sd)
        if  dn     == to_find_dir :
            return(sd)

        if  not dn  :
            sd      = ""
            break
        sd          = p

    sd      = our_dir
    while sd and (not sd.endswith(os.path.normpath("/"))) :
        p           = os.path.join(sd, to_find_dir)
        if  os.path.isdir(p) :
            return(p)

        sd          = os.path.split(sd)[0]

    return("")



def find_upper_file_or_dir(to_find, our_dir = None) :
    our_dir         = our_dir or "."
    our_dir         = os.path.abspath(our_dir)
    to_find         = os.path.normpath(to_find)

    sd              = our_dir
    while sd        :
        p           = os.path.join(sd, to_find)
        if  os.path.exists(p) :
            return(p)

        if  sd.endswith(os.path.normpath("/")) :
            break

        sd          = os.path.split(sd)[0]

    return("")





def file_signature(file_name)    :
    """ Return the CRC of the file's name, size and date/time. """

    return(blkcrc32(INITIAL_CRC32_VALUE, file_name + str(os.path.getsize(file_name)) + str(os.path.getmtime(file_name))))






def unpickle_file(fn) :
    fd  = safe_read_whole_binary_file(fn)
    if  fd != None :
        try :

            return(cPickle.loads(fd))

        except ( cPickle.PickleError, TypeError, AttributeError, EOFError, ImportError, IndexError, ) :         # among other errors
            pass
        except :
            pass
        pass

    return(None)


def pickle_file(fn, o, proto = 0)  :
    try :
        fd  = cPickle.dumps(o, protocol = min(cPickle.HIGHEST_PROTOCOL, max(0, proto or 0)))
    except ( cPickle.PickleError, TypeError, AttributeError, ) :
        return(False)

    return(safe_write_whole_binary_file(fn, fd))





#
#   Or to make outside packages, like ReportLab, stop fussing (unless multiprocessing is the order of the day):
#
#       import warnings
#
#       with warnings.catch_warnings() :
#           warnings.filterwarnings("ignore", category = DeprecationWarning)
#           from    PIL import Image
#
#
def pil_tostring(img) :
    """ Sigh. """
    return(getattr(img, 'tobytes',   getattr(img, 'tostring'))())
def pil_fromstring(img) :
    """ Sigh. """
    return(getattr(img, 'frombytes', getattr(img, 'fromstring')))


class   a_pickleable_pil_image(object) :
    def __init__(me, img) :
        me.mode = img.mode
        me.size = img.size
        me.s    = pil_tostring(img)
    #   a_pickleable_pil_image



def best_w_h_fit_scale(to_w, to_h, from_w, from_h) :
    """ Return a scale factor that will make a "from_" image fit tightly in a "to_" image preserving the aspect ratio. """
    return(min(to_w / float(from_w), to_h / float(from_h)))


def best_line_fit(x, w, mn, mx) :
    """ Return an integer X value that is greater than or equal to mn, w less than mx if possible, and is as close as possible to x - int(w)/2. So that a w long line from x fits inside mn and mx and includes x, if possible. """
    x   = int(x)
    w   = int(w)
    mn  = int(mn)
    mx  = int(mx)
    v   = max(mn, x - (w / 2))
    v   = min(v, min(mx, v + w) - w)
    v   = max(mn, v)                # if the line doesn't fit (or not mn <= x < mx), return mn.
    return(v)




def base_36_encode(number, alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') :
    '''
        Convert positive integer to a base36 string.
        Modified: http://en.wikipedia.org/wiki/Base_36
    '''


    if  not isinstance(number, (int, long)) :
        number  = int(number)                       # let the chips fall where they may in the case of floats and others

    if  number == 0 :
        return('0')

    base36      = ''

    sign        = ''
    if  number  < 0:
        sign    = '-'
        number  = -number

    while number   != 0 :
        number, i   = divmod(number, len(alphabet))
        base36      = alphabet[i] + base36

    return(sign + base36)

def base_36_decode(number) :
    return(int(number,36))




def q_get(q, timeout = None) :
    """
        Get from a Queue.Queue(), but with a single parameter.
            timeout == None     wait forever
            timeout ==  0       non-blocking
            otherwise           wait for timeout time.
        Return None if timeout or nothing in queue.
    """

    try         :
        if  timeout == None :
            r   = q.get()
        elif not timeout :
            r   = q.get(False)
        else    :
            r   = q.get(True, timeout)
        pass
    except ( Queue.Empty, IOError, OSError, EOFError, ) :
        r       = None
    return(r)


def make_q_empty(q) :
    """ Suck a queue dry, returning None and allowing for bad things to happen as a program shuts down. """
    while q :
        try     :
            q.get_nowait()
        except ( Queue.Empty, IOError, OSError, EOFError, ) :
            q   = None
        pass
    return(q)




def _open_w_a(fn, bt_mode = "") :
    """ Open a file for writing, or, if that fails, try appending. Return the file object or None. """
    bt_mode = bt_mode or ""         # 'b' or 't' or ''
    f       = None
    try     :
        f   = open(fn, "w" + bt_mode)
    except ( OSError, IOError ) :
        try :
            f   = open(fn, "a" + bt_mode)
        except ( OSError, IOError ) :
            f   = None
        pass
    return(f)


def reroute_stdout_err(argv) :
    """
        According to command line parameters, reroute stdout and stderr (for use at the top of .exe files made with py2exe).
    """

    try :
        import  replace_file
    except ImportError  :
        replace_file    = None

    stdout_name = None
    stderr_name = None
    ai          = 0
    while ai    < len(argv) :
        arg = argv[ai]
        if  arg  in [ "--std_out", "--std-out", "--stdout", ] :
            del(argv[ai])
            stdout_name = argv.pop(ai)
        elif arg in [ "--std_err", "--std-err", "--stderr", ] :
            del(argv[ai])
            stderr_name = argv.pop(ai)
        elif arg in [ "--std_out_err", "--std-out-err", "--stdouterr", "--std_err_out", "--std_err_out", "--stderrout", ] :
            del(argv[ai])
            stderr_name = argv.pop(ai)
            stdout_name = stderr_name
        else :
            ai             += 1
        pass

    f_out                   = None
    f_err                   = None
    if  stdout_name and stderr_name :
        if  replace_file    :
            replace_file.safe_replace_file(stdout_name, None, stdout_name + ".bak")
        f_out               = _open_w_a(stdout_name)
        if  same_file(stdout_name, stderr_name) :
            f_err           = f_out
        else                :
            if  replace_file :
                replace_file.safe_replace_file(stderr_name, None, stderr_name + ".bak")
            f_err           = _open_w_a(stderr_name)
        pass
    elif stdout_name        :
        if  replace_file    :
            replace_file.safe_replace_file(stdout_name, None, stdout_name + ".bak")
        f_out               = _open_w_a(stdout_name)
    elif stderr_name        :
        if  replace_file    :
            replace_file.safe_replace_file(stderr_name, None, stderr_name + ".bak")
        f_err               = _open_w_a(stderr_name)

    if  f_out               :  sys.stdout  = f_out
    if  f_err               :  sys.stderr  = f_err

    return(f_out, f_err)


def close_rerouted_stdout_err(f_out, f_err) :
    """
        Close the files (or None's) returned by reroute_stdout_err().
    """

    if  f_out                                       : f_out.close()
    if  f_err and (not same_object(f_out, f_err))   : f_err.close()




class   a_kalman_filter(object) :

    def __init__(me, process_variance = 0.01, measurement_variance = 0.04, initial_value = 0.0) :
        me.pv       = process_variance      or  0.01
        me.mv       = measurement_variance  or  0.04
        me.guess    = initial_value         or  0.0         # the current best guess of the output value
        me.offset   = 1.0                                   # our tracker, so to speak. How much we juice the process_variance the next measurement.

    def next(me, measurement) :
        pm          = me.offset   + me.pv                   # make the current process variance, sort of
        mult        = pm    / (pm + me.mv)                  # make the current tracking multiplier
        me.guess   += (mult * (measurement - me.guess))     # track the measurement
        me.offset   = (1    -  mult) * pm                   # update our tracker (notice that if we think the measurement is perfect, we go back to the initial state)

        return(me.guess)

    #   a_kalman_filter



def weighted_choice(wates) :
    """ Given a list of (positive) weights, yield a randomly chosen index (like random.choice()), likely to be of a higher weight. """

    wates       = [ max(0, w) for w in wates ]
    if  not max(wates) :
        wates   = [ 1 ] * len(wates)

    mxw         = max(wates) * 2.0
    ii          = int(random.random() * len(wates))
    w           = 0.0
    while True  :
        w      += (random.random() * mxw)
        while w > wates[ii]:
            w  -= wates[ii]
            ii  = (ii + 1) % len(wates)
        yield(ii)
    pass




def cmp_str_with_ints(a, b) :
    """
        For use in numbered file name sorting, compare two strings with integer values in them.
        E.g. [ 'fn_1_1.txt', 'fn_1_9.txt', 'fn_1_10.txt', 'fn_1_100.txt', 'fn_1_20.txt', ].sort(tzlib.cmp_str_with_ints).
    """
    def _strint(g) :
        return("%0*u" % ( max(len(g.group(1)), 32), int(g.group(1)), ) )

    a   = re.sub(r'(\d+)', _strint, a)
    b   = re.sub(r'(\d+)', _strint, b)
    return(cmp(a, b))

def cmp_lower_str_with_ints(a, b) :
    """
        For use in numbered file name sorting, compare two strings with integer values in them.
        E.g. [ 'fn_1_1.txt', 'fn_1_9.txt', 'fn_1_10.txt', 'fn_1_100.txt', 'fn_1_20.txt', ].sort(tzlib.cmp_str_with_ints).
        Lower case version.
    """

    a   = a.lower()
    b   = b.lower()
    return(cmp_str_with_ints(a, b))




KMEANS_PASS_COUNT       = 20
KMEANS_SMALL_MOVEMENT   = 0.0

def kmeans_cluster(a, k, distance_rtn = None, make_center_rtn = None, pass_count = KMEANS_PASS_COUNT, small_movement = KMEANS_SMALL_MOVEMENT) :
    """
        Return an 'k' length array of cluster numbers corresponding with the items in 'a'.

        Callback routine examples:

            class   a_ksample(object) :
                def __init__(me, d) :
                    me.d    = d
                #   a_ksample

            def _cmp_dist(p1, p2) :
                if  (p1 is None) and (p2 is None) :
                    return(0)
                if  p1 is None  :
                    return( sys.maxint)
                if  p2 is None  :
                    return(-sys.maxint)
                return(abs(p1.d - p2.d))

            def _mkctr(a) :
                if  not len(a) :
                    return(None)
                return(a_ksample(float(sum([ s.d for s in a ]) / len(a))))

    """

    def mkctr_rtn(a) :
        """ Given an array of things, return a thing that's in the center of the things in the array. """
        if  not len(a) :
            return(None)
        return(float(sum(a)) / len(a))

    def d_rtn(p1, p2) :
        """
            Given two things (or None for either or both) return a distance (that can be compared with the '>' operator).
            If both things are None, return 0.
            Or, if either thing is None, return a huge distance.
            Otherwise, return the distance between the things.
        """
        if  (p1 is None) and (p2 is None) :
            return(0)
        if  p1 is None  :
            return( sys.maxint)
        if  p2 is None  :
            return(-sys.maxint)
        return(abs(p1 - p2))


    class   a_cluster(object) :
        """ Keep an array of things that are in this cluster. Compute/create a center thing that can be distance_rtn-compared with array things. """
        def __init__(me,  a  = [], make_center_rtn = None) :
            me.a        = a or []
            me.mkctr    = make_center_rtn   or mkctr_rtn
            me.center()
        def append(me, p) :
            me.a.append(p)
        def clear(me)   :
            me.a        = []
        def center(me)  :
            me.ctr      = me.mkctr(me.a)
            return(me.ctr)
        #   a_cluster


    k       = int(k)
    if  (len(a) < k) or (k < 1):
        return([ 0 ] * len(a))              # make everybody cluster zero

    dist        = distance_rtn                          or d_rtn
    pass_count  = ((pass_count    > 0) and pass_count)  or KMEANS_PASS_COUNT
    smlmv       = small_movement
    if  (smlmv is None) or (smlmv < 0) :
        smlmv   = KMEANS_SMALL_MOVEMENT

    ctrs    = [ a_cluster([ a[i] ], make_center_rtn) for i in xrange(k) ]
    a2ctr   = [ -1 for p in a ]             # we think every thing is in cluster -1 - so all things will move clusters the first time around

    for ps in xrange(pass_count) :
        for c in ctrs :
            c.clear()                       # forget the things in the cluster
        chng    = False
        for pi, p in enumerate(a) :
            bd  = dist(p, ctrs[0].ctr)
            bi  = 0
            for i in xrange(1, len(ctrs)) :
                d   = dist(p, ctrs[i].ctr)
                if  bd  > d :               # find the closest cluster
                    bd  = d
                    bi  = i
                pass
            if  bi     != a2ctr[pi] :
                a2ctr[pi]   = bi            # remember what cluster the thing is in
                chng        = True          # not the same cluster as last time
            ctrs[bi].append(p)              # add this thing to the closest cluster

        if  not chng        :
            break                           # kick out if no thing changed clusters

        bd          = smlmv - 1
        for c in ctrs :
            if  not len(c.a) :
                c.append(random.choice(a))  # fake a bright, new day
            octr    = c.ctr                 # remember the previously made center thing
            nctr    = c.center()            # compute a new center for the cluster
            d       = dist(octr, nctr)
            if  bd  < d :
                bd  = d
            pass
        if  bd <= smlmv :
            break                           # kick out if the cluster centers didn't move
        pass

    return(a2ctr)


def sort_kmeans_clusters(ka, a, k = 0, cmp_rtn = None) :
    """
        Change the cluster numbers in ka (which was returned by kmeans_cluster()) so that the lower cluster numbers probably have values in 'a' that sort earlier.

        Note:   Not passing a 'k' value is more stable (no unassigned cluster numbers), but probably slower.

        Note:   This routine should really compare the centers of the clusters rather than an arbitrary instance from each cluster.
                And when not given 'k', we could simply look for the max value in 'ka' to be 'k' and do the rest of the logic from there.

    """

    cmp_rtn = cmp_rtn or cmp

    if  k  <= 0     :                                           # find the cluster numbers from the ka array?
        kns         = [ [ kn, a[v], ] for kn, v in make_index_dictionary(ka).items() ]
    else            :
        kns         = [ [ kn, None, ] for kn in range(k) ]
        for kv in kns :
            i       = array_find(ka, kv[0])
            kv[1]   = None  if i < 0    else    a[i]
        pass


    def _cr(a, b) :
        if  (a[1] is None) and (b[1] is None) :
            return(0)
        if  a[1] is None :
            return( sys.maxint)
        if  b[1] is None :
            return(-sys.maxint)
        return(cmp_rtn(a[1], b[1]))
    kns.sort(_cr)

    kns = make_index_dictionary([ kv[0] for kv in kns ])

    for i, kn in enumerate(ka) :
        ka[i]   = kns[kn]

    pass




def restricted_fac(x):
    if  (type(x) != int) or (x < 0) :
        raise ValueError

    if  x == 0:
        return(1)

    for n in xrange(2, x) :
        x  *= x

    return(x)



def restricted_sinc(x) :
    if  x == 0  :
        return(1)

    return(math.sin(x) / x)



restricted_list     = [ 'acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', ]

restricted_dict     = {}
for k in restricted_list    :
    if  hasattr(math, k) :
        restricted_dict[k]  = getattr(math, k)
    pass

restricted_dict['enumerate']    = enumerate

restricted_dict['abs']      = abs
restricted_dict['min']      = min
restricted_dict['max']      = max
restricted_dict['sum']      = sum
restricted_dict['int']      = int
restricted_dict['float']    = float
restricted_dict['round']    = round
restricted_dict['len']      = len

restricted_dict['fac']      = restricted_fac
restricted_dict['sinc']     = restricted_sinc

restricted_dict['False']    = False
restricted_dict['True']     = True
restricted_dict['FALSE']    = False
restricted_dict['TRUE']     = True
restricted_dict['false']    = False
restricted_dict['true']     = True

restricted_dict['None']     = None
restricted_dict['none']     = None
restricted_dict['null']     = None
restricted_dict['nill']     = None

def restricted_eval(s, allowed = None) :

    allowed = allowed or {}
    allowed.update(restricted_dict)
    try     :
        return(eval(s, { "__builtins__" : {} }, allowed))
    except  :
        pass
    raise ValueError


def restricted_exec(s, allowed = None) :
    allowed = allowed or {}
    try :
        g   = { "__builtins__" : {} }
        g.update(restricted_dict)
        g.update(allowed)
        vd  = {}
        exec(s, g, vd)

        return(vd)

    except  :
        pass
    raise ValueError


full_user_name  = None
def get_full_user_name() :
    """ Return the user's full name, if it's there. Otherwise, return the user login name. """
    global  full_user_name
    if      full_user_name != None :
        return(full_user_name)

    n   = getpass.getuser()
    if  n :
        r, rs   = run_program('finger -p %s' % n)
        if  not r :
            g   = re.search(r"Login: " + re.escape(n) + r"\s+Name:\s+(.+?)[\r\n]", rs)
            if  g :
                nn  = g.group(1).strip()
                if  nn :
                    n   = nn
                pass
            pass
        pass
    full_user_name      = n or ""

    return(n)



def create_valid_id(hi) :
    """ Return a non-zero, etc. random number up to the given 'hi' number. """
    while   True    :
        n           = random.randint(0x10001, hi)
        if  not (0x19000101 <= n <= 0x20991231) :
            break
        pass
    return(n)


def create_small_id() :
    """ Return a non-zero, 31-bit, random number. """
    return(create_valid_id(0x7fffFFeF))


def create_uid(length = 8) :
    """ Return a UID - an 8 or given-length character, random, base-36-number string. """
    length  = ((length <= 0) and 8) or length
    n       = create_valid_id((36 ** length) - 1)
    return((("0" * length) + base_36_encode(n).lower())[-length:])



def get_system_wide_lock(process_name = None):
    """
        Return a lock for this program - actually a system-wide mutex/lock by the given name.

        So we can see if we are already running.

        Make sure the returned variable stays in scope or else it will be deleted by Python and won't work as you want it to.

    """
    process_name    = process_name or undotted_file_name_able(__file__) or "tzlib_py"
    if  win32api    :
        import  win32event, winerror

        lock    = win32event.CreateMutex(None, False, process_name)
        if  win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS :

            return(None)

        pass
    else        :
        import  socket

        lock    = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try     :
            lock.bind('\0' + process_name)
        except socket.error:

            return(None)

        pass

    return(lock)


def release_system_wide_lock(lock) :
    """
        Release the given system wide lock.

        It won't be used any more.

        Return the lock if something goes wrong. Otherwise, return None.

    """
    if  not lock :
        return(None)

    if  win32api :
        if  win32api.CloseHandle(lock) :

            return(None)

        pass

    else        :
        import  socket

        try     :
            lock.close()
            return(None)
        except socket.error:
            pass
        pass

    return(lock)                    # something went wrong



def get_all_drive_paths() :
    """ Get a list of all the drives on the system. For now, this here to note how to do this under Windows. """
    drives          = []
    if  win32api    :
        try         :
            drives  = [ dn.rstrip('\\') for dn in win32api.GetLogicalDriveStrings().split('\0') if dn ]
        except      :
            pass
        pass
    if  not drives  :
        if  sys.platform == 'win32' :
            drives  = [ d + ':' for d in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists(d + ':') ]
        else        :
            drives  = [ '/', ]              # doesn't work yet
        pass
    return(drives)


def get_mount_point(dn) :
    """ Return the path to this path's mount point. """
    dn      = os.path.abspath(dn)
    if  sys.platform == 'win32' :
        while True  :
            ndn = os.path.dirname(dn)
            if  ndn == dn :
                break
            dn  = ndn
        return(dn)

    while not os.path.ismount(dn) :
        ndn = os.path.dirname(dn)
        if  ndn == dn :
            break
        dn  = ndn
    return(dn)


def get_system_drive_path() :
    """ Get the system drive's path. """
    if  sys.platform == 'win32' :
        return(os.getenv('SystemDrive') or "C:")
    return('/')


def get_disk_space(drv = None) :
    """
        Get the disk space and space available on the given drive (e.g. C: or /).

        Return (None, None) if the drive isn't there.

    """
    drv     = drv or get_system_drive_path()
    if  win32api :
        try :
            ds  = win32api.GetDiskFreeSpaceEx(drv)
        except pywintypes.error :
            return(None, None)
        return(ds[1], ds[0])

    ds      = os.statvfs(drv)                                       # note: must be a path, not and /dev/sd??
    return(ds.f_blocks * ds.f_bsize, ds.f_bavail * ds.f_bsize)




def sha_directory(dn) :
    """ Return a dictionary keyed by SHA1 hex strings and valued by an array of file names - and keyed by fn_{base_file_name}, valued by SHA1 of file and keyed by 'FN_', valued by the absolute directory name. """
    dn      = os.path.abspath(dn)
    sha_dir = {}
    for fn in glob.glob(os.path.join(dn, "*")) :
        if  os.path.getsize(fn) :
            hs      = hashlib.sha1(safe_read_whole_binary_file(fn)).hexdigest().lower()
            sha_dir[hs] = sha_dir.get(hs, [])
            sha_dir[hs].append(fn)
            sha_dir['fn_' + os.path.basename(fn)]   = hs
        pass
    sha_dir['FN_']  = dn
    return(sha_dir)


def sha_dir_compare(from_sha_dir, to_sha_dir) :
    """ Return a list of files in the from_dir not in the to_dir and an (overriding) list of files that collide between the two directories. """
    ufns    = []
    hashes  = [ hs for hs in from_sha_dir.keys() if not hs.lower().startswith('fn_') ]
    for hs in hashes :
        if  hs not in to_sha_dir :
            ufns   += from_sha_dir[hs]
        pass

    cfns            = []
    nfns            = []
    for fn in ufns  :
        if  ('fn_'  + os.path.basename(fn)) in to_sha_dir :
            cfns.append(fn)
        else        :
            nfns.append(fn)
        pass

    return(nfns, cfns)



#
#
#       Test
#
#
def test() :
    """ Test some of the code. Crash if anything is found wrong. """
    ctm = elapsed_time()
    print "%20.10f" % ( ctm )

    swlock  = get_system_wide_lock()
    if  not swlock :
        raise ValueError("Get system wide lock failed!")

    a = [ 1, 2, 3 ]

    d = make_dictionary(a)

    print d[1], d[2], d[3]
    d = make_dictionary(a, "17")

    b = d.keys()
    a.sort()
    b.sort()
    for i in range(0, max(len(a), len(b))) :
        if  a[i] != b[i] :
            s   = "make_dictionary a != b %d" % i
            raise ValueError(s)
        pass

    a   = [ 10, 11, 12, 13, 14 ]
    d   = make_index_dictionary(a)
    for i in range(max(len(a), len(d))) :
        if  i != d[a[i]] :
            s   = "make_index_dictionary i != d[a[i]] %d" % i
            raise ValueError(s)
        pass


    d   = { "xyzzy" : "y", "a" : "baby" }
    rd  = invert_dictionary(d)
    if  rd != { "y" : "xyzzy", "baby" : "a" } :
        s   = "invert_dictionary(%s) is %s" % ( repr(d), repr(rd) )
        raise ValueError(s)

    d   = { "x" : "y", "a" : "y" }
    rd  = invert_dictionary(d, dupable_values = { 'y' : 'x' })
    if  rd != { "y" : "x" } :
        s   = "invert_dictionary(%s) is %s" % ( repr(d), repr(rd) )
        raise ValueError(s)

    d   = { "x" : "y", "a" : "y" }
    rd  = invert_dictionary(d, dupable_values = { 'y' : 'a' })
    if  rd != { "y" : "a" } :
        s   = "invert_dictionary(%s) is %s" % ( repr(d), repr(rd) )
        raise ValueError(s)

    try :
        d   = { "x" : "y", "a" : "y" }
        rd  = invert_dictionary(d)
        raise ValueError("invert_dictionary(%s) happy" % repr(d))
    except IndexError :
        pass


    a   = [ [ 'a', 1 ], [ 'b', 2 ], ]
    rd  = buples_to_dictionary(a)
    if  len(rd) != 2 :
        s   = "buples_to_dictionary not 2 long! %s" % rd
        raise ValueError(s)
    if  (rd['a'] != 1) or (rd['b'] != 2) :
        s   = "buples_to_dictionary values wrong! %s" % rd
        raise ValueError(s)


    a   = [ 1, 2, 3, 4 ]
    d   = { 1 : 1, 2 : 2, 3 : 3, 5 : 5, }
    if  not_in(d, a) != [ 5 ] :
        raise ValueError('5 not not_in, is %s' % repr(not_in(d, a)))

    a   = [ 1, 2, 3, 4 ]
    d   = { 2 : 2, }
    if  not_in(d, a) != [] :
        raise ValueError('not_in nothing not nothing, is %s' % repr(not_in(d, a)))

    d   = [ 0, 1, 2, 3, 4, ]
    a   = { 1 : 1, 2 : 2, 3 : 3, }
    if  sorted(not_in(d, a)) != [ 0, 4 ] :
        raise ValueError('0 not not_in, is %s' % repr(not_in(d, a)))

    d   = [ 1, 2, 3, 4, ]
    a   = { 2 : 2, }
    if  sorted(not_in(d, a)) != [ 1, 3, 4, ] :
        raise ValueError('not_in not 1, 3, 4 with odd types, is %s' % repr(not_in(d, a)))

    d   = [ 1, 2, 3, 4, ]
    a   = { }
    if  not_in(d, a) != d :
        raise ValueError('not_in nothing not nothing with odd types, is %s' % repr(not_in(d, a)))


    d   = { "xYz" : 5, "zyZ" : 10, "yyz" : 15, }
    update_all_case_keys(d)
    if  (
            (d['xyz'] != 5)
         or (d['XYZ'] != 5)
         or (d['xYz'] != 5)
         or (d['zyz'] != 10)
         or (d['ZYZ'] != 10)
         or (d['zyZ'] != 10)
         or (d['yyz'] != 15)
         or (d['YYZ'] != 15)
         or (len(d) != 8)
        ) :
        s   = "update_all_case_keys " + str(d)
        raise ValueError(s)

    crc = blkcrc32(_TEST_CRC_VALUE, "now is the time")
    crc = long(crc) & 0xFFFFffffL
    print "crc=0x%08lx %lu" % ( crc, crc )
    if  crc != 0xa458b82eL :
        s    = "crc32 [%s] is wrong!" % ( str(crc) )
        raise ValueError(s)
    crc = blkcrc32(0x98765431L, "now is the time")
    crc = crc & 0xFFFFffffL
    print "crc=0x%08lx %lu" % ( crc, crc )
    if  crc != 0xb525d257L :
        s    = "crc32 [%s] is wrong!" % ( str(crc) )
        raise ValueError(s)

    crc = 0
    bts = 0
    for i in range(1000) :
        s   = "%u %f" % ( i, random.random() )
        pc  = pure_python_crc32(crc, s)
        bts |= crc
        nc  = blkcrc32(crc,          s)
        if  pc != nc :
            s   = "crc mismatch 'tween pure and zlib (%s (%08lx:%u) %08lx:%u != %08lx:%u)!" % ( s, crc, crc, pc, pc, nc, nc )
            raise ValueError(s)
        if  random.random() >= 0.5 :
            crc = pc
        else :
            crc = nc

        if  (i > 100) and ((bts & 0xFFFFffffL) == 0xFFFFffffL) :
            break
        pass

    print "bcrc = %08x" % ( crc )


    crc = blkcrc16(_TEST_CRC_VALUE, "now is the time")
    print "crc=0x%04x %u" % ( crc, crc )
    if  crc != 0xe6eb :
        s    = "crc16 [0x%04x %s] is wrong!" % ( crc, str(crc) )
        raise ValueError(s)
    crc = blkcrc16(0x1234L,         "now is the time")
    print "crc=0x%04x %u" % ( crc, crc )
    if  crc != 0x11ee :
        s    = "crc16 [0x%04x %s] is wrong!" % ( crc, str(crc) )
        raise ValueError(s)


    vls = [
            [ 0,                 '0',           ],
            [  1,                '1',           ],
            [ -1,               '-1',           ],
            [  1234,             'YA',          ],
            [ -1234,            '-YA',          ],
            [  123456787901234,  '17RF9JYFQQ',  ],
            [ -123456787901234, '-17RF9JYFQQ',  ],
            [  1234.9,           'YA',          ],
            [ -1234.9,          '-YA',          ],
          ]
    for v, vs in vls :
        s   = base_36_encode(v)
        if  s != vs :
            raise ValueError("base_36 of %s is %s" % ( str(v), str(s), ) )
        s   = base_36_decode(s)
        if  s != int(v) :
            raise ValueError("un-base_36 of %s is %s" % ( str(v), str(s), ) )
        pass



    if  bool_to_0_or_1(False) != 0 :
        raise ValueError("bool_to_0_or_1(False) == %s" % bool_to_0_or_1(False))

    if  bool_to_0_or_1(True) != 1 :
        raise ValueError("bool_to_0_or_1(True) == %s" % bool_to_0_or_1(True))


    if  array_find( [ 1, 2, 3 ], 2) != 1 :
        s = "1st array_find != 1"
        raise ValueError(s)
    if  array_find( [ 1, 2, 3 ], [ 2, 1 ] ) != 1 :
        s = "2nd array_find != 1"
        raise ValueError(s)
    if  array_find( [ 1, 2, 3 ], [ 1, 2 ] ) != 0 :
        s = "array_find != 0"
        raise ValueError(s)
    if  array_find( [ 1, 2, 3 ], [ 4, 5, 6, 7 ] ) >= 0 :
        s = "array_find >= 0"
        raise ValueError(s)

    v   = [ [], [ 1, 2, 3 ], "4", [ 5, ], "", [ 6, [ 7, [ [], [ 8, 9, ], [] ], [10], [], [ 11, 12, 13, ] ], '14', ], 15, [], ]
    if  flatten_array(v) != [ 1, 2, 3, "4", 5, "", 6, 7, 8, 9, 10, 11, 12, 13, "14", 15 ] :
        s = "flatten_array %s" % flatten_array(v)
        raise ValueError(s)

    v   = [[1], 2, [[3,4], 5], [[[]]], [[[6]]], 7, 8, []]
    if  flatten_array(v) != [ 1, 2, 3, 4, 5, 6, 7, 8, ] :
        s   = "flatten_array %s" % flatten_array(v)
        raise ValueError(s)

    v   = [ 1, 2, 3, 4, 5 ]
    vv  = list(v)
    a   = pop_slice(v, 1, 3)
    if  (a != [ 2, 3, ]) or (v != [ 1, 4, 5 ]) :
        s   = "pop_slice() %s -> %s %s" % ( vv, v, a, )
        raise ValueError(s)

    v   = [ 1, 2, 3, 4, 5 ]
    vv  = list(v)
    a   = pop_slice(v, 1, 7)
    if  (a != [ 2, 3, 4, 5 ]) or (v != [ 1 ]) :
        s   = "pop_slice() %s -> %s %s" % ( vv, v, a, )
        raise ValueError(s)

    v   = [ 1, 2, 3, 4, 5 ]
    vv  = list(v)
    a   = pop_slice(v, 1)
    if  (a != [ 2, 3, 4, 5 ]) or (v != [ 1 ]) :
        s   = "pop_slice() %s -> %s %s" % ( vv, v, a, )
        raise ValueError(s)

    v   = [ 1, 2, 3, 4, 5 ]
    vv  = list(v)
    a   = pop_slice(v, to = 2)
    if  (a != [ 1, 2 ]) or (v != [ 3, 4, 5 ]) :
        s   = "pop_slice() %s -> %s %s" % ( vv, v, a, )
        raise ValueError(s)


    ov      = [ ( 1, 2, 3 ), ( 4, 5, 6 ) ]
    sov     = str(ov)
    v       = rotate_2d_array_clockwise(ov)
    sv      = str( [ ( 4, 1 ), ( 5, 2 ), ( 6, 3 ) ] )
    if  str(v) != sv :
        raise ValueError("rotate_2d_array_clockwise " + str(v) + " " + sv)

    v       = rotate_2d_array_counter_clockwise(v)
    if  str(v)  != sov :
        raise ValueError("rotate_2d_array_counter_clockwise " + str(v) + " " + sov)


    if  find_arg(  "x"   ,   "y") >= 0 :
        raise ValueError("find_arg found  y in   x")
    if  find_arg([ "x", ], [ "y", ])  >= 0 :
        raise ValueError("find_arg found [y] in [x]")
    if  find_arg(  "x"   ,   "_x_"   ) < 0 :
        raise ValueError("find_arg not found  _x_  in  x ")
    if  find_arg([ "x", ], [ "_x_", ]) < 0 :
        raise ValueError("find_arg not found [_x_] in [x]")
    if  find_arg([ "-x-", ], [ "_x_", ]) < 0 :
        raise ValueError("find_arg not found [_x_] in [-x-]")
    if  find_arg([ "b", "--x_y", ], [ "-a", "--xy", ]) < 0 :
        raise ValueError("find_arg not found [--xy] in [--x_y]")
    if  find_arg([ "b", "--x-y", ], [ "-a", "--x_y", ]) < 0 :
        raise ValueError("find_arg not found [--x_y] in [--x-y]")
    if  find_arg([ "b", "--xy", ], [ "-a", "--x_y", ]) < 0 :
        raise ValueError("find_arg not found [--x_y] in [--xy]")

    if  find_argi(  "x"   ,   "y") >= 0 :
        raise ValueError("find_argi found  y in   x")
    if  find_argi([ "x", ], [ "y", ])  >= 0 :
        raise ValueError("find_argi found [y] in [x]")
    if  find_argi(  "x"   ,   "_x_"   ) != 0 :
        raise ValueError("find_argi not found  _x_  in  x ")
    if  find_argi([ "x", ], [ "_x_", ]) != 0 :
        raise ValueError("find_argi not found [_x_] in [x]")
    if  find_argi([ "-x-", ], [ "_x_", ]) != 0 :
        raise ValueError("find_argi not found [_x_] in [-x-]")
    if  find_argi([ "b", "--x_y", ], [ "-a", "--x-y", ]) != 1 :
        raise ValueError("find_argi not found [--xy] in [--x-y]")
    if  find_argi([ "b", "--x-y", ], [ "-a", "--x_y", ]) != 1 :
        raise ValueError("find_argi not found [--x_y] in [--x-y]")
    if  find_argi([ "b", "--xy", ], [ "-a", "--x_y", ]) != 1 :
        raise ValueError("find_argi not found [--x_y] in [--xy]")
    if  find_argi([ "---xy", "--x_y", '--xy', ], [ "-a", "---x-y", ]) != 0 :
        raise ValueError("find_argi not found [---xy] in [---x-y]")


    if  strrev("x") != "x" :
        s = "strrev of 'x' is " + strrev("x")
        raise ValueError(s)

    if  strrev("xy") != "yx" :
        s = "strrev of 'xy' is " + strrev("xy")
        raise ValueError(s)

    if  strrev("xyz") != "zyx" :
        s = "strrev of 'xyz' is ", strrev("xyz")
        raise ValueError(s)


    s   = file_name_able("abc:^%&\"\';?*blah")
    if  s != "abc__%__;__blah" :
        raise ValueError("file_name_able not right! [%s]" % s)

    s   = file_name_able("-abc")
    if  s != "_abc" :
        raise ValueError("file_name_able not right! [%s]" % s)

    s   = file_name_able(u"\xe0bc:^%&\"\';?*blah")
    if  s != u"abc__%__;__blah" :
        raise ValueError("file_name_able not right! [%s]" % s)

    s   = undotted_file_name_able(u"\xe0bc:^%&\"\';?*bl.a.h")
    if  s != u"abc__%__;__bl_a_h" :
        raise ValueError("file_name_able not right! [%s]" % s)



    s   = safe_relpath(None)
    if  s != None :
        raise ValueError("safe_relpath of None! [%s]" % str(s))

    s   = safe_relpath("")
    if  s != "" :
        raise ValueError("safe_relpath of ''! [%s]" % str(s))

    s   = safe_relpath("./x.y")
    if  s != "x.y".replace('/', os.path.sep) :
        raise ValueError("safe_relpath of ./x.y! [%s]" % str(s))

    s   = safe_relpath("../x.y")
    if  s != "../x.y".replace('/', os.path.sep) :
        raise ValueError("safe_relpath of ../x.y! [%s]" % str(s))


    if  same_file("tzlib.py", "tz_lib_test.py") :
        raise ValueError('same_file("tzlib.py", "tz_lib_test.py")' is True)

    if  not same_file("tzlib.py", "tzlib.py") :
        raise ValueError('same_file("tzlib.py", "tzlib.py")' is False)

    if  not same_file("../tzpython/tzlib.py", "tzlib.py") :
        raise ValueError('same_file("../tzpython/tzlib.py", "tzlib.py")' is False)



    if  not can_run_program('shipit.py') :
        s = "Cannot run ship.py, apparently!"
        raise ValueError(s)

    if  can_run_program('xxx.yyy') :
        s = "Can run xxx.yyy, apparently!"
        raise ValueError(s)

    if  sys.platform != 'win32' :
        if  can_run_program('tzlib.py') :
            s = "Can run tzlib.py, apparently!"
            raise ValueError(s)
        pass

    ( r, rs )   = run_program("python factor.py %u" % ( 2 * 3 * 5 * 7 * 11 * 13 ) )
    if  r       :
        raise ValueError("Failure to run_program('python factor.py') : %s", str(r))
    if  rs.find("30030") < 0 :
        raise ValueError("run_program('python factor.py') failed to print result")
    print rs


    print "Dir of *.py files in this directory:"
    files = ambiguous_file_list("*.py")
    print len(files), files

    print "Dir of *.py files in this directory and sub-dirs:"
    files = ambiguous_file_list("*.py", True)
    print len(files), files

    print "Ext dir of *.py files in this directory:"
    files = ext_ambiguous_file_list(".", "py")
    print len(files), files

    print "Ext dir of *.py files in this directory and sub-dirs:"
    files = ext_ambiguous_file_list(".", "py", True)
    print len(files), files

    if  tz_vector_cosine( [ 1, 2, 3 ], [ 4, -5, 6 ]) != 0.365486942323903610 :
        s = "Cosine problem %2.50f" % ( tz_vector_cosine( [ 1, 2, 3 ], [ 4, -5, 6 ]) )
        raise ValueError(s)


    s   = " ".join(string_pairs( [ "a", "bb", "c", "d" ], 1, "x"))
    if  s != "axbb bbxc cxd" :
        s = "string_pairs problem: " + s
        raise ValueError(s)


    s   = " ".join(flat_positional_strings( [ "a", "bb", "c", "d" ], 3, "_%u_%s_"))
    if  s != "_0_a_ _1_bb_ _1_c_ _2_d_ _3_a_ _3_bb_ _4_c_ _4_d_" :
        s = "flat_positional_strings problem: " + s
        raise ValueError(s)


    s   = " ".join(log_positional_strings( [ "a", "bb", "c", "d", "e", "f", "g", "h", "i", "j" ], 2.0, "_%u_%s_"))
    if  s != "_0_a_ _1_bb_ _2_c_ _2_d_ _3_e_ _3_f_ _3_g_ _4_h_ _4_i_ _4_j_" :
        s = "log_positional_strings problem: " + s
        raise ValueError(s)


    s   = " ".join(log_positional_strings( [ "a", "bb", "c", "d", "e", "f", "g", "h", "i", "j" ], 3.0, "_%u_%s_"))
    if  s != "_0_a_ _2_bb_ _3_c_ _4_d_ _4_e_ _5_f_ _5_g_ _6_h_ _6_i_ _6_j_" :
        s = "log_positional_strings problem: " + s
        raise ValueError(s)


    ( m, a )    = linear_regression( ( -2, -1, 0, 1, 2, 3 ), ( -1, 0, 1, 2, 3, 4 ) )
    if  (m != 1.0) or (a != 1.0) :
        s   = "Line: m=" + str(m) + " a=" + str(a)
        raise ValueError(s)


    ( m, a )    = linear_regression( None, ( -1, 1, 3, 5, 7 ) )
    if  (m != 2.0) or (a != -1.0) :
        s   = "NoneX: m=" + str(m) + " a=" + str(a)
        raise ValueError(s)


    ( m, a )    = linear_regression( 1, ( -1, 1, 3, 5, 7 ) )
    if  (m != 2.0) or (a != -3.0) :
        s   = "OneX: m=" + str(m) + " a=" + str(a)
        raise ValueError(s)


    ( m, a )    = linear_regression( ( -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6 ), ( -4, -5, -2, -3, 0, -1, 1, 3, 2, 5, 4, 7, 6 ) )
    if  (int(round(m * 1000.0)) != 967) or (a != 1.0) :
        s   = "Jag: m=" + str(m) + " a=" + str(a)
        raise ValueError(s)

    try :
        linear_regression( ( 5.0, 5.0, 5.0 ), ( -6.0, 0.0, 10.0 ) )
        raise ValueError("linear_regression did not ValueError on vertical line")
    except ValueError :
        pass


    s   = strip_c_comments("""/* now is the time
*/ for all "/* */" fun "//" blah // testing
// more test
and finally/**/ this end
""")
    if  s != ' for all "/* */" fun "//" blah \n\nand finally this end\n' :
        s   = repr(s)
        raise ValueError(s)


    s   = decode_html_entities("hearts:&hearts; sigma:&sigma; oacute=&oacute; gt=&gt; lt=&#60;").encode('utf8')
    ss  = ("hearts:" + unichr(0x2665) + " sigma:" + unichr(0x3c3) + " oacute=" + "\xf3".decode('latin1') + " gt=> lt=<").encode('utf8')
    if  s != ss :
        s = "decode_html_entities problem: " + s
        raise ValueError(s)


    s   = safe_html("\x00&<><>&~\x7f\x80\xff#\r\n-----\r\n------\r\n-------\r\n-\r-\n-\r\n")
    if  s != "&#0;&amp;&lt;&gt;&lt;&gt;&amp;~&#127;&#128;&#255;#<BR>-----<BR><HR><BR><HR><BR>-<BR>-<BR>-<BR>" :
        s = "safe_html problem: " + s
        raise ValueError(s)


    s   = printable(" !@#$%^&*()_-|\\{}[];:'\x22<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  \x00\x01\x02\x1f\x7f\x80\xff z", "~+~")
    if  s !=        " !@#$%^&*()_-|\\{}[];:'\x22<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  ~+~~+~~+~~+~~+~~+~~+~ z" :
        s =  "printable problem: " + s
        raise ValueError(s)

    s   = printable(" !@#$%^&*()_-|\\{}[];:'\x22<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  \x00\x01\x02\x1f\x7f\x80\xff z")
    if  s !=        " !@#$%^&*()_-|\\{}[];:'\x22<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  _______ z" :
        s =  "printable problem: " + s
        raise ValueError(s)


    s   = printable_str(" !@#$%^&*()_-|{}[];:'\x22<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  \x00\x01\x02\x1f\x7f\x80\xff z")
    ss  =            r""" !@#$%^&*()_-|{}[];:'"<>,.?/`~abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890  \x00\x01\x02\x1f\x7f\x80\xff z"""
    if  s != ss :                                               # note: the backslash, "\\" is interpreted or converted differently in Python 2.4 and 2.5. Arrgh.
        for ci in range(min(len(ss), len(s))) :
            if  ss[ci] != s[ci] :
                print "char mismatch %u [%s]!=[%s]" % ( ci, s[ci], ss[ci] )
                break
            pass
        s =  "printable_str problem: %s %u %u" % ( s, len(s), len(ss) )
        raise ValueError(s)


    s       =   c_string("[\\ \' \" \a \b \f \n \r \t \v \\]")
    if  s  !=   r"[\134 \' \" \a \b \f \n \r \t \v \134]" :
        s   =   "c_string: " + repr(s)
        raise ValueError(s)


    s       =   c_ctrl_esc("[\\ [null\0null] [1f\x1f1f] [at@at] [dollar$dollar] [percent%percent] \' \" \a \b \f \n \r \t \v \\]")
    if  s  !=   r"[\134 [null\000null] [1f\0371f] [at\100at] [dollar\044dollar] [percent\045percent] \' \" \a \b \f \n \r \t \v \134]" :
        s   =   "c_ctrl_esc: " + repr(s)
        raise ValueError(s)


    s       =   lf_only("\r\r\r\n\n\tnow\t\r\nis\r the \n\r\ntime  \r\r\nfor")
    if  s  !=   "\n\n\tnow\t\nis\n the \n\ntime  \nfor" :
        s   =   "lf_only: " + c_string(s)
        raise ValueError(s)

    s       =   lf_only_with_no_trailing_white_space("   \n   blah   \n lkjsd    \f   \t   \n lkjsdf  \t")
    if  s  !=   "\n   blah\n lkjsd\n lkjsdf\n" :
        s   =   "lf_only_with_no_trailing_white_space: " + c_string(s)
        raise ValueError(s)

    s       =   lf_only_with_no_trailing_white_space("   \n   blah   \n lkjsd    \f   \t   \n lkjsdf  \t\n")
    if  s  !=   "\n   blah\n lkjsd\n lkjsdf\n" :
        s   =   "lf_only_with_no_trailing_white_space: " + c_string(s)
        raise ValueError(s)

    s       =   no_blank_lines("\r\r\r\n\n\tnow\t\r\nis\r the \n\r\ntime  \r\r\nfor")
    if  s  !=   "\tnow\nis\n the\ntime\nfor\n" :
        s   =   "no_blank_lines: " + c_string(s)
        raise ValueError(s)


    s       =   multiline_strip("  x \r\n\t \tx \r  \t x\nbla   \t   x \n test \n")
    if  s  !=   "x\nx\nx\nbla   \t   x\ntest\n" :
        s   =   "multiline_strip: " + c_string(s)
        raise ValueError(s)

    s       =   multiline_strip("x \r\n\t \tx \r  \t x\nbla   \t   x \n test ")
    if  s  !=   "x\nx\nx\nbla   \t   x\ntest" :
        s   =   "multiline_strip: " + c_string(s)
        raise ValueError(s)

    s       =   multiline_strip("\r  x \r\n\t \tx \r  \t x\nbla   \t   x \n test ")
    if  s  !=   "\nx\nx\nx\nbla   \t   x\ntest" :
        s   =   "multiline_strip: " + c_string(s)
        raise ValueError(s)

    s       =   multiline_strip("  \r  x \r\n\t \tx \r  \t x\nbla   \t   x \n test ")
    if  s  !=   "\nx\nx\nx\nbla   \t   x\ntest" :
        s   =   "multiline_strip: " + c_string(s)
        raise ValueError(s)

    s       =   multiline_strip("  \r  xZ \r\n\tZ \tx \r  \t x\nbla   \t   x \n test ", " \tZ")
    if  s  !=   "\nx\nx\nx\nbla   \t   x\ntest" :
        s   =   "multiline_strip: " + c_string(s)
        raise ValueError(s)


    s       =   multiline_flush_left("   \r   xZ \r\n  \tZ \tx \r  \t x \r\n    bla   \t   x \r\n\r\n      test ")
    if  s  !=   " \r   xZ\n\tZ \tx \r  \t x\n  bla   \t   x\n\n    test" :
        s   =   "multiline_flush_left: [%s]" % c_string(s)
        raise ValueError(s)


    s       =   " now is the time "
    cs      =   maybe_wrap_with_cdata(s)
    if  s  != cs :
        raise ValueError("gratuitous cdata")

    s       =   " now is the <time "
    cs      =   maybe_wrap_with_cdata(s)
    if  s  == cs :
        raise ValueError("Missed cdata <")

    s       =   " now is the &time "
    cs      =   maybe_wrap_with_cdata(s)
    if  s  == cs :
        raise ValueError("Missed cdata &")

    s       =   " now is the \ntime "
    cs      =   maybe_wrap_with_cdata(s)
    if  s  == cs :
        raise ValueError("Missed cdata \\n")

    s       =   " now is the \rtime "
    cs      =   maybe_wrap_with_cdata(s)
    if  s  == cs :
        raise ValueError("Missed cdata \\r")

    s       =   "<![CDATA[ now is the &time ]]>"
    cs      =   maybe_wrap_with_cdata(s)
    if  s  != cs :
        raise ValueError("Double cdata")

    s       =   " <![CDATA[ now is the &time ]]>"
    cs      =   maybe_wrap_with_cdata(s)
    if  s  == cs :
        raise ValueError("Missed imperfect cdata")
    if  cs !=   "<![CDATA[ <![CDATA[ now is the &time &#93;&#93;&gt;]]>" :
        raise ValueError("Missed included cdata data [%s]" % ( cs ))

    if  s_except_1(1) == 's' :
        raise ValueError("s_except_1 for 1")
    if  s_except_1(1.0) == 's' :
        raise ValueError("s_except_1 for 1")
    if  s_except_1(0) != 's' :
        raise ValueError("s_except_1 for 0")
    if  s_except_1(2) != 's' :
        raise ValueError("s_except_1 for 2")
    if  s_except_1(-1) != 's' :
        raise ValueError("s_except_1 for -1")


    s   = u"a L1 x91 \u0091".encode('latin1')
    cs  = convert_to_unicode(s)
    if  cs != u"a L1 x91 \u0091" :
        raise ValueError("convert_to_unicode of %s is %s" % ( repr(s), repr(cs) ) )

    s   = u"a L1 D-cross \u00d0 e-umlaut \u00eb".encode('latin1')
    cs  = convert_to_unicode(s)
    if  cs != u"a L1 D-cross \u00d0 e-umlaut \u00eb" :
        raise ValueError("convert_to_unicode of %s is %s" % ( repr(s), repr(cs) ) )

    s   = u"a utf8 L1 C-ish char \u00c7 - a C-ish".encode('utf8')
    cs  = convert_to_unicode(s)
    if  cs != u"a utf8 L1 C-ish char \u00c7 - a C-ish" :
        raise ValueError("convert_to_unicode of %s is %s" % ( repr(s), repr(cs) ) )

    s   = u"a utf8 U chars \u0189 \ua72a - D and E-ish".encode('utf8')
    cs  = convert_to_unicode(s)
    if  cs != u"a utf8 U chars \u0189 \ua72a - D and E-ish" :
        raise ValueError("convert_to_unicode of %s is %s" % ( repr(s), repr(cs) ) )


    s   = "abcdx&* \0\033\010\015\012\x7f\t"
    cs  = best_ascii(s)
    if  cs != "abcdx&* \0\033\010\015\012\x7f\t" :
        raise ValueError("best_ascio of %s is %s" % ( repr(s), repr(cs) ) )

    s   = "a\xc1\xe1b"
    cs  = best_ascii(s)
    if  cs != "aAab" :
        raise ValueError("best_ascio of %s is %s" % ( repr(s), repr(cs) ) )

    s   = "o\xc2\xba\xc3\xb2\xc3\xb3\xc3\xb4\xc3\xb5\xc3\xb6\xc3\xb8\xc5\x93 9{"
    cs  = best_ascii(s)
    if  cs != u'ooooooo\xf8\u0153 9{' :
        raise ValueError("best_ascio of %s is %s" % ( repr(s), repr(cs) ) )


    s   = ""
    cs  = de_dupe_str(s)
    if  cs != s :
        raise ValueError("de_dupe_str of %s is %s" % ( repr(s), repr(cs) ) )

    s   = "abc"
    cs  = de_dupe_str(s)
    if  cs != s :
        raise ValueError("de_dupe_str of %s is %s" % ( repr(s), repr(cs) ) )

    s   = "aabbbccabccc"
    cs  = de_dupe_str(s)
    if  cs != "abc" :
        raise ValueError("de_dupe_str of %s is %s" % ( repr(s), repr(cs) ) )

    s   = "dabababcabcabc"
    cs  = de_dupe_str(s)
    if  cs != "dabc" :
        raise ValueError("de_dupe_str of %s is %s" % ( repr(s), repr(cs) ) )

    s   = u"ab\u1234\u5678\u1234"
    cs  = de_dupe_str(s)
    if  cs != u"ab\u1234\u5678" :
        raise ValueError("de_dupe_str of %s is %s" % ( repr(s), repr(cs) ) )


    if  cmp_str_with_ints('abc23', 'abc219') >= 0 :
        raise ValueError("cmp_str_with_ints abc32 abc219")

    if  cmp_str_with_ints('abc00532', 'abc51') <= 0 :
        raise ValueError("cmp_str_with_ints abc00532 51")

    if  cmp_str_with_ints('abc32A', 'abc32a') >= 0 :
        raise ValueError("cmp_str_with_ints abc32A abc32a")

    if  cmp_lower_str_with_ints('abc32A', 'abc32a') != 0 :
        raise ValueError("cmp_lower_str_with_ints abc32A abc32a")

    if  cmp_lower_str_with_ints('abc32Z', 'abc32a') <= 0 :
        raise ValueError("cmp_lower_str_with_ints abc32Z abc32a")


    r   = binary_search([ 3, 6, 9, 12, 12, 13 ], 12)
    if  r != 3 :
        raise ValueError("binary_search(12) not 3 is %d" % r)

    r   = binary_search([ 3, 6, 9, 10, 12, 13, 14 ], 10)
    if  r != 3 :
        raise ValueError("binary_search(10) not 3 is %d" % r)

    r   = binary_search([ 3, 6, 9, 10, 12, 13, 14 ], 11)
    if  r != 4 :
        raise ValueError("binary_search(11) not 4 is %d" % r)

    r   = binary_search([ 3, 6, 9, 10, 12, 13, 14 ], 110)
    if  r != 7 :
        raise ValueError("binary_search(110) not 7 is %d" % r)

    r   = binary_search([ 3, 6, 9, 10, 12, 13, 14 ], -1)
    if  r != 0 :
        raise ValueError("binary_search(-1) not 0 is %d" % r)

    r   = max_index([ 1, 2, 5, -1, 0 ])
    if  r != 2 :
        raise ValueError("max_index() not 2 is %d" % r)

    r   = max_index([])
    if  r != -1 :
        raise ValueError("max_index of [] not -1")

    r   = min_index([ 1, 2, 5, -1, 0 ])
    if  r != 3 :
        raise ValueError("min_index() not 3 is %d" % r)

    r   = min_index([])
    if  r != -1 :
        raise ValueError("min_index of [] not -1")


    for vv in [ 1/2.0, 3/4.0, 2/3.0, 66/100.0, 1/3.0, 1/7.0, 1/5.0, 14/100.0, 3/10.0, 12/10.0, 1.0 / math.pi, math.pi, 5/1.0, -3/10.0, -25/10.0, ] :
        n, d    = as_integer_ratio(vv)
        if  abs(vv - n / d) > .00000001 :
            raise ValueError("as_integer_ratio(%s) is %s/%s" % ( vv, n, d, ))
        pass


    for a, e, m in [
                    [ [ -3, 1, 5, ],      1, None ],
                    [ [ -3, -2, 5, ],    -2, None ],
                    [ [ -2, -3, 0, ],    -2, None ],
                    [ [  0,  3, 2, ],     2, None ],
                    [ [ ],             None, None ],
                    [ [  3,  2, 5, ],     3, None ],
                    [ [  3,  2, 4, 5, ],  3.5, None ],
                    [ [  3,  2, 5, 5, ],  4,   None ],
                    [ [  9,  2, 5, 3, ],  4,   None ],
                    [ [  9, ],            9,   0.1234 ],
                    [ [  9, ],            9,   None ],
                    [ [  1, 2, 3, 4, 5, 6, 7, 8, 9,    ],  5,   0.5     ],
                    [ [  1, 2, 3, 4, 5, 6, 7, 8, 9     ],  3,   0.25    ],
                    [ [  1, 2, 3, 4, 5, 6, 7, 8, 9,    ],  7,   0.75    ],
                    [ [  1, 2, 3, 4, 5, 6, 7,          ],  3,   1/3.0   ],
                    [ [  1, 2, 3, 4, 5, 6, 7, 8,       ],  3 + 1/3.0, 1/3.0   ],
                    [ [  1, 2, 3, 4, 5, 6, 7, 8, 9,    ],  3 + 2/3.0, 1/3.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  3,         1/3.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  4.5, 0.5     ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  2.25,   0.25    ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  6.75,   0.75    ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  6,   2/3.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  3,   1/3.0   ],
                    [ [  0, 1, 2, 3, 4, 5,             ],  1,   1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5,             ],  2,   2/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5,             ],  3,   3/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5,             ],  4,   4/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6,          ],  1.2,   1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6,          ],  2.4,   2/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6,          ],  3.6,   3/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6,          ],  4.8,   4/5.0   ],

                    [ [  0, 1, 2, 3, 4, 5, 6, 7,       ],  1.4,   1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7,       ],  2.8,   2/5.0   ],

                    [ [  0, 1, 2, 3, 4, 5, 6, 7,       ],  4.2,   3/5.0   ],

                    [ [  0, 1, 2, 3, 4, 5, 6, 7,       ],  5.6,   4/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8,    ],  1.6,   1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8,    ],  3.2,   2/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8,    ],  4.8,   3/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8,    ],  6.4,   4/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  1.8,   1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  3.6,   2/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  5.4,   3/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ],  7.2,   4/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ],  2,     1/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ],  4,     2/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ],  6,     3/5.0   ],
                    [ [  0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ],  8,     4/5.0   ],
                    [ [  1, -3, 5, ],     -3, 0 ],
                    [ [ -3,  5, 1, ],      5, 1 ],
                    [ [ [  8,  5, 1, ], [ 2, 3, 4, [ 5, 6, 7, ], 9, ], ], 5, None ],
                ] :
        # import  numpy
        # r       = median(numpy.array(a), middle = m)      # note: comment the non-1D array at the end of the test items
        r       = median(a, middle = m)
        if  ((r is None) != (e is None)) or ((r != None) and (abs(r - e) > 0.0000000000001)) :
            raise ValueError("median(%s) of %s is %s, not %s as it should be" % ( str(m), str(a), str(r), str(e), ))
        pass

    a   = [ 'a9', 'a10', 'a 5a', 'a 5A', 'a 50', 'a 1.5', 'a 1.11', 'a .118', 'a .11', 'a.0122', 'a -10', 'a -9', 'a20.10', 'a200', 'a20.1', 'a20.10', 'a -.11', 'a -.111', ]
    b   = sorted_numerically(a)
    if  b != ['a -.11', 'a -.111', 'a -9', 'a -10', 'a .11', 'a .118', 'a 1.11', 'a 1.5', 'a 5A', 'a 5a', 'a 50', 'a.0122', 'a9', 'a10', 'a20.10', 'a20.1', 'a20.10', 'a200'] :
        raise ValueError("sorted_numerically of %s is not %s" % ( a, b, ))


    r   = west_valley([ 1, 2, 3, 2, 1 ], 2)
    if  r != 0 :
        raise ValueError("west_valley not 0")

    r   = west_valley([ 3, 2, 2, 3, 2, 1, 1, 2 ], 3)
    if  r != 1 :
        raise ValueError("west_valley not 1")

    r   = east_valley([ 1, 2, 3, 2, 1 ], 2)
    if  r != 4 :
        raise ValueError("east_valley not 4")

    r   = east_valley([ 3, 2, 2, 3, 2, 1, 1, 2 ], 3)
    if  r != 6 :
        raise ValueError("east_valley not 6")


    for a, xywh, sm, avg in [
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 1, 1, 2, 2, ],
                                    28,
                                    7,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 1, 1, ],
                                    1,
                                    1,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 0, 1, ],
                                    0,
                                    None,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 1, 0, ],
                                    0,
                                    None,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, -1, 1, ],
                                    0,
                                    None,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 1, -1, ],
                                    0,
                                    None,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 10, 1, ],
                                    6,
                                    2,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 1, 10, ],
                                    12,
                                    4,
                                ],
                                [
                                    [
                                        [ 1, 2, 3, ],
                                        [ 4, 5, 6, ],
                                        [ 7, 8, 9, ],
                                    ],
                                    [ 0, 0, 10, 10, ],
                                    45,
                                    5,
                                ],
                            ] :
        cs  = cumsum(a)

        r   = cumsum_sum(cs, xywh[0], xywh[1], xywh[2], xywh[3])
        if  r != sm :
            raise ValueError("cumsum_sum     of %s in %s is %u, should be %u" % ( repr(xywh), repr(a), r, sm, ))

        r   = cumsum_average(cs, xywh[0], xywh[1], xywh[2], xywh[3])
        if  r != avg :
            raise ValueError("cumsum_average of %s in %s is %u, should be %u" % ( repr(xywh), repr(a), r, avg, ))

        if  False   :
            # import  numpy                     # uncomment to test - commented to avoid necessarily pulling numpy in to programs that include this module
            # cs  = cumsum(numpy.array(a))      # ditto

            r   = cumsum_sum(cs, xywh[0], xywh[1], xywh[2], xywh[3])
            if  r != sm :
                raise ValueError("cumsum_sum     of %s in %s is %u, should be %u" % ( repr(xywh), repr(a), r, sm, ))

            pass

        pass



    # print "tfn", temp_file_name()
    # print "tfn", temp_file_name()

    if  excel_column_name(0) != 'a' :
        raise ValueError("Excel column name 0 is %s!" % str(excel_column_name(0)))
    if  excel_column_name(1) != 'b' :
        raise ValueError("Excel column name 1 is %s!" % str(excel_column_name(1)))
    if  excel_column_name(26) != 'aa' :
        raise ValueError("Excel column name 26 is %s!" % str(excel_column_name(26)))
    if  excel_column_name(53) != 'bb' :
        raise ValueError("Excel column name 53 is %s!" % str(excel_column_name(53)))
    if  excel_column_name(676) != 'za' :
        raise ValueError("Excel column name 676 is %s!" % str(excel_column_name(676)))
    if  excel_column_name(701) != 'zz' :
        raise ValueError("Excel column name 701 is %s!" % str(excel_column_name(701)))


    a   = list_lstrip([ "bad", "bad", "good", "bad"], "bad")
    if  len(a) != 2 :
        raise ValueError("list_lstrip: 3 "  + str(a))
    a   = list_lstrip([ "bad", "bad", "good", "bad"], "good")
    if  len(a) != 4 :
        raise ValueError("list_lstrip: 4 "  + str(a))
    a   = list_lstrip([ "bad", "bad", "good", "bad"], [ "bad" ])
    if  len(a) != 2 :
        raise ValueError("list_lstrip: 2a " + str(a))
    a   = list_lstrip([ "", "", "", "good"], [ "" ])
    if  len(a) != 1 :
        raise ValueError("list_lstrip: 1a " + str(a))
    a   = list_lstrip([ "", "", "", "good"], "")
    if  len(a) != 1 :
        raise ValueError("list_lstrip: 1 "  + str(a))
    a   = list_lstrip([ 2, 2, 2 ], 2)
    if  len(a) != 0 :
        raise ValueError("list_lstrip: 0 "  + str(a))

    s   = de_html_str(u"<HTML> <BODY>\n\r\n\n\r\r\nText  on  a\tline<BR>after <script>scripting</script>break</P attrib='lksjdflkjsldkjflsjdlfkjsldjfljsdf'> after paragraph <HR><script >and more scripting</script ><HR> \xd0 &amp; &lt;DIR&gt; after angled DIR <DIR>after DIR</LI>After end li")
    cs  = unicode("\nText on a line\nafter break\n\nafter paragraph\n----------------------------------------\n\n----------------------------------------\n\xd0 & <DIR> after angled DIR\nafter DIR\nAfter end li", 'latin1')
    if  s != cs :

        print len(s), len(cs)

        def cstr(c) :
            if  (ord(c) >= 32) and (ord(c) < 0x7f) :
                return(c)
            return("|" + str(ord(c)) + "|")

        for i in xrange(len(s)) :
            if  s[i] != cs[i] :

                print i, cstr(s[i]), cstr(cs[i])
                break
            pass

        s = "de_html_str problem: [" + "".join([ cstr(s[i]) for i in xrange(len(s)) ]) + "]"
        raise ValueError(s)


    t   = elapsed_time()
    print "%20.10f %20.10f" % ( t, t - ctm )

    time.sleep(0.2)

    t   = elapsed_time()
    print "%20.10f %20.10f" % ( t, t - ctm )

    ta  = [
            [   1.23456      +  2 * 60 +  3 * 60 * 60 + 4 * 60 * 60 * 24 + 567 * 60 * 60 * 24 * 7, "3973:03:02:01.23456", "567:4:03:02:01.23456"    ],
            [   0            +  0 * 60 +  0 * 60 * 60 + 0 * 60 * 60 *  0 + 567 * 60 * 60 * 24 * 7, "3969:00:00:00"      , "567:0:00:00:00"          ],
            [   1            +  2 * 60 +  3 * 60 * 60 + 4 * 60 * 60 * 24 + 567 * 60 * 60 * 24 * 7, "3973:03:02:01"      , "567:4:03:02:01"          ],
            [   50           +  2 * 60 +  3 * 60 * 60 + 4 * 60 * 60 * 24 + 567 * 60 * 60 * 24 * 7, "3973:03:02:50"      , "567:4:03:02:50"          ],
            [   1.0000000001 + 59 * 60 + 23 * 60 * 60 + 1 * 60 * 60 * 24                         , "1:23:59:01"         , "1:23:59:01"              ],
            [   1.0000000001 + 59 * 60 + 23 * 60 * 60                                            , "23:59:01"           , "23:59:01"                ],
            [   1.0000000001 + 59 * 60                                                           , "59:01"              , "59:01"                   ],
            [   59           + 59 * 60                                                           , "59:59"              , "59:59"                   ],
            [   59.9999                                                                          , "59.9999"            , "59.9999"                 ],
            [   59.9999      + 1  * 60                                                           , "1:59.9999"          , "1:59.9999"               ],
            [   .5                                                                               , ".5"                 , ".5"                      ],
            [   .05                                                                              , ".05"                , ".05"                     ],
           ]

    for ti, tt in enumerate(ta) :
        s   = wdhms_str(tt[0])
        if  s != tt[1] :
            raise ValueError("wdhms_str of %s[%u] is %s not %s" % (tt[0], ti, s, tt[1] ) )
        s   = wdhms_str(tt[0], weeks = True)
        if  s != tt[2] :
            raise ValueError("wdhms_str(weeks) of %s[%u] is %s not %s" % (tt[0], ti, s, tt[2] ) )
        pass


    d   = same_time_ish(1000000000, 1000000000 + 7.9 * 3600)
    if  not d :
        s   = "same_time_ish of 7.9 hours is different 'time'"
        raise ValueError(s)

    d   = same_time_ish(1000000000, 1000000000 + 14.1 * 3600)
    if  d   :
        s   = "same_time_ish of 14.1 hours is same 'time'"
        raise ValueError(s)


    d   = find_upper_dir("tzpython")
    if  os.path.split(d)[1] != "tzpython" :
        s   = "Could not find this or parent 'tzpython' directory [%s]" % ( str(d) )
        raise ValueError(s)

    d   = find_upper_dir("blahblahblahblah")
    if  os.path.split(d)[1] == "blahblahblahblah" :
        s   = "Found this or parent 'blahblahblahblah' directory [%s]" % ( str(d) )
        raise ValueError(s)
    if  d :
        s   = "Found this or parent 'blahblahblahblah' directory [%s]" % ( str(d) )
        raise ValueError(s)


    d   = find_upper_file_or_dir("tzpython/tzlib.py")
    if  os.path.split(d)[1] != "tzlib.py" :
        s   = "Could not find this or parent 'tzpython' directory [%s]" % ( str(d) )
        raise ValueError(s)

    d   = find_upper_file_or_dir("tzpython/blahblah.blah")
    if  d   :
        s   = "Found tzpython/blahblah.blah [%s]" % ( str(d) )
        raise ValueError(s)


    for v, r in [
                    [ 0b0100, 0b0101 ],
                    [ 0b0101, 0b0111 ],
                    [ 0b0111, 0b1111 ],
                    [ 0b1001, 0b1011 ],
                ] :
        a   = raise_left_zero_bit(v)
        if  a != r :
            raise ValueError("raise_left_zero_bit(%s) == %s, not %s" % ( bin(v), bin(a), bin(r), ))
        pass


    for v, r in [
                    [ 0b1001, 0b0010 ],
                    [ 0b0111, 0b1000 ],
                    [ 0b1011, 0b0100 ],
                ] :
        a   = only_right_zero_bit(v)
        if  a != r :
            raise ValueError("only_right_zero_bit(%s) == %s, not %s" % ( bin(v), bin(a), bin(r), ))
        pass


    for v, r in [
                    [ 0b0100, 0b0000 ],
                    [ 0b0101, 0b0100 ],
                    [ 0b0111, 0b0110 ],
                    [ 0b0110, 0b0100 ],
                ] :
        a   = lower_left_bit(v)
        if  a != r :
            raise ValueError("lower_left_bit(%s) == %s, not %s" % ( bin(v), bin(a), bin(r), ))
        pass


    for v, r in [
                    [ 0b0100, 0b0111 ],
                    [ 0b0101, 0b0101 ],
                ] :
        a   = raise_all_right_xero_bits(v)
        if  a != r :
            raise ValueError("raise_all_right_xero_bits(%s) == %u, not %u" % ( hex(v), a, r, ))
        pass


    for v, r in [
                    [ 0b0000, 0 ],
                    [ 0b0100, 1 ],
                    [ 0b0101, 2 ],
                    [ 0b0111, 3 ],
                    [ 0b1010, 2 ],
                    [ 0xfffe, 15 ],
                    [ 0xfffb, 15 ],
                    [ 0xefff, 15 ],
                    [ 0xffffFFFF, 32 ],
                    [ 0x1ffffFFFFffffFFFF, 65 ],
                    [ 0x10000000000000000, 1 ],
                ] :
        a   = bit_count(v)
        if  a != r :
            raise ValueError("bit_count(%s) == %u, not %u" % ( hex(v), a, r, ))
        pass


    for v, r in [
                [ 4, 3 ],
                [ 5, 3 ],
                [ 7, 3 ],
                [ 1, 1 ],
                [ 0, 0 ],
                [ -4, 3 ],
                [ -5, 3 ],
                [ -7, 3 ],
                [ -1, 1 ],
                [ -0, 0 ],
                [ 0x700000000, 35 ],
                [ 0x80000000,  32 ],
                [ 0x8000000000000000,  64 ],
                [ 0x10000000000000000,  65 ],
                [ 0x30000000000000000,  66 ],
                [ 0x40000000,  31 ],
              ] :
        a   = bit_length(v)
        if  a != r :
            raise ValueError("bit_length(%s) == %u, not %u" % ( hex(v), a, r, ))
        pass


    for v, r, u in [
                    [ 0, 0, 0 ],
                    [ 1, 1, 1 ],
                    [ 3, 2, 2 ],
                    [ 2, 3, 3 ],
                    [ 6, 4, 4 ],
                    [ 7, 5, 0x0b ],
                    [ 5, 6, 0x0c ],
                    [ 4, 7, 0x0d ],
                    [ 0xc, 8, 0x0e ],
                    [ 0x8, 0xf, 0xf ],
                    [ 0xfe, 0xab, 0x5d ],
                    [ 0xff, 0xaa, 0xbc ],
                    [ 0x8000, 0xffff, None ],
                    [ 0xfffe, 0xaaab, None ],
                    [ 0x010000000, 0x1fffFFFF,  None ],
                    [ 0x0ffffFFFF, 0x0aaaaAAAA, None ],
                    [ 0x100000000, 0x1ffffFFFF, None ],
                    [ 0x200000000, 0x3ffffFFFF, None ],
                    [ 0x23456789a, 0x3d86450ec, None ],
                    [  1 <<  893,                       0x3fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffL, None ],
                    [ (1 << 1279) - 0xfedcab87564321a,  0x55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555fe3d9850ced76bbL, None ]
                ] :
        a   = un_gray_code(v)
        if  a != r :
            raise ValueError("un_gray_code(%s) == %s, not %s" % ( hex(v), hex(a), hex(r), ))
        r   = gray_code(a)
        if  r != v :
            raise ValueError("gray_code(%s) == %s, not %s" % ( hex(a), hex(r), hex(v), ))
        if  0 <= v < 256 :
            a   = balanced_8_bit_un_gray_code(v)
            if  a != u :
                raise ValueError("balanced_8_bit_un_gray_code(%s) == %s, not %s" % ( hex(v), hex(a), hex(u), ))
            r   = balanced_8_bit_gray_code(a)
            if  r != v :
                raise ValueError("balanced_8_bit_gray_code(%s) == %s, not %s" % ( hex(a), hex(r), hex(v), ))
            pass
        pass
    cnts    = [ 0 ] * 9
    pc      = 0x80
    for n in xrange(256) :
        gc  = balanced_8_bit_gray_code(n)
        bd  = gc ^ pc
        if  bit_count(bd) != 1  :
            raise ValueError("balanced_8_bit_gray_code(%s) == %s is not gray compared to previous code %s -> %s has %u bits" % ( hex(n), hex(gc), hex(pc), hex(bd), bit_count(bd), ))
        cnts[bit_length(bd)]   += 1
        pc  = gc
        nn  = balanced_8_bit_un_gray_code(gc)
        if  nn != n :
            raise ValueError("round trip balanced_8_bit_un_gray_code(balanced_8_bit_gray_code(%s)) == %s, bgc == %s" % ( hex(n), hex(nn), hex(gc), ))
        pass
    cnts    = cnts[1:]
    cnts.sort()
    if  cnts[0] != cnts[-1] :
        raise ValueError("balanced_8_bit_gray_code table is not balanced %s" % str(cnts))


    for v, e in [
                    [ ( 2, 3 ),         [ 0, 0, 0, 1, 0, 1, 1, 1, ]    ],
                    [ ( "abcd", 2 ),    "aabacadbbcbdccdd"          ],
                ] :
        r   = de_bruijn(*v)
        if  r != e :
            raise ValueError("de_bruijn of %s not %s, but is %s" % ( v, e, r, ))
        pass


    for WH in [ 2, 4, 8, 64 ] :
        xys     = {}
        for i in xrange(0, WH * WH) :
            xy  = square_hilbert_i_to_xy(WH, i)
            if  str(xy) in xys :
                s   = "Hilbert curve index %u in duplicated at %s" %  ( i, str(xy), )
                raise ValueError(s)
            xys[str(xy)]    = True
            j   = square_hilbert_xy_to_i(WH, xy[0], xy[1])
            if  i != j :
                s   = "Hilbert curve index %u out not same as in %u at %s" %  ( j, i, str(xy), )
                raise ValueError(s)
            if  str(j) in xys :
                s   = "Hilbert curve index %u out duplicated at %s" %  ( j, str(xy), )
                raise ValueError(s)
            xys[str(j)] = True
            # print i, j, xy
        pass


    for a, b, d in [
                    [  1, 99,  2 ],
                    [ 99,  2,  3 ],
                    [ 90, 40, 50 ],
                    [ 90, 41, 49 ],
                    [ 90, 39, 49 ],
                    [ 40, 90, 50 ],
                    [ 41, 90, 49 ],
                    [ 39, 90, 49 ],
                    [  0, 50, 50 ],
                    [ 50,  0, 50 ],
                    [  1, 52, 49 ],
                    [ 52,  1, 49 ],
                    [ 25, 26,  1 ],
                    [ 26, 23,  3 ],
                   ] :
        r   = torus_distance(a, b, 100)
        if  r != d :
            s   = "torus_distance(%u, %u, 100) != %u" % ( a, b, d, )
            raise ValueError(s)
        pass


    for x, y, d in [
                        [  0,  1,   0 ],
                        [  4,  4,  45 ],
                        [  4,  0,  90 ],
                        [  4, -4, 135 ],
                        [  0, -4, 180 ],
                        [ -4, -4, 225 ],
                        [ -4,  0, 270 ],
                        [ -4,  4, 315 ],
                   ]    :
        a   = compass_angle(math.atan2(y, x))
    if  a != d :
        s   = "Wrong compass angle for %i, $i %i != %f!" % ( x, y, d, a, )
        raise ValueError(s)


    a   = math.degrees(radian_angle_difference(math.radians(0), math.radians(10)))
    if  not (-11 <= a <= -9) :
        s   = "radian(0 - 10) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(10), math.radians(1)))
    if  not (8 <= a <= 10) :
        s   = "radian(10 - 1) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(170), math.radians(-170)))
    if  not (-21 <= a <= -19) :
        s   = "radian(170 - -170) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(90), math.radians(-170)))
    if  not (-101 <= a <= -99) :
        s   = "radian(90 - -170) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(-170), math.radians(90)))
    if  not (99 <= a <= 101) :
        s   = "radian(-170 - 90) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(-170), math.radians(170)))
    if  not (19 <= a <= 21) :
        s   = "radian(-170 - 170) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(170), math.radians(10)))
    if  not (159 <= a <= 161) :
        s   = "radian(170 - 10) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(170), math.radians(100)))
    if  not (69 <= a <= 71) :
        s   = "radian(170 - 100) == %f" % a
        raise ValueError(s)

    a   = math.degrees(radian_angle_difference(math.radians(100), math.radians(170)))
    if  not (-71 <= a <= -69) :
        s   = "radian(100 - 170) == %f" % a
        raise ValueError(s)


    for ang, rv in  [
                        [  100, 80  ],
                        [  -10, 10  ],
                        [  -80, 80  ],
                        [ -269, 89  ],
                        [  269, 89  ],
                        [   19, 19  ],
                        [  219, 39  ],
                        [    0,  0  ],
                        [  180,  0  ],
                        [  179,  1  ],
                        [ -179,  1  ],
                        [  181,  1  ],
                        [ -181,  1  ],
                    ] :
        a   = math.degrees(radian_angle_from_horizontal(math.radians(ang)))
        if  (rv < 0) or (abs(a - rv) > 0.00000001) :
            s   = "from_hz(%u) == %f" % ( ang, rv, )
            raise ValueError(s)
        pass


    aa  = None
    a   = average_angle(aa)
    if  a != None :
        raise ValueError("average_angle of %s is %s not None" % ( str(aa), str(a), ))
    aa  = []
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != 0.0 :
        raise ValueError("average_angle of %s is %s not 0.0" % ( str(aa), str(a), ))
    aa  = [ 0 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != 0.0 :
        raise ValueError("average_angle of %s is %s not 0.0" % ( str(aa), str(a), ))
    aa  = [ 0, 10, 350 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  abs(radian_angle_difference(a, 0.0)) >= 0.000000001 :
        raise ValueError("average_angle of %s is %s not 0.0" % ( str(aa), str(a), ))
    aa  = [ 0, 180 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != 0.0 :                  # radian_angle_difference(a, math.radians(90)) >= 0.000000000000001 :
        raise ValueError("average_angle of %s is %s not 0.0" % ( str(aa), str(a), ))
    aa  = [ 0, 180, 270 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != math.radians(270) :    # radian_angle_difference(a, math.radians(270)) >= 0.00000000000001 :
        raise ValueError("average_angle of %s is %s not 270.0" % ( str(aa), str(math.degrees(a)), ))
    aa  = [ 90, 180, 270 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != math.pi :              # radian_angle_difference(a, math.pi) >= 0.0000000000000001 :
        raise ValueError("average_angle of %s is %s not pi" % ( str(aa), str(math.degrees(a)), ))
    aa  = [ 0, 90, 180, 270 ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  a != 0.0 :                  # radian_angle_difference(a, math.radians(0)) >= 0.00000000000000000001 :
        raise ValueError("average_angle of %s is %s not 0.0" % ( str(aa), str(math.degrees(a)), ))
    aa  = [ 320, 330, 340, 350, 0, ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  abs(radian_angle_difference(a, math.radians(340)))     >= 0.000000000000001 :
        raise ValueError("average_angle of %s is %s not 340.0" % ( str(aa), str(math.degrees(a)), ))
    aa  = [ 320, 330, 340, 350, 0, 10, ]
    a   = average_angle([ math.radians(a) for a in aa ])
    if  abs(radian_angle_difference(a, math.radians(345)))     >= 0.000000000000001 :
        raise ValueError("average_angle of %s is %s not 345.0" % ( str(aa), str(math.degrees(a)), ))
    if  True :
        aa  = [ 320, 330, 340, 350, 10, ]
        a   = average_angle([ math.radians(a) for a in aa ])
        if  abs(radian_angle_difference(a, math.radians(341.894795196)))    >= 0.00000000001 :
            raise ValueError("average_angle of %s is %s not 341.894795196"  % ( str(aa), str(math.degrees(a)), ))
        aa  = [ 320, 330, 340, 350, 380, 400, ]
        a   = average_angle([ math.radians(a) for a in aa ])
        if  abs(radian_angle_difference(a, math.radians(352.705023342)))    >= 0.00000000001 :
            raise ValueError("average_angle of %s is %s not 352.705023342"  % ( str(aa), str(math.degrees(a)), ))
        aa  = [ 320, 330, 340, 20, ]
        a   = average_angle([ math.radians(a) for a in aa ])
        if  abs(radian_angle_difference(a, math.radians(341.972749481)))    >= 0.00000000001 :
            raise ValueError("average_angle of %s is %s not 341.972749481"  % ( str(aa), str(math.degrees(a)), ))
        aa  = [ 252.0, 288.0, 324.0, 72.0, ]
        a   = average_angle([ math.radians(a) for a in aa ])
        if  abs(radian_angle_difference(a, math.radians(306)))              >= 0.00000000001 :
            raise ValueError("average_angle of %s is %s not 306"            % ( str(aa), str(math.degrees(a)), ))
        pass

    aa  = [ 6, 7, 8, 9, ]
    a   = average_modulo(aa, 10)
    if  abs(a - 7.5) > 0.00000000000001 :
        raise ValueError("average_modulo of %s is %s not 7.5" % ( str(aa), str(a), ))
    aa  = [ 7, 8, 9, 0 ]
    a   = average_modulo(aa, 10)
    if  abs(a - 8.5) > 0.00000000000001 :
        raise ValueError("average_modulo of %s is %s not 8.5" % ( str(aa), str(a), ))
    aa  = [ 7, 8, 9, 2 ]
    a   = average_modulo(aa, 10)
    if  abs(a - 8.5) > 0.00000000000001 :
        raise ValueError("average_modulo of %s is %s not 9" % ( str(aa), str(a), ))

    if  True :
        aa  = [ 7, 8, 9, 1 ]
        a   = average_modulo(aa, 10)
        if  abs(a - 8.62183826553) > 0.00000000001 :
            raise ValueError("average_modulo of %s is %s not 8.62183826553" % ( str(aa), str(a), ))
        pass


    (x, y)  = get_line_intersection([ [ -4, 10 ], [ -4, 19 ], ], [ [ -4, 21 ], [ -4, 19 ], ], 0.0)
    if  (x != -4) or (y != 19) :
        s   = "Fail %s:%s" % ( str(x), str(y) )
        raise ValueError(s)

    (x, y)  = get_line_intersection([ [ -4, 10 ], [ -4, 19 ], ], [ [ -4, 21 ], [ -4, 20 ], ], 0.0)
    if  (x != None) or (y != None) :
        s   = "Fail %s:%s" % ( str(x), str(y) )
        raise ValueError(s)

    (x, y)  = get_line_intersection([ [ 3, 2 ], [ 5, 6 ], ], [ [ 1, 3 ], [ 5, 1 ], ])
    if  (x != 3) or (y != 2) :
        s   = "Fail %s:%s" % ( str(x), str(y) )
        raise ValueError(s)

    (x, y)  = get_line_intersection([ [ 3, 2 ], [ 5, 6 ], ], [ [ 1, 3 ], [ 5, 1 ], ], -0.1)
    if  (x != None) or (y != None) :
        s   = "Fail %s:%s" % ( str(x), str(y) )
        raise ValueError(s)


    r       = area_of_irregular_polygon([ [ -3, -2 ], [ -1, 4 ], [ 6, 1 ], [ 3, 10 ], [ -4, 9 ], ])
    if  r  != 60.0 :
        raise ValueError("area_of_irregular_polygon() is not 60.0, is %.1f" % r)


    va      = [ a_point(100, 100), a_point(200, 100), a_point(200, 200), a_point(100, 200), ]   # square
    for p  in [
                [  50, 150 ],
                [ 150,  50 ],
                [ 150, 250 ],
                [ 250, 150 ],
                [ 150, 200 ],   # rt/bt
                [ 200, 150 ],   # rt/bt
                [ 200, 200 ],   # rt/bt
              ] :
        r       = point_in_polygon(va, a_point(p[0], p[1]))
        if  r   :
            s   = "%u:%u is inside a 100x100 square at 100:100!" % ( p[0], p[1], )
            raise ValueError(s)
        pass
    for p  in [
                [ 150, 150 ],
                [ 100, 110 ],
                [ 100, 100 ],
                [ 110, 100 ],
                [ 100, 150 ],
              ] :
        r       = point_in_polygon(va, a_point(p[0], p[1]))
        if  not r :
            s   = "%u:%u is not inside a 100x100 square at 100:100!" % ( p[0], p[1], )
            raise ValueError(s)
        pass

    va      = [ a_point(200, 200), a_point(300, 300), a_point(200, 400), a_point(100, 300), ]       # diamond
    for p  in [
                [ 100, 100 ],
                [ 300, 200 ],
                [ 300, 400 ],
                [ 100, 400 ],
                [ 110, 110 ],
                [ 280, 210 ],
                [ 290, 390 ],
                [ 110, 390 ],
                [ 200, 400 ],           # rt/bt
                [ 300, 300 ],           # rt/bt
                [ 250, 250 ],           # rt/bt
                [ 250, 350 ],           # rt/bt
                [ 200, 200 ],           # this should really be inside, I'd think
              ] :
        r       = point_in_polygon(va, a_point(p[0], p[1]))
        if  r   :
            s   = "%u:%u is inside a a diamond 200:200!" % ( p[0], p[1], )
            raise ValueError(s)
        pass
    for p  in [
                [ 200, 300 ],
                [ 199, 299 ],
                [ 201, 299 ],
                [ 199, 301 ],
                [ 201, 301 ],
                [ 150, 250 ],
                [ 250, 251 ],
                [ 250, 349 ],
                [ 150, 251 ],
                [ 150, 349 ],
                [ 100, 300 ],
                [ 150, 350 ],
              ] :
        r       = point_in_polygon(va, a_point(p[0], p[1]))
        if  not r :
            s   = "%u:%u is not inside a a diamond 200:200!" % ( p[0], p[1], )
            raise ValueError(s)
        pass

    make_color_wheel()


    poly    = poly_from_xy_list([ 50,150, 200,50, 350,150, 350,300, 250,300, 200,250, 150,350, 100,250, 100,200 ])
    for clipopy in [
                    poly_from_xy_list([ 100,100, 100,300, 300,300, 300,100 ]),
                    poly_from_xy_list([ 100,100, 300,100, 300,300, 100,300 ]),
                   ] :
        r   = clip_polygon(poly, clipopy)
        ra  = [ [100.0, 116.66666666666667], [125.00000000000001, 100.0], [275.0, 100.0], [300.0, 116.66666666666667], [300.0, 299.99999999999994], [250.0, 300.0], [200, 250], [175.0, 300.0], [125.0, 300.0], [100.0, 250.0] ]
        for pi, p in enumerate(ra) :
            for xy in [ 0, 1 ] :
                d   = abs(p[xy] - r[pi][xy])
                if  d   > 0.00000000001 :
                    s   = "clip_polygon failed on (1-based) %u'th vertex XY[%u] %.14f should be %.14f!" % ( pi + 1, xy, r[pi][xy], p[xy], )
                    raise ValueError(s)
                pass
            pass
        pass
    poly    = [ [ 100, 100 ], [ 200, 100 ], [ 200, 200 ], [ 100, 200 ] ]
    clipopy = [ [ 600, 100 ], [ 800, 100 ], [ 800, 200 ], [ 600, 200 ] ]
    r       = clip_polygon(poly, clipopy)
    if  len(r) :
        s   = "clip_polygon found overlap where there is none!"
        raise ValueError(s)
    poly    = [ [ 100, 100 ], [ 200, 100 ], [ 200, 200 ], [ 100, 200 ] ]
    clipopy = [ [  20, 100 ], [  40, 100 ], [  40, 200 ], [  20, 200 ] ]
    r       = clip_polygon(poly, clipopy)
    if  len(r) :
        s   = "clip_polygon found overlap where there is none!"
        raise ValueError(s)
    poly    = [ [ 100, 100 ], [ 200, 100 ], [ 200, 200 ], [ 100, 200 ] ]
    clipopy = [ [ 600,  10 ], [ 800,  10 ], [ 800,  20 ], [ 600,  20 ] ]
    r       = clip_polygon(poly, clipopy)
    if  len(r) :
        s   = "clip_polygon found overlap where there is none!"
        raise ValueError(s)
    poly    = [ [ 100, 100 ], [ 200, 100 ], [ 200, 200 ], [ 100, 200 ] ]
    clipopy = [ [ 600, 510 ], [ 800, 510 ], [ 800, 520 ], [ 600, 520 ] ]
    r       = clip_polygon(poly, clipopy)
    if  len(r) :
        s   = "clip_polygon found overlap where there is none!"
        raise ValueError(s)


    a = (0,0)
    b = (0,1)
    c = (1,1)
    d = (1,0)
    if  do_line_segments_intersect((a, b), (c, d)) :
        s   = "Intersect seg %s-%s %s-%s" % ( str(a), str(b), str(c), str(d) )
        raise ValueError(s)
    if  do_line_segments_intersect((a, b), (d, c)) :
        s   = "Intersect seg %s-%s %s-%s" % ( str(a), str(b), str(d), str(c) )
        raise ValueError(s)
    if  not do_line_segments_intersect((a, c), (b, d)) :
        s   = "Intersect not seg %s-%s %s-%s" % ( str(a), str(c), str(b), str(d) )
        raise ValueError(s)
    if  do_line_segments_intersect((a, d), (b, c)) :
        s   = "Intersect seg %s-%s %s-%s" % ( str(a), str(d), str(b), str(c) )
        raise ValueError(s)


    print "ThreadID:", get_tid()


    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 3 } ], 'a')
    if  a  != [ 1, 2 ] :
        s   = "%s should be '[ 1, 2 ]'" % str(a)
        raise ValueError(s)
    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 3 } ], 'b')
    if  a  != [ 2, 3, 4 ] :
        s   = "%s should be '[ 2, 3, 4 ]'" % str(a)
        raise ValueError(s)
    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 4 } ], 'c')
    if  a  != [ 3, 4 ] :
        s   = "%s should be '[ 3, 4 ]'" % str(a)
        raise ValueError(s)

    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 3 } ], 'a', 9)
    if  a  != [ 1, 2, 9 ] :
        s   = "%s should be '[ 1, 2, 9 ]'" % str(a)
        raise ValueError(s)
    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 3 } ], 'b', 9)
    if  a  != [ 2, 3, 4 ] :
        s   = "%s should be '[ 2, 3, 4 ]'" % str(a)
        raise ValueError(s)
    a   = value_array_for_key([ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 4 } ], 'c', 9)
    if  a  != [ 9, 3, 4 ] :
        s   = "%s should be '[ 9, 3, 4 ]'" % str(a)
        raise ValueError(s)

    a   = [ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 4 } ]
    replace_value_array_for_key(a, 'd', [ 5, 6, 7 ])
    a   = value_array_for_key(a, 'd')
    if  a  != [ 5, 6, 7 ] :
        s   = "%s should be '[ 5, 6, 7 ]'" % str(a)
        raise ValueError(s)

    a   = [ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 4 } ]
    try :
        replace_value_array_for_key(a, 'e', [ 5, ])
        raise ValueError("Short replace_value_array_for_key did not raise exception")
    except IndexError :
        pass

    a   = [ { 'b' : 2, 'a' : 1 }, { 'b' : 3, 'a' : 2, 'c' : 3 }, { 'b' : 4, 'c' : 4 } ]
    try :
        replace_value_array_for_key(a, 'f', [ 5, 6, 7, 8 ])
        raise ValueError("Long replace_value_array_for_key did not raise exception")
    except IndexError :
        pass



    r   = best_w_h_fit_scale(10, 10, 5, 2)
    if  r != 2 :
        raise ValueError("best_w_h_fit_scale(10,10,5,2) != 2, is %f" % r)
    r   = best_w_h_fit_scale(20, 10, 5, 2)
    if  r != 4 :
        raise ValueError("best_w_h_fit_scale(20,10,5,2) != 4, is %f" % r)
    r   = best_w_h_fit_scale(30, 10, 5, 2)
    if  r != 5 :
        raise ValueError("best_w_h_fit_scale(30,10,5,2) != 5, is %f" % r)


    r   = best_line_fit(2, 7, 0, 10)
    if  r != 0 :
        raise ValueError("best_line_fit(2, 7, 0, 10) != 0, is %u" % r)
    r   = best_line_fit(5, 7, 0, 10)
    if  r != 2 :
        raise ValueError("best_line_fit(2, 7, 0, 10) != 1, is %u" % r)
    r   = best_line_fit(9, 4, 0, 10)
    if  r != 6 :
        raise ValueError("best_line_fit(9, 4, 0, 10) != 6, is %u" % r)
    r   = best_line_fit(8, 4, 0, 10)
    if  r != 6 :
        raise ValueError("best_line_fit(8, 4, 0, 10) != 6, is %u" % r)
    r   = best_line_fit(8, 4, 1,  3)
    if  r != 1 :
        raise ValueError("best_line_fit(8, 4, 1,  3) != 1, is %u" % r)


    for tt in xrange(1) :
        wa  = [ 500, 1, 1, 1000, 1, 0, 150, 1 ]
        c   = weighted_choice(wa)
        a   = [ c.next() for i in xrange(100) ]
        ca  = [ 0 ] * len(wa)
        for v in a :
            ca[v] += 1
        if  max(ca) != ca[3] :
            raise ValueError("Probably just a random thing: 1000 isn't chosen the most! %u %s" % ( tt, str(ca) ) )
        if  ca[0] <= ca[6] :
            raise ValueError("Probably just a random thing: 500 isn't chosen more than 150! %u %s" % ( tt, str(ca) ) )
        if  ca[6] <= ca[1] + ca[2] + ca[4] + ca[5] + ca[7] :
            raise ValueError("Probably just a random thing: 150 isn't chosen more than the 1's! %u %s" % ( tt, str(ca) ) )

    for tt in xrange(10) :
        cnt = 10000.0
        wa  = [ -1000, 0, 0, 0, 0 ]
        c   = weighted_choice(wa)
        a   = [ c.next() for i in xrange(int(cnt)) ]
        ca  = [ 0 ] * len(wa)
        for v in a :
            ca[v] += 1
        gv  = cnt / len(wa)
        for v in ca :
            if  abs(v - gv) > gv / 10 :
                raise ValueError("weighted_choice of zero'd array with a negative weight is unbalanced %u %s!" % ( tt, str(ca) ) )
            pass
        pass

    for tt in xrange(1) :
        cnt = 10000.0
        wa  = [ 0, 0, 0, 0, 0 ]
        c   = weighted_choice(wa)
        a   = [ c.next() for i in xrange(int(cnt)) ]
        ca  = [ 0 ] * len(wa)
        for v in a :
            ca[v] += 1
        gv  = cnt / len(wa)
        for v in ca :
            if  abs(v - gv) > gv / 10 :
                raise ValueError("weighted_choice of zero'd array is unbalanced %u %s!" % ( tt, str(ca) ) )
            pass
        pass


    for ti in xrange(100) :
        k   = random.randint(5, 35)
        pa  = [ random.randint(100, 135) for i in range(35) ]
        ka  = kmeans_cluster(pa, k, pass_count = 100)
        kaa = list(ka)
        sort_kmeans_clusters(kaa, pa)
        kak = list(ka)
        sort_kmeans_clusters(kak, pa, k)
        if  False :
            print [ "%3u" % v for v in pa  ]
            print [ "%3u" % v for v in ka  ]
            print [ "%3u" % v for v in kaa ]
            print [ "%3u" % v for v in kak ]
        m   = 0
        for i in xrange(k) :
            a   = [ pa[pi] for pi, v in enumerate(kaa) if v == i ]
            if  min(a + [ m + 1 ]) <= m :
                s   = "Out of order kmeans %u for value %u!" % ( k, m, )
                raise ValueError(s)
            if  len(a) :
                m   = max(a)
            pass
        m   = 0
        for i in xrange(k) :
            a   = [ pa[pi] for pi, v in enumerate(kak) if v == i ]
            if  min(a + [ m + 1 ]) <= m :
                s   = "Out of order kmeans %u for value %u!" % ( k, m, )
                raise ValueError(s)
            if  len(a) :
                m   = max(a)
            pass
        if  kak != kaa :
            raise ValueError("Two sorted kmeans cluster mappings were not the same!")
        pass



    if  restricted_eval("pi") != math.pi :
        raise ValueError("restricted_eval of pi failed!")
    if  restricted_eval(" sin(2)") != math.sin(2) :
        raise ValueError("restricted_eval of sin() failed!")
    if  restricted_eval(" fac(8)") != restricted_fac(8) :
        raise ValueError("restricted_eval of fac() failed!")
    if  restricted_eval(" len('a')") != 1 :
        raise ValueError("restricted_eval of len('a') failed!")
    try :
        restricted_eval("blow('a')")
        s   = "restricted_eval of blow('a') failed!"
    except ValueError :
        s   = None
    if  s   :
        raise ValueError(s)

    ld  = restricted_exec("x = 5\ny = x\nz = 'xyzzy'\n")
    if  ld.get('x', None) != 5 :
        raise ValueError("restricted_exec x wrong [%s]!" % str(ld.get('x', None)))
    if  ld.get('y', None) != 5 :
        raise ValueError("restricted_exec y wrong [%s]!" % str(ld.get('y', None)))
    if  ld.get('z', None) != 'xyzzy' :
        raise ValueError("restricted_exec z wrong [%s]!" % str(ld.get('z', None)))


    tfn = "tzlib.tmp"
    d   = { 'x' : [ 2, 3, 4 ], 5 : { 'sdf' : 4.5, }, }
    if  not pickle_file(tfn, d) :
        raise ValueError("Pickle error")

    dd  = unpickle_file(tfn)
    os.remove(tfn)
    if  d != dd :
        raise ValueError("Pickle/unpickle error: %s != %s" % ( str(d), str(dd) ))

    tfn = "tzlib.tmp"
    d   = { 'x' : [ 2, 3, 4 ], 5 : { 'sdf' : 4.5, }, }
    if  not pickle_file(tfn, d, sys.maxint) :
        raise ValueError("Pickle error")

    dd  = unpickle_file(tfn)
    os.remove(tfn)
    if  d != dd :
        raise ValueError("Pickle/unpickle error: %s != %s" % ( str(d), str(dd) ))

    tfn = "tzlib.tmp"
    d   = { 'x' : [ 2, 3, 4 ], 5 : { 'sdf' : 4.5, }, }
    if  not pickle_file(tfn, d, -1) :
        raise ValueError("Pickle error")

    dd  = unpickle_file(tfn)
    os.remove(tfn)
    if  d != dd :
        raise ValueError("Pickle/unpickle error: %s != %s" % ( str(d), str(dd) ))


    tfn = "tzlib.tmp"
    write_whole_binary_file(tfn, "blah blah")
    if  not os.path.isfile(tfn) :
        raise ValueError("Cannot write 'tzlib.tmp' for whacking test!")
    whack_file(tfn)
    if  os.path.exists(tfn) :
        raise ValueError("Cannot whack 'tzlib.tmp'!")

    print "Full user name:", get_full_user_name()

    print "Small ID: %08x   UID: %s" % ( create_small_id(), create_uid(), )

    if  not get_system_wide_lock('tzlib') :
        raise ValueError("Got wrong system wide lock didn't succeed!")
    if  get_system_wide_lock() :
        raise ValueError("Got double system wide lock should not have been possible!")

    if  release_system_wide_lock(swlock) :
        raise ValueError("Release system wide lock failed!")

    swlock  = get_system_wide_lock()
    if  not swlock :
        raise ValueError("Get system wide lock failed!")


    dns     = [ 'sha_dir1', 'sha_dir2' ]

    for dn in dns : whack_full_dir(dn)

    fns     = [ 'tmp1.tmp', 'tmp2.tmp', 'tmp3.tmp', 'tmx1.tmp', 'tmx2.tmp', 'tmx3.tmp', 'tmy1.tmp', ]
    nws     = [ 'new1.tmp', 'new2.tmp', ]
    sdrs    = []
    for dn in dns :
        os.mkdir(dn)
        for fn in fns :
            write_whole_text_file(os.path.join(dn, fn), "%08x\n" % blkcrc32(INITIAL_CRC32_VALUE, fn[:3] + (((fn[2:4] == 'x2') and dn) or '')))
        for fn in nws :
            write_whole_text_file(os.path.join(dn, fn), "%08x\n" % blkcrc32(INITIAL_CRC32_VALUE, fn[:3] + (((fn[2:4] == 'x2') and dn) or '')))
        nws = []
        sdrs.append(sha_directory(dn))

    df, cf  = sha_dir_compare(sdrs[0], sdrs[1])

    print "Sha dir new files:", df
    print "Sha collide files:", cf

    if  sorted([ os.path.basename(fn) for fn in df ]) != sorted([ 'new1.tmp', 'new2.tmp', ]) :
        raise ValueError("sha dir new files: %s !" % str(df))
    if  sorted([ os.path.basename(fn) for fn in cf ]) != sorted([ 'tmx2.tmp', ]) :
        raise ValueError("sha dir new files: %s !" % str(cf))

    # print sorted(sdrs[0].keys())
    # print sorted(sdrs[1].keys())

    if  safe_file_datetime('lblahlkjsdlfkjlsdf') != None :
        raise ValueError("safe_file_datetime not None for non-existent file!")
    if  safe_file_datetime('tzlib.py') <= 0 :
        raise ValueError("safe_file_datetime for tzlib.py not positive!")

    for dn in dns : whack_full_dir(dn)

    for dn in dns :
        if  os.path.exists(dn) :
            raise ValueError("SHA directory should have been whacked %s!" % dn)
        pass

    if  int(str_base(123456789012345, 35), 35) != 123456789012345 :
        raise ValueError("str_base(123456789012345)")
    if  int(str_base(9876543210987, 36), 36) != 9876543210987 :
        raise ValueError("str_base(123456789012345)")
    print str_base(12345678909876543210, 36), 'base36 ==', str_base(12345678909876543210), "base10"

    print "All drive paths:                  ", get_all_drive_paths()
    print "Disk space for system drive:      ", get_disk_space()
    print "User home mount point:            ", get_mount_point(expand_user_vars("~/"))
    print "User home no-such-dir mount point:", get_mount_point(expand_user_vars("~/blah_blah_blah/"))



if  __name__ == '__main__' :
    test()

#
#
# eof
