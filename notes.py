import pprint
import math
import numpy as np
import matplotlib.pyplot as plt

from to_lily import *

DEBUG_BOOL = False

def get_file_name():
  file_name = input("Enter the file name: ")
  return file_name

def get_input_from_fusion(file_name):
  f = open(file_name, "r")

  line = ""
  start_line = 361
  for _ in range(start_line):
    line = f.readline()

  data = []
  data_row = []
  curr = ""
  jj = 0
  kk = False
  while (len(line) > 3):
    for ch in line:
      if ( (ch != ' ') and (ch != '\n') ):
        curr += ch
        if (kk == False):
          kk = True
      elif (kk):
        if (jj == 0):
          data_row.append(int(curr))
        else:
          data_row.append(float(curr))
        jj += 1

        curr = ""
        kk = False

    data.append(data_row)
    data_row = []
    jj = 0

    # Get next line and loop
    line = f.readline()

  return data

def show_fusion_data(fusion):
  print("[")
  for ii in range(len(fusion)):
    print(fusion[ii])
  print("]")

def get_rad_column(fusion):
  rads = []

  for ii in range(len(fusion)):
    rads.append(fusion[ii][2])

  return rads

def get_all_scale_harmonics(all_notes, tolerance):
  scale_harmonics = {}
  for n in range(len(all_notes)):
    curr_harms = all_notes[n].find_scale_haromonics(all_notes, tolerance)
    if (len(curr_harms) > 0):
      scale_harmonics[all_notes[n]] = curr_harms
    curr_harms = []

  return scale_harmonics

def get_all_value_harmonics(all_notes, tolerance, mode=0):
  value_harmonics = {}
  for n in range(len(all_notes)):
    curr_harms = all_notes[n].find_value_harmonics(all_notes, tolerance, mode)
    if (len(curr_harms) > 0):
      value_harmonics[all_notes[n]] = curr_harms
    curr_harms = []

  return value_harmonics

def find_gcf(f1, f2):

  if (f2 == 0):
    return f1

  return find_gcf(f2, f1 % f2)

def find_min_mode(freqs):

  modes = {}

  # Find the modes
  for f in freqs:
    if f in modes:
      modes[f] += 1
    else:
      modes[f] = 1
  
  # Remove zero and modes of 1
  modes2 = {}
  for k,v in modes.items():
    if ( (k != 0) and (v > 1) ):
      modes2[k] = v

  # Find the minimum
  if (len(modes2) == 1):
    return next(iter(modes2.keys()))
  elif (len(modes2) == 0):
    return max(freqs, key=freqs.count)
  else:
    return min(modes2.keys())

def gen_lily_file(file_name, all_notes, scale_harms, value_harms, reltv_harms):
  outp = gen_lily_version() + gen_lily_header(file_name) + gen_lily_content(all_notes, scale_harms, value_harms, reltv_harms)
  return outp

#t
def gen_lily_version():
  return "\\version \"2.18.2\"\n"

#t
def gen_lily_header(title):
  return "\\header {\n  title = " + str(title) + "\n}\n"

#t
def gen_lily_all_notes(all_notes):
  r = "\\score {\n  \\new Staff {\n    "
  for n in all_notes:
    r += n.get_lily() + " "
  r += "\n  }\n  \\header {\n    piece = \"All Notes\"\n  }\n}\n"
  return r

#t
def gen_lily_harmonics(harms, mode):

  r = "\\score {\n  \\new Staff {\n"

  for k,v in harms.items():
    r += "    " + k.get_lily() + "1 "
    for n in v:
      r += n.get_lily() + "4 "
    # r += "| \\break\n"
    r += "\\bar \"|.\"\n"

  r += "  }\n  \\header {\n    piece = \""

  if (mode == 0):
    r += "Harmonics by Octave"
  elif (mode == 1):
    r += "Harmonics by Common Multiple"
  elif (mode == 2):
    r += "Harmonics by Multiple"
  else:
    r += "Harmonics"

  r += "\"\n  }\n}\n"
  return r

#t
def gen_lily_content(all_notes, scale_harms, value_harms, reltv_harms):
  return gen_lily_all_notes(all_notes) + gen_lily_harmonics(scale_harms, 0) + gen_lily_harmonics(value_harms, 1) + gen_lily_harmonics(reltv_harms, 2)

