<p align="center">
  <img width="460" height="300" src="https://github.com/Mario181091/Mario_content/blob/master/bg.png">
</p>

# PitE-Ai-Tetris


This is the project of the course "Python in the Enterprise", has been implemented an Artificial intelligence for the game [Tetris](https://en.wikipedia.org/wiki/Tetris) by using [DLV](https://en.wikipedia.org/wiki/DLV) and then through a Java Module link it with Python.

## Structure 
The structure of our project can be described with follow image:

<p align="center">
  <img width="460" height="300" src="https://raw.githubusercontent.com/Mario181091/Mario_content/master/structure_project.png">
</p>

From a structural point of view, the main problem of project was linking DLV system with Python module, infact there isn't wrapper between these two languages. 
As can be seen in the image this problem has been solved with the help of Java virtual machines. This was possible becouse exist a wrapper between DLV an Java ([DLV Wrapper](http://www.dlvsystem.com/dlvwrapper/)) and at same time exist also a wrapper between Java and Python ([Py4j](https://www.py4j.org/install.html#install-instructions)). So it was possible use Java like a bridge throught DLV and Python.       

* **DLV** <br />
Datalog is a declarative (programming) language. This means that the programmer does not write a program that solves some problem but instead specifies what the solution should look like, and a Datalog inference engine tries to find the the way to solve the problem and the solution itself. This is done with rules and facts.<br />  **Facts** are the input data, and **rules** can be used to derive more facts, and hopefully, the solution of the given problem.<br /> 
DLV (datalog with disjunction) is a powerful though freely available deductive database system. It is based on the declarative programming language datalog, which is known for being a convenient tool for knowledge representation. With its disjunctive extensions, it is well suited for all kinds of nonmonotonic reasoning, including diagnosis and planning.

* **DLV rappresentation of Tetris Game** <br />
TO DO:




  
## Authors

* **Mario Egidio Carricato** - *Erasmus student AGH* - [other projects](https://github.com/mario181091)
* **Marco Amato** - *Erasmus student AGH* - [other projects](https://github.com/mark91m12)
