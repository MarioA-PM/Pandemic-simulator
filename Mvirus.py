from mod import scene_graph as sg, easy_shaders as es, transformations as tr, basic_shapes as bs, text_renderer as tx
import numpy as np
from OpenGL.GL import *
import matplotlib.pyplot as plt

class Square:

    def __init__(self,scale):
        self.scale = scale
        gpuSquare = es.toGPUShape(bs.createColorQuadLines(1, 1, 1))
        screen = sg.SceneGraphNode('screen')
        screen.transform = tr.matmul([tr.translate(-0.5, 0, 0), tr.scale(0.4, 0.8, 1), tr.uniformScale(scale)])
        screen.childs += [gpuSquare]
        self.model = screen

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNodeLines(self.model, pipeline, 'transform')

class Label:

    def __init__(self, textTexture, r, g, b):
        self.textTexture = textTexture
        charSize = 0.05
        charSize2 = 0.04
        self.r = r
        self.g = g
        self.b = b
        self.up = 0.45
        xAxisShape = tx.textToShape('Day', charSize, charSize)
        self.gpuXAxis = es.toGPUShapeText(xAxisShape, GL_STATIC_DRAW, self.textTexture)
        yAxisShape = tx.textToShape('# People', charSize, charSize)
        self.gpuYAxis = es.toGPUShapeText(yAxisShape, GL_STATIC_DRAW, self.textTexture)
        originShape = tx.textToShape('0', 0.03, 0.03)
        self.gpuOrigin = es.toGPUShapeText(originShape, GL_STATIC_DRAW, self.textTexture)
        radiusAxisShape = tx.textToShape('Radius', 0.03, 0.03)
        self.gpuRadiusAxisShape = es.toGPUShapeText(radiusAxisShape, GL_STATIC_DRAW, self.textTexture)
        probAxisShape = tx.textToShape('Per. of', 0.03, 0.03)
        self.gpuProbAxisShape = es.toGPUShapeText(probAxisShape, GL_STATIC_DRAW, self.textTexture)
        probAxisShape2 = tx.textToShape('movement', 0.03, 0.03)
        self.gpuProbAxisShape2 = es.toGPUShapeText(probAxisShape2, GL_STATIC_DRAW, self.textTexture)

        infectedShape = tx.textToShape('Cases', charSize2, charSize2)
        uninfectedShape = tx.textToShape('Uninfected', charSize2, charSize2)
        recoveredShape = tx.textToShape('Recovered', charSize2, charSize2)
        deathsShape = tx.textToShape('Deaths', charSize2, charSize2)
        self.gpuInfected = es.toGPUShapeText(infectedShape, GL_STATIC_DRAW, self.textTexture)
        self.gpuUninfected = es.toGPUShapeText(uninfectedShape, GL_STATIC_DRAW, self.textTexture)
        self.gpuRecovered = es.toGPUShapeText(recoveredShape, GL_STATIC_DRAW, self.textTexture)
        self.gpuDeaths = es.toGPUShapeText(deathsShape, GL_STATIC_DRAW, self.textTexture)

    def draw(self,pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), self.r, self.g, self.b, 1)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0, 0, 0, 0)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.05, -0.65 + self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuXAxis)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.6, -0.22 + self.up, 0),
                                      tr.rotationZ(np.pi/2),
                                      tr.scale(1, 0.5, 1)]))
        pipeline.drawShape(self.gpuYAxis)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.61, -0.22 - 0.2, 0),
                                      tr.rotationZ(np.pi/2),
                                      tr.scale(1, 0.5, 1)]))
        pipeline.drawShape(self.gpuRadiusAxisShape)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.65, -0.22 - 0.43 - 0.28, 0),
                                      tr.rotationZ(np.pi / 2),
                                      tr.scale(1, 0.5, 1)]))
        pipeline.drawShape(self.gpuProbAxisShape)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.61, -0.22 - 0.43 - 0.28, 0),
                                      tr.rotationZ(np.pi / 2),
                                      tr.scale(1, 0.5, 1)]))
        pipeline.drawShape(self.gpuProbAxisShape2)

        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(-0.5 - 0.03/4, -0.59 + self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuOrigin)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.9, 0.2, 0.2, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.6, 0.3+self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuInfected)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.2, 0.2, 0.9, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.6, 0.2 + self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuUninfected)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.3, 0.3, 0.3, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.6, 0.1 + self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuRecovered)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 90 / 255, 0, 140 / 255, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.6, 0 + self.up, 0),
                                      tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuDeaths)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), self.r, self.g, self.b, 1)

