#!/usr/bin/python

# tgcmsg.py
#       --copyright--                   Copyright 2007 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       June 30, 2003           bar
#       February 3, 2004        bar     amp_messages_from_file
#                                       ignore empty messages
#       September 28, 2004      bar     define True and False
#       February 25, 2005       bar     able to convert non-string fields to ascii msg
#                                       handle weird stuff
#       November 6, 2005        bar     amp_messages_to_file
#       April 28, 2006          bar     strip_comment_fields()
#       November 18, 2007       bar     turn on doxygen
#       November 20, 2007       bar     comments
#       November 27, 2007       bar     insert boilerplate copyright
#       May 17, 2008            bar     email adr
#       May 9, 2009             bar     allow / to be in msg fields without escaping
#       June 3, 2009            bar     able to encode latin1 or utf8, whichever seems best
#       September 20, 2010      rmb     added Unicode support to parse_tgc_msg, tgc_msg_as_string, amp_messages_from_file, and amp_messages_to_file
#       November 27, 2010       bar     merge encoding logic back in to the library
#                                       rework escaping entirely
#                                       escape $ and @ in case Perl wants to have trouble with the strings
#                                       escape unicode chars to \uXXXX
#                                       explicitly de-escape \uXXXX
#                                       if encoded file, don't escape a0..ffff
#                                       handle the unusual things the C ref does e.g. \_
#       December 6, 2010        bar     learn to type. pass_thru_non_ascii, that's C not D
#                                       back to understanding comments any place in the message
#       December 30, 2010       bar     able to handle non-string message fields in tgc_msg_as_string()
#       February 15, 2011       bar     make command line decoding of files show exceptions
#       November 29, 2011       bar     pyflake cleanup
#       May 27, 2012            bar     doxygen namespace
#       February 19, 2013       bar     epydoc indentation corrected
#       December 2, 2013        bar     msgs_only()
#       July 9, 2014            bar     allow null bytes
#       July 18, 2014           bar     allow read/write from file-like objects
#       September 9, 2014       bar     be a bit - emphasis, bit - more forgiving of either utf8 or latin1 characters in the input. But if the input is utf8, we have a problem
#       --eodstamps--
##      \file
#       \namespace              tzpython.tgcmsg
#
#
"""
    Do things for TGC messages - AMP protocol messages, that is.

    TGC messages are in text form with N fields, space delimited.

    If a field contains white-space, double-quotes or a leading semi-colon (necessarily if it's the first field),
    then the field is enclosed in double-quotes.

    Messages are meant to be typing-friendly. Backspaces mean to backspace, for instance.

        - This code has the ability to put out non-ascii as unescaped characters in the assumption that encoding is done before from-msg and after to-msg.

    Graphics, control characters and other characters can be (and are normally) escaped C style.
        - NOTE:
          The (reference) C implementation of TGCMSG handles \u and \e and other Perl and else-wise oddities.

          The Perl and Python implementations are both weak in handling certain pathological \ escapes.

          All implementations themselves output-escape using 3 digit octal values so that subsequent input is unambiguous.

          Input with escapes like \t \r \f \" \' \; \z \_ etc. can be assumed to be typed by a human or proxy thereof.

"""



import  codecs
import  os.path
import  re






##  Run under older Pythons
try:
    True, False
except NameError:
    True    = 1
    False   = 0


WHITE_SPACE = " \t\r\n\f"

word_re     = re.compile(r"([^" + WHITE_SPACE +  "]+)(.*)$",                            re.DOTALL)
qstring_re  = re.compile(r"\"(.*?[^\\])\"(.*)$",                                        re.DOTALL)     # !!!! use better regex from net to parse quoted strings
qneed_re    = re.compile(r'[ "]',                                                       re.DOTALL)     # note: doesn't need any but space 'cause others are escaped
escape_re   = re.compile( r"[^a-zA-Z0-9 \!\^\*\(\)\-\_\=\+\|\[\]\{\}\:\?\<\>\,\.\/]",   re.DOTALL)
ps_esc_re   = re.compile(ur"[^a-zA-Z0-9 \!\^\*\(\)\-\_\=\+\|\[\]\{\}\:\?\<\>\,\.\/\xa0-\xff\u0100-\uffff]", re.DOTALL)
uni_esc_re  = re.compile(r"\\u([0-9a-fA-F]{4})",                                        re.DOTALL)

comments_re = re.compile(r"^\s*;.*$",                                                   re.MULTILINE)


def msgs_only(s) :
    """ Return messages only, stripping comments and leading/trailing white space and blank lines and getting rid of inter-line CRs. """
    s   = "\n".join( [ ln.strip() for ln in re.split(r"\r?\n|\r", s) ] )
    s   = comments_re.sub('', s)
    s   = re.sub("\n{2,}", "\n", s)
    s   = s.lstrip()
    return(s)



def uni_unhex(g) :
    return(unichr(int(g.group(1), 16)))


