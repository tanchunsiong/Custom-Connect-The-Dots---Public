#!/usr/bin/python

# tz_usb.py
#       --copyright--                   Copyright 2011 (C) Tranzoa, Co. All rights reserved.    Warranty: You're free and on your own here. This code is not necessarily up-to-date or of public quality.
#       --url--                         http://www.tranzoa.net/tzpython/
#       --email--                       pycode is the name to send to. tranzoa.com is the place to send to.
#       --bodstamps--
#       September 21, 2011      bar     spin off from two files
#       November 8, 2011        bar     use linux /dev area to do the search
#       November 9, 2011        bar     gosh, why not debug those new typos a little?
#       November 29, 2011       bar     pyflake cleanup
#       March 13, 2012          bar     allow finds by serial number, too
#       May 27, 2012            bar     doxygen namespace
#       June 16, 2012           bar     just fail to return any names if win32api, et el are not there
#       September 24, 2012      bar     catch an exception under windows when an ftdi driver is not installed on the pc
#       February 20, 2015       bar     get that serial number filtering logic back in to the 2nd half of the linux find-port logic
#       May 14, 2015            bar     find ACM devices
#                                       allow devices to not have serial numbers
#       --eodstamps--
##      \file
#       \namespace              tzpython.tz_usb
#
#
#       USB stuff.
#
#

import  glob
import  os
import  re
import  sys

have_win32                  = False
usb                         = None
if  sys.platform == 'win32' :

    try :
        import  win32api
        import  win32con
        import  pywintypes
    except ImportError :
        win32api            = None
    pass

else :

    try :
        import  usb
    except ImportError :
        usb                 = None
    pass


import  tzlib