class Plots:

    def __init__(self, x, n_infections, n_uninfected, n_recovered, n_deaths, radiusesT, probT, textureText, r, g, b):
        assert(len(n_infections)>1)
        self.textureText = textureText
        self.n = x[-1]
        self.r = r
        self.g = g
        self.b = b
        charSize = 0.03
        gpuDivision = es.toGPUShape(bs.createLine(r,g,b))
        self.mark = sg.SceneGraphNode('marks')
        self.x=x

        self.transMax1 = -0.5 * charSize / 2
        self.transMax2 = -1 * charSize / 2
        self.transMax3 = -1.5 * charSize / 2
        self.up = 0.45
        self.divisionsX = []

        self.marksBajas = sg.SceneGraphNode('dcskdvd')
        self.marksBajas.transform = tr.translate(-0.5,-0.5+self.up+0.05,0)

        if self.n>60:
            factorX = 10
        else:
            factorX = 5

        self.factorX = factorX
        for k in range(self.n // factorX + 1):
            ejeXnum = tx.textToShape(str(k*factorX), charSize, charSize)
            gpuEjeXnum = es.toGPUShapeText(ejeXnum, GL_STATIC_DRAW, self.textureText)
            self.divisionsX.append(gpuEjeXnum)

            markChica = sg.SceneGraphNode('markChica')
            markChica.childs += [gpuDivision]
            markChica.transform = tr.matmul([tr.translate(factorX * k / self.n, 0, 0), tr.scale(1, 0.5, 1)])
            self.mark.childs += [markChica]
            self.marksBajas.childs += [markChica]

        peopleI = n_uninfected[0] + 1
        self.peopleI = peopleI
        self.divisionsY = []

        if peopleI <= 100:
            factorY = 25
        elif peopleI <= 1200:
            factorY = 100
        else:
            factorY = 400

        self.factorY = factorY

        for k in range(1, peopleI // factorY + 1):
            markChica = sg.SceneGraphNode('markChica')
            markChica.childs += [gpuDivision]
            markChica.transform = tr.matmul([tr.translate(0, k * factorY / peopleI, 0),
                                              tr.rotationZ(-np.pi / 2),
                                              tr.scale(1, 0.25, 1)])
            self.mark.childs += [markChica]

            ejeYnum = tx.textToShape(str(k * factorY), charSize, charSize)
            gpuEjeYnum = es.toGPUShapeText(ejeYnum, GL_STATIC_DRAW, self.textureText)
            self.divisionsY.append(gpuEjeYnum)

        self.radiusMax = np.max(radiusesT)
        self.divisionsYRadiuses = []
        self.divisionsYProb = []
        self.markRadius = sg.SceneGraphNode('marks')

        for k in range(5):
            markChica = sg.SceneGraphNode('markChica')
            markChica.childs += [gpuDivision]
            markChica.transform = tr.matmul([tr.translate(0, k / 4, 0),
                                              tr.rotationZ(-np.pi / 2),
                                              tr.scale(1, 0.25, 1)])
            self.markRadius.childs += [markChica]

            ejeYnum = tx.textToShape(str(np.around(k / 4,2)), charSize, charSize)
            gpuEjeYnum = es.toGPUShapeText(ejeYnum, GL_STATIC_DRAW, self.textureText)
            self.divisionsYProb.append(gpuEjeYnum)

            ejeYnum = tx.textToShape(str(np.around(k * self.radiusMax / 4, 3)), charSize, charSize)
            gpuEjeYnum = es.toGPUShapeText(ejeYnum, GL_STATIC_DRAW, self.textureText)
            self.divisionsYRadiuses.append(gpuEjeYnum)

        gpuAxis = es.toGPUShape(bs.createArrows(r, g, b))
        gpuInfections = es.toGPUShape(bs.plotMultipleData(x, n_infections, 0.9, 0.2, 0.2, peopleI))
        gpuUninfected = es.toGPUShape(bs.plotMultipleData(x, n_uninfected, 0.2, 0.2, 0.9, peopleI))
        gpuRecovered = es.toGPUShape(bs.plotMultipleData(x, n_recovered, 0.3, 0.3, 0.3, peopleI))
        gpuDeaths = es.toGPUShape(bs.plotMultipleData(x, n_deaths, 75/255, 0, 130/255, peopleI))
        gpuRadiuses = es.toGPUShape(bs.plotMultipleData(x, radiusesT, 0, 0, 0, self.radiusMax))
        gpuProb = es.toGPUShape(bs.plotMultipleData(x, probT, 0, 0, 0, 1))

        self.axis = sg.SceneGraphNode('axis')
        self.axis.childs += [gpuAxis]
        self.axis.transform = tr.translate(-0.5, -0.5 + self.up, 0)

        self.radiusesNode = sg.SceneGraphNode('curva')
        self.radiusesNode.childs += [gpuRadiuses]
        self.radiusesNode.transform = tr.matmul([tr.translate(-0.5, -0.55, 0), tr.scale(1, 0.35, 1)])

        self.probNode = sg.SceneGraphNode('curva')
        self.probNode.childs += [gpuProb]
        self.probNode.transform = tr.matmul([tr.translate(0, -0.43, 0),
                                             tr.translate(-0.5, -0.55, 0),
                                             tr.scale(1, 0.35, 1)])

        self.plotsRyP = sg.SceneGraphNode('curva')
        self.plotsRyP.childs += [self.radiusesNode, self.probNode]

        infections = sg.SceneGraphNode('curva')
        infections.childs += [gpuInfections]

        uninfected = sg.SceneGraphNode('curva')
        uninfected.childs += [gpuUninfected]

        recovered = sg.SceneGraphNode('curva')
        recovered.childs += [gpuRecovered]

        deaths = sg.SceneGraphNode('curva')
        deaths.childs += [gpuDeaths]

        self.plot = sg.SceneGraphNode('plot')
        self.plot.transform = tr.translate(-0.5, -0.5 + self.up, 0)
        self.plot.childs += [infections, uninfected, recovered, deaths]

        self.markRadius.transform = tr.matmul([tr.translate(-0.5, -0.55, 0), tr.scale(1, 0.35, 1)])
        self.axisRadius = sg.SceneGraphNode('axisRadius')
        self.axisRadius.childs += [gpuAxis]
        self.axisRadius.transform = tr.matmul([tr.translate(-0.5, -0.5 - 0.05, 0), tr.scale(1, 0.35, 1)])

        self.axisProb = sg.SceneGraphNode('axisProb')
        self.axisProb.childs += [gpuAxis]
        self.axisProb.transform = tr.matmul([tr.translate(-0.5, -0.5 - 0.48, 0), tr.scale(1, 0.35, 1)])

        self.markProb = sg.SceneGraphNode('markProb')
        self.markProb.childs += [self.markRadius]
        self.markProb.transform = tr.translate(0, -0.43, 0)

        self.markXRadius = sg.SceneGraphNode('fdsfv')
        self.markXRadius.childs += [self.marksBajas]
        self.markXRadius.transform = tr.translate(0, -0.55, 0)

        self.markXProb = sg.SceneGraphNode('fdsfv')
        self.markXProb.childs += [self.markXRadius]
        self.markXProb.transform = tr.translate(0, -0.43, 0)

        self.othersMarks = sg.SceneGraphNode('fdsvdsg')
        self.othersMarks.childs += [self.markXRadius, self.markXProb]

        self.mark.transform = tr.translate(-0.5, -0.5 + self.up, 0)

    def draw(self, pipeline, pipelineText):
        glUseProgram(pipeline.shaderProgram)
        sg.drawSceneGraphNodeLines(self.plot, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.axis, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.mark, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.markRadius, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.axisRadius, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.axisProb, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.markProb, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.othersMarks, pipeline, 'transform')
        sg.drawSceneGraphNodeLines(self.plotsRyP, pipeline, 'transform')

        glUseProgram(pipelineText.shaderProgram)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), self.r, self.g, self.b, 1)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0, 0, 0, 0)

        n = len(self.divisionsX)
        for j in range(n):
            if j < 2:
                glUniformMatrix4fv(glGetUniformLocation(pipelineText.shaderProgram, "transform"), 1, GL_TRUE,
                                   tr.matmul([tr.translate(-0.5 + self.transMax1, -0.59 + self.up, 0),
                                              tr.translate(j * self.factorX / self.n, 0, 0),
                                              tr.scale(0.5, 1, 1)]))

                pipelineText.drawShape(self.divisionsX[j])

            else:
                glUniformMatrix4fv(glGetUniformLocation(pipelineText.shaderProgram, "transform"), 1, GL_TRUE,
                                   tr.matmul([tr.translate(-0.5 + self.transMax2, -0.59 + self.up, 0),
                                              tr.translate(j * self.factorX / self.n, 0, 0),
                                              tr.scale(0.5, 1, 1)]))

                pipelineText.drawShape(self.divisionsX[j])

        ny = len(self.divisionsY)
        for j in range(ny):

            glUniformMatrix4fv(glGetUniformLocation(pipelineText.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(-0.54 + self.transMax3, -0.5 + self.transMax1 + self.up, 0),
                                          tr.translate(0, (j + 1) * self.factorY / self.peopleI, 0),
                                          tr.scale(0.5, 1, 1)]))

            pipelineText.drawShape(self.divisionsY[j])

        for j in range(5):

            glUniformMatrix4fv(glGetUniformLocation(pipelineText.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(-0.54 + self.transMax3 - 0.02, -0.55 + self.transMax1, 0),
                                          tr.translate(0, j*0.35/4, 0),
                                          tr.scale(0.4, 0.8, 1)]))

            pipelineText.drawShape(self.divisionsYRadiuses[j])

            glUniformMatrix4fv(glGetUniformLocation(pipelineText.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(-0.54 + self.transMax3 - 0.02, -0.55 + self.transMax1 - 0.43, 0),
                                          tr.translate(0, j * 0.35 / 4, 0), tr.scale(0.4, 0.8, 1)]))

            pipelineText.drawShape(self.divisionsYProb[j])

