# Pandemic simulator

Simple graphic simulation of the spread of a virus. 

<p align="center">
  <img src="https://github.com/MarioA-PM/Pandemic-simulator/blob/main/resources/gameIm/f1.jpg" height="300"/>
</p>

The simulation works by iterations representing a day, which means that a person can infect only at the end of the iteration and not while is moving. The parameters percentage of movement (which indicates the probability of a person to move on the respecting day) and contagion radius can be modified interactively during the simulation.

## Start the simulation

The file pandemic_simulator.py must be executed from a terminal passing a json file as follows:

``$ python pandemic_simulator.py virus.json``

The json file must have the following format:

```json
[
  {
    "Radius": 0.05,
    "Contagious_prob": 0.1,
    "Death_rate": 0.009,
    "Initial_population": 1000,
    "Days_to_heal": 8
  }
]
```

Where:

* **Radius** is the contagion radius between two people.
* **Contagious_prob** is the probability of an infected person to infect another within the contagion radius. 
* **Death_rate** is the probability of an infected person to die in every iteration.
* **Initial_population** is the number of people involved.
* **Days_to_heal** is the number of days after a person stops infecting. A recovered person is not susceptible to get infected again.

## Controls

<kbd class="text-bold hx_text-body">→</kbd> advance one day

<kbd class="text-bold hx_text-body">C</kbd> advance the days continually

<kbd class="text-bold hx_text-body">I</kbd> goes back to the manual advance of days

<kbd class="text-bold hx_text-body">P</kbd> ends the simulation and generate a plot with OpenGL

<kbd class="text-bold hx_text-body">S</kbd> generate a plot using matplotlib

<kbd class="text-bold hx_text-body">M</kbd> select the parameter percentage of movement to be modified

<kbd class="text-bold hx_text-body">R</kbd> select the parameter contagion radius to be modified

<kbd class="text-bold hx_text-body">↑</kbd> turn up the selected parameter

<kbd class="text-bold hx_text-body">↓</kbd> turn down the selected parameter

<kbd class="text-bold hx_text-body">esc</kbd> exit the program

<p align="center">
  <img src="https://github.com/MarioA-PM/Pandemic-simulator/blob/main/resources/gameIm/f2.jpg" height="300"/>
</p>

<p align="center">
  <img src="https://github.com/MarioA-PM/Pandemic-simulator/blob/main/resources/gameIm/f3.jpg" height="300"/>
</p>

<p align="center">
  <img src="https://github.com/MarioA-PM/Pandemic-simulator/blob/main/resources/gameIm/Figure_1.jpeg" height="300"/>
</p>
