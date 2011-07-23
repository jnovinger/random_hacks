#!/usr/bin/env python

import wx

class MyFrame(wx.Frame):
    """Derive new class of Frame."""

    #noinspection PyArgumentList
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title = title, size = (200, 100))
        self.control = wx.TextCtrl(self, style = wx.TE_MULTILINE)
        self.CreateStatusBar()

        filemenu = wx.Menu()

        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', 'Information about this program.')
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, '&Exit', 'Quit')

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        menubar = wx.MenuBar()
        menubar.Append(filemenu, '&File')
        self.SetMenuBar(menubar)

        self.Show(True)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, 'A small text editor', 'About Small Text Editor', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

app = wx.App(False)
frame = MyFrame(None, 'Small Editor')
app.MainLoop()