def find_likely_USB_ports(vendor_id = None, product_id = None, serial_number = None, list_level = 0) :
    """
        Return an array of COM# or /dev/tty(USB|ACM)# names of appropriate ports.

        There is probably an API to do this, but finding it and using it seems to be really something.
    """

    ports   =   []

    if  sys.platform == 'win32' :

        def get_all_usb_friendly_names() :
            """
                There is probably an API to do this, but finding it and using it seems to be really something.
            """

            if  not win32api :
                return([])

            regx    = re.compile("Vid_([0-9a-f]+)\&Pid_([0-9a-f]+)", re.IGNORECASE)

            def search_keys(nms, rdy, k, n, snm) :
                try :
                    if  not rdy             :
                        ( obj, val )        = win32api.RegQueryValueEx(k, r"HardwareID")
                        g                   = regx.search(str(obj))
                        # print "@@@@", snm, serial_number
                        if  g and ((vendor_id is None) or (int(g.group(1), 16) == vendor_id)) and ((product_id is None) or (int(g.group(2), 16) == product_id)) and ((serial_number is None) or (snm.lower() == str(serial_number).lower())) :
                            ( obj, val )    = win32api.RegQueryValueEx(k, r"FriendlyName")                          # just make sure it's there nowadays
                            rdy             = True
                        pass
                    else :
                        ( obj, val )        = win32api.RegQueryValueEx(k, r"PortName")
                        nms.append(str(obj))

                        return

                    pass
                except pywintypes.error :
                    # e   = sys.exc_info()
                    # print "fnam", e[0], e[1], n
                    pass


                i   = 0
                while True :
                    try :
                        kn  = "....."
                        s   = win32api.RegEnumKey(k, i)

                        kn  = n + "\\" + s
                        sk  = win32api.RegOpenKey(k, s, win32con.KEY_ENUMERATE_SUB_KEYS | win32con.KEY_READ)

                        search_keys(nms, rdy, sk, kn, s)

                        win32api.RegCloseKey(sk)
                    except pywintypes.error :
                        # e   = sys.exc_info()
                        # print "fnam", e[0], e[1], n
                        break

                    i      += 1

                pass


            nms = []
            for n in [ r"SYSTEM\CURRENTCONTROLSET\ENUM\USB", r"SYSTEM\CURRENTCONTROLSET\ENUM\FTDIBUS" ] :
                try :
                    k   = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, n, win32con.KEY_ENUMERATE_SUB_KEYS + win32con.KEY_READ)
                    search_keys(nms, False, k, n, None)
                    win32api.RegCloseKey(k)
                except pywintypes.error :
                    pass
                pass

            return(nms)


        ports   = get_all_usb_friendly_names()

    else    :

        dvs = glob.glob('/sys/bus/usb/devices/*')
        for dn in dvs :
            try     :
                vid = int(tzlib.safe_read_whole_text_file(os.path.join(dn, "idVendor" )).strip(), 16)
                pid = int(tzlib.safe_read_whole_text_file(os.path.join(dn, "idProduct")).strip(), 16)
                snm =    (tzlib.safe_read_whole_text_file(os.path.join(dn, "serial"   )) or "").strip()
                # print "vid=%04x pid=%04x serial_number=[%s] %s" % ( vid, pid, snm, dn, )
                if  ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)) and ((serial_number is None) or (snm.lower() == str(serial_number).lower())) :
                    # print "vid=%04x pid=%04x serial_number=[%s]" % ( vid, pid, snm ), serial_number
                    dns = glob.glob(os.path.join(dn, os.path.basename(dn) + "*"))
                    for sdn in dns :
                        for fn in glob.glob(os.path.join(sdn, "*")) :
                            # print "@@@@", fn
                            if  re.search(r"\/tty(USB|ACM)[0-9]+$", fn) :
                                ports.append(os.path.join("/dev", os.path.basename(fn)))
                            elif fn.endswith("/tty") :
                                for ffn in glob.glob(os.path.join(fn, "*")) :
                                    if  re.search(r"\/tty(USB|ACM)[0-9]+$", ffn) :
                                        ports.append(os.path.join("/dev", os.path.basename(ffn)))
                                    pass
                                pass
                            pass
                        pass
                    pass
                pass
            except ( ValueError, TypeError, AttributeError ) :
                # tzlib.print_exception()
                pass
            pass

        if  (not len(ports)) and usb    :
            fd  = None
            for bus in usb.busses()     :
                for dev in bus.devices  :
                    if  ((vendor_id is None) or (dev.idVendor == vendor_id)) and ((product_id is None) or (dev.idProduct == product_id)) and ((serial_number is None) or (str(dev.iSerialNumber).lower() == str(serial_number).lower())) :
                        # print "@@@@", "%04x:%04x" % ( dev.idVendor, dev.idProduct, ), dev.deviceClass, dev.deviceSubClass, dev.deviceProtocol, "Bus: %s  Device: %s" % ( str(bus.dirname), str(dev.filename) )
                        # print dir(dev.configurations[0].interfaces[0][0]), dev.configurations[0].interfaces[0][0], dev.configurations[0].interfaces[0][0].interfaceProtocol
                        # print dev.configurations[0].interfaces[0][0].endpoints[0].address, dev.configurations[0].interfaces[0][0].endpoints[0].type
                        if  True or ((dev.deviceClass == 0) and (dev.deviceSubClass == 0) and (dev.deviceProtocol == 0)) :
                            # print "found bus:", bus.dirname, "device:", dev.filename
                            #
                            # ?     how to find which ttyUSB%u it is, and how to find which ttyS%u that is (done with "ln -b /dev/ttyUSB0 /dev/ttyS0" where -b makes a ~ backup of the old link or whatever it is)
                            #       OR BETTER YET: we now take the command line parm /dev/ttyUSB%u and it works,
                            #          so all we need to do is to tie the usb device to the ttyUSB
                            #       hwinfo has enough info to find out:
                            #          bus.dirname and dev.filename give the hwinfo usb.bus_number and usb.linux.device_number
                            #          then linux.sysfs_path looks like this:
                            #              linux.sysfs_path = '/sys/devices/pci0000:00/0000:00:1d.7/usb8/8-2/8-2.2/8-2.2:1.0'
                            #          and that ties back to a previous device that has:
                            #              linux.sysfs_path = '/sys/devices/pci0000:00/0000:00:1d.7/usb8/8-2/8-2.2/8-2.2:1.0/ttyUSB1/tty/ttyUSB1'
                            #              serial.device = '/dev/ttyUSB1'
                            #              serial.port = 1 (0x1)
                            #              linux.device_file = '/dev/ttyUSB1'
                            #          or
                            #              hwinfo --usb
                            #              .
                            #              .
                            #              .
                            #              25: USB 00.0: 0700 Serial controller
                            #              .
                            #              .
                            #              .
                            #                Unique ID: Mwf_.yosUmW5iOW6
                            #                Parent ID: 2XnU.erpEvbsFWX1
                            #                Model: "Prolific PL2303 Serial Port"
                            #                Hotplug: USB
                            #                Vendor: usb 0x067b "Prolific Technology, Inc."
                            #                Device: usb 0x2303 "PL2303 Serial Port"
                            #              .
                            #              .
                            #              .
                            #                Device File: /dev/ttyUSB1
                            #              .
                            #              .
                            #              .
                            #           and so,
                            #              rx  = re.compile(r"  Vendor: usb 0x([0-9a-f]{4}).*?  Device: usb 0x([0-9a-f]{4}).*?  Device File: /dev/ttyUSB([0-9]+)", re.DOTALL)
                            #              print rx.findall(rs)
                            #
                            #
                            #        Also (later, after the devices have moved) dmesg (/var/log/messages) has this, looking from the bottom to the top:
                            #             [30309.568340] usb 8-2.2: new full speed USB device using ehci_hcd and address 36
                            #             [30309.660907] usb 8-2.2: configuration #1 chosen from 1 choice
                            #             [30309.661169] usb 8-2.2: cp210x converter detected
                            #             [30309.661246] usb 8-2.2: cp210x converter now attached to ttyUSB0
                            #          So it appears that the bus.dirname is in the "usb BUS.DIRNAME-2.2...
                            #             and the dev.filename is "address DEV.FILENAME"
                            #        !!!! code uses this method
                            #          Problem with this is that the log may have been flushed since the device was plugged in.
                            #
                            #        Also, The /sys/devices directory can be searched for the device. The files seem to have the information that lsusb and hwinfo output.
                            #          And, apparently, udev rules can be used to assign things to stable device names or whatever.
                            #        Also,
                            #            dir /sys/bus/usb-serial/devices/
                            #            total 0
                            #            drwxr-xr-x 2 root root 0 2011-11-08 21:09 ./
                            #            drwxr-xr-x 4 root root 0 2011-11-08 20:52 ../
                            #            lrwxrwxrwx 1 root root 0 2011-11-08 21:09 ttyUSB0 -> ../../../devices/pci0000:00/0000:00:13.1/usb6/6-1/6-1:1.0/ttyUSB0/
                            #       Also,
                            #            /sys/bus/usb/devices/5-3/idVendor           Contains the hex vendor  ID
                            #            /sys/bus/usb/devices/5-3/idProduct          Contains the hex product ID
                            #            /sys/bus/usb/devices/5-3/5-3:1.0/ttyUSB1/   Exists as a directory.
                            #         so searching all the sub-dirs of /sys/bus/usb/devices for the proper idVendor and idProduct, then searching in all subdirectories that start with the basename of the idVendor/idProduct dir's base name for ttyUSB# finds the port.
                            #
                            #
                            ps  = "Bus: %s  Device: %s" % ( str(bus.dirname), str(dev.filename) )


                            fnd = 0
                            if  not fd :
                                try :
                                    fd  = tzlib.read_whole_text_file("/var/log/messages")
                                except IOError :
                                    fd  = ""
                                pass
                            if  not fd :
                                break

                            ba  = str(int(str(bus.dirname),  10))
                            da  = str(int(str(dev.filename), 10))
                            fre = re.compile(r" usb " + ba + r"-\d[^\n]+? and address " + da + r".*? usb " + ba + r"-\d[^\n]+? now attached to (\S+)", re.DOTALL)
                            fa  = fre.findall(fd)
                            if  fa  :
                                ps  = "/dev/" + fa[-1]
                                ports.append(ps)
                                fnd = 1
                            ba  = str(int(str(bus.dirname),  10))
                            da  = str(int(str(dev.filename), 10))
                            fre = re.compile(r"cdc_acm\s+%s-%s[\d:\.]+\s+(ttyACM\d+): USB ACM device" % ( ba, da, ), re.DOTALL)
                            fa  = fre.findall(fd)
                            if  fa  :
                                ps  = "/dev/" + fa[-1]
                                ports.append(ps)
                                fnd = 1
                            if  list_level + fnd >= 2 :
                                print ps
                            pass
                        pass
                    pass
                pass

            if  False and (vendor_id is None) and (product_id is None) and (serial_number is None) :
                ports.append(glob.glob('/dev/ttyACM*'))             # can only find these generically. Oooof. And, since we examine all USB devices with the True in the if statement looking at the class and protocol, we don't need this code
            pass
        pass

    ports.sort()

    return(ports)