def _parse_tgc_msg(s) :
    """
        Parse the given string into an array of de-escaped fields.
    """

    ra  = []

    if  s != None :
        s = s.strip(WHITE_SPACE)

        s = re.sub(r"^\010+", "",       s)                              # de-backspace
        s = re.sub(r"[^\r\n]\010", "",  s)
        s = re.sub(r"\010", "",         s)                              # get rid of any that didn't delete previous characters

        s = re.sub(r"\r", "\\x0d", s)
        s = re.sub(r"\n", "\\x0a", s)

        s = s.strip()
        while True :
            s = s.lstrip(WHITE_SPACE)
            if  not len(s)  :   break
            if  s[0] == ';' :   break                                   # ignore comments and blank lines

            fs      = ""
            if  (len(s) >= 2) and (s[0] == '"') and (s[1] == '"') :     # is this field empty - two double quotes?
                s   = s[2:]                                             #   fine, it's a valid field, just really short and remaining text is without the two double quotes

            elif s[0] == '"' :                                          # does this field start with a double quote?
                g   = qstring_re.match(s)                               #   then make the field what's inside the quotes and the rest, the rest
                fs  = g.group(1)                                        #   This does not handle "abc\\" correctly!!!!
                s   = g.group(2)                                        #   It should skip ending quotes with odd number of slashes.

            else :
                g       = word_re.match(s);                             # otherwise, take the next non-spaces/word for the field
                if  g   :
                    fs  = g.group(1)
                    s   = g.group(2)
                else    :
                    fs  = s
                    s   = ""
                pass

            fs  = re.sub(r"\r", "\\r",    fs)
            fs  = re.sub(r"\n", "\\n",    fs)

            fs  = re.sub(r"\\e", "\\033", fs)
            fs  = re.sub(r"\\_", "",      fs)                           # printable character to make a string non-empty, but still be empty (helps in command lines)
            fs  = re.sub(r"\\z", "\\032", fs)

            try :
                fs  = uni_esc_re.sub(uni_unhex, fs)                     # \uXXXX characters force the field to unicode - we really should just always !!!! return the fields as unicode
            except UnicodeDecodeError :                                 # this little dance is only a guess - really, writers need to either write \OOO \uXXXX form text or go all the way with UTF8 at the file read/write level or an emulation thereof - that is give this routine unicode already decoded from utf8 and convert to string without escaping latin1 and unicode chars
                try :
                    fs  = uni_esc_re.sub(uni_unhex, unicode(fs.decode('utf8')))     # less likely to succeed than latin1 and more likely to be in a random file from a human. the caller should have already converted utf8 to unicode on the input to this routine - even though utf8 is less forgiving than latin1, we still don't want to do it first, as latin1 has historical precedence
                except UnicodeDecodeError :
                    fs  = uni_esc_re.sub(uni_unhex, unicode(fs.decode('latin1')))   # we'll let him get away with latin1 characters in the input - but they should have been escaped in \OOO form
                pass

            fs  = fs.replace('\0', r'\0')                               # eval doesn't like nulls

            fs  = eval('u"' + fs + '"')                                 # translate normal, C-escaped characters
            ra.append(fs)

        pass

    return(ra)


def parse_tgc_msg(s) :
    """
        Parse the given string into an array of de-escaped fields.
    """

    try :
        return(_parse_tgc_msg(s))
    except :
        pass
    return([])


def escape_group0(g)    :
    c           = ord(g.group(0))
    if  c < 256 :
        return("\\%03o"  % c)
    return(    "\\u%04x" % c)


def tgc_msg_as_string(tgc_msg, pass_thru_non_ascii = False) :
    """
        Convert an array of strings into a TGC / AMP message string (without ending CR LF).
    """

    if  isinstance(tgc_msg, basestring) :
        tgc_msg = [ tgc_msg]

    msg = ""
    spc = ""
    for s in tgc_msg :
        if  not isinstance(s, basestring) :
            s   = str(s)                            # handle numeric and other fields

        if  pass_thru_non_ascii :
            s   = ps_esc_re.sub(escape_group0, s)
        else    :
            s   = escape_re.sub(escape_group0, s)

        if  (not len(s)) or (s[0] == ';') or qneed_re.search(s) :
            s   = '"' + s + '"'

        msg    += spc + s
        spc     = ' '

    return(msg)




def tgc_msg(msg, pass_thru_non_ascii = False) :
    """
        Convert a string to a TGC/AMP message, or vice versa.
    """

    if  isinstance(msg, ( list, tuple )) :
        return(tgc_msg_as_string(msg, pass_thru_non_ascii = pass_thru_non_ascii))

    return(parse_tgc_msg(msg))



def amp_messages_from_file(fname, encoding = None, safe = False) :
    """
        Get an array of AMP message from a text file.
    """

    if  fname  == None :
        return(None)

    if  hasattr(fname, 'readline') :
        fi      = fname
        fi.seek(0)
    else        :
        fname   = os.path.normpath(fname)
        if  not os.path.isfile(fname) : return(None)
        fi      = open(fname, "r")


    xms     = []
    li      =    fi.readline()
    if  li  :
        #   Read over UTF-8 BOM
        if  li[0:3]    == '\xef\xbb\xbf' :
            li          = li[3:]
            encoding    = 'utf8'

        while True      :
            if encoding :
                li      = unicode(li, encoding)
            if  safe    :
                xm      = parse_tgc_msg(li)
            else        :
                xm      = _parse_tgc_msg(li)
            if  xm and len(xm) :
                xms.append(xm)

            li          = fi.readline()
            if  not li  :       break
            pass
        pass

    if  not hasattr(fname, 'readline') :
        fi.close()

    return(xms)


