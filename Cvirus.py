import glfw
import sys
import numpy as np
from Mvirus import Plots
from OpenGL.GL import glClearColor

class Controller:
    def __init__(self):
        self.model = None
        self.parameters = None
        self.modify = 1
        self.simulation = True
        self.plot = None
        self.textTexture = None
        self.firstTime = True

    def set_model(self, model, parameters, textTexture):
        self.model = model
        self.parameters = parameters
        self.textTexture = textTexture

    def on_key(self,window,key,scancode,action,mods):
        if not (action == glfw.PRESS):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif key == glfw.KEY_C:
            self.model.continuo = True
            self.model.move = True

        elif key == glfw.KEY_I:
            self.model.continuo = False

        elif key == glfw.KEY_RIGHT:
            self.model.move = True

        elif key == glfw.KEY_DOWN:
            if self.modify:
                if self.model.radius - 0.005 < 0:
                    self.model.radius = 0
                else:
                    self.model.radius = np.around(self.model.radius - 0.005, 3)
                self.parameters.updateRadius(self.model.radius)
            else:
                if self.model.probMove - 0.1 <= 0.05:
                    self.model.probMove = 0
                else:
                    self.model.probMove = np.around(self.model.probMove - 0.1, 1)
                self.model.static()
                self.parameters.updateProb(self.model.probMove)

        elif key == glfw.KEY_UP:
            if self.modify:
                self.model.radius = np.around(self.model.radius + 0.005, 3)
                self.parameters.updateRadius(self.model.radius)
            else:
                if self.model.probMove + 0.1 > 1:
                    self.model.probMove = 1
                else:
                    self.model.probMove = np.around(self.model.probMove + 0.1, 1)
                self.model.static()
                self.parameters.updateProb(self.model.probMove)

        elif key == glfw.KEY_R:
            self.modify = 1
            self.parameters.mod = True

        elif key == glfw.KEY_M:
            self.modify = 0
            self.parameters.mod = False

        elif key == glfw.KEY_P:
            if self.simulation:
                self.simulation = False
                glClearColor(1, 1, 1, 1.0)
                daysX = np.arange(self.model.day + 1)
                self.plot = Plots(daysX, self.model.historyInfected, self.model.historyUninfected,
                                  self.model.historyRecovered, self.model.historyDeaths,
                                  self.model.historyRadius, self.model.historyProb, self.textTexture, 0, 0, 0)

        elif key == glfw.KEY_S:
            if self.firstTime and not self.simulation:
                self.firstTime = False
                self.model.plotMatplot()
