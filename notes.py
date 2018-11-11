import pprint
import math
import numpy as np
import matplotlib.pyplot as plt

def get_input_from_fusion():
  file_name = input("Enter the file name: ")
  f = open(file_name, "r")

  line = ""
  start_line = 361
  for i in range(start_line):
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

def get_all_reltv_harmonics(all_notes, tolerance):
  reltv_harmonics = {}
  # for n in range(len(notes)):
  for n in range(len(all_notes)):
    curr_harms = all_notes[n].find_reltv_harmonics(all_notes, tolerance)
    if (len(curr_harms) > 0):
      reltv_harmonics[all_notes[n]] = curr_harms
    curr_harms = []
  
  return reltv_harmonics


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

    def find_base_frequency(this, that, tolerance):
      
      tolerance *= 10
      if (tolerance > 10):
        tolerance = 10

      curr = 0
      intr = 0
      if (this == that):
        print("found my twin")
        return 0
      elif (this < that):
        intr = round(10*(that/this))
        curr = intr % 10

        # Why didn't I write:
        # v = that/this
        # curr = round(v % 1)

        if ( (curr <= tolerance) or ( (10 - curr) <= tolerance) ):
          return round(intr/10)

    harm_notes = []

    for n in range(len(all_notes)):
      if ( self != all_notes[n] ):
        if (mode):
          base = find_base_frequency(self.freq, all_notes[n].freq, tolerance)
        else:
          base = self.freq
        if (base):
          harm_notes.append(all_notes[n])

    return harm_notes

  def find_reltv_harmonics(self, all_notes, tolerance):

    """
    def find_notes_harmonics(this):
      max_f = 12600
      collect = []
      
      for i in range(1, max_f // round(this.freq)):
        collect.append(self.freq * i)

      return collect

    harm_notes = []

    print(self.get_all())
    print(find_notes_harmonics(self))

    for n in range(len(all_notes)):
      if ( self != all_notes[n] ):
        print(all_notes[n].freq in list())
        if (base):
          harm_notes.append(all_notes[n])
      
    return harm_notes
    """

    harm_notes = []


    for n in range(len(all_notes)):
      if ( self != all_notes[n] ):
        print("curr val: ",all_notes[n].freq/self.freq)

    return harm_notes

  def __str__(self):
    # TODO: lilypond export
    return self.notation()

  def __repr__(self):
    return self.notation()

def main():

  asking_for_input = False;

  pp = pprint.PrettyPrinter(indent=4)

  tol_fac = 8
  tol = 1/tol_fac

  if (asking_for_input):
    f_data = get_input_from_fusion()
    rads = get_rad_column(f_data)

    notes = []
    for r in rads:
      notes.append(Note(r))

  else: #testing

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
  

  # for f in frqs:
  #   notes.append(Note(f,1))

  # for n in range(len(notes)):
  #   print("For mode " + str(n+1) + ":")
  #   print(notes[n].notation())
  #   print()

  scale_harmonics = get_all_scale_harmonics(notes, tol)
  # Actually, this one is wrong
  value_harmonics = get_all_value_harmonics(notes, tol)
  # Can't help but feel that this one **MUST** be wrong
  reltv_harmonics = get_all_value_harmonics(notes, tol, 1)

  print("Harmonics by octave:")
  pp.pprint(scale_harmonics)
  print()
  print("Harmonics by (common) multiples:")
  pp.pprint(value_harmonics)
  print()
  print("Harmonics by (strict) multiples:")
  pp.pprint(reltv_harmonics)
  
  # reltv_harmonics = get_all_reltv_harmonics(notes, tol)
  # pp.pprint(reltv_harmonics)

  plotput = {}
  for k,v in scale_harmonics.items():
    plotput[k.notation()] = len(v)
  f = plt.figure(1)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Scale")
  plt.title("Harmonics by octave:")

  plotput = {}
  for k,v in value_harmonics.items():
    plotput[k.notation()] = len(v)
  g = plt.figure(2)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Integer")
  plt.title("Harmonics by (common) multiples:")

  plotput = {}
  for k,v in reltv_harmonics.items():
    plotput[k.notation()] = len(v)
  h = plt.figure(3)
  plt.bar(list(plotput.keys()), plotput.values(), color='g')
  plt.xticks(rotation='vertical')
  # yint = range(min(y), math.ceil(max(y))+1)
  # plt.yticks(yint)
  plt.xlabel('Note in notation')
  plt.ylabel('Harmonizing Notes (#)')
  # plt.title("Harmonic by Series")
  plt.title("Harmonics by (strict) multiples:")

  plt.show()


if __name__ == '__main__':
  main()