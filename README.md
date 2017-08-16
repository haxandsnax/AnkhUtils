# AnkhUtils
Utility scripts for AnkhBot!

Purpose of this script is to simplify adding shared features to all your scripts without having to duplicate code.

1. Copy the AnkhUtils script into your `Scripts` folder, alongside all your other scripts

2. When you first add the utility, you need to modify each script and add the following code

```python
import os
import sys
#---------------------------------------
# Load Utility Module
#---------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../AnkhUtils')))
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
