# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import numpy as np
import matplotlib
import re
import os, winsound
import time

matplotlib.use('Qt5Agg')
np.set_printoptions(threshold='nan')

import PyQt5.QtWidgets as QT
from PyQt5.QtCore import QProcess
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as Toolbar
from matplotlib.figure import Figure


'''
==============================================================

Main window Block

==============================================================
'''  

class Form(QT.QLabel) :

    def __init__(self,parent = None) :
        
        super(Form, self).__init__(parent)

        self.xs = []
        self.ys = []
        self.Loaded = False
        self.extrawindow = MCNP_Handle()
        self.extrawindow.passer = True
        self.setWindowTitle("DetUtil")
        self.setGeometry(200,200,1000,900)
        
        self.m = MSelect(self)
        self.o = MSelect(self)
        self.o.m_text.setText("Choose Output Files  ")
        self.o.m_dir_edit.setText('')
        self.t = TSelect(self)
        
        self.make = QT.QPushButton(self)
        self.make.setText("Generate Output Files with MCNP Handler")

        self.loader = QT.QListWidget(self)
        
        self.spec = QT.QPushButton(self)
        self.spec.setText("Generate Spectrum")
        
        self.wiper = QT.QPushButton(self)
        self.wiper.setText("Clear Selections")
        
        #self.eff = QT.QPushButton(self)
        #self.eff.setText("Generate Efficiency Curve")
        
        self.output = QT.QLineEdit(" ")
        self.output.selectAll()
        self.output.setStyleSheet('color: rgb(255, 0, 255)')
        
        self.tally_list = QT.QComboBox(self)
        self.opt = QT.QLabel(self)
        self.opt.setText("     Plotting Tally: ")
        self.omit_label = QT.QLabel(self)
        self.omit_label.setText("  Omit First Channels:")
        self.omit = QT.QLineEdit('10')
        self.omit.selectAll()
        self.scale_label = QT.QLabel(self)
        self.scale_label.setText("  Log Scale")
        self.scale = QT.QCheckBox(self)
        
        
        self.plot = MatplotlibCanvas()
        self.navbar = Toolbar(self.plot, self)
        self.navbar.hide()
        
        self.zooms = QT.QPushButton('Zoom')
        self.zooms.clicked.connect(self.zoom)
         
        self.pans = QT.QPushButton('Pan')
        self.pans.clicked.connect(self.pan)
        
        self.homes = QT.QPushButton('Home')
        self.homes.clicked.connect(self.home)
        
        self.saver = QT.QPushButton(self)
        self.saver.setText("  Save Spectrum Plot  ")
        
        
        self.ver = QT.QLabel(self)
        self.ver.setText("       ver 1.2.1, 12/5/2016  ")
        self.ver.setStyleSheet('color: rgb(169, 169, 169)')
        
        # Layout Section
        layout = QT.QVBoxLayout()
        
        first = QT.QGridLayout()
        first.setSpacing(3)
        first.addWidget(self.m.m_text,0,0)
        first.addWidget(self.m.m_dir_edit,0,1)
        first.addWidget(self.m.m_loader,0,2)
        first.addWidget(self.o.m_text,1,0)
        first.addWidget(self.o.m_dir_edit,1,1)
        first.addWidget(self.o.m_loader,1,2)
        first.addWidget(self.t.t_text1,2,0)
        first.addWidget(self.t.t_edit,2,1)
        first.addWidget(self.t.t_text2,2,2)
        
        left_opt = QT.QHBoxLayout()
        left_opt.addWidget(self.opt)
        left_opt.addWidget(self.tally_list)
        left_opt.addWidget(self.omit_label)
        left_opt.addWidget(self.omit)
        
        plot_opt = QT.QHBoxLayout()
        plot_opt.addWidget(self.wiper)
        plot_opt.addWidget(self.spec)
        
        right_opt = QT.QHBoxLayout()
        right_opt.addWidget(self.homes)
        right_opt.addWidget(self.zooms)
        right_opt.addWidget(self.pans)
        right_opt.addWidget(self.scale_label)
        right_opt.addWidget(self.scale)
        
        second = QT.QGridLayout()
        second.setSpacing(2)
        second.addLayout(plot_opt,0,0)
        second.addWidget(self.saver,0,2)
        second.addLayout(left_opt,1,0)
        second.addLayout(right_opt,1,2)

        bottom = QT.QGridLayout()
        bottom.setSpacing(2)
        bottom.addWidget(self.output,0,0)
        bottom.addWidget(self.ver,0,1)
        
        layout.addLayout(first)
        layout.addWidget(self.make)
        layout.addWidget(self.loader)
        layout.addLayout(second)
        layout.addWidget(self.plot)
        layout.addLayout(bottom)
        self.setLayout(layout)
        
        self.loader.doubleClicked.connect(self.GetSpec)
        self.o.m_loader.pressed.connect(self.OutputDir)
        self.m.m_loader.pressed.connect(self.MCNPDir)
        self.wiper.pressed.connect(self.clearlist)
        self.spec.pressed.connect(self.GetSpec)
        self.make.pressed.connect(self.RunMCNP)
        self.tally_list.currentIndexChanged.connect(self.updatePlot)
        self.scale.stateChanged.connect(self.updatePlot)
        self.saver.pressed.connect(self.PlotSave)
        
        
    def MCNPDir(self):
        if self.extrawindow.passer:
            dir_name = QT.QFileDialog.getExistingDirectory(self, 'MCNP Directory', '/path/to/default/')
            dir_name = str(dir_name)
            self.m.m_dir_edit.setText(dir_name)
        else:
            self.output.setText('MCNP Directory cannot be changed while running schedule through MCNP Handler')
            self.output.setStyleSheet('color: rgb(255, 0, 255)')
            winsound.PlaySound('*', winsound.SND_ASYNC)
        
    def OutputDir(self):
        files = QT.QFileDialog.getOpenFileNames(self, 'Output Files', '/path/to/default/', 'Output Files (*.o)')
        self.o.m_dir_edit.setText(str(files[0]))
        for i in files[0]:
            self.loader.addItem(i)
   
    def RunMCNP(self):
        if self.extrawindow.passer:
            self.extrawindow.dir_text = self.m.m_dir_edit.text()
            self.extrawindow.show()
    
    def clearlist(self):
        self.loader.clear()
            
    def GetSpec(self):
        tally = str(self.t.t_edit.text())
        if tally == '':
            self.output.setText('Invalid tally request: No tallies given')
            self.output.setStyleSheet('color: rgb(255, 0, 255)')
            winsound.PlaySound('*', winsound.SND_ASYNC)
        else:
            tally = tally.split(',')
            try:
                tally = [int(i) for i in tally]
                try:
                    fil_name = self.loader.currentItem().text()
                    fil_name = str(fil_name)
                    self.GenSpec(fil_name,tally)
                except AttributeError:
                    self.output.setText('Invalid Spectrum request: Select an output file')
                    self.output.setStyleSheet('color: rgb(255, 0, 255)')
                    winsound.PlaySound('*', winsound.SND_ASYNC)
            except ValueError:
                self.output.setText('Input Error: Check input type then use Generate Spectrum')
                self.output.setStyleSheet('color: rgb(255, 0, 255)')
                winsound.PlaySound('*', winsound.SND_ASYNC)
    
    def GenSpec(self,fil_name,tally):
        found=[]
        startflags=[]
        stopflags=[]
        dataflags=[]
        ranges=[]
        blocks=[]
        count = 0
        fil = open(fil_name, 'r')
        fils = fil.readlines()
        fil.close
        
        self.Loaded=False
        scaler = self.scale.isChecked()
        try:
            omits = abs(int(self.omit.text()))
            self.omit.setText(str(omits))
        except UnboundLocalError:
            pass
        self.tally_list.clear()
        self.xs = []
        self.ys = []
        #Determines what lines the tallies start and stop
        for line in fils:
            count +=1
            for i in tally:
                tallyflag = str(i)
                place = re.search('1tally *' + tallyflag + '  ', line)
                if place != None:
                    found.append(i)
                    startflags.append(count)
            place = re.search('      total', line)
            if place != None:
                stopflags.append(count)
            place = re.search('      energy', line)
            if place != None:
                dataflags.append(count)
        if startflags == []:
            self.output.setText('Tally error: None of the requested tallies could be found')
            self.output.setStyleSheet('color: rgb(255, 0, 255)')
            winsound.PlaySound('*', winsound.SND_ASYNC)
        else:
            self.output.setText('Tallies Found:  ' + str(found))
            for i in found:
                self.tally_list.addItem('Tally F' + str(i))
            
            for i in startflags:
                index = i
                end = True
                while end:
                    index+=1
                    if index in dataflags:
                        startline = index
                    if index in stopflags:
                        stopline = index
                        end = False
                ranges.append(range(startline+1+omits,stopline))
            
            for i in ranges:
                count = 0
                block = []
                for line in fils:
                    count+=1
                    if count in i:
                        block.append(line)
                blocks.append(block)
            
            for i in blocks:
                xblock=[]
                yblock=[]
                for j in i:
                    vals = j.split(' ')
                    x = float(vals[4])
                    xblock.append(x)
                    y = float(vals[7])
                    yblock.append(y)
                self.xs.append(xblock)
                self.ys.append(yblock)
                
            self.plot.redraw(self.xs[0],self.ys[0],scaler)
            self.Loaded = True
    '''
    ==============================================================
    Widget Groups to interact with plots
    ==============================================================
    '''
    def updatePlot(self):
        i = int(self.tally_list.currentIndex())
        if self.Loaded:
            scaler = self.scale.isChecked()
            if i >= 0:
                self.plot.redraw(self.xs[i],self.ys[i],scaler)
    
    def PlotSave(self):
        name = QT.QFileDialog.getSaveFileName(self, 'Save Spectrum As', '/path/to/default/*.png', "Image File (*.png)")
        name=str(name[0])
        self.plot.fig.savefig(name, bbox_inches='tight')
    def zoom(self):
        self.navbar.zoom()
    def pan(self):
        self.navbar.pan()
    def home(self):
        self.navbar.home()
        
