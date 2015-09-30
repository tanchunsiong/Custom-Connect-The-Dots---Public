#!/usr/bin/python

# tz_cms50.py
#       --copyright--                   Copyright 2011 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       September 19, 2011      bar
#       September 20, 2011      bar     figure out bottom 4 bits of 3rd byte (dupes of top 4 of 2nd byte, Y value)
#                                       8O1 instead of 8N1 - like PC program
#                                       fix timeouts
#                                       fix > 127 heart rates
#       September 21, 2011      bar     .png file output
#                                       put the sample getting inside the thing
#                                       spin off find_likely_COM_ports() to tz_usb.py
#       September 22, 2011      bar     continue to fight auto-upload and upload in general
#       September 23, 2011      bar     rememmber the a0, b0, c0 cmds that come in every 255th sample in upload
#                                       remember the hr==ox==0 samples
#                                       --verbose
#       September 24, 2011      bar     time stamp the file name of the main wave sample output file
#                                       run the .png file
#                                       auto-restart the com port in case it was yanked
#       September 25, 2011      bar     don't write .dat files and whack empty .plsoxi files after they've been written
#       September 27, 2011      bar     allow no io to be given at create time
#       September 28, 2011      bar     print average wave values or something else
#       September 29, 2011      bar     upload needs slower timeout
#       October 2, 2011         bar     put the USB/serial ids in constants at the top
#       October 4, 2011         bar     write_new_samples when flushing a recording file
#       October 10, 2011        bar     finger samples
#                                       rework sample parsing
#       October 11, 2011        bar     able to restart writing to a new file
#       October 14, 2011        bar     allow simple sample ox of 255 (as in recordings)
#       November 9, 2011        bar     be robust in the face of no pygooglechart installed
#                                       and allow graph with the finger "samples" in there
#       November 9, 2011        bar     try multiplying the low 3 bits of the 1st byte in to the waveform values
#       November 11, 2011       bar     only use one bit from byte 3 as the high bit of the heart rate - ignore the byte 3 high bit
#                                       except that the byte 3 high bit will cause us now to ignore the sample entirely
#       November 13, 2011       bar     try sending an E to the device (another device responds with version info)
#       November 29, 2011       bar     pyflake cleanup
#       May 27, 2012            bar     doxygen namespace
#       --eodstamps--
##      \file
#       \namespace              tzpython.tz_cms50
#
#
#       Communicate with a CMS50E Pulse Oximeter
#
#       Notes:
#
#           When recording, occasionally a USB stream has dropped samples - several. You can see the jump in the waveform.
#           When screen changes happen, ditto.
#           See the note: comments in upload code for information about what the device sends.
#
#       TODO:
#           figure out what the 6 low bits in the 1st byte are
#               0x08 and 0x10 seem to be triggered by valsalva - PC program says "Searching" and flat-lines the waveform display
#               it's the low nibble values of 5, 6, and 7 that come through for no easy-to-understand reason
#           figure out the a0, b0, c0 cmds in upload data
#           figure out what the top 0x30 bits in the 3rd byte are (top 3 bits have been detected set, but the top bit is not necessarily what we make of it (hr + 256))
#           figure out commands to device (use \winbin\portmon on PC - note: cannot run from a net drive)
#               Any byte sent to it seems to turn on USB streaming (f5 and f6 do it - some others did, too)
#
#           Upload from portmon:
#               >> f5 f5            These seem to also be sent out in the middle of the dump from the device
#               << 86 09 01
#               << 47 5f
#               << 86 08 01
#               << 47 5f
#               .
#               .
#               .
#               >> f6 f6 f6
#
#

import  math
import  os
import  re
import  socket
import  sys
import  time
import datetime
import  serial              # from pySerial


import  tz_usb
import  tzlib

from azure.servicebus import ServiceBusService


key_name = "linuxlogger"
key_value = "SdcLrzfc7JMq5Ny+s972ydTwwU98DMBp6slwTXLGx68="

sbs = ServiceBusService("cspi1-ns",shared_access_key_name=key_name, shared_access_key_value=key_value)


USB_VENDOR_ID   = 0x10c4
USB_PRODUCT_ID  = 0xea60


SAMPLE_RATE     = 60


class   a_cms50_exception(Exception) :
        pass

class   a_cms50_timeout_exception(a_cms50_exception) :
        pass                                # there's nothing to be had for now

class   a_cms50_data_exception(a_cms50_exception) :
        pass                                # the data isn't ready yet

class   a_cms50_no_finger_exception(a_cms50_exception) :
        pass                                # a "finger" isn't in the device



