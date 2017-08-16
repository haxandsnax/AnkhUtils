# AnkhUtils
Utility scripts for AnkhBot!
The purpose of this script is to add shared features to all your scripts without having to duplicate code.

## Getting started
1. Copy the `AnkhUtils` directory into your `Scripts` folder, alongside all your other scripts

2. When you first add the utility, you need to modify each script and add the following code

```python
import os
import sys
#---------------------------------------
# Load Utility Module
#---------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import AnkhUtils
```
3. Initialize the Util object with your script name and optionally your command name

```python
Command = '!hello'
#---------------------------------------
#  [command] is optional but can later be set with Utils.SetCommand('!hello')
#  Utils needs to know command name if you want to manipulate cooldowns, etc
#---------------------------------------
Utils = AnkhUtils.setup(ScriptName, command=Command)
```

4. Inject the `Utils` object into the script functions (Execute, Init, etc)

```python
@AnkhUtils.inject(Utils)
def ReloadSettings(jsonData):
  Utils.SetSettings(jsonData)
```

5. Now you can use the `Utils` object in your functions!

```python
@AnkhUtils.inject(Utils)
def Init():
  global ScriptName
  Utils.ReloadSettings(__file__, filename='settings.json')
  Utils.Log('Initialized {0} script, settings loaded succesfully', ScriptName)
  return
```

## Adding new functionality
Use the UtilsClass as a base for adding any utilities you need. Simply define new class methods and call them in your script.
You can also add other python scripts to the `AnkhUtils` directory and import them to keep things organized!

`mymodule.py`:
```python
def LogUser(Utils):
  Utils.Log('Logged user {0}', Utils.Data.User)
```
Then in `__init__.py` add a new class method:
```python
import mymodule

class UtilClass:
  #... other methods / etc

  # Define new methods with whatever parameters you want
  # Here we use the method imported from 'mymodule'
  def LogUser(self):
    mymodule.LogUser(self)
    return
```