'''
==============================================================

Extra Widget Groups of a specific form

==============================================================
'''  
                    
class MSelect(QT.QLabel):
    def __init__(self,parent = None) :
        super(MSelect, self).__init__(parent)
        
        self.m_text = QT.QLabel(self)
        self.m_text.setText("Set MCNP Directory")
        self.m_dir_edit = QT.QLineEdit('C:\MCNP')
        self.m_dir_edit.selectAll()
        self.m_dir_edit.setReadOnly(True)
        self.m_loader = QT.QPushButton(self)
        self.m_loader.setText("Browse")
        
class TSelect(QT.QLabel):
    def __init__(self,parent = None) :
        super(TSelect, self).__init__(parent)
        
        self.t_text1 = QT.QLabel(self)
        self.t_text1.setText("Set Fn Tallies")
        self.t_edit = QT.QLineEdit()
        self.t_edit.selectAll()
        self.t_text2 = QT.QLabel(self)
        self.t_text2.setText("  example: 4, 8, 18, ...  ")

'''
==============================================================

MCNP Execution Window Block

==============================================================
'''  
        
class MCNP_Handle(QT.QLabel):
    def __init__(self,parent = None) :
        super(MCNP_Handle, self).__init__(parent)
        
        self.setWindowTitle("MCNP Handler")
        self.setGeometry(700,400,725,450)
        self.livetapes = []
        self.files = MSelect(self)
        self.files.m_text.setText("Choose Input Files  ")
        self.files.m_dir_edit.setText('')
        
        
        self.passer = True
        self.runtext = None
        self.arguments = None
        self.num = 0
        self.queue = 0
        self.start_time = 0
        
        self.process = QProcess(self)
        self.process.setProcessChannelMode(2)
        
        self.loader = QT.QListWidget(self)
        self.dir_text = None
        self.i_text = QT.QLabel(self)
        self.i_text.setText("Included MCNP Arguments  ")
        self.i_dir_edit = QT.QLineEdit('tasks 30')
        self.i_dir_edit.selectAll()
        self.iarg_text = QT.QLabel(self)
        self.iarg_text.setText("  example: 'tasks n mcrun'   ")
        
        self.begin = QT.QPushButton(self)
        self.begin.setText('Begin Scheduled MCNP Runs')
        
        self.wiper = QT.QPushButton(self)
        self.wiper.setText("Clear Selections")
        self.erase = QT.QPushButton(self)
        self.erase.setText('Erase runtapes in directory')
        self.tape_text = QT.QLabel(self)
        self.tape_text.setText("                      Erase runtape after run?  ")
        self.notape = QT.QCheckBox(self)
        self.notape.setChecked(True)
        
        layout = QT.QVBoxLayout()
        first = QT.QGridLayout()
        first.setSpacing(3)
        first.addWidget(self.files.m_text,0,0)
        first.addWidget(self.files.m_dir_edit,0,1)
        first.addWidget(self.files.m_loader,0,2)
        first.addWidget(self.i_text,1,0)
        first.addWidget(self.i_dir_edit,1,1)
        first.addWidget(self.iarg_text,1,2)
        
        tapes = QT.QHBoxLayout()
        tapes.addWidget(self.tape_text)
        tapes.addWidget(self.notape)
        
        second = QT.QGridLayout()
        second.setSpacing(2)
        second.addWidget(self.wiper,0,0)
        second.addWidget(self.erase,0,1)
        second.addLayout(tapes,0,2)
        
        layout.addLayout(first)
        layout.addWidget(self.loader)
        layout.addLayout(second)
        layout.addWidget(self.begin)
        
        self.setLayout(layout)
        self.files.m_loader.pressed.connect(self.OutputDir)
        self.begin.pressed.connect(self.Runner)
        self.wiper.pressed.connect(self.Blank)
        self.erase.pressed.connect(self.Eraser)
        self.process.finished.connect(self.WaitToRun)
    
    def Locate(self):
        self.livetapes = []
        tapes = []
        dirlist = os.listdir(os.getcwd())
        for i in range(97,123):
            tapes.append(str('runtp') + str(chr(i)))
        for j in dirlist:
            if j in tapes:
                self.livetapes.append(j) 
        
    def OutputDir(self):
        fil = QT.QFileDialog.getOpenFileNames(self, 'Input Files', '/path/to/default/', 'Input Files (*.i)')
        self.files.m_dir_edit.setText(str(fil[0]))
        for i in fil[0]:
            self.loader.addItem(i)
    '''
    ==============================================================
    MCNP Handler Execution Block. 
    Note: Specifically set up to queue subprocesses in the background
    ==============================================================
    '''  
    def Primer(self):
        i = self.queue
        inputtext = str(self.loader.item(i).text())
        outputtext = inputtext[:-2] + str('.o')
        self.runtext = str(self.dir_text + '/MCNP_CODE/bin/mcnp6.exe')
        self.arguments = str(' i=' + inputtext + ' o=' + outputtext + ' ' + self.i_dir_edit.text())
        print str('\n\n=======================Handler Output========================')
        print str('   MCNP task initiated by MCNP Handler: task ' + str(i+1) + ' of ' + str(self.num))
        print str('   Input file located at ' + inputtext)
        print str('   Additional Arguments: ' + self.i_dir_edit.text())
        print str('========================MCNP6 Output=========================\n\n')
        
    def Runner(self):        
        self.num = int(self.loader.count())
        if self.num == 0:
            winsound.PlaySound('*', winsound.SND_ASYNC)
        elif self.passer == False:
            winsound.PlaySound('*', winsound.SND_ASYNC)
        else:
            self.passer = False
            self.start_time = time.time()
            self.queue = 0
            self.Locate()
            self.Primer()
            self.process.start(self.runtext + self.arguments)
                        
    def WaitToRun(self):
        if self.passer == False:
            if self.notape.isChecked():
                    for i in range(97,123):
                        tape = str('runtp') + str(chr(i))
                        if tape not in self.livetapes:
                            try:
                                os.remove(tape)
                            except WindowsError:
                                pass
            self.num = int(self.loader.count())
            if self.queue+1 < self.num:   
                self.queue += 1
                self.Locate()
                self.Primer()
                self.process.start(self.runtext + self.arguments)
            else:
                alltime = time.time() - self.start_time
                alltime = str(alltime/60)
                print str('\n\n=======================Handler Output========================')
                print str('      MCNP Handler run schedule completed\n      ') + str(self.num) + str(' tasks completed successfully')
                print str('      Total run time:  ' + alltime + '  minutes')
                print str('=============================================================\n\n')
                if self.notape.isChecked():
                    for i in range(97,123):
                        tape = str('runtp') + str(chr(i))
                        if tape not in self.livetapes:
                            try:
                                os.remove(tape)
                            except WindowsError:
                                pass
                self.passer = True
                
    '''
    ==============================================================
    Extra MCNP Handler Things
    ==============================================================
    '''          
    def Blank(self):
        if self.passer:
            self.loader.clear()
        else:
            winsound.PlaySound('*', winsound.SND_ASYNC)
    
    def Eraser(self):
        if self.passer:
            self.Locate()
            for i in self.livetapes:
                try :
                    os.remove(i)
                except WindowsError:
                    pass
        else:
            winsound.PlaySound('*', winsound.SND_ASYNC)