def amp_messages_to_file(fname, msgs, encoding = None) :
    """
        Write an array of AMP messsages to a text file.
    """

    if  hasattr(fname, 'write') :
        fo      = fname
    else        :
        fname   = os.path.normpath(fname)

        tname   = fname + ".tmp"
        fo      = open(tname, "wt")

    if  encoding == 'utf8':
        fo.write(codecs.BOM_UTF8)

    for msg in msgs :
        ms  = tgc_msg_as_string(msg, encoding and True)
        if  ms :
            if  encoding :
                ms  = ms.encode(encoding)
            fo.write(ms + "\n")
        pass


    if  not hasattr(fname, 'write') :
        fo.close()
        replace_file.replace_file(fname, tname, fname + ".bak")

    pass



def strip_comment_fields(msg) :
    """
        Get rid of any fields that are semi-colon comments.
    """

    return([ f for f in msg if f.lstrip()[0] != ';' ])



#
#
#   Test code.
#
#
if __name__ == '__main__' :

    import  sys

    s   = " now is the time \"for all \" good men  to_come  "
    r   = tgc_msg(tgc_msg(s))
    s   = re.sub(r"\s+", " ", s).replace('\\', '').strip()
    if  r != s :
        raise ValueError("\n[" + s + "]\n[" + r + "]")

    s   = "\b no\017w \r\n\bis th\be time \"for all \" good men  to_come"
    r   = tgc_msg(tgc_msg(s))
    s   = "no\\017w \\015\\012is te time \"for all \" good men to_come"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "\b no\017w \r\n\bis \"\" th\be time \"for all \" \"go\tod\" men  to_come"
    r   = tgc_msg(tgc_msg(s))
    s   = "no\\017w \\015\\012is \"\" te time \"for all \" go\\011od men to_come"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a[\\xe0][\xe0]b"
    r   = tgc_msg(tgc_msg(s))
    s   = "a[\\340][\\340]b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a\\e\\z\\_\\x15ba\\e\\z\\_\\x15ba\\e\\z\\_\\15ba\\e\\z\\_\\15b"
    r   = tgc_msg(tgc_msg(s))
    s   = r"a\033\032\025ba\033\032\025ba\033\032\015ba\033\032\015b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")


    s   = "a\\234\234b"
    r   = tgc_msg(tgc_msg(s))
    s   = unicode(r"a\234\234b", 'latin1')
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = u"a\u1234b a\\u1234b"
    # print         str([ [ len(f), f ]   for f in tgc_msg(s, True) ])

    r   = tgc_msg(tgc_msg(s))
    s   = u"a\\u1234b a\\u1234b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a\u1234b a\\u1234b"
    # print         str([ [ len(f), f ]   for f in tgc_msg(s ) ])

    r   = tgc_msg(tgc_msg(s, True), True)
    s   = u"a\u1234b a\u1234b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a\u1234b a\\u1234b"
    # print         str([ [ len(f), f ]   for f in tgc_msg(s ) ])

    r   = tgc_msg(tgc_msg(s))
    s   = "a\\u1234b a\\u1234b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a\341\210\264b a\\341\\210\\264b"
    # print         str([ [ len(f), f ]   for f in tgc_msg(s) ])
    r   = tgc_msg(tgc_msg(s))
    s   = r"a\341\210\264b a\341\210\264b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = u"a\u1234b".encode('utf8')
    # print         str([ [ len(f), f ]   for f in tgc_msg(s) ])
    r   = tgc_msg(tgc_msg(s))
    s   = r"a\341\210\264b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    s   = "a\341\210\264b".decode('utf8')
    # print         str([ [ len(f), f ]   for f in tgc_msg(s) ])
    r   = tgc_msg(tgc_msg(s))
    s   = "a\\u1234b"
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    r   = tgc_msg( [ ";_not_comment", " another field ", "xy\"za", "", "ender\b", " " ] )
    s   = r'\073_not_comment " another field " xy\042za "" ender\010 " "'
    if  r != s :
        raise ValueError("\n[" + repr(s) + "]\n[" + repr(r) + "]")

    if  strip_comment_fields([ 'This', '  ; BUG ', ' ok ', '; BUG' ]) != [ 'This', ' ok ' ] :
        raise ValueError("strip_comment_fields")

    if  len(sys.argv) > 1 :
        fname   = sys.argv[1]
        xms     = amp_messages_from_file(fname, safe = False)

        print xms

        amp_messages_to_file("x.tmp", xms)

    pass




##      Public things.
__ALL__ = [
            "escape_group0",

            "parse_tgc_msg",
            "tgc_msg_as_string",

            "tgc_msg",

            'amp_messages_from_file',
            'amp_messages_to_file',

            'strip_comment_fields',
          ]


#
#
#
# eof
