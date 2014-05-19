## Synopsis

The Navigation and Viewing Framework was designed to enable users to create a variety of viewing setups using different input and display devices and user types in the VR lab at Bauhaus University Weimar (and elsewhere with similar infrastructure). It is based on the Virtual Reality framework avango and the rendering engine guacamole. In order to specify a concrete viewing setup within the framework, generic configuration files can be written.

## Motivation

There are many ways to interactively explore a virtual environment with multiple users. One has to choose from a large variety of input devices, display devices, navigation techniques and mechanisms for interacting with other parties. Many specialized navigation and viewing setups for several fields of application already exist in our laboratory, so we aimed at building a generic and configurable framework based on them. Input devices and the number of users of different types should be easily specified in a file, such that the framework builds up the navigation and viewing setups without the need of editing pieces of code. In addition, we want users to have avatar representations and groups should be able to couple theirselves to each other in order to explore the virtual environment together. To achieve maximum rendering performance, this framework should also be distributable to several hosts in a network if desired.

## Installation

No installation is necessary, the framework can be directly run using the command ./start-all.sh CONFIGURATION_FILE

## Documentation

All the classes including their variables and functions are explained in the documentation located at http://timdomino.github.io/navigation-viewing-framework/. Furthermore, all the tags usable in display and viewing setup configuration files are introduces and illustrated with examples.

## Contributors

André Kunert: andre.kunert@uni-weimar.de<br/>  
Joshua Reibert: joshua.reibert@uni-weimar.de<br/>  
Tim Weißker: tim.weissker@uni-weimar.de<br/> 