class   a_simple_sample(object) :

    p_attrs = [ 'hr', 'ox', ]

    def __init__(me, hr = 0, ox = 0) :
        me.hr   = hr
        me.ox   = ox
        if  (me.ox > 255) :
            raise ValueError("ox:%s" % str(me.ox))
        if  me.hr is None :
            raise ValueError("hr:%s" % str(me.hr))
        pass

    def print_str(me) :
		thisRunWaterMark=datetime.datetime.now()
		timecreated=thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S." + (thisRunWaterMark.strftime("%f")) + "0Z")
		stringtosend2 ="{\"guid\":\"12345\",\"organization\":\"orgname\",\"timecreated\":\""+timecreated+"\",\"displayname\":\"displayname\",\"location\":\"locn\",\"measurename\":\"oxygen\",\"unitofmeasure\":\"%\",\"value\":"+str(me.ox)+"}";
		stringtosend3 ="{\"guid\":\"12345\",\"organization\":\"orgname\",\"timecreated\":\""+timecreated+"\",\"displayname\":\"displayname\",\"location\":\"locn\",\"measurename\":\"heartrate\",\"unitofmeasure\":\"bpm\",\"value\":"+str(me.hr)+"}";
		#modifysendstring( accesssendstring()+stringtosend2+stringtosend3)
		#sbs.send_event('ehdevices',stringtosend2);
		#sbs.send_event('ehdevices',stringtosend3);
		
		return("%s\n%s" % (stringtosend2, stringtosend3 ) )

    def __str__(me) :
        aa      = [ getattr(me, atr, None) for atr in me.p_attrs ]
        return(repr(aa))

    #   a_simple_sample



class   a_finger_sample(a_simple_sample) :

    p_attrs = [ 'on', 'when', ]

    def __init__(me, on = False, when = None) :
        me.when = when or time.time()
        me.on   = on

    def print_str(me) :
        return("Finger %s %f %s" % ( ((me.on and "on") or "off"), me.when, time.strftime('"%H:%M:%S %b %d, %Y"', time.localtime(me.when)), ) )

    #   a_finger_sample

counter = 0

def accesscounter():
  return counter
  # This returns whatever the global value of 'x' is

def modifycounter(var):
  global counter
  counter = var
  return counter
  # This function makes the global 'x' equal to 'modified', and then returns that value

sendstring = ""

def accesssendstring():
  return sendstring
  # This returns whatever the global value of 'x' is

def modifysendstring(var):
  global sendstring
  sendstring = var
  return sendstring
  # This function makes the global 'x' equal to 'modified', and then returns that value

class   a_full_sample(a_simple_sample) :

    csv_header  = '"Sample", "Beat", "Value", "Oxi%", "BPM", "?b1", "?b3hi"'

    p_attrs     = a_simple_sample.p_attrs + [ 'num', 'y', 'beat', 'bc', 'ac', ]

    def __init__(me, hr = 0, ox = 0, num = 0, y = 0, beat = False, bc = 0, ac = 0) :
        super(a_full_sample, me).__init__(hr = hr, ox = ox)
        me.num  = num
        me.y    = y
        me.beat = beat

        me.bc   = bc            # low 6 bits of 1st byte
        me.ac   = ac            # 0x30 bits of 3rd byte

        # me.y    = ((me.y) * ((me.bc & 0xf) + 1)) / 4.5

    def csv_str(me) :
        return("%d, %s, %d, %d, %d, %d, %d"             % ( me.num, ((me.beat and '"B"') or ''),  me.y, me.ox, me.hr, me.bc, me.ac, ) )


    def print_str(me) :
		
		
		#if (accesscounter()>=50):
		thisRunWaterMark=datetime.datetime.now()
		timecreated=thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S." + (thisRunWaterMark.strftime("%f")) + "0Z")
		stringtosend ="{\"guid\":\"12345\",\"organization\":\"orgname\",\"timecreated\":\""+timecreated+"\",\"displayname\":\"displayname\",\"location\":\"locn\",\"measurename\":\"heartgraph\",\"unitofmeasure\":\"unit\",\"value\":"+str(me.y)+"}";
		#sbs.send_event('ehdevices',stringtosend);
		#modifysendstring( accesssendstring()+stringtosend)
		#print(accesssendstring());
		#modifycounter(0)
		#modifysendstring("")
		#else:
		#if (accesscounter()==1):
		#	modifysendstring("[")
		#thisRunWaterMark=datetime.datetime.now()
		#timecreated=thisRunWaterMark.strftime("%Y-%m-%dT%H:%M:%S." + (thisRunWaterMark.strftime("%f")) + "0Z")
		#stringtosend ="{\"guid\":\"12345\",\"organization\":\"orgname\",\"timecreated\":\""+timecreated+"\",\"displayname\":\"displayname\",\"location\":\"locn\",\"measurename\":\"heartgraph\",\"unitofmeasure\":\"unit\",\"value\":"+str(me.y)+"}\n";
		#modifysendstring( accesssendstring()+stringtosend)
		#modifycounter(accesscounter()+1)
		return(stringtosend+"\n%s"    % ( super(a_full_sample, me).print_str() ) )

    #   a_full_sample