class Parameters:

    def __init__(self, textureText, charSizeD, charSizeP, day, infected, uninfected, recovered,
                 deaths, radius, probMove):

        self.textureText = textureText
        self.charSizeD = charSizeD
        self.charSizeP = charSizeP
        self.mod = True

        dayShape = tx.textToShape('Day ' + str(day) + '  ', self.charSizeD, self.charSizeD)
        infectedShape = tx.textToShape('Cases: ' + str(int(infected)) + '   ', self.charSizeP, self.charSizeP)
        uninfectedShape = tx.textToShape('Uninfected: ' + str(uninfected) + '   ', self.charSizeP, self.charSizeP)
        recoveredShape = tx.textToShape('Recovered: ' + str(recovered) + '   ', self.charSizeP, self.charSizeP)
        deathsShape = tx.textToShape('Deaths: ' + str(deaths) + '   ', self.charSizeP, self.charSizeP)
        radiusShape = tx.textToShape('Contagion radius: ' + str(radius) + '  ', self.charSizeP, self.charSizeP)
        probMovShape = tx.textToShape('Percentage of movement: ' + str(probMove) + '  ', self.charSizeP,
                                      self.charSizeP)

        self.gpuDay = es.toGPUShapeText(dayShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuInfected = es.toGPUShapeText(infectedShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuUninfected = es.toGPUShapeText(uninfectedShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuRecovered = es.toGPUShapeText(recoveredShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuDeaths = es.toGPUShapeText(deathsShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuRadius = es.toGPUShapeText(radiusShape, GL_DYNAMIC_DRAW, self.textureText)
        self.gpuProbMov = es.toGPUShapeText(probMovShape, GL_DYNAMIC_DRAW, self.textureText)

    def updateRadius(self,newRadius):
        radiusShape = tx.textToShape('Contagion radius: ' + str(newRadius) + '  ', self.charSizeP, self.charSizeP)
        es.updateGPUShape(self.gpuRadius, radiusShape, GL_DYNAMIC_DRAW)

    def updateProb(self, nuevaProb):
        probMovShape = tx.textToShape('Percentage of movement: ' + str(nuevaProb) + '  ', self.charSizeP,
                                    self.charSizeP)
        es.updateGPUShape(self.gpuProbMov, probMovShape, GL_DYNAMIC_DRAW)

    def updateToll(self, newDay, newUninfected, newInfected, newRecovered, newDeaths):
        dayShape = tx.textToShape('Day ' + str(newDay), self.charSizeD, self.charSizeD)
        infectedShape = tx.textToShape('Cases: ' + str(int(newInfected)), self.charSizeP, self.charSizeP)
        uninfectedShape = tx.textToShape('Uninfected: ' + str(int(newUninfected)), self.charSizeP, self.charSizeP)
        recoveredShape = tx.textToShape('Recovered: ' + str(int(newRecovered)), self.charSizeP, self.charSizeP)
        deathsShape = tx.textToShape('Deaths: ' + str(int(newDeaths)), self.charSizeP, self.charSizeP)

        es.updateGPUShape(self.gpuDay, dayShape, GL_DYNAMIC_DRAW)
        es.updateGPUShape(self.gpuInfected, infectedShape, GL_DYNAMIC_DRAW)
        es.updateGPUShape(self.gpuUninfected, uninfectedShape, GL_DYNAMIC_DRAW)
        es.updateGPUShape(self.gpuRecovered, recoveredShape, GL_DYNAMIC_DRAW)
        es.updateGPUShape(self.gpuDeaths, deathsShape, GL_DYNAMIC_DRAW)

    def draw(self, pipeline):
        glUseProgram(pipeline.shaderProgram)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 1, 1, 1, 1)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.1, 0.5, 0), tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuDay)

        if self.mod:
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(0.1, -0.3, 0), tr.scale(0.5, 1, 1)]))
            pipeline.drawShape(self.gpuProbMov)

            glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0.2, 0.2, 0.6, 0.5)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(0.1, -0.2, 0), tr.scale(0.5, 1, 1)]))
            pipeline.drawShape(self.gpuRadius)

        else:
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(0.1, -0.2, 0), tr.scale(0.5, 1, 1)]))
            pipeline.drawShape(self.gpuRadius)

            glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0.2, 0.2, 0.6, 0.5)
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                               tr.matmul([tr.translate(0.1, -0.3, 0), tr.scale(0.5, 1, 1)]))
            pipeline.drawShape(self.gpuProbMov)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.9, 0.2, 0.2, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.1, 0.3, 0), tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuInfected)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.2, 0.2, 0.9, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.1, 0.2, 0), tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuUninfected)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 0.3, 0.3, 0.3, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.1, 0.1, 0), tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuRecovered)

        glUniform4f(glGetUniformLocation(pipeline.shaderProgram, "fontColor"), 90/255, 0, 140/255, 1)
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.matmul([tr.translate(0.1, 0, 0), tr.scale(0.5, 1, 1)]))
        pipeline.drawShape(self.gpuDeaths)

