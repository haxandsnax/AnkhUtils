import os
import sys

#---------------------------------------
# Load Utility Module from path. AnkhUtils directory should be
# placed in the Scripts directory alongside other scripts
#---------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import AnkhUtils

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = 'Example AnkhUtils Script'
Website = 'http://mywebsite.tv'
Description = '!hello command says "Hello" to a user'
Creator = 'Awesome Developer'
Version = '1.0.0.0'

# Your other variables
Command = '!hello'

#---------------------------------------
#  Command can be a single command or a list of commands that should be matched
#  Utils needs to know command name if you want to manipulate cooldowns, etc
#  If passed a list, the first command will be used for cooldown purposes
#---------------------------------------
Utils = AnkhUtils.setup(ScriptName, Command)

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
@AnkhUtils.inject(Utils)
def Init():
  Utils.ReloadSettings(__file__, filename='settings.json')
  Utils.Log('Initialized {0} command, settings loaded succesfully', Command)
  return

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
@AnkhUtils.inject(Utils)
def Execute(data):
  commandinfo = Utils.ProcessCommand()
  if commandinfo:
    Utils.ChatOrWhisper('Hello, {0}'.format(commandinfo.Target if commandinfo.Target else commandinfo.User))
  return

#---------------------------------------
# [Required] Run code for every bot tick
#---------------------------------------
@AnkhUtils.inject(Utils)
def Tick():
   return

#---------------------------------------
# [Optional] Called when settings are saved from within the bot
#---------------------------------------
@AnkhUtils.inject(Utils)
def ReloadSettings(jsonData):
  Utils.SetSettings(jsonData)
