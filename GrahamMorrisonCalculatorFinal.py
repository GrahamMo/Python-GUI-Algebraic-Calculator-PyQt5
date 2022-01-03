#Graham Morrison
#GrahamMorrisonCalculatorFinal.py
#Desktop calculator using pyqt5.

#Bonus Features:
#Dock Window Memory + Users can double click
#Active memory saving with exceptions to error statements and empty
#Memory Wipe
#Algebra solver + Assume 0 when one side left blank
#User can type input
#Sin, cos, tan
#sqrt()
#Exponent - **
#delete button
#Convert to fraction
#Visual Changes
#Pi button
#Hints for Can not compute
#Tooltip for what certain buttons do

#----------------------------------------------------------------------------
#PACKAGES
#PyQt5 - Terminal - pip install PyQt5
#SymPy - Terminal - pip3 install sympy
#----------------------------------------------------------------------------
#IMPORTING
import sys #opens and closes applications
import math #gain access to more than basic math functions

from sympy import symbols, Eq, solve #another math module for algebra

from fractions import Fraction #allows to change into fractions

#WIDGETS
# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtWidgets import* #just imports everything instead since I am using so many things, but Ill specify everything anyway
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication #to start
from PyQt5.QtWidgets import QMainWindow #provides a framework for building an application's user interface. 
from PyQt5.QtWidgets import QWidget #widget that pretty much all pyqt5 interfaces is based on as the central widget. It is what recieves events (ex. click, keydown)
from PyQt5.QtWidgets import QDesktopWidget #gives access to methods to get centre point of desktop

#DockWindow
from PyQt5.QtWidgets import QDockWidget #to make memory dock window
from PyQt5.QtWidgets import QListWidget #to make list on dock window
from PyQt5.QtWidgets import QAction #FOR TOGGLE VIEW

#StatusBar
from PyQt5.QtWidgets import QStatusBar

#button and grid layout
from PyQt5.QtWidgets import QGridLayout #to make button grid layout
from PyQt5.QtWidgets import QLineEdit #to make outputdisplay
from PyQt5.QtWidgets import QPushButton #to add buttons
from PyQt5.QtWidgets import QVBoxLayout #used to construct vertical box layout objects, will be base layout for buttons