class Models:

    def __init__(self):
        gpuCircleContagiada = es.toGPUShape(bs.createColorCircle(0.9, 0.2, 0.2))
        gpuCircleUninfected = es.toGPUShape(bs.createColorCircle(0.2, 0.2, 0.9))
        gpuCircleRecovered = es.toGPUShape(bs.createColorCircle(0.3, 0.3, 0.3))
        gpuRadius = es.toGPUShape(bs.createColorCircleLines(1, 0, 0))

        self.modelContagiada = sg.SceneGraphNode('circleInfected')
        self.modelContagiada.childs += [gpuCircleContagiada]
        self.modelRadius = sg.SceneGraphNode('radiusI')
        self.modelRadius.childs += [gpuRadius]
        self.modelUninfected = sg.SceneGraphNode('circleSano')
        self.modelUninfected.childs += [gpuCircleUninfected]
        self.modelRecovered = sg.SceneGraphNode('circleRecovered')
        self.modelRecovered.childs += [gpuCircleRecovered]

class Groups:

    def __init__(self, n, daysRec):
        self.n = n
        self.infected = np.zeros(n)
        self.uninfected = np.zeros(n)
        self.recovered = []
        self.deaths = []
        self.daysInfected = np.zeros(n)
        self.days_to_heal = daysRec

    def addInfected(self, indices):
        self.infected[indices] = True

    def addUninfected(self, indices):
        self.uninfected[indices] = True

    def addRecovered(self, indices):
        self.recovered += list(indices)

    def addDeaths(self, indices):
        self.deaths += list(indices)

    def deleteUninfected(self, indices):
        self.uninfected[indices] = False

    def deleteInfected(self, indices):
        self.infected[indices] = False

    def getInfected(self):
        return (np.where(self.infected))[0]

    def getUninfected(self):
        return (np.where(self.uninfected))[0]

    def updateDaysInfected(self):
        self.daysInfected[(np.where(self.infected))[0]] += 1
        recovered = (np.where(self.daysInfected > self.days_to_heal))[0]
        self.daysInfected[recovered] = 0
        self.addRecovered(recovered)
        self.deleteInfected(recovered)
        return recovered

    def numberInfections(self):
        return np.sum(self.infected)

    def numberUninfected(self):
        return np.sum(self.uninfected)

    def numberRecovered(self):
        return len(self.recovered)

    def numberDeaths(self):
        return len(self.deaths)