def _parse_sample(s) :
    try :
        return(eval(s))
    except ( TypeError, ValueError ) :
        pass
    return(None)

def _create_sample(aa, cls) :
    if  len(aa) == len(cls.p_attrs) :
        kwargs  = dict(zip(cls.p_attrs, aa))
        try :
            return(cls(**kwargs))
        except ( TypeError, ValueError ) :
            pass
        pass
    return(None)


def parse_sample(s) :
    aa  = _parse_sample(s)
    ss  = _create_sample(aa, a_full_sample) or _create_sample(aa, a_simple_sample) or _create_sample(aa, a_finger_sample)
    return(ss)


class   a_recording(object) :

    FILE_EXT            = ".plsoxi"

    def __init__(me, tm = None, samples = [], fd = "") :
        if  tm is None  :
            tm          = time.time()
        me.tm           = tm
        me.samples      = samples or []                             # a_???_sample()s
        me.fd           = fd      or ""                             # raw data
        me.fo           = None                                      # file we are outputting to, if any

    def forget_old_samples(me, how_many) :
        how_many        = max(0, int(how_many))
        me.samples      = me.samples[how_many:]                     # let's not run out of memory if this thing runs for days
        if  me.fo       :
            me.wfsi     = max(0, me.wfsi - how_many)
        pass

    def append(me, sample) :
        me.samples.append(sample)

    def tm_str(me) :
        if  me.tm < 3600 * 24 * 365 :
            tm  = me.tm % ( 3600 * 24 )
            return("%02u:%02u" % ( tm / 3600, (tm / 60) % 60 ) )    # hour:minute
        return(time.strftime('"%H:%M:%S %b %d, %Y"', time.localtime(me.tm)))


    def flush_file(me) :
        me.write_new_samples()
        if  me.fo :
            me.fo.flush()
        pass

    def write_new_samples(me) :
        if  not me.fo :
            return(False)

        nsc         = len(me.samples)
        cnt         = nsc   - me.wfsi
        for sa in me.samples[me.wfsi:nsc] :
            if  me.wfna    != sa.p_attrs :
                me.wfna     = sa.p_attrs
                me.fo.write("fields %s\n" % str(me.wfna))
            me.fo.write("s %s\n" % str(sa))
        me.wfsc    += cnt
        me.wfsi     = nsc
        return(cnt)

    def close_write_file(me) :
        if  me.fo   :
            me.write_new_samples()
            me.fo.close()
            me.fo   = None
            if  not me.wfsc :
                os.remove(me.fn)                        # whack the file if there were no samples written
            return(True)
        return(False)

    def open_write_file(me, fn, only_new_samples = False) :
        me.close_write_file()

        me.wfsi     = (only_new_samples and len(me.samples)) or 0
        me.wfsc     = 0
        me.wfna     = []
        me.fn       = os.path.splitext(fn)[0] + me.FILE_EXT         # force the proper ext (?)

        me.fo       = output_files.a_file(me.fn)
        me.fo.write("tm %u %s\n\n" % ( me.tm, me.tm_str() ) )
        return(me.fn)


    def write_file(me, fn) :
        fn      = me.open_write_file(fn)
        if  me.close_write_file() :
            return(fn)
        return(None)


    @staticmethod
    def parse(fd) :
        samples = [ parse_sample(li[2:]) for li in re.split(r"\r?\n", fd) if li and li.startswith("s ") ]
        samples = [ sa for sa in samples if sa ]
        if  len(samples) :
            g   = re.search(r"\ntm (\d+)", fd)
            if  g :
                tm  = int(g.group(1))
                return(a_recording(tm, samples))
            pass

        return(None)


    @staticmethod
    def parse_file(fn) :
        fd  = tzlib.read_whole_text_file(fn)
        return(a_recording.parse(fd))

    #   a_recording



