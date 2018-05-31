<p align="center">
  <img width="460" height="300" src="https://github.com/Mario181091/Mario_content/blob/master/bg.png">
</p>

# PitE-Ai-Tetris

[![HitCount](http://hits.dwyl.io/mark91m12/PitE-AI-Tetris.svg)](http://hits.dwyl.io/mark91m12/PitE-AI-Tetris)     [![M&M](https://img.shields.io/badge/m%26m-projects-blue.svg)](https://img.shields.io/badge/m%26m-projects-blue.svg)

This is the project of the course "Python in the Enterprise", has been implemented an Artificial intelligence for the game [Tetris](https://en.wikipedia.org/wiki/Tetris), has been used [DLV](https://en.wikipedia.org/wiki/DLV) for the core of A.I. and then through a Java Module it has been linked with Python.

## Structure 
The structure of our project can be described by the following image:

<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/structure_project.png">
</p>

From a structural point of view, the main problem of project was linking DLV system with Python module, indeed there isn't a library that link directly these two languages. 
As can be seen in the image this problem has been solved with the help of Java virtual machines. This was possible because exists a wrapper between DLV and Java ([DLV Wrapper](http://www.dlvsystem.com/dlvwrapper/)) and at same time exist also a "bridge" between Java and Python ([Py4j](https://www.py4j.org/install.html#install-instructions)). So it was possible use Java like a bridge between DLV and Python.       

* **DLV** <br />
Datalog is a declarative (programming) language. This means that the programmer does not write a program that solves some problem but instead specifies what the solution should look like, and a Datalog inference engine tries to find the the way to solve the problem and the solution itself. This is done with rules and facts.<br />  **Facts** are the input data, and **rules** can be used to derive more facts, and hopefully, the solution of the given problem.<br /> 
DLV (datalog with disjunction) is a powerful though freely available deductive database system. It is based on the declarative programming language datalog, which is known for being a convenient tool for knowledge representation. With its disjunctive extensions, it is well suited for all kinds of nonmonotonic reasoning, including diagnosis and planning.

* **DLV representation of Tetris Game** <br />
The following image rapresents how pieces are built for the A.I.: there are 4 configuration for pieces (S,Z,J,L,T), 2 configuration for the I piece and just one for the O piece, the cell (2,2) of each piece rapresents the pivot of the shape (the piece will be placed on the board by the A.I. based on this cell).<br/>
<p align="center">
  <img width="760" height="700" src=https://raw.githubusercontent.com/Mario181091/Mario_content/master/Copy%20of%20shapes%20Tetris%20-%20New%20frame.jpg">
</p><br/>
The following example show how the A.I. works, it takes in input the new piece (in this case L with all its configuration) and the current board configuration, at this point based on this notions and applying all rules, it gives in output the cell where the piece must be placed.<br/>
<p align="center">
  <img width="760" height="500" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/Copy%20of%20shapes%20Tetris%20-%20New%20frame%20(1).jpg">
</p>

* **DLV Wrapper and py4j library** <br />
The DLV Wrapper API is a Java Library containing a class called **DLVWrapper**; this class is a singleton that always returns the same object instance of WLVWrapper. The DLVWrapper class implements the necessary methods to create a new object that provides to initialize, execute and recive the results from a DLV process. The interface DLVInvocation implements the pattern Observer and it is the observable that notifies to every signed observer (each class implementing the interface DLVHandler) the results of DLV execution.<br /><br /> 
**Py4J** enables Python programs running in a Python interpreter to dynamically access Java objects in a Java Virtual Machine. Methods are called as if the Java objects resided in the Python interpreter and Java collections can be accessed through standard Python collection methods. Py4J also enables Java programs to call back Python objects.
These two library are used rispectively for enable the comunication between DLV and Java and between Java and Python. The result is a custom wrapper that are used like a bridge between the DLV system and the Python module.

* **Python module** <br />
Has been developed python desktop application that is able to receive messages from the Java module containing the game logic. <br />Information like **next piece**, **rotation or position of the piece** are conteined in this comunication, the application exhibit proper performance and good usability, infact it efficiently processes the message and consequentily updates the GUI <br />During the development has been used **Pygame** and **PyQt5** libraries.


## Features

* **Start Game** : start a classic istance of Tetris game.
* **Start Frenzy Game** : start a fast and frenzy game with the scope to test the response of AI at high speed.

## Getting Started

**Prerequisites**
* In order to run this project is important to use python version 3 or upper,Java 1.8 or upper and DLV Wrapper, py4j, Pygame and PyQt5 libraries.<br />

  Install Python with:
  
  ```shell
   $ sudo apt-get install python3
  ```
  now check your version: 
  ```shell
  $ python --version
  ```
  Install Java follow this [guide](https://www.java.com/en/download/help/windows_manual_download.xml)
  
  now check your version: 
  ```shell
  $ java --version
  ```
  
   Install Pygame with:
  
  ```shell
   $ pip install Pygame
  ```
  
   Install PyQt5 with:
  
  ```shell
   $ pip install PyQt5
  ```
  
   Install py4j with:
  
  ```shell
   $ pip install py4j
  ```
  
**Basic usage**
<br> You can use the [eclipse](https://www.eclipse.org/downloads/packages/all) ide for java developers, once the project has been imported in order to run the Java module you need to configure the build path adding the libraries DlvWrapper and Py4j, now you can run the Java module named Bridge.
At this point once the server is running you can launch the python game directly from ecplipse using the plugin [PyDev](http://www.pydev.org/) or you simply move in the project folder, precisely in the folder "src/game" and run the following command :
  
  ```shell
   $ python MainMenu.py
  ```

## Games approaches and Testing
Like in real life were taken into consideration two of most common ways to play Tetris: the horizontal one (rarely used) and the vertical one.<br>

**Horizontal approach**
this way of play tetris tries to minimize the height of the Board Configuration and he doesn't care of the problem of the blanks space in each rows. 
<br>
The follow image show the results of 15 run with this kind of approach:

<p align="center">
  <img width="660" height="400" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/horizontal.PNG">
</p>

**Vertical approach** 
Is a kind of approach that tries to minimize the blanks in each rows of the Board Configuration and it doesn't care of the problem of the configuration's height. Of course this approach aims to build better configuration for the next pieces in input. 
<br>
The follow image show the results of 15 run with this kind of approach:


<p align="center">
  <img width="660" height="400" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/vertical.PNG">
</p>

**Skynet** 
Our solution is a fusion of this two kinds of approaches. Like a human our Artificial Intelligence (Skynet) mix both way to play. It tries to minimize the blanks in each rows of the Board Configuration using the vertical approach, and when the configuratuon become too height it change strategy and tries to minimize this height with horizontal approach.
<br>
So like a real player it bases its strategy on a current event of game. The follow image show the results of 15 run with Skynet:


<p align="center">
  <img width="660" height="400" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/skynet.PNG">
</p>

As we can see with the combination of two strategy the means of point for match is significantly higher.

## Game Screen

In this section are proprosed some screenshots of game.

* User Interface:
<p align="center">
  <img width="460" height="330" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/main.PNG">
</p>


* Instance of game interface:
<p align="center">
  <img width="330" height="420" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/game.PNG">
</p>
 
## Authors

* **Mario Egidio Carricato** - *Erasmus student AGH* - [other projects](https://github.com/mario181091)
* **Marco Amato** - *Erasmus student AGH* - [other projects](https://github.com/mark91m12)