find_likely_COM_ports   =   find_likely_USB_ports



def open_ports(ports) :
    try :
        import  serial

        for cport in ports :
            try :
                io  = serial.Serial(port = cport, timeout = 0.001)             # serial.Serial() multiplies 'timeout' by 1000 before passing to windows (This 1 mill is minimum for windows. I don't know about other OS's.)
                io.close()
            except serial.SerialException :
                print "Port " + str(cport) + " cannot be opened!"
            pass
        pass

    except ImportError :
        print "Cannot import serial"
    pass


help_str    = """
%s

    Do something with USB for debugging.

Options:

    --open_all          Print if any port can't be opened.

"""


#
#
#
if  __name__ == '__main__' :

    import  TZCommandLineAtFile


    program_name    = sys.argv.pop(0)

    TZCommandLineAtFile.expand_at_sign_command_line_files(sys.argv)


    if  tzlib.array_find(sys.argv, [ "--help", "-h", "-?", "/?", "?", "/h", ] ) >= 0 :

        print help_str % ( os.path.basename(program_name) )
        sys.exit(254)


    open_all    = False

    while True :
        oi  = tzlib.array_find(sys.argv, [ "--open_all", "--oa" ] )
        if  oi < 0 :    break
        del sys.argv[oi]
        open_all        = True


    ports       = find_likely_USB_ports()
    print "Default:", ports
    if  open_all :
        open_ports(ports)

    for nm, vid, pid in [
                            (   "CP210x",    0x10c4, 0xea60, ),          # Pulse Oximeter
                            (   "Prolific",  0x067b, 0x2303, ),          # GH615 GPS
                            (   "Prolific",  0x0403, 0x6001, ),          # FTDI cables
                            (   "Freescale", 0x1357, 0x0707, ),          # FRDM-KL25Z dev board ttyACM#
                        ] :
        ports   = find_likely_USB_ports(vendor_id = vid, product_id = pid)
        print "%s vid=%04x pid=%04x %s" % ( nm, vid, pid, str(ports) )

    pass

#
#
#
# eof