from functools import partial #using instead of lambda
#----------------------------------------------------------------------------
class calcView(QMainWindow): #subclass of QMainWindow, where QMainWindow is the framework for buidling the GUI
    '''
    QMainWindow Layout
    ______________________________________
   |__Menu Bar____________________________| #dropdown menu selections file, edit, etc. not necessary for calculator
   |_______________ToolBars_______________| #makes buttons that give users access to functions, typcially just visual buttons for menu bar quick access not necessary for calculator
   |   __________Dock Windows__________   | #creates side view next to the central widget
   |  |                                |  |
   |  |                                |  |
   |  |          Cental Widget         |  | #the main widget, which is almost always QWidget to recieve the user's inputs
   |  |                                |  |
   |  |________________________________|  |
   |______________________________________|
   |___Status Bar_________________________| #can add temperary or permanent messages
    '''
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #INIT
    def __init__(self): #initialize the view
        super().__init__() #initialize the QMainWindow
        self.setWindowTitle('Calculator') #name the titlebar
        self.setFixedSize(350, 305) #define the size of the window
        self.setStyleSheet("background-color: #F6FCFC;")

        self.makeCentralWidget() #call the methods to make the parts of the window
        self.makeDockingWidget()
        self.makeMenuBar()

        self.moveToCentre()
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Central Widget
    def makeCentralWidget(self):
        self.centralWidget = QWidget(self) #make a variable to self that is an instance of QWidget
        self.setCentralWidget(self.centralWidget) #define that as the central widget

        self.baseLayout = QVBoxLayout() #make a variable to self that is an instance of QVBoxLayout, (taking that as base)
        self.centralWidget.setLayout(self.baseLayout) #from the class Q widget (which central widget is instance of,) set the layout to be and instance of QVBoxLayout

        self.createOutputLine() #making the display for the output
        self.createButtons() #making the buttons
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MenuBar
    def makeMenuBar(self):
        menuSelect = self.menuBar()
        menuSelectFile = menuSelect.addMenu('File')

        #saveAction = ('Save', self) #make save action
        self.saveAction = menuSelectFile.addAction('Save') #add the action to the menu

        #quitAction = ('Quit', self)
        self.quitAction = menuSelectFile.addAction('Quit')

        #events
        self.quitAction.triggered.connect(self.quitTrigger) #if quit action clicked then call quit method
        self.saveAction.triggered.connect(self.specialSave) #if save action clicked then call append to the memory the outputText

    #Special Save
    def specialSave(self):
        currentOutput = str(self.getOutputText()) #take of string of outputline

        memoryFile = open("GrahamCalculatorMemorySpecialSave.txt", "a") #also going to open the file / make it if it has not been made and (a for) append the last equation
        memoryFile.write(currentOutput) #then appends output to memoryFile
        memoryFile.write('\n') #make a new line
        memoryFile.close()#closes file after writing to it
        
        self.giveHint('Saved to GrahamCalculatorMemorySpecialSave.txt') #hi

    #Quit Action
    def quitTrigger(self):
        qApp.quit() #quits the application

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Docking Widget
    def makeDockingWidget(self):
        self.memoryBar = QDockWidget("Memory", self) #make new dock widget, "Memory" is title

        self.memoryList = QListWidget() #create instance of QListWidget
        self.memoryBar.setWidget(self.memoryList) #set that to the widget for the dock window

        self.memoryBar.setFloating(False) #keeps from moving

        self.addDockWidget(Qt.RightDockWidgetArea, self.memoryBar) #adds it to the right of central widget

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MOVE TO CENTRE
    def moveToCentre(self):
        self.rectangleInterface = self.frameGeometry() #calls frame geometry
        self.centerPoint = QDesktopWidget().availableGeometry().center() #which has the the ability to find the centre point of the desktop
        self.rectangleInterface.moveCenter(self.centerPoint) #following 2 lines move it to the centre point
        self.move(self.rectangleInterface.topLeft())
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MAKING OUTPUTLINE
    def createOutputLine(self): #make the display for the output Line
        self.outputLine = QLineEdit() #make the outputLine line an instace of widget QLineEdit 
        self.outputLine.setStyleSheet("background-color: #99BDD9; color: black") #set the background and text colour of the output line

        self.outputLine.setStyleSheet("font: bold") #making the font bold so its easier to read

        #edit the properties from QLineEdit
        self.outputLine.setFixedHeight(35) #set the height to 35 pixels
        self.outputLine.setAlignment(Qt.AlignRight) #make the text inside it aligned
        self.outputLine.setReadOnly(False) #set read only to false so the user can use the line to input numbers
        
        # Add the outputLine to the general layout
        self.baseLayout.addWidget(self.outputLine)
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MAKING BUTTONS
    def createButtons(self): #make all the buttons
        self.buttons = {} #make a dictionary so the text can be associated with a coordinate
        buttons = {'sin(': (0, 0), #giving buttons coordinates
                   'cos(': (0, 1), #ex. the button with 8 will be in coordinate 0,1
                   'tan(': (0, 2),
                   '(': (0, 3),
                   ')': (0, 4),
                   'CC': (0, 5),
                   '7': (1, 0),
                   '8': (1, 1),
                   '9': (1, 2),
                   '**': (1, 3),
                   'sqrt(': (1, 4),
                   'C': (1, 5),
                   '4': (2, 0),
                   '5': (2, 1),
                   '6': (2, 2),
                   '*': (2, 3),
                   '/': (2, 4),
                   'del': (2, 5),
                   '1': (3, 0),
                   '2': (3, 1),
                   '3': (3, 2),
                   '+': (3, 3),
                   '-': (3, 4),
                   'x': (3, 5),
                   '0': (4, 0),
                   '.': (4, 1),
                   'Enter': (4, 2),
                   'pi': (4, 3),
                   '≈': (4, 4),
                   '=': (4, 5),
                  }
        
        buttonLayout = QGridLayout() #make the button layout an instance of a grid layout

        for text, coordinate in buttons.items(): #create a for loop for each text in the dictionary, but also needs access to the definition / associated term of that text which is the coordinate
            self.buttons[text] = QPushButton(text) #make a variable that is the button+its text that is an instance of QPushButton (button making class) and add it to the object... QpushButton needs to know what to put on the button which is the argument (text)
            self.buttons[text].setFixedSize(35, 35) #define the size for the buttons
            #now a button object has been made and the dictionary, is now... ex. {'7': <PyQt5.QtWidgets.QPushButton object at 0x0000023E26CA0C10>, etc.} so the object is assiated with the text from the dictionary

            buttonLayout.addWidget(self.buttons[text], coordinate[0], coordinate[1]) #buttonLayout is an instance of grid layout... start making the grid layout with the now made buttons and their respective coordinates to the text in the dictionary
        
        self.buttonColourSets() #call to make the button visuals sets

        #setting tooltips for complicated buttons
        self.setToolTip('≈', 'This button converts a decimal into a fraction.') #call method with arguements being the button text and the tip
        self.setToolTip('x', "This button adds the varible x to the screen. Use with '=' to solve for x.")
        self.setToolTip('=', 'This button allows the calculator to solve for variables using algebra.')
        self.setToolTip('CC', "This button empties the file and memory window's memory.")
        self.setToolTip('C', "This button clears the output and adds it to the calculator's memory.")
        self.setToolTip('Enter', "This button evalutes the expression.")
        self.setToolTip('sqrt(', "This operator finds the square root of what is in the brackets. Ensure to close brackets.")
        self.setToolTip('**', "This operator also known as x^, makes the previous number to the power of the next inserted number of set of brackets.")

        # Add the grid layout (buttonLayout) to the base QVbox layout (buttonLayout instance)
        self.baseLayout.addLayout(buttonLayout)
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def buttonColourSets(self):
        numberStyle = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] #is just text so make str not int
        self.buttonSetColourChange(numberStyle, '#42858C', 'white') #call buttonSetColour change which will change the colour of every button in the given list

        #same for next style
        mainOperatorStyle = ['+', '-', '*', '/', '(', ')', '**', 'sqrt(']
        self.buttonSetColourChange(mainOperatorStyle, '#96AFB8', 'black')

        trigStyle = ['sin(', 'cos(', 'tan(']
        self.buttonSetColourChange(trigStyle, '#63CCCA', '#2F4F4F')

        algebraStyle = ['x', '=']
        self.buttonSetColourChange(algebraStyle, '#FFF7D0', 'black')

        clearStyle = ['C', 'CC']
        self.buttonSetColourChange(clearStyle, 'white', 'black')

        #even for singles going to make sets because than easier when more buttons added that want same colour set just to add to list
        fractionStyle = ['≈']
        self.buttonSetColourChange(fractionStyle, '#ADD8E6', 'black')

        deleteStyle = ['del']
        self.buttonSetColourChange(deleteStyle, '#F08080', 'white')

        enterStyle = ["Enter"]
        self.buttonSetColourChange(enterStyle, '#A0D6B4', 'black')

        piStyle = ["pi"]
        self.buttonSetColourChange(piStyle, '#8ED6D5 ', 'black')

    def buttonSetColourChange(self, buttonSet, backgroundColour, colour):
        for buttonText in buttonSet: #for for each text in the style set
            self.changeButtonColour(buttonText, backgroundColour, colour) #call the button colour changer to change each of those buttons to the specified background and text colour

    def changeButtonColour(self, text, backgroundColour, colour):
        self.buttons[text].setStyleSheet("background-color: {}; color: {};".format(backgroundColour, colour))  #set button text colour... add variables colour into {} by .format tuple order
    
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #HOVER TIP SETTER
    def setToolTip(self, text, tip):
        self.buttons[text].setToolTip(tip) #call setToolTip built in method that creates box with the 'tip' argument, when you hover over the instance of buttons[text]

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #OUTPUT TEXT 
    # MUTATOR / SETTER
    def setOutputText(self,output): #function that sets the text for the output. needs the paramter being the output which will be a string and access to self because setting text to self.outputLine
        self.outputLine.setText(output) #using setText method from class QLineEdit to give the line text, which is in this case the output. (cant be insert or else can not have clear function)
        self.outputLine.setFocus() #have to use setFocus method (universal method), sets all user input to the this

    # ACCESSOR / GET
    def getOutputText(self): #only needs access to self since is not setting anything, (the output has already been defined to self in the mutator)
        return self.outputLine.text() #return the outputline

    #CLEAR OUTPUTLINE
    def clearOutputText(self):
        self.oldOutput = str(self.getOutputText()) #first store current outputText to oldOutput
        self.appendToMemory(self.oldOutput) #then call appendToMemory where it will be added to a list

        self.setOutputText("") #finally call the setOutputText metheod with output argument being an empty string

    #DELETE OUTPUTLINE CHAR
    def deleteButton(self):
         self.outputLine.backspace() #calls backspace built in method from QlineEdit, outputline is the instance of qlineEdit

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #MEMROY
    #ADDING TO MEMORY
    def appendToMemory(self, lastEquation):
        if lastEquation == ("DOES NOT COMPUTE") or lastEquation == '': #if the current output is not an error, or has nothing in it,
            return #then do nothing
        else: #otherwise add to memory
            #DOCK ADD
            self.memoryList.addItem(lastEquation)#adds whatever the last outputLine was
            
            #FILE ADD
            memoryFile = open("GrahamCalculatorMemory.txt", "a") #also going to open the file / make it if it has not been made and (a for) append the last equation
            memoryFile.write(lastEquation) #then appends output to memoryFile
            memoryFile.write('\n') #make a new line
            memoryFile.close()#closes file after writing to it
    
    #CLEAR MEMORY
    def memoryWipe(self):
        #DOCK WIPE
        QListWidget.clear(self.memoryList)

        #FILE WIPE
        memoryFile = open("GrahamCalculatorMemory.txt","r+") #open file, for read and writing (r+)
        memoryFile.truncate(0) #truncate erases content of text file
        memoryFile.close() #close file
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #GET LIST ITEM AND GIVE TO OUTPUT
    def getListItem(self): #decided not to append to memory because they could restore ans just by re entering
        self.setOutputText(self.memoryList.currentItem().text()) #calls setOutputText to the text of the current item being selected (double clicked) from memorylist

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #HINT SETTOR / MUTATOR
    def giveHint(self, hint): #take in string as hint
        self.statusBar().showMessage(hint,5000) #calls QMainWindow to show message hit for 5000 miliseconds