class   a_comm :

    def __init__(me, io = None, timeout = 0.01) :
        me.io           = io
        me.timeout      = timeout
        me.ibuf         = ""
        me.scnt         = 1
        me.rx_when      = tzlib.elapsed_time() - 10000.0
        me.data         = []                    # queue of a_recording's driven by data coming in from the device

        if  not me.io   :
            me.reopen()
        pass


    def rx(me, how_many = 1) :
        try :
            return(me.io.read(how_many))
        except ( serial.SerialException, serial.serialutil.SerialException, OSError, IOError, AttributeError ) :
            pass
        return('')


    def read(me, how_many = 1, timeout = None) :
        timeout         = timeout or me.timeout

        t               = nt    = tzlib.elapsed_time()
        r               = ""
        while True :
            rr          = me.ibuf[:how_many]
            me.ibuf     = me.ibuf[how_many:]
            how_many   -= len(rr)
            rc          = len(rr)
            r          += rr
            if  not how_many :
                break

            rr          = me.rx(how_many)
            how_many   -= len(rr)
            rc         += len(rr)
            r          += rr
            if  not how_many :
                break


            if  rc      :
                t       = nt

            if  nt - t >= timeout :
                if  len(r) :
                    break
                raise a_cms50_timeout_exception("read")

            nt          = tzlib.elapsed_time()

            if  not rc  :
                time.sleep(min(0.1, timeout / 2.0))
            pass

        # print "rxing", len(r), "%04x" % ( len(r) ), hexify(r)

        return(r)



    def read_upload(me, progress_rtn = None, verbose = 0) :
        timeout     = 10
        while True  :
            try     :
                r   = me.read(1, timeout = timeout)
                timeout = 0.1
                a1  = me.read(1, timeout = timeout)
                a2  = me.read(1, timeout = timeout)
                cmd = ord(r)
                if  (cmd == 0xf2) and (ord(a1) & 0x80) :
                    me.ibuf = r + a1 + a2 + me.ibuf
                    break
                elif cmd == 0xf0 :
                    raise a_cms50_data_exception("No upload header")
                else :
                    me.ibuf = a1 + a2 + me.ibuf
            except ( a_cms50_exception, a_cms50_timeout_exception, ) :
                return(None)
            pass

        fd          = ""
        tm          = 0
        prv         = 0
        mxc         = 10000000
        samples     = []
        while True  :
            try     :
                r   = me.read(1, timeout = timeout) + me.read(1, timeout = timeout) + me.read(1, timeout = timeout)
                cmd = ord(r[0])
                hr  = ord(r[1])
                ox  = ord(r[2])
                if  not (cmd & 0x80) :
                    # print "@@@@ bad cmd %02x:%02x:%02x" % ( cmd, ord(r[1]), ord(r[2]) )
                    break

                sa  = None

                if  (not hr) and (not ox) :
                    # a = hr | (ox << 8)
                    # print "@@@@ @%u toss out msg: 2nd/3rd no hi bit cmd %02x arg=%02x:%02x d=%d x=%04x" % ( len(fd) / 3, cmd, hr, ox, a, a )
                    sa  = a_full_sample(hr, ox, bc = cmd)
                    r   = ""                                        # this may be a bug in the device. not sure. not sure whether tis correct to toss the data out of mxc tracking. Too, a ox of 0xff came up in a recording that had 6 extra samples even after this, which happened at 255-bytes in.
                elif cmd == 0xf2 :
                    tm  = 60 * ((60 * (hr & 0x1f)) + ox)
                    prv = 0xf2
                else    :
                    if  prv == 0xf2 :
                        mxc = ((cmd & 0x3f) << 14) | ((hr & 0x7f) << 7) | ox
                        # print "@@@@ @%u mxc=%u %02x:%02x:%02x" % ( len(fd), mxc, cmd, hr, ox, )
                        mxc = mxc + len(fd) - 9
                    elif ((cmd & 0xf0) != 0xf0) :
                        # a         = hr | (ox << 8)
                        # print "@@@@ info@%u: cmd %02x arg=%02x:%02x le:%d:0x%04x" % ( len(fd), cmd, hr, ox, a, a )
                        if  (cmd   == 0x80) and (len(fd) + 3 >= mxc) :
                            me.ibuf = r + me.ibuf
                            r       = ""                                # !!!! kludge to remove ending, regular, 5-byte samples
                            mxc    -= 3
                        elif (cmd  == 0x80) and (hr == 0) :
                            sa      = a_full_sample(hr, ox, bc = cmd)
                            mxc    -= 3                                 # !!!! is this sample a reflection of a glitch in the recording? and, if so, why doesn't the byte count reflect it? (or does it mark something? or what?)
                        else        :
                            sa      = a_full_sample(hr, ox, bc = cmd)   # note: every 256th sample (after the 1st, 253rd - 256, including the two F2 and the 8x length "samples") is one of these - cmds are in [ 0xa0, 0xb0, 0xc0, ], hr and oxi are normal
                        pass
                    else    :
                        hr          = ((cmd & 0x3) << 7) | (hr & 0x7f)
                        sa          = a_simple_sample(hr, ox)           # note: in each 256 sample batch, the 85th sample and the 170th sample are ox==255
                    prv = cmd

                if  sa  :
                    samples.append(sa)

                fd += r
                if  progress_rtn :
                    progress_rtn(len(fd), mxc)

                if  len(fd) >= mxc :
                    # print "@@@@ ctmxc", len(fd), mxc
                    break
                pass
            except ( a_cms50_exception, a_cms50_timeout_exception, ) :
                # print "@@@@ timeout"
                break
            pass

        if  progress_rtn :
            progress_rtn(len(fd), len(fd))

        # print "@@@@", len(fd), "of", mxc, "   ", len(fd) / 3, "msgs of", (mxc + 2) / 3

        return(a_recording(tm = tm, samples = samples, fd = fd))



    def read_sample(me, progress_rtn = None, verbose = 0, mismatch_callback = None) :
        s       = None
        try     :
            b           = ord(me.read())
            me.rx_when  = tzlib.elapsed_time()

            if  b  == 128 :
                ba  = [ b ]
                t   = me.rx_when
                while (len(ba) < 5) and (t - me.rx_when < 0.1) :
                    t   =   tzlib.elapsed_time()
                    ba.append(ord(me.read()))

                me.scnt    += 1

                if  False and (ba[1] in [ 0, 0xff ]) :              # 321390_Kanograf_(8400).pdf
                    if  len(ba) == 5 :
                        print "@@@@ %02x:%02x:%02x:%02x:%02x" % ( ba[0], ba[1], ba[2], ba[3], ba[4] )
                    else    :
                        print "@@@@", str(ba)
                    pass

                raise a_cms50_no_finger_exception

            if  b   < 128 :
                # print "@@@@ toss read %02x" % b
                pass
            else    :
                y   = ord(me.read())
                ay  = ord(me.read())

                if  (b == 0xf2) and (y & 0x80) :
                    me.ibuf = chr(b) + chr(y) + chr(ay) + me.ibuf
                    dt      = me.read_upload(progress_rtn = progress_rtn, verbose = verbose)
                    if  dt  :
                        me.data.append(dt)

                    return(None)

                hr  = ord(me.read())
                if  (ay == 0xf2) and (hr & 0x80) :
                    me.ibuf = chr(ay) + chr(hr) + me.ibuf
                    dt      = me.read_upload(progress_rtn = progress_rtn, verbose = verbose)
                    if  dt  :
                        me.data.append(dt)

                    return(None)

                hr |= ((ay & 0x40) << 1)

                ox  = ord(me.read())

                if  ay & 0x80 :
                    # me.ibuf = chr(ay) + chr(hr) + chr(ox) + me.ibuf       # note: the few times this has happened have not indicated that this is a good idea - nor that interpreting the ay|hr|ox bytes as uploaded data is a good idea
                    return(None)                                            # punt as best we can

                bc  = (b & ~(64 | 128))
                ac  = ay >> 4
                # print "@@@@ %02x" % b, hr, ox, me.scnt, y, ay, bc, ac
                s   = a_full_sample(hr, ox, me.scnt, y, ((b & 64) and True) or False, bc = bc, ac = ac & 3)

                if  (ay & 0x0f) != (y / 8) :            # apparently, these 4 bits are a dupe of the top 4 or the 7 bits in "y" - let's force that to be so - crashes when device dumps memory
                    # print "@@@@ b=%02x ay & 0xf != y/8  ay:0x%02x != y:0x%02x" % ( b, ay, y )           # can happen if upload is starting
                    if  mismatch_callback :
                        mismatch_callback(s, b, ay)     # tell the caller this happened if he wants to know
                    s       = None

                me.scnt    += 1
            pass

        except ( a_cms50_exception, a_cms50_timeout_exception, ) :
            if  tzlib.elapsed_time() - me.rx_when > 0.5 :
                me.scnt     = 1
            raise

        return(s)



    def close(me)   :
        if  me.io   :
            c       = me.io
            me.io   = None
            try     :
                c.close()
            except socket.error :
                raise a_cms50_exception("Close error!")
            pass
        pass



    def blind_close(me) :
        try :
            me.close()
        except a_cms50_exception :
            pass
        pass


    def reopen(me, port = None) :
        me.blind_close()

        if  not port :
            port    = tz_usb.find_likely_COM_ports(vendor_id = USB_VENDOR_ID, product_id = USB_PRODUCT_ID)
            if  port :
                port    = port[0]
            pass

        if  not port :
            return(None)

        try :
            port    = int(port)
            cport   = port - 1
        except ValueError :
            cport   = port

        try :
            me.io   = serial.Serial(port = cport, baudrate = 19200, parity = "O", timeout = 0.001)                # note: PC program sets 8O1. serial.Serial() multiplies timeout by 1000 before passing to windows (This 1 mill is minimum for windows. I don't know about other OS's.)
        except serial.SerialException :
            return(False)

        return(True)


    def start_usb(me) :
        try     :
            me.io.write("\xf5")                             # try to get the USB streaming going again in case it's off
        except ( OSError, IOError, AttributeError, serial.SerialException ) :
            me.reopen()
        pass

    pass        # a_comm



