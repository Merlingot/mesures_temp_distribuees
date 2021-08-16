
class Appareil():

    def __init__(self,date=None,tdelta=None,temp=None, pos=None,name='',isDatalogger=False):
        self.name = name
        self.isDatalogger = isDatalogger
        self.date = date
        self.tdelta = tdelta
        self.pos = pos
        self.temp = temp