#t
def remove_out_of_bounds_notes(all_notes, low_end=20, high_end=20000):
  notes_to_keep = []
  kk = 0
  for n in all_notes:
    if ( (n.freq > low_end) and (n.freq < high_end) ):
      notes_to_keep.append(n)
    else:
      kk += 1
  
  print(kk, "notes have been discarded.")

  return notes_to_keep
      

class Note:
  
  # Private Vars
  midi_note = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B" ]
  EPS = 0.1
  # This is an approximation for the analytical assistant
  #  (still need to mathematically evaulate a better ver.)
  f_fac = 39.5

  # Constructor
  def __init__(self, frequency = 0, mode = 0):
    def r2f(radian):

      frq = 2 * math.pi * radian
      if (frq < self.EPS):
        frq = 0
      
      frq /= self.f_fac

      return frq

    def f2r(frequency):

      rad = frequency * self.f_fac

      rad /= 2 * math.pi

      return rad

    def f2m(frequency):
      return ( 12*math.log2(frequency/440) + 69 )

    def m2f(midi):
      return 440*2**( (midi - 69)/12 )

    def m2o(midi):
      c_fac = 2
      return int( midi//12 + 1 - c_fac )

    def m2n(midi):
      return self.midi_note[round(midi) % 12]

    def m2c(midi):
      c = abs(midi - round(midi))

      # If need to flip
      if ( (c + math.floor(midi)) < midi):
        c *= -1
        # If this would push note to next octave
        if ( (round(midi) > math.floor(midi)) and ( (round(midi) % 12) == 0 ) ):
          # NOTE: unsure if this would violate proper form
          self.octv = m2o(midi + 1)

      return 100*c

    if (frequency):
      if (mode == 1):
        self.freq = frequency
        self.rads = f2r(self.freq)
        #
        self.midi = f2m(self.freq)
        self.octv = m2o(self.midi)
        self.note = m2n(self.midi)
        self.cent = m2c(self.midi)
      elif (mode == 2):
        self.midi = frequency
        self.freq = m2f(self.midi)
        self.rads = f2r(self.freq)
        #
        #
        self.octv = m2o(self.midi)
        self.note = m2n(self.midi)
        self.cent = m2c(self.midi)
      else:
        self.rads = frequency
        self.freq = r2f(self.rads)
        self.midi = f2m(self.freq)
        self.octv = m2o(self.midi)
        self.note = m2n(self.midi)
        self.cent = m2c(self.midi)
    else:
      self.rads = 0
      self.freq = 0
      self.midi = 0
      self.octv = 0
      self.note = 0
      self.cent = 0

  def get_all(self):
    print("  " + str(self.rads) + "(rads)")
    print("  " + str(self.freq) + "(Hz)")
    print("  " + str(self.midi) + "(midi)")
    print("  " + str(self.octv) + "(octave)")
    print("  " + str(self.note) + "(note)")
    print("  " + str(self.cent) + "(cent(s))")
    print("  " + self.notation())

  def notation(self):
    s = ""
    s += str(self.note) + str(self.octv)

    if round(self.cent):
      if (self.cent < 0):
        s += " - " + str(round(abs(self.cent)))
      else:
        s += " + " + str(round(self.cent))
      if abs(self.cent) > 1:
        s += " cents"
      else:
        s += " cent"
    
    return s

  def find_scale_haromonics(self, all_notes, tolerance):

    harm_notes = []

    if (abs(self.cent/100) < tolerance):
      for n in range(len(all_notes)):
        if ( (self != all_notes[n]) and (abs(all_notes[n].cent/100) < tolerance) and (self.note == all_notes[n].note) ):
          harm_notes.append(all_notes[n])

    return harm_notes

  def find_value_harmonics(self, all_notes, tolerance, mode=0):

    """
    def find_base_frequency(this, that, tolerance):

      if (this > that):
        temp = this
        this = that
        that = temp

      if ( ( ( 10*(that/this) % 1 ) == 0 ) and ( this*( (that/this) % 1 ) ) ):
        mult_c = this*( (that/this) % 1 )
        print("The common multiple is: ", mult_c)
        return that/mult_c
    """

    def find_base_frequency(this, those, tolerance):
      
      # this.get_all()

      base_potential = []
      for n in range(len(all_notes)):
        if ( this != all_notes[n] ):
          base_potential.append(find_gcf(this.freq, all_notes[n].freq))
      
      eval_freq = find_min_mode(base_potential)

      if ( (eval_freq/this.freq) < tolerance ):
        return this.freq
      else:
        return eval_freq

    def find_strict_multiple(this, that, tolerance):
      
      val = (that/this) % 1

      if ( (val < tolerance) or (( 1 - val ) < tolerance) ):
        return ( that/this )

    harm_notes = []

    # Empirical, but gets this to work
    tolerance /= 4

    curr_freq = self.freq

    if (not mode):
      # print("For freq " + str(curr_freq) + ":", end = "")
      curr_freq = find_base_frequency(self, all_notes, tolerance)
      # print(str(curr_freq))

    for n in range(len(all_notes)):
      if ( self != all_notes[n] ):
        # Search base on common multiple
        if (not mode):
          mult = find_strict_multiple(curr_freq, all_notes[n].freq, tolerance)
        # Search for strict multiples
        else:
          mult = find_strict_multiple(curr_freq, all_notes[n].freq, tolerance)

        if (mult):
          harm_notes.append(all_notes[n])

    return harm_notes

  def get_lily(self, mode=0):

    r = ""

    temp1 = self.note
    if (len(temp1) > 1):
      r += temp1[0].lower() + "es"
    else:
      r += temp1.lower()
    
    temp2 = self.octv
    if (temp2 >= 4):
      r += (temp2 - 3)*"'"
    else:
      r += (3 - temp2)*","

    if mode:
      r += str(mode)

    temp3 = int(self.cent)
    if (temp3 > 0):
      r += "^\\markup { " + str(round(self.cent)) + " }"
    elif (temp3 < 0):
      r += "_\\markup { " + str(round(self.cent)) + " }"
    
    return r

  def __str__(self):
    return self.notation()

  def __repr__(self):
    return self.notation()

def main():

  asking_for_input = True

  pp = pprint.PrettyPrinter(indent=4)

  tol_fac = 8
  tol = 1/tol_fac

  if (asking_for_input):
    f_name = get_file_name()
    f_data = get_input_from_fusion(f_name)
    rads = get_rad_column(f_data)

    notes = []
    for r in rads:
      notes.append(Note(r))

  else: #testing

    f_name = "Test"

    fr = [
      220,
      330,
      440,
      550,
      660,
      700,
      770,
      880
    ]
    notes = []
    for f in fr:
      notes.append(Note(f, 1))

  notes = extract_notes_in_range(notes)

  # """
  for n in notes:
    n.get_all()
    print()
  # """

  scale_harmonics = get_all_scale_harmonics(notes, tol)
  # print("Checking for commons:")
  value_harmonics = get_all_value_harmonics(notes, tol)
  # !TODO: fix this one
  # print("\nChecking for stricts:")
  reltv_harmonics = get_all_value_harmonics(notes, tol, 1)

  print("Harmonics by octave:")
  pp.pprint(scale_harmonics)
  print()
  print("Harmonics by (common) multiples:")
  pp.pprint(value_harmonics)
  print()
  # print("Harmonics by (strict) multiples:")
  # pp.pprint(reltv_harmonics)
  
  # reltv_harmonics = get_all_reltv_harmonics(notes, tol)
  # pp.pprint(reltv_harmonics)

  plotput = {}
  for k,v in scale_harmonics.items():
    plotput[k.notation()] = len(v)
  _ = plt.figure(1)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Scale")
  plt.title("Harmonics by octave:")

  plotput = {}
  for k,v in value_harmonics.items():
    plotput[k.notation()] = len(v)
  _ = plt.figure(2)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Integer")
  plt.title("Harmonics by (common) multiples:")

  plotput = {}
  for k,v in reltv_harmonics.items():
    plotput[k.notation()] = len(v)
  _ = plt.figure(3)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  # yint = range(min(y), math.ceil(max(y))+1)
  # plt.yticks(yint)
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Series")
  plt.title("Harmonics by (strict) multiples:")

  print()
  print("Attempting to generate lily file.. ", end="   ")
  # for n in notes:
  #   print(n.get_lily())

  f = open("output.ly", "w")
  f.write(generate_lily_content("Results", notes, scale_harmonics, value_harmonics, reltv_harmonics))
  f.close()

  import subprocess
  subprocess.run(["lilypond", "--silent", "output.ly"])

  print("..lily file generated!")

  # plt.show()


if __name__ == '__main__':
  main()