def _program_version_str(ident) :
    return("V" + re.sub(r".*<program_version>([\d\.]+)</program_version>.*", r"\1", ident))



def get_output_file_name(ofile_name, program_name = None, ext = a_recording.FILE_EXT) :
    if  not ofile_name :
        ofile_name  = os.path.basename(program_name or __file__)
    ofile_name      = os.path.splitext(ofile_name)[0] + ("_%010u%s" % ( int(time.time()), ext ))

    return(ofile_name)


def hms(t) :
    it  = int(t)
    return("%2u:%02u:%04.1f" % ( it / 3600, (it / 60) % 60, t - ((it / 60) * 60) ) )




class   a_progress_rtn(object) :
    def __init__(me) :
        me.pc   = -1
        me.sh   = False

    def show_progress(me, how_many, to_do) :
        pc  = (100  * how_many) / max(1, to_do)
        if  me.pc  != pc :
            me.pc   = pc
            if  how_many != to_do :
                me.sh   = True
                sys.stdout.write("%3u%%\r" % me.pc)
                sys.stdout.flush()
            elif me.sh :
                sys.stdout.write('%3u%%\n' % me.pc)
                sys.stdout.flush()
            pass
        pass

    #   a_progress_rtn


def main(ident) :
    import      TZCommandLineAtFile
    import      TZKeyReady
    try :
        import  tz_google_chart
        import  tz_browser
    except ImportError :
        tz_google_chart = None


    if  ident :
        sys.argv.insert(1, ident)
        sys.argv.insert(1, '--ident')

    program_name    = sys.argv.pop(0)

    TZCommandLineAtFile.expand_at_sign_command_line_files(sys.argv)


    ident       = ""
    port        = 0             # my COM port, not yours
    port_list   = 0
    verbose     = 0


    help_str    = """
%s (options) (output_files_base_name)

    I get the streaming data from a CMS50E Pulse Oximeter.

Options:

    --port  port_number     Set the COM port number
    --port_list             List possible ports (twice, list all available ports)
    --version               Print the program version number.


""" % ( os.path.basename(program_name) )


    oi  = tzlib.array_find(sys.argv, [ "--help", "-?", "?", "-h", "/h", "/?", "?" ] )
    if  oi >= 0 :
        print help_str
        sys.exit(254)


    while True :
        oi  = tzlib.array_find(sys.argv, [ "--ident", "-i" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        if  (oi >= len(sys.argv)) or not len(sys.argv[oi]) :
            print "Program IDENT info not given!"
            sys.exit(101)
        ident       = sys.argv.pop(oi)


    while True :
        oi  = tzlib.array_find(sys.argv, [ "--version", "-v" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        print "version", _program_version_str(ident)
        if  not sys.argv :
            sys.exit(0)
        pass


    while True :
        oi  = tzlib.array_find(sys.argv, [ "--port", "-p" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        if  (oi >= len(sys.argv)) or not len(sys.argv[oi]) :
            print "No COM port given!"
            sys.exit(102)
        port        = sys.argv.pop(oi)


    while True :
        oi  = tzlib.array_find(sys.argv, [ "--port_list" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        port_list  += 1

    while True :
        oi  = tzlib.array_find(sys.argv, [ "--verbose" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        verbose    += 1



    ofile_name      = None
    if  len(sys.argv) >= 1 :
        ofile_name  = sys.argv.pop(0)

        if  ofile_name.startswith('-') :
            print "Put the whole path or a dot/slash before the output file name. Dashes are confusing: [%s]" % ofile_name
            sys.exit(104)

        pass

    if  len(sys.argv) :
        print "I don't understand %s (--help for options)!" % ( sys.argv )
        sys.exit(104)



    if  port_list :
        tz_usb.find_likely_COM_ports(vendor_id = USB_VENDOR_ID, product_id = USB_PRODUCT_ID, list_level = port_list)


    if  not port :
        port    = tz_usb.find_likely_COM_ports(vendor_id = USB_VENDOR_ID, product_id = USB_PRODUCT_ID)
        if  port :
            print   "Using port", port[0],
            if  len(port) > 1 :
                print "Found ports", port,
            print
            port    = port[0]
        pass

    if  not port :
        print "Please tell me a COM port to use with the --port option (e.g. --port 2 )!"
        sys.exit(103)

    try :
        port    = int(port)
        cport   = port - 1
    except ValueError :
        cport   = port

    try :
        io  = serial.Serial(port = cport, baudrate = 19200, parity = "O", timeout = 0.001)                # note: PC program sets 8O1. serial.Serial() multiplies timeout by 1000 before passing to windows (This 1 mill is minimum for windows. I don't know about other OS's.)
    except serial.SerialException :
        print "Port %s [%s] cannot be opened!" % ( str(port), str(cport) )
        sys.exit(111)

    me      = a_comm(io)

    samples = a_recording()

    if  ofile_name :
        if  os.path.splitext(ofile_name)[1].lower() == ".csv" :
            fo  = output_files.a_file(ofile_name)
            fo.write(a_full_sample.csv_header + "\n")
        else    :
            fo  = None
            fn  = get_output_file_name(ofile_name, program_name = program_name)
            print "Outputting to: ", samples.open_write_file(fn)
        pass

    prg     = a_progress_rtn()
    stopped = 1000
    finger  = False
    lay     = []
    mx      = -10000
    mn      =  10000
    msa     = [ 64 ] * 300
    mss     = float(sum(msa))
    ts      = tzlib.elapsed_time()
    rx_when = ts
    png_drs = [ 7.5, 15.0, 30.0, 60.0, 120.0, 10 * 60.0, 15 * 60.0, 60 * 60.0, 2 * 60 * 60.0, 6 * 60 * 60.0, 12 * 60 * 60.0, ]
    png_di  = 0
    sb      = 0xf5

    me.start_usb()              # in case he's not turned it on (though we'll do this every half second of silence from the device, anyway

    print "Type ? for help"

    while True :
        try :
            s       = me.read_sample(progress_rtn = prg.show_progress, verbose = verbose)
            if  s   :
                yy  = s.y

                if  False :
                    msa.append(s.y)
                    mss        += s.y
                    mss        -= msa[0]
                    del(msa[0])
                else            :
                    mss         = 64
                if  False       :
                    yy          = ((s.y) * ((s.bc & 0xf) + 1)) / 4.5        # tends to flatten out in the middle when there is a change to low amplitude waves
                    if  False :
                        if  yy  < 0 :
                            yy  = -math.log(-yy + math.e)
                        else    :
                            yy  =  math.log( yy + math.e)
                        pass
                    pass

                mx  = max(mx, yy)
                mn  = min(mn, yy)

                if  s.ac & 3 :
                    print "@@@@ ac=%u" % s.ac
                    lay.append(s.ac)

                if  not  finger :
                    samples.append(a_finger_sample(True))
                samples.append(s)
                if  ofile_name  :
                    if  fo      :
                        fo.write("%s\n" % s.csv_str())
                    samples.write_new_samples()
                ys      = (' ' * int((100.0 * (yy - mn)) / max(1.0, (mx - mn)))) + '*'
                # avya  = [ ox for ox in samples.samples[-5 * SAMPLE_RATE : ] if hasattr(ox, 'y') ]
                # avy   = sum([ ox.y for ox in avya ]) / float(max(1, len(avya)))
				#dreamtcs might want to skip this
                print ( s.print_str() )               # (100.0 * yy) / (yy + (s.bc & 0xf)), ys )

                if  not finger :
                    finger  = True
                    samples.flush_file()
                    print "Finger"
                stopped = max(stopped - 10, 0)

                if  len(samples.samples) > png_drs[-1] * SAMPLE_RATE * 2 :
                    samples.flush_file()
                    samples.forget_old_samples(png_drs[-1] * SAMPLE_RATE)
                rx_when = tzlib.elapsed_time()
            t   = tzlib.elapsed_time()
            if  t - ts > 59 :
                ts  = t
                samples.flush_file()
            pass
        except   a_cms50_no_finger_exception :
            if  finger  :
                finger  = False
                samples.append(a_finger_sample(False))
                print "No finger"
                samples.flush_file()
            pass
        except   a_cms50_data_exception, msg :
            samples.flush_file()
            print msg                                   # those bits are not, apparently, dupes of each other
            if  not stopped :
                sys.exit(199)
            stopped    -= 1
        except ( a_cms50_exception, a_cms50_timeout_exception, ) :
            t   = tzlib.elapsed_time()
            if  t - rx_when > 0.5 :
                rx_when = t
                ts      = t
                mx      = -10000
                mn      =  10000
                samples.flush_file()
                me.start_usb()
            pass

        if  len(me.data) :
            samples.flush_file()
            while len(me.data) :
                dt  = me.data.pop(0)
                # print "@@@@", len(dt.samples), len(dt.fd), "at", dt.tm / 3600, (dt.tm / 60) % 60
                if  len(dt.samples) :
                    fn  = get_output_file_name(ofile_name, program_name = program_name, ext = ".dat")
                    # tzlib.write_whole_binary_file(fn, dt.fd)
                    dfn = dt.write_file(fn)
                    if  not dfn :
                        print "Probably no data to write, so file not written."
                    else :
                        print "Wrote driven upload to", fn, "and", dfn, len(dt.samples)
                    pass
                pass
            mx      = -10000
            mn      =  10000
            ts      = tzlib.elapsed_time()
            stopped = 1000

        k   = TZKeyReady.key_ready()
        if  k :
            print

            if  k in [ 'q', ] :
                break

            if  k == '?' :
                if  tz_google_chart :
                    pcmd    = ("""
p       Write .png file showing graph to a file named like %s.
        And write %s file with graphed data.
""" % ( get_output_file_name(ofile_name, program_name = program_name, ext = ".png"), a_recording.FILE_EXT, ) ).rstrip()
                else :
                    pcmd    = ("""
p       Write %s file with latest data.
""" % (                                                                              a_recording.FILE_EXT, ) ).rstrip()
                print ("""
q       Quit.
ESC     Quit.
?       Help.
r       Reset some values.
+       Up    the .png duration - currently %s
-       Lower the .png duration.%s
d       Wait for data upload to write to %s file.

""") % ( hms(png_drs[png_di]), pcmd, a_recording.FILE_EXT )
                print "ymx=%d ymn=%d lay=%s %.1f samples per second" % ( mx, mn, str(lay), me.scnt / max(1, (tzlib.elapsed_time() - ts)) )       # 60 per second

            if  k == 'r' :
                samples.flush_file()
                mx      = -10000
                mn      =  10000
                ts      = tzlib.elapsed_time()
                lay     = []
                me.scnt = 1

            if  k == 'd' :
                samples.flush_file()
                stopped = 1000
                fn      = get_output_file_name(ofile_name, program_name = program_name, ext = ".dat")
                print "Uploading to", fn
                dt      = me.read_upload(progress_rtn = prg.show_progress, verbose = verbose)
                # print "@@@@", len(fd), "at", tm / 3600, (tm / 60) % 60
                if  dt and len(dt.samples) :
                    # tzlib.write_whole_binary_file(fn, dt.fd)
                    dfn = dt.write_file(fn)
                    if  not dfn :
                        print "Probably no data to write, so file not written."
                    else :
                        print "Wrote upload to", fn, "and", dfn, len(dt.samples)
                    pass
                else    :
                    print "Failed to upload."
                pass


            if  k == 'E' :
                print "Sending E"
                me.io.write("E")
            if  k == 'F' :
                print "Sending F"
                me.io.write("F")
            if  k == 'G' :
                print "Sending G"
                me.io.write("G")
            if  k == 'H' :
                print "Sending H"
                me.io.write("H")

            if  k == 's' :
                if  False :
                    me.io.write(chr(sb))
                    print "s %02x:%u" % ( sb, sb )
                    sb -= 1
                    if  sb  < 0 :
                        sb  = 255
                    pass
                else :
                    me.io.write("\xf5\xf5")
                pass

            if  k == 'S' :
                if  False :
                    me.io.write(chr(sb))
                    print "s %02x:%u" % ( sb, sb )
                    sb += 1
                    if  sb  > 255 :
                        sb  = 0
                    pass
                else :
                    me.io.write("\xf6\xf6\xf6")
                pass


            if  k in [ '+', '=' ] :
                png_di  = min(len(png_drs) - 1, png_di + 1)
                print ".png duration %s" % hms(png_drs[png_di])
            if  k in [ '-', '_' ] :
                png_di  = max(0, png_di - 1)
                print ".png duration %s" % hms(png_drs[png_di])
            if  k == 'p' :
                if  (len(samples.samples) > 60) and (mn < mx) :
                    fn  = get_output_file_name(ofile_name, program_name = program_name, ext = ".png")

                    sma = [ sa for sa in samples.samples if hasattr(sa, 'ox') ]
                    tw  = min(int(png_drs[png_di] * SAMPLE_RATE), len(sma))
                    sma = sma[len(sma) - tw : ]

                    if  not len(sma) :
                        "No data to write/graph"
                    else :
                        dt  = a_recording(samples = sma)
                        dfn = dt.write_file(fn)
                        if  not dfn :
                            print "Probably no data to write, so file not written."
                        else :
                            print "Wrote %s" % dfn

                        if  tz_google_chart :
                            def png_y(x) :
                                return(sma[x].y)
                            def png_hr(x) :
                                return(sma[x].hr)
                            def png_ox(x) :
                                return(sma[x].ox)

                            mso = "SPo2 %u..%u" % ( min([ sa.ox for sa in sma ]), max([ sa.ox for sa in sma ]) )
                            msb =  "BPM %u..%u" % ( min([ sa.hr for sa in sma ]), max([ sa.hr for sa in sma ]) )

                            png = tz_google_chart.get_chart(("CMS50E wave %s" % time.strftime("%H:%M:%S %b %d, %Y")),
                                                            width   = 600,
                                                            hite    = 400,
                                                            tnames  = [ " ", mso, msb, " ", ],
                                                            lnames  = [ '0', '64', '128' ],
                                                            bnames  = [ "%.1f" % (((len(sma) / SAMPLE_RATE) * i) / 10.0) for i in xrange(11) ],
                                                            xfunc   = range(tw),
                                                            yfuncs  = [ png_y, ],
                                                            ymin    = 0,
                                                            ymax    = 128
                                                           )        # note: can be only 300,000 pixels or smaller
                            if  png :
                                tz_google_chart.write_chart(fn, png)
                                print "Wrote %s" % fn
                                tz_browser.start_file(fn)
                            pass
                        pass
                    pass
                pass

            pass
        pass

    if  ofile_name  :
        if  fo      :
            fo.close()
        samples.close_write_file()

    me.blind_close()


if  __name__ == '__main__' :

    main("")


#
#
# eof
