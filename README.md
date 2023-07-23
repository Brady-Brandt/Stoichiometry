# Stoichiometry
### This was my final project for my high school chemistry class. My class seemed to struggle a lot with stoichiometry, so I decided to create an interactive app that would guide people through stiochiometry problems. Since I only had a about a week to build it, I didn't get make it complete. I have since added more features and fixed some bugs, but it still has some issues. 

### Features
## Practice Option that will give you a random problem to solve. 

![alt text](https://github.com/Brady-Brandt/Stoichiometry/blob/main/pictures/StepOne.png?raw=true)
![alt text](https://github.com/Brady-Brandt/Stoichiometry/blob/main/pictures/Steptwo.png?raw=true)
![alt text](https://github.com/Brady-Brandt/Stoichiometry/blob/main/pictures/FinalSteps.png?raw=true)

## Help me Option where you can input your own stoich problem that you need help solving
![alt text](https://github.com/Brady-Brandt/Stoichiometry/blob/main/pictures/Help.png?raw=true)

## Has a built in periodic table so you get all the atomic masses 
![alt text](https://github.com/Brady-Brandt/Stoichiometry/blob/main/pictures/table.png?raw=true)

# Install 
## Dependencies
+ [Python3](https://www.python.org/)
+ [Tkinter](https://docs.python.org/3/library/tkinter.html)
+ [Chempy](https://pypi.org/project/chempy/)

## MacOs 
### To install macos it is easiest to just install both the dev tools and homebrew.
### Open the terminal application and paste in the following commands. 
```Console
gcc
```
### This will give a prompt to install the dev tools. Click install and wait for that to finish. 
### Next we need to install homebrew to get tkinter. Copy these one by one commands: 
```Console
git clone https://github.com/Homebrew/brew homebrew
eval "$(homebrew/bin/brew shellenv)"
brew update --force --quiet
chmod -R go-w "$(brew --prefix)/share/zsh"
```
### Install tkinter 
```Console
brew install python-tk
```
### Install chempy
```Console
pip3 install chempy
```
### Clone this repo
```Console
git clone https://github.com/Brady-Brandt/Stoichiometry
```
### Open the Stoichiometry Folder
``` Console
cd Stoichiometry
```
### Run it
```Console
python3 main.py
```





# Issues
+ The layout of the widgets on the screen is not very dynamic. There is plenty of overlap issues.
+ Scrollbar doesn't reset after completing a problem.
+ Periodic table window is not resizable
+ Colorscheme is bland
