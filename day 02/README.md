# Python Lesson 2 – Input Methods and Exercises (Weizmann Institute)

This folder contains the scripts and notes from the second Python lesson at the Weizmann Institute.  
The main topic covered in this session was how different types of input can be provided to Python programs.

---

## Lesson Content

We explored three main modes of interaction between the user and a Python script:

### 1. CLI (Command Line Interface)
A text-based interface where the user interacts with the program by typing commands into a terminal.  
Inputs are provided through arguments or user prompts, for example by running a script and specifying an input file in the command line.

### 2. GUI (Graphical User Interface)
A visual interface with buttons, text boxes, sliders, or other graphical components.  
The user interacts using a mouse or touch rather than typing commands.  
GUIs are often built using libraries such as tkinter, PyQt, or Streamlit.

### 3. REPL (Read–Eval–Print Loop)
An interactive environment that reads user commands, evaluates them, and prints the result immediately.  
It is the mode used when typing directly into the Python interpreter or a Jupyter Notebook.  
This approach is useful for testing and quick exploration.

---

## Folder Structure

- in_class_exercises/ – Scripts and notebooks created during the lesson.  
- homework/ – Assignments and additional practice problems to complete independently.

---

## Homework Project: NeuroRender

For the homework, I developed a small program called NeuroRender, which allows the user to visualize selected brain regions from the ARA atlas.

### What is ARA?
ARA stands for Allen Reference Atlas, a standardized 3D anatomical atlas of the mouse brain developed by the Allen Institute for Brain Science.

### How it works
NeuroRender takes one or more brain region names or acronyms as input (for example, VISp, CA1, MOp) and displays a 3D rendering of the mouse brain highlighting the chosen areas.  
This visualization helps in understanding spatial relationships between different brain structures.

---

## Technologies Used

- Python 3.x  
- Libraries: numpy, matplotlib, plotly, nibabel, and brainrender (for 3D visualization)

---

## Notes

These scripts are meant for educational purposes, demonstrating:
- Different input handling strategies (CLI, GUI, REPL)  
- Practical application of 3D visualization in neuroscience