'''-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
End GUI class
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''
#INTERFACE TO CALCULATOR CONNECTION
class connector:
#INIT
    def __init__(self, calculatorObj, guiVisuals): #if it is going to connect the calculator and gui needs both as arguments
        self.calculate = calculatorObj #making calc and guiVisuals instances a part of the connecter object to it has acess to their methods
        self.guiVisualsObj = guiVisuals

        self.senseButtons() #need to call method that activates the button input, so the calculator can actually take in data

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#EXPRESSION CONNECTOR
    def transferExpression(self): #access the expression from the guiVisuals to the calc and then returns and sets the andser back to the guiVisuals
        answer = self.calculate.defaultEval(self.guiVisualsObj.getOutputText(), False) # call default eval from the calculator, with outputText as the argument (also the input Text) so it will evaluate that. False means it is not nested
        #Needs to call method getOutputText from instance of class guiVisuals, which is defined as self.guiVisualsObj
        
        #before changing display to answer,
        oldOutput = str(self.guiVisualsObj.getOutputText()) #first store current outputText to oldOutput with getOutputText from instance of calcView defined to self as guiVisualsObj in this class
        self.guiVisualsObj.appendToMemory(oldOutput) #then call appendToMemory where it will be added to a list

        self.guiVisualsObj.setOutputText(answer) #now call the mutator to change the outputText to what the calculator evaluated

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CALL FRACTION CONVERTER
    def callToConvert(self):
        answer = self.calculate.fractionConvert(self.guiVisualsObj.getOutputText())

        #before changing display to answer,
        oldOutput = str(self.guiVisualsObj.getOutputText()) #first store current outputText to oldOutput with getOutputText from instance of calcView defined to self as guiVisualsObj in this class
        self.guiVisualsObj.appendToMemory(oldOutput) #then call appendToMemory where it will be added to a list

        self.guiVisualsObj.setOutputText(answer) #now call the mutator to change the outputText to what the calculator evaluated
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#GIVE RETURNED EXPRESSION TO VISUAL OUTPUTLINE
    def appendToOutput(self, input): #if a button is hit....
        if self.guiVisualsObj.getOutputText() == self.calculate.error: #if the outputText currently an error... (retrieving error from instance calculate of calculator)
            self.guiVisualsObj.clearOutputText() #it will call to clear it
        #then continue as it would with any other button

        equation = self.guiVisualsObj.getOutputText() + input #set equation equal to the current output, then adding the input onto the end, like insert but allows for setText and clear method
        self.guiVisualsObj.setOutputText(equation) #call method setOutputText from obj guiVisuals and set the text as the arguement (equation)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CHECK IF BUTTONS ARE BEING CLICKED
    def senseButtons(self): #scanner for button import
        for text, buttonObjEx in self.guiVisualsObj.buttons.items(): #text is has already been defined as first (string) of dictionary... so for the text of each object (buttonEx) in the button dictionary 
            #text is a part of dictionary so it does not belong to an object even though its defnition is an object. So I create buttonObjEx which lets me use clicked.connect
            if text not in {'Enter', 'C', 'CC', '≈', 'del'}: #if not one of these buttons
                buttonObjEx.clicked.connect(partial(self.appendToOutput, text)) #append that text to the output

        #BUTTONS THAT SHOULD NOT ADD TO OUTPUT
        #If double clicked on memory list add it to outputline
        self.guiVisualsObj.memoryList.itemDoubleClicked.connect(self.guiVisualsObj.getListItem)

        #Enters / call transferExpression to evaluate
        self.guiVisualsObj.buttons['Enter'].clicked.connect(self.transferExpression) #if button 'Enter' from buttons is clicked then calls transfer expression which will evaluate
        self.guiVisualsObj.outputLine.returnPressed.connect(self.transferExpression)  #if user hits enter it will do the same

        #clear memory
        self.guiVisualsObj.buttons['C'].clicked.connect(self.guiVisualsObj.clearOutputText) #if C clicked calls clearOutputText method

        #Memory Delete
        self.guiVisualsObj.buttons['CC'].clicked.connect(self.guiVisualsObj.memoryWipe) #if CC button is clicked calls memoryWipe method

        #FractionConvert
        self.guiVisualsObj.buttons['≈'].clicked.connect(self.callToConvert) #if button pressed call convert to fraction

        #Delete Button
        self.guiVisualsObj.buttons['del'].clicked.connect(self.guiVisualsObj.deleteButton) #call to delete

class calculator:
#INIT
    def __init__(self, guiVisuals): #intialize calc, needs guiVisuals to make instance of it
        self.error = "DOES NOT COMPUTE" #set error message

        self.answer = '' #make str variable to self 
        self.hint = '' #and one for hint

        #Make substring Exceptions that will make the calculator follow different logic then default eval
        self.sqrtException = 'sqrt('
        self.sinException = 'sin('
        self.cosException = 'cos('
        self.tanException = 'tan('
        self.piException = 'pi'
        self.equalsException = '='
        self.variableException = 'x'

        self.guiVisualsObj2 = guiVisuals #make an instance of the guiVisuals to self so calc can add hints based on certain error conditions
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#BASIC CALC
    def defaultEval(self, outputText, nestedCheck):
        self.evalIsNested = nestedCheck
        if self.evalIsNested == False: #only make the self.inputInstance if it is the first time through
            self.inputInstance = outputText #make an variable of the instance of outputText, could turn it into str but better to keep it as imported so if has to be used as other does not have to convert back
        else:
            self.nestedInputInstance = outputText # if this is second time through default eval needs to keep self.inputInstance the same
        try: #try just generic evaluation
            self.answer = str(eval(outputText, {}, {})) #uses the default eval functin which will evaluate basic equations, then convert it to a str
        except Exception: #if it returns an error
            self.exceptionCheck() #then call exception check to check exceptions that could have made it crash / operators that eval does not understand
            self.getAnswer()
        return self.answer

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ANSWER ACCESSOR
    def getAnswer(self):
        return self.answer
    
#ANSWER MUTATOR / SETTER
    def setAnswer(self, ans):
        self.answer = str(ans)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#HINT SETTER / MUTATOR
    def setHint(self, inputHint): #takes inputHint
        self.hint = inputHint #and stores it to self.hint

#BRACKET HINT CHECK
    def bracketHintCheck(self): #common error among all exceptions that must be called so better to create method to call then repeat following each time
        if self.inputInstance.count('(') != self.inputInstance.count(')'): #if there are a different number of () then will give hint...
                self.setHint('Unmatched bracket.')#call set hint to change self.hint to inputted string
                self.guiVisualsObj2.giveHint(self.hint)#give them this message
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ERROR EXCEPTION CHECKER AND CALLER
    def exceptionCheck(self): #going to check to see if any exceptions are true
        self.exceptionMade = False
        
        #SQRT
        if self.sqrtException in str(self.inputInstance): #the the substring 'sqrt' is in eval line,
            self.specialOperatorMethodCheckNest('sqrt') #call the special operator with sqrt as operator arguement
            self.exceptionMade = True #change that an exception has been made and to not return error - has to be after in case exception check gets called again within method

        #TRIG - sin, cos, tan
        if self.sinException in str(self.inputInstance): #same as above but for sin
            self.specialOperatorMethodCheckNest('sin')
            self.exceptionMade = True

        if self.cosException in str(self.inputInstance): #same as above but for cos
            self.specialOperatorMethodCheckNest('cos')
            self.exceptionMade = True

        if self.tanException in str(self.inputInstance): #same as above but for tan
            self.specialOperatorMethodCheckNest('tan')
            self.exceptionMade = True

        #PI
        if self.piException in str(self.inputInstance):
            self.piMethod()
            #does not set exception made to true because pi method is only replace, so if there is error it is user error and piMethod shouldnt handle

        #SOLVE FOR X
        if self.equalsException in str(self.inputInstance) and self.variableException in str(self.inputInstance): #if equation has an equals and variable x
            self.solveForX() #call method
            self.exceptionMade = True

        elif self.variableException in str(self.inputInstance): #if user had an x without an = sign
            self.setHint("'=' Sign required to isolate for a variable.") #call set hint to change self.hint to inputted string
            self.guiVisualsObj2.giveHint((self.hint)) #give them this message
            self.setAnswer(self.error) #you know it will crash so might as well just tell it here,
            return #and end the function to speed up processing

        elif self.equalsException in str(self.inputInstance): #if user had an = without an x
            self.setHint("'=' Operator requires a variable(x) to solve for.") #call set hint to change self.hint to inputted string
            self.guiVisualsObj2.giveHint((self.hint)) #give them this message
            self.setAnswer(self.error) #you know it will crash so might as well just tell it here,
            return #and end the function to speed up processing

        if self.exceptionMade == False: #if non of the exceptions were triggered, / didnt enter any exception ifs
            self.bracketHintCheck() #call to check if brackets were reason to possibly display error message
            self.setAnswer(self.error)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def specialOperatorMethodCheckNest(self, operatorName):
        try:
            if self.evalIsNested == True:
                self.specialOperatorMethodMain(operatorName, self.nestedInputInstance)
            else:
                self.specialOperatorMethodMain(operatorName, self.inputInstance)
        except Exception: #if crashes at any point...
            self.bracketHintCheck() #call to check if brackets were reason to possibly display error message
            self.setAnswer(self.error) #answer is error

    def specialOperatorMethodMain(self, operatorName, inputInstance): #by having this seperate class, it simplifies the code any allows for hints to be made
        self.findSubstringBracket(operatorName, inputInstance) #return back to this to check equation in brackets to see for possible errors

        if operatorName == 'sqrt':
            if self.substringSolved < 0 and operatorName == 'sqrt': #if the substring is negative, AND OPERATOR IS SQRT
                self.setAnswer(self.error) #it would cause an error so set it answer to error
                self.setHint('Sqrt( operator requires positive input')
                self.guiVisualsObj2.giveHint(self.hint) #give them this mesages
            else:
                self.sqrtEvalBrackets(inputInstance) #have to have specific def, since math.var returns error
        
        elif operatorName == 'sin': #have seperate and not in a for in case want to add hints
            self.sinEvalBrackets(inputInstance)
        
        elif operatorName == 'cos':
            self.cosEvalBrackets(inputInstance)

        elif operatorName == 'tan':
            self.tanEvalBrackets(inputInstance)

        print('input inst copy = ' + str(inputInstance))
        print('op+bracket = ' + str(self.opPlusBracketSubstring))
        #for all since only special part was op name    
        self.inputInstanceCopy = inputInstance.replace(self.opPlusBracketSubstring, self.ans) #replace the sqrt/sin etc. part of the origional string / nested string, (whatever inputInstacne is), with a solved number
        self.defaultEval(self.inputInstanceCopy, True) #now that it has been replace with a float string, call default eval again

    def findSubstringBracket(self, operatorName, inputInstance):
        print("input instance is "+ str(inputInstance))
        self.findChar = operatorName[(len(operatorName))-1] #find the last character of the operator
        self.charCount = 0
        
        #find pos of last letter of operator
        for char in (inputInstance): #for each character in the str inputInstance, start @ char 0
            self.charCount += 1 #add one to the count - before if break so on t it adds to count 
            
            if char == self.findChar:#if that character is last of operator
                break #then stop adding to char count

        self.closeBracketLoopCount = 0 #make variable that counts times it goes through next loop

        self.timesToFind = 0 #will be changed to 1 first time in for loop, since first character will equal (
        self.timesFound = 1
        
        self.looking = True
        for char in inputInstance[self.charCount:]: #again but now starting at ( to find end bracket... starting at charCount = ( then going to the end which is the length + 1 since 0
            self.closeBracketLoopCount += 1 #add 1 to the count
            if char == '(': #if another bracket appears,
                self.timesToFind += 1 #then it needs to find another close bracket after the first one found

            if char == ')': #once it gets to this char
                self.timesFound += 1
                if self.timesToFind == self.timesFound: #if it has found it enough times according to number of ( in substring
                    self.looking = False
                else:
                    self.timesFound += 1 #find it another time
            
            if self.looking == False: #exit loop once counted to selected bracket
                break
        
        self.closeBracketCount = self.charCount + self.closeBracketLoopCount #make variable close bracket count which is the index of the closing sqrt/sin/etc. bracket or the number of times it went through both loops +1 for final bracket

        self.opPlusBracketSubstring = (inputInstance[(self.charCount-(len(operatorName))):self.closeBracketCount]) #make a substring that has the operator lettes so it can be replaced too
        
        self.bracketSubstring = (inputInstance[self.charCount:self.closeBracketCount]) #make the substring between the 2 brackets and make varible copy

        self.substringSolved = float(self.defaultEval(self.bracketSubstring, True)) #call default eval with the substring / equation in brackets - by using self and oop if it re-enters this def they will be new instances. True means it will not redefine the input instance.
#---------------------------------------------------------------------------------------------------------------
#EVAL BRACKETS METHODS
#SQRT
    def sqrtEvalBrackets(self, inputInstance):
        self.ans = str(math.sqrt(self.substringSolved)) #calculate the sqrt/sin/cos/tan of the substring - cant be operatorName because math.sqrt() is method from package and will not math.var will return error

#SIN    
    def sinEvalBrackets(self, inputInstance):
        self.ans = str(math.sin(self.substringSolved))

#COS
    def cosEvalBrackets(self, inputInstance):
        self.ans = str(math.cos(self.substringSolved))

#TAN
    def tanEvalBrackets(self, inputInstance):
        self.ans = str(math.tan(self.substringSolved))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#PI
    def piMethod(self):
        self.piValue = '3.14159265358979' #make var pi
        self.inputInstance = self.inputInstance.replace('pi', self.piValue) #replace string pi for number
        self.defaultEval(self.inputInstance, True) #calls default eval now that it has been replace with nested = true since it is not entering for first time

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#SOLVE FOR X
    def solveForX(self):
        try: #can still have user error
            self.stringList = list(self.inputInstance) #first split string into char list... easier to add thing in specific spots to list vs string
            self.stringList.append('-') #add a negative sign to the end of the string
            self.stringList.append('(') #open a bracket 

            self.isolating = True 
            self.runsThrough = 0 #tracks how many times the loop has occured.. SEE IF:
            while self.isolating: #using a while loop to send all the strings before the '=' string to the back 
                if self.stringList[0] == '=': #if the first index is an equals 
                    if self.runsThrough == 0: #SEE IF: if it the run through and '=' is index 0
                        self.stringList.append('0') #it appends a 0 to the end of the list which will make the brackets not empty, so if equation starts with 0, it sets a default to 0=y
                    self.stringList.pop(0) #then remove it
                    self.isolating = False #set loop to false since that is the finished expression wanted
                    break #break so it does not pop and append another index below
                self.stringList.append(self.stringList.pop(0)) #apped to the end of the string what you are popping from the front of the string... needs to be after if in case = is first input program can assume = to 0
                self.runsThrough += 1

            self.stringList.append(')') #close the bracket

            self.expression = '' #make new var str called expression 

            #now that stringList is reordered...
            for char in self.stringList: #convert list back into string, for character in the list
                self.expression += char #add the character to the string expression
            
            self.ans = str(solve(self.expression)) #sympy returns as list in case x can equal 2 things
            self.setAnswer(self.ans) #call set answer

        except Exception:
            self.equalsOccurences = self.inputInstance.count('=') #python count method counts how many instances of the substring = are in the string ouput text
            if self.equalsOccurences > 1: #if there are more than 1 equals signs,
                self.guiVisualsObj2.giveHint(partial("Too many '=' operators.")) #then call to give that hint of why the calculator could not compute

            else: #only calls as else to speed up processing
                self.bracketHintCheck() #call to check if brackets were reason to possibly display error message

            self.setAnswer(self.error) #then set the answer to error

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def fractionConvert(self, outputText):
        self.inputInstance = outputText #make an variable of the instance of outputText, could turn it into str but better to keep it as imported so if has to be used as other does not have to convert back

        try:
            self.floatAnswer = float(self.inputInstance) #try to convert inputInstance into a float
            self.ans = str(Fraction(self.floatAnswer).limit_denominator(1000)) #use fraction function from import that turns float into fraction, then take str. The limit denominator creates a maximum for the denom since floats can be imprecise. (ex. without .33 = a massive number)
            self.setAnswer(self.ans) #call set answer to set answer to var ans

        except Exception: #if they press button when output can not be converted to a float / is still an equation
            self.setAnswer(self.error) #set the answer to error message
            self.setHint("Float required to convert to fraction.") #call set hint to change self.hint to inputted string
            self.guiVisualsObj2.giveHint((self.hint))#give them this message
        return self.answer

#MAIN
def main():
    GrahamMorrisonCalculator = QApplication(sys.argv) #make an instance of Qapllication / the calc
    
    guiVisuals = calcView() #call the class and asign it to guiVisuals
    guiVisuals.show() #show the guiVisuals
    
    calculatorObj = calculator(guiVisuals) #make a an obj of calc class
    connector(calculatorObj, guiVisuals) #call the connector with the 2 arguments
    
    sys.exit(GrahamMorrisonCalculator.exec_())#exit main

if __name__ == '__main__':
    main()