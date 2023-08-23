# Swish Bish Prolog

The project consists of an interpreter and an accompanying editor built with **tkinter**. 

## How to run 

* Install dependencies

```sh
pip install -r requirements.txt
```

* To start the editor 

```sh
python editor.py
```  

* To run the tests

```sh 
pytest tests
```


## Project Overview

### Intepreter 
The programming language is a subset of pure prolog.

* The prolog interpreter implements an SLD resolution scheme(unification + backtracking). 

* Negation as failure is also supported.   

Sample programs can be found in the **sample** folder.  

#### Examples

Given the clauses in the ```family_relations.pl``` program in the **sample** folder, here are some sample queries\: 

```pl
ancestor(X, Y).
```  

```pl
ancestor(hamish, anne).
```  

```pl
ancestor(hamish, 'anne').
```

```pl
ancestor(hamish, 'rosie').
```

```pl
sibling(X, Y).
```

```pl
not(ancestor(hamish, jack)).
```


### Editor features 

#### File menu 

Includes the standard operations ```new```,```open```, ```save```, ```save as```, ```exit```.

#### Preferences menu 

* Font  
The user can set the font family and size

* Mode  
There are 3 modes to choose from\:  
    * Dark
    * Light
    * Swish Bish

#### Other features 

* Line-number bar 
* Key-bindings 
    * for saving ```<Control-s>```   
    * for running the current program, with respect to the current query ```<Control-Return>```


## Future improvements

* list support
* more informative error messages
* arithmetics
* unification over infinite trees