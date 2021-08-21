import glfw
import sys

from Mvirus import *
from Cvirus import Controller
import json
from mod import text_renderer as tx

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        raise Exception('No se ingresó el archivo con datos')
    else:
        file = sys.argv[1]
    # file = 'virus.json'

    if not glfw.init():
        sys.exit()

    width = 1800
    height = 900

    window = glfw.create_window(width, height, "Pandemic Simulator", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controller = Controller()

    glfw.set_key_callback(window, controller.on_key)

    pipeline = es.SimpleTransformShaderProgram()
    texturePipeline = es.SimpleTextureShaderProgram()
    textPipeline = tx.TextureTextRendererShaderProgram()

    glClearColor(0.1, 0.1, 0.1, 1.0)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    with open(file) as f:
        data = json.load(f)

    radius = data[0]["Radius"]
    contagious_prob = data[0]["Contagious_prob"]
    death_rate = data[0]["Death_rate"]
    initial_population = data[0]["Initial_population"]
    days_to_heal = data[0]["Days_to_heal"]

    # Creating texture with all characters
    textBitsTexture = tx.generateTextBitsTexture()
    # Moving texture to GPU memory
    gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)

    parameters = Parameters(gpuText3DTexture, 0.08, 0.05, 0, 1, initial_population - 1, 0, 0, radius, 1)
    label = Label(gpuText3DTexture,0,0,0)
    square = Square(1.98)
    groups = Groups(initial_population, days_to_heal)
    population = Population(initial_population, 0.2, groups, radius, contagious_prob, death_rate,
                            days_to_heal, parameters)

    models = Models()

    controller.set_model(population, parameters, gpuText3DTexture)
    people = [Person(initial_population, population, 0, models_1 = models, state = 1)]
    groups.addInfected(0)

    for i in range(initial_population-1):
        people.append(Person(initial_population, population, i + 1, models_1 = models, state = 2))
        groups.addUninfected(i + 1)

    population.setLista(people)
    aFactor = 0.000008 * initial_population ** 2 - 0.016 * initial_population + 16
    if initial_population>=2000:
        aFactor = 16
    t0 = glfw.get_time()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)

        t1 = glfw.get_time()
        dt = (t1 - t0) / aFactor
        t0 = t1

        if controller.simulation:
            square.draw(pipeline)
            population.update(dt)
            for person in people:
                person.update(population.move)
                person.draw(pipeline)
            parameters.draw(textPipeline)
        else:
            controller.plot.draw(pipeline, textPipeline)
            label.draw(textPipeline)

        glfw.swap_buffers(window)

    glfw.terminate()
