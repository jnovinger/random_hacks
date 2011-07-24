#!/usr/bin/python

from time import sleep
import subprocess
import re
import sys, getopt
from platform import system

def help_message():
    print '''ubnt_signal_reader.py -- uses espeak and ssh on Linux boxes to read out loud the connection strength of a Ubiquiti AirMax device
    Useage examples:
    
        python ubnt_signal_reader.py
        Runs the GUI version of UBNT Signal Reader.
    
        python ubnt_signal_reader.py -s 5
        Uses Ubiquiti default host IP, but will sleep for 5 seconds.  
        
        python ubnt_signal_reader.py -s 10 10.1.1.1
        Sleeps for 10 seconds in between reading signal strengths from Ubiquiti device at 10.1.1.1.
        
        python ubnt_signal_reader.py help
        This help message.
        
Since SSH is used underneath, actual resolvable hostnames can be used instead of IP addresses.

To make the best use of this script, is it helpful to create a local SSH key with no passphrase and transfer it to the Ubiquiti device, like so:

$ ssh-keygen -t dsa (hit enter three times for no passphrase)
$ ssh-copy-id admin@hostname'''
    
    sys.exit(0)

def speakAloud(strength):
    spkCmd = 'say'
    if system() == 'Linux':
        spkCmd = 'espeak'
        
    return subprocess.Popen([spkCmd, strength], stdout=subprocess.PIPE)


def report_signal(host):
    # get regular expression ready
    p = re.compile('=-(.* dBm)  Noise', re.IGNORECASE)

    try:
        strength = subprocess.Popen(['ssh', 'admin@' + host, "'iwconfig'", '2>/dev/null'], stdout=subprocess.PIPE)
        strength = p.search(strength.communicate()[0])
        return strength.group(1)
    except AttributeError:
        return -1
    except Exception as e:
        sys.exit('Exiting for unknown reason: %s' % e)


def cli_ubnt_signal_reader(argv):

    # set default values
    host = '192.168.1.20'
    sleep_time = 2

    # try grabbing cli arguments and using instead of defaults
    try:
        options, xarguments = getopt.getopt(argv[1:], 's', [])

        if 'help' in options or 'help' in xarguments:
            help_message()
    except SystemExit:
        sys.exit()
    except:
        options = []

    for option in options[:]:

        if option[0] == '-s':
            sleep_time = xarguments[0]
            options.remove(option)
            xarguments.remove(sleep_time)
            sleep_time = float(sleep_time)

    try:
        host = xarguments[0]
    except:
        print 'Using default Ubiquiti device IP of 192.168.1.20'

    # start main loop
    while True:
        try:
            strength = report_signal(host)
            if strength != -1:
                speakAloud(strength)
            else:
                sys.exit('Apparent network error, exiting.')
            sleep(sleep_time)
        except KeyboardInterrupt:
            sys.exit('Caught Ctrl-C, exiting')


def gui_ubnt_signal_reader():
    try:
        import wx

        class GuiReaderFrame(wx.Frame):
            def __init__(self, parent, title, size):
                self.title = title
                self.iterations = 10
                self.sleep_time = 2
                
                wx.Frame.__init__(self, parent, title = title, size = size)
                self.CreateStatusBar()

                panel = wx.Panel(self)

                # Menu
                fileMenu = wx.Menu()
                menuAbout = fileMenu.Append(wx.ID_ABOUT, '&About', 'Information about this program.')
                menuExit = fileMenu.Append(wx.ID_EXIT, '&Exit', 'Quit')

                # Menu bar
                menuBar = wx.MenuBar()
                menuBar.Append(fileMenu, '&File')
                self.SetMenuBar(menuBar)

                # Bind Menu items
                self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
                self.Bind(wx.EVT_MENU, self.onExit, menuExit)

                self.host_box = wx.TextCtrl(panel, pos = (5, 8), size = (200, 23), value = '192.168.1.20')
                self.speakButton = wx.Button(panel, label = "Speak!", pos = (210, 5))

                self.Bind(wx.EVT_BUTTON, self.speakClicked, self.speakButton)

            def speakClicked(self, event):
                for iteration in range(0, self.iterations):
                    strength = report_signal(self.host_box.GetValue())
                    if strength != -1:
                        speakAloud(strength)
                        sleep(self.sleep_time)
                    else:
                        self.errorDialog()
                        return

            def errorDialog(self):
                dlg = wx.MessageDialog(self,
                                       "A network error occurred, check the address you entered and try again.",
                                       'Alert',
                                       wx.OK)
                dlg.ShowModal()
                dlg.Destroy()


            def onAbout(self, event):
                dlg = wx.MessageDialog(self,
                                       "A small WxPython program to read aloud the signal from a Ubiquiti AirOS device.\n\nWritten by Jason Novinger.\n\nContact: jnovinger@gmail.com\n\nCode: https://github.com/jnovinger/random_hacks/tree/master/ubnt_signal_reader",
                                       'About %s' % self.title,
                                       wx.OK)
                dlg.ShowModal()
                dlg.Destroy()

            def onExit(self, event):
                self.Close(True)
                sys.exit(0)


        app = wx.App(False)
        GuiReaderFrame(None, title = 'UBNT Signal Reader', size = (300, 89)).Show()
        app.MainLoop()

    except ImportError:
        print 'Please install the wxpython package.'
        exit(1)
    
if __name__ == '__main__':
    if system() != 'Linux':
        print sys.argv[0] + ' is currently only supported on Linux.'
        sys.exit(1)
        
    if len(sys.argv) > 1 and sys.argv[1] != '--gui':
        cli_ubnt_signal_reader(sys.argv)
    else:
        gui_ubnt_signal_reader()