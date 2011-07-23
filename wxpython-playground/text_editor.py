#!/usr/bin/env python
import os
import wx

class MyFrame(wx.Frame):
    """Derive new class of Frame."""

    #noinspection PyArgumentList
    def __init__(self, parent, title):
        self.dirName=''

        wx.Frame.__init__(self, parent, title = title, size = (200, -1))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()

        # Menu
        fileMenu = wx.Menu()
        menuAbout = fileMenu.Append(wx.ID_ABOUT, '&About', 'Information about this program.')
        menuOpen = fileMenu.Append(wx.ID_OPEN, '&Open', 'Open a file.')
        menuExit = fileMenu.Append(wx.ID_EXIT, '&Exit', 'Quit')

        # Menu bar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, '&File')
        self.SetMenuBar(menuBar)

        # Events
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0, 6):
            self.buttons.append(wx.Button(self, -1, 'Button &' + str(i)))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.control, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show(True)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, 'A small text editor', 'About Small Text Editor', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnOpen(self, event):
        dlg = wx.FileDialog(self, 'Choose a file', self.dirName, '', '*.*', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            f = open(os.path.join(self.dirName, self.fileName), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

app = wx.App(False)
frame = MyFrame(None, 'Small Editor')
app.MainLoop()