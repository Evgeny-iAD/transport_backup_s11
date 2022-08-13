import wx

class CustomTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        """Constructor"""
        wx.TaskBarIcon.__init__(self)
        self.frame = frame

        icon = wx.Icon('iconka_prog.ico', wx.BITMAP_TYPE_ICO)

        self.SetIcon(icon, "Restore")

        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnTaskBarLeftClick)

    def OnTaskBarActivate(self, evt):
        """"""
        pass

    def OnTaskBarClose(self, evt):
        """
            Уничтожает иконку панели задач и рамку в самой иконке панели задач
        """
        self.frame.Close()

    def OnTaskBarLeftClick(self, evt):
        """
        Создаёт меню, появляющееся при нажатии правой кнопки мыши
        """
        self.frame.Show()
        self.frame.Restore()