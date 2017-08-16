import json
import os
import codecs
import math


#---------------------------------------
# inject decorator inserts the Utils object so it can be
# used directly in your Execute, Init functions etc.
#---------------------------------------
def inject(util):
  def injectfn(fn):
    def wrapped(*args, **kwargs):
      util.SetData(fn.__globals__.get('Parent'), args, kwargs)
      fn.__globals__['Utils'] = util
      return fn(*args, **kwargs)
    return wrapped
  return injectfn

#---------------------------------------
# Call this to create the initial Utils object
#---------------------------------------
def setup(script, command=None):
  return UtilClass(script, command)

#---------------------------------------
# Add functions to this class to expand functionality
#---------------------------------------
class UtilClass:
  def __init__(self, scriptname, commandname):
    self.ScriptName = scriptname
    self.CommandName = commandname
    self.Settings = dict()
    self.Data = None

  # Sets command name if not set in __init__, used for cooldowns etc
  def SetCommand(self, name):
    self.CommandName = name

  # Called when injected into Execute, Init etc
  # Extracts Data object from parameter if it exists, such as in Execute
  def SetData(self, Parent, args, kwargs):
    self.Parent = Parent
    for arg in args:
      try:
        if 'User' in dir(arg):
          self.Data = arg
      except Exception as e:
        self.Log('[AnkhUtils] Unable to set data object. Error: {0}'.format(str(e)))

  # Logging with string formatting. Also keeps you from having to add
  # ScriptName parameter every time
  # Usage: Utils.Log('{0} + {0} = {1}', 2, 4)
  def Log(self, str, *args):
    if len(args) > 0:
      try:
        self.Parent.Log(self.ScriptName, str.format(*args))
      except Exception as e:
        self.Parent.Log(self.ScriptName, '[AnkhUtils] Invalid format string or parameters for Utils.Log')
    else:
      self.Parent.Log(self.ScriptName, str)

  # Allows you to set the settings object directly.
  def SetSettings(self, data):
    self.Settings = data

  # Loads settings from a file. Pass __file__ from your script
  # to load relative to your script. Optionally override the filename
  def ReloadSettings(self, base, filename='settings.json'):
    try:
      with codecs.open(os.path.join(os.path.dirname(base), filename), encoding='utf-8-sig') as jsonData:
        self.SetSettings(json.loads(jsonData.read()))
        return self.Settings
    except Exception as e:
      self.Log('[AnkhUtils] Error loading {0}: {1}'.format(filename, str(e)))
      return

  # Helper to get pretty formatted cooldown text from Seconds remaining
  def CooldownText(self, cd, seconds=True, minutes=True, hours=True):
    h = int(math.floor(cd/3600))
    m = int(math.floor((cd%3600)/60))
    s = cd % 60
    hourtext = '{0} hour{1}'.format(h, '' if h == 1 else 's') if hours and h > 0 else ''
    minutetext = '{0} minute{1}'.format(m, '' if m == 1 else 's') if minutes and m > 0 else ''
    secondtext = '{0} second{1}'.format(s, '' if s == 1 else 's') if seconds and s > 0 else ''
    if hours and h > 0 and minutes and m > 0:
      minutetext = ' '+minutetext
    if seconds and s > 0 and ((minutes and m > 0) or (hours and h > 0)):
      secondtext = ' '+secondtext
    return '{0}{1}{2}'.format(hourtext, minutetext, secondtext)

  # Sends a Twitch or Discord chat message or a whisper/DM depending on where the
  # initiating message came from
  def ChatOrWhisper(self, msg, discord=True, whisper=True):
    if self.Data is None:
      self.Parent.SendTwitchMessage(msg)
      return
    whisper = whisper and self.Data.IsWhisper()
    if self.Data.IsFromTwitch():
      self.Parent.SendTwitchWhisper(self.Data.User, msg) if whisper else Parent.SendTwitchMessage(msg)
    elif discord and self.Data.IsFromDiscord():
      self.Parent.SendDiscordDM(self.Data.User, msg) if whisper else Parent.SendDiscordMessage(msg)
