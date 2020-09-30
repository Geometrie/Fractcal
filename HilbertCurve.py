import wx
import random
def curve_map(position, sum_len):
    index = [0] * sum_len
    for i in range(sum_len):
        index[sum_len - i - 1] = position % 4
        position = position // 4
    mat = [1, 0, 0, 1]
    x = 0
    y = 0
    for i in range(sum_len):
        x_tmp = (index[i]) % 4 // 2 * 2 - 1
        y_tmp = (index[i] + 1) % 4 // 2 * 2 - 1
        x = x * 2 + mat[0] * x_tmp + mat[1] * y_tmp
        y = y * 2 + mat[2] * x_tmp + mat[3] * y_tmp
        if (index[i] == 0):
            mat_tmp = mat * 1
            mat[0] = mat_tmp[1]
            mat[1] = mat_tmp[0]
            mat[2] = mat_tmp[3]
            mat[3] = mat_tmp[2]
        elif (index[i] == 3):
            mat_tmp = mat * 1
            mat[0] = -mat_tmp[1]
            mat[1] = -mat_tmp[0]
            mat[2] = -mat_tmp[3]
            mat[3] = -mat_tmp[2]
    return [x, y]

class Canvas(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, -1)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_UP, self.on_key)
        self.sum_len = 1
        self.max_coord = 2
        self.point_size = 4
        self.point_list = []
        self.radius = 256
        self.draw_curve = True
        for i in range(self.point_size):
            coord = curve_map(i, self.sum_len)
            self.point_list.append(wx.Point(coord[0] * self.radius / self.max_coord, -coord[1] * self.radius / self.max_coord))
    def on_key(self, event):
        if event.GetKeyCode() == wx.WXK_LEFT:
            if self.sum_len > 1:
                self.sum_len = self.sum_len - 1
                self.max_coord = self.max_coord >> 1
                self.point_size = self.point_size >> 2
                self.point_list.clear()
                for i in range(self.point_size):
                    coord = curve_map(i, self.sum_len)
                    self.point_list.append(wx.Point(coord[0] * self.radius / self.max_coord, -coord[1] * self.radius / self.max_coord))
                self.draw_curve = True
                self.Refresh()
        elif event.GetKeyCode() == wx.WXK_RIGHT:
            if self.sum_len < 8:
                self.sum_len = self.sum_len + 1
                self.max_coord = self.max_coord << 1
                self.point_size = self.point_size << 2
                self.point_list.clear()
                for i in range(self.point_size):
                    coord = curve_map(i, self.sum_len)
                    self.point_list.append(wx.Point(coord[0] * self.radius / self.max_coord, -coord[1] * self.radius / self.max_coord))
                self.draw_curve = True
                self.Refresh()
        elif event.GetKeyCode() == ord('c') or event.GetKeyCode() == ord('C'):
            self.point_list.clear()
            for i in range(self.point_size):
                coord = curve_map(i, self.sum_len)
                self.point_list.append(wx.Point(coord[0] * self.radius / self.max_coord, -coord[1] * self.radius / self.max_coord))
            self.draw_curve = True
            self.Refresh()
        elif event.GetKeyCode() == ord('n') or event.GetKeyCode() == ord('N'):
            self.point_list.clear()
            for i in range(int(self.point_size)):
                para = int(random.gauss(self.point_size / 2, self.point_size / 6) + 0.5)
                if para >= 0 and para < self.point_size:
                    coord = curve_map(para, self.sum_len)
                    self.point_list.append(wx.Point(coord[0] * self.radius / self.max_coord + 300, -coord[1] * self.radius / self.max_coord + 300))
            self.draw_curve = False
            self.Refresh()
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        dc.SetPen(wx.BLACK_PEN)
        if self.draw_curve:
            dc.DrawLines(self.point_list, 300, 300)
        else:
            dc.DrawPointList(self.point_list)

class MainFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw, size=(600, 600))
        self.canvas = Canvas(self)
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None, title = "HibertCurve")
    frame.Show()
    app.MainLoop()
