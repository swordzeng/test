#coding=utf-8
import wx

class FormInit(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None)
		self.Title = 'AMS'
		self.Size = (800, 600)
		self.panel = wx.Panel(self, -1)
		
		vbox = wx.BoxSizer(wx.VERTICAL)
		btn_box = wx.BoxSizer(wx.HORIZONTAL)
		
		lbn_date = wx.StaticText(self.panel, -1, label='Date', size=(100,600), style = wx.ALIGN_CENTER)
		font = wx.Font(14, wx.ROMAN, wx.FONTSTYLE_NORMAL, wx.NORMAL)
		lbn_date.SetFont(font)
		btn_box.Add(lbn_date, 0, wx.EXPAND | wx.TOP, 7)
		
		btn_rpt = wx.Button(self.panel, label='REPORT')
		btn_box.Add(btn_rpt)
		
		lbn_grid = wx.StaticText(self.panel, -1, style = wx.ALIGN_CENTER)
		lbn_grid.SetLabel('GRID')	
		
		vbox.Add(btn_box)
		vbox.Add(lbn_grid)
		
		self.panel.SetSizer(vbox)
		
if __name__ == '__main__':
	app = wx.App()
	frame = FormInit()
	frame.Show()
	app.MainLoop()