class Person:

    def __init__(self, n, posiciones, i, models_1, state):
        self.n = n
        self.scale = -0.000002*n + 0.022
        self.i = i
        self.move = False
        self.matrix = posiciones
        self.posiciones = posiciones.pos
        self.pos = self.posiciones[i]
        self.alive = True
        self.state = state
        self.models = models_1
        self.modelRadius = None

        if self.state == 1:
            self.model = self.models.modelContagiada
            self.modelRadius = self.models.modelRadius
        elif self.state == 2:
            self.model = self.models.modelUninfected
        else:
            self.model = self.models.modelRecovered

    def update(self, move):
        if move and self.alive:
            self.pos = self.matrix.pos[self.i]

    def recover(self):
        if self.alive:
            self.state = 3
            self.model = self.models.modelRecovered

    def getInfected(self):
        if self.alive:
            self.state = 1
            self.model = self.models.modelContagiada
            self.modelRadius = self.models.modelRadius

    def draw(self, pipeline):
        if self.alive:
            glUseProgram(pipeline.shaderProgram)
            self.model.transform = tr.matmul([tr.translate(-0.5, 0, 0),
                                              tr.scale(0.4, 0.8, 1),
                                              tr.translate(self.pos[0], self.pos[1], 0),
                                              tr.uniformScale(self.scale)])
            sg.drawSceneGraphNode(self.model, pipeline, 'transform')

            if self.state == 1:
                self.modelRadius.transform = tr.matmul([tr.translate(-0.5, 0, 0),
                                                       tr.scale(0.4, 0.8, 1),
                                                       tr.translate(self.pos[0], self.pos[1], 0),
                                                       tr.uniformScale(self.matrix.radius*2)])
                sg.drawSceneGraphNodeLines(self.modelRadius, pipeline, 'transform')