'''
==============================================================

MCNP Execution Window Block

==============================================================
'''  
        
class MCNP_Study(QT.QLabel):
    def __init__(self,parent = None) :
        super(MCNP_Handle, self).__init__(parent)
        
        self.setWindowTitle("MCNP Study")
        self.setGeometry(700,400,725,450)
        
        self.directory = MSelect(self)
        self.directory.m_text.setText("Set Study Directory")
        self.directory.m_dir_edit.setText('')
        
        self.master = MSelect(self)
        self.master.m_text.setText("Set Master File")
        self.master.m_dir_edit.setText('')
        
        self.passer = True
        self.runtext = None
        self.arguments = None
        self.num = 0
        self.queue = 0
        
        self.loader = QT.QListWidget(self)
        self.dir_text = None
        self.i_text = QT.QLabel(self)
        self.i_text.setText("Included MCNP Arguments  ")
        self.i_dir_edit = QT.QLineEdit('tasks 30')
        self.i_dir_edit.selectAll()
        self.iarg_text = QT.QLabel(self)
        self.iarg_text.setText("  example: 'tasks n mcrun'   ")
        
        self.begin = QT.QPushButton(self)
        self.begin.setText('Generate Inputs')
        
        self.wiper = QT.QPushButton(self)
        self.wiper.setText("Clear Selections")

        layout = QT.QVBoxLayout()
        first = QT.QGridLayout()
        first.setSpacing(3)
        first.addWidget(self.directory.m_text,0,0)
        first.addWidget(self.directory.m_dir_edit,0,1)
        first.addWidget(self.directory.m_loader,0,2)
        first.addWidget(self.master.m_text,1,0)
        first.addWidget(self.master.m_dir_edit,1,1)
        first.addWidget(self.master.m_loader,1,2)
        
        tapes = QT.QHBoxLayout()
        tapes.addWidget(self.tape_text)
        tapes.addWidget(self.notape)
        
        layout.addLayout(first)
        layout.addWidget(self.loader)
        layout.addWidget(self.begin)
        
        self.setLayout(layout)
        
        self.directory.m_loader.pressed.connect(self.SetDir)
        self.master.m_loader.pressed.connect(self.MasterName)
        self.begin.pressed.connect(self.Runner)
        self.wiper.pressed.connect(self.Blank)
        self.erase.pressed.connect(self.Eraser)
        self.process.finished.connect(self.WaitToRun)
        
    def SetDir(self):
        dir_name = QT.QFileDialog.getExistingDirectory(self, 'Study Directory', '/path/to/default/')
        dir_name = str(dir_name)
        self.directory.m_dir_edit.setText(dir_name)
        
    def MasterName(self):
        fil = QT.QFileDialog.getOpenFileName(self, 'Master File', '/path/to/default/', 'Input File (*.i)')
        self.master.m_dir_edit.setText(str(fil[0]))
        
'''
================================================================

Inset Plotter Block

================================================================
'''            
        
class MatplotlibCanvas(FigureCanvas) :
    
    def __init__(self, parent=None, width=6, height=5, dpi=75) :
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QT.QSizePolicy.Expanding, QT.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
      
    def compute_initial_figure(self):
        self.x = 10
        self.y = 10
        self.axes.plot(self.x, self.y)
        self.axes.set_xlabel('Energy', fontsize = 12)
        self.axes.set_ylabel('Pulse Height', fontsize = 12)    
        
    def redraw(self, x, y, scale) :
        self.axes.plot(x, y)
        self.axes.set_xlabel('Energy (MeV)', fontsize = 12)
        self.axes.set_ylabel('Pulse Height', fontsize = 12)  
        if scale:
            self.axes.set_yscale('log')
        else:
            self.axes.set_yscale('linear')
        self.draw()

app = QT.QApplication(sys.argv)
form = Form()
widget = MatplotlibCanvas()
form.show()
#MCNP_Study().show
app.exec_()