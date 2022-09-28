#! /usr/bin/env python3

import re
import sys

ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

class Spell(object):
  def __init__(self):
    self.name = None
    self.circle = None
    self.uses = None
    self.uses_special = ""
    self.verbal = 0
    self.material = None
    self.active = None
    self.caveats = []
    self.description = ""
    self.associated_spells = []
    self.points = None

  def __repr__(self):
    return f"<Spell: {self.name} ({self.circle} circle)>"

  def print_component(self, component, name, suffix=""):
    if component:
      print(f"{name}: {component}{suffix}")
  
  def to_text(self):
    print(f"{self.name} ({ordinal(self.circle)} Circle)")
    print()
    self.print_component(self.uses, "Uses")
    self.print_component(self.verbal, "Verbal")
    self.print_component(self.active, "Active")
    self.print_component(self.material, "Material")
    self.print_component(self.caveats, "Caveats")
    print()
    print(self.description)    

  def html_radio(self, radio_name):
    return f"""<label class="spell-radio"><input type="radio" name="{radio_name}" value="{self.name}">{self.name}</label>"""
    
  def get_component(self, components, name, required=False):
    regex = re.search(name + r" ([^:]+) - ", components)
    if not regex:
      regex = re.search(name + r" ([^:]+)$", components)
      if not regex:
        if required:
          raise ValueError(f"Could not find '{name}' for spell {self} in: " + components)
        return None
    return regex.group(1)

def split_or_none(s, sep):
  if s:
    return s.split(sep)
  return None
    
SPELL_COMPONENTS, SPELL_DESCRIPTION = range(2)
    
def spells(omnibus):
  line = omnibus[0]
  while line.find("{#spell-descriptions}") == -1:
    line = omnibus.pop(0)

  mode = SPELL_DESCRIPTION
  all_spells = []
  spell_dict = {}
  spell = None
  blank_lines = 0
  components = []
  while True:
    line = omnibus.pop(0)
    if mode == SPELL_DESCRIPTION:
      if line.startswith("###"):
        spell = Spell()
        all_spells.append(spell)
        regex = re.match(r"### (.*) [(](\d).* Circle[)] ### {#.*}", line)
        if not regex:
          raise ValueError("Did not understand line: " + line)
        spell.name = regex.group(1)
        spell_dict[spell.name] = spell
        spell.circle = int(regex.group(2))
        mode = SPELL_COMPONENTS
        components = []
        blank_lines = 0
      elif line.find("{#rules-for-event-holders}") != -1:
        break
      elif spell:
        spell.description += line
      else:
        continue
    elif mode == SPELL_COMPONENTS:
      if not line.strip():
        blank_lines += 1
        if blank_lines >= 2:
          components = " ".join(components)
          spell.uses = spell.get_component(components, "__Uses:__", True)
          spell.verbal = spell.get_component(components, "__Verbal:__")
          spell.material = spell.get_component(components, "__Material:__")
          spell.active = spell.get_component(components, "__Active:__")
          spell.caveats = split_or_none(spell.get_component(components, "__Caveats:__"), ", ")
          
          mode = SPELL_DESCRIPTION
      else:
        components.append(line.strip())
  return spell_dict, all_spells

def main(argv):
  if len(argv) < 2:
    print(f"Usage: {sys.argv[0]} <Omnibus.md>")
    exit()
  with open(argv[1]) as f:
    spell_dict, all_spells = spells(f.readlines())
#    spell = "Light"
#    if len(argv) > 2:
#      spell = argv[2]
    for spell in [spell for spell in all_spells if spell.circle == 1]:
      print(spell.html_radio("spells"))

if __name__ == "__main__":
  main(sys.argv)
  