class Population:

    def __init__(self, populationInitial, delta, states, radius, probContagio, mortality, daysRecover, toll):
        self.move = False
        self.delta = delta
        self.n = populationInitial
        self.pos = np.random.uniform(low = -0.95, high = 0.95, size = (self.n, 2))
        self.count = 0
        self.angles = np.random.uniform(low = 0, high = 2 * np.pi, size = self.n)
        self.states = states
        self.lista = None
        self.radius = radius
        self.probContagio = probContagio
        self.mortality = mortality
        self.daysRecover = daysRecover
        self.day = 0
        self.mobilityLess = False
        self.listaStill = np.ones(self.n)
        self.probMove = 1
        self.tollText = toll
        self.historyInfected = [1]
        self.historyUninfected = [populationInitial - 1]
        self.historyRecovered = [0]
        self.historyDeaths = [0]
        self.historyRadius = [radius]
        self.historyProb = [1]
        self.continuo = False

    def setLista(self,lista):
        self.lista = lista

    def static(self):
        if self.probMove < 1:
            self.listaStill = np.random.choice([0, 1], self.n, p = [1 - self.probMove, self.probMove])
            self.mobilityLess = True
        else:
            self.listaStill = np.ones(self.n)
            self.mobilityLess = False

    def getInfected(self):
        infected = self.states.getInfected()
        uninfected = self.states.getUninfected()
        for k in infected:
            enRadius = np.where((np.linalg.norm(self.pos[k] - self.pos[uninfected], axis = 1)) <= self.radius)
            probas = np.random.choice([0, 1], len(enRadius[0]), p = [1 - self.probContagio, self.probContagio])
            newsInfections = np.where(probas)
            self.states.addInfected(uninfected[(enRadius[0])[newsInfections[0]]])
            self.states.deleteUninfected(uninfected[(enRadius[0])[newsInfections[0]]])
            for j in uninfected[(enRadius[0])[newsInfections[0]]]:
                self.lista[j].getInfected()

    def die(self):
        infected = self.states.getInfected()
        deaths = np.random.choice([0, 1], len(infected), p = [1 - self.mortality, self.mortality])
        self.states.addDeaths(infected[(np.where(deaths))[0]])
        self.states.deleteInfected(infected[(np.where(deaths))[0]])
        for j in infected[(np.where(deaths))[0]]:
            self.lista[j].alive = False

    def update(self, dt):
        if self.move:
            sgtePos = self.pos + (np.array([np.cos(self.angles)*self.listaStill,
                                            np.sin(self.angles)*self.listaStill]).
                                  transpose())*dt

            matrix = (sgtePos > 0.95) + (sgtePos < -0.95)
            indices = np.where((np.any(matrix, axis = 1)))
            directions = np.random.uniform(low = -0.95, high = 0.95, size = (len(indices), 2)) - self.pos[indices]
            neg = directions[:, 1] >= 0
            ang = np.arccos(np.dot(directions, np.array([1, 0])) / (np.linalg.norm(directions, axis = 1)))
            angles = ang*neg + (-ang*~neg)
            self.angles[indices] = angles
            self.pos = sgtePos
            self.pos[indices] += (np.array([np.cos(angles), np.sin(angles)]).transpose())*dt
            self.count += dt

            if self.count >= self.delta:
                self.angles = np.random.uniform(low = 0, high = 2 * np.pi, size = self.n)
                recovered = self.states.updateDaysInfected()
                for k in recovered:
                    self.lista[k].recover()
                self.count = 0
                if not self.continuo:
                    self.move = False
                self.day += 1
                self.die()
                self.getInfected()
                if self.mobilityLess:
                    self.listaStill = np.random.choice([0, 1],self.n,
                                                            p = [1 - self.probMove, self.probMove])
                uninfected = self.states.numberUninfected()
                infected = self.states.numberInfections()
                recovered = self.states.numberRecovered()
                deaths = self.states.numberDeaths()
                
                self.tollText.updateToll(self.day, uninfected, infected, recovered, deaths)
                self.historyUninfected.append(uninfected)
                self.historyInfected.append(infected)
                self.historyRecovered.append(recovered)
                self.historyDeaths.append(deaths)
                self.historyRadius.append(self.radius)
                self.historyProb.append(self.probMove)

    def plotMatplot(self):
        daysX = np.arange(self.day + 1)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, gridspec_kw={'height_ratios': [3, 1, 1]})
        ax1.plot(daysX, self.historyInfected, color=(0.9, 0.2, 0.2))
        ax1.plot(daysX, self.historyUninfected, color=(0.2, 0.2, 0.9))
        ax1.plot(daysX, self.historyRecovered, color=(0.3, 0.3, 0.3))
        ax1.plot(daysX, self.historyDeaths, color=(75 / 255, 0, 130 / 255))
        ax1.legend(('Infected', 'Uninfected', 'Recovered', 'Deaths'), loc=0)
        ax1.set_title('Total count per day')
        ax2.plot(daysX, self.historyRadius)
        ax2.set_title('Radius per day')
        ax3.plot(daysX, self.historyProb)
        ax3.set_title('Percentage of movement per day')
        ax1.set(ylabel='Number of people')
        ax2.set(ylabel='Radius')
        ax3.set(ylabel='Per. of movement')
        plt.xlabel('Day')
        fig.tight_layout()
        plt.show()