import math
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib import interactive


def get_input_from_fusion():
  file_name = input("Enter the file name: ")
  f = open(file_name, "r")

  line = ""
  start_line = 361;
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
  for n in range(len(notes)):
    curr_harms = notes[n].find_scale_haromonics(notes, tol)
    if (len(curr_harms) > 0):
      scale_harmonics[notes[n]] = curr_harms
      """
      for i in curr_harms:
        scale_harmonics[notes[n]] = i
      """
      """
      for i in curr_harms:
        if (notes[n] in scale_harmonics):
          scale_harmonics[notes[n]] += i
        else:
          scale_harmonics[notes[n]] = i
      """
    curr_harms = []

  return scale_harmonics

def get_all_value_harmonics(all_notes, tolerance):
  value_harmonics = {}
  for n in range(len(notes)):
    curr_harms = notes[n].find_value_harmonics(notes, tol)
    if (len(curr_harms) > 0):
      value_harmonics[notes[n]] = curr_harms
    curr_harms = []

  return value_harmonics

def count_num(lst):
  if (lst == []):
    return 0
  elif (len(lst) == 1):
    return 1
  else:
    return 1 + count_num(lst[1:])

# def make_harmonic_plot(harms):

#   plotput = {}
#   for k,v in harms.items():
#     plotput[k.notation()] = count_num(v)

#   plt.bar(list(plotput.keys()), plotput.values(), color='g')
  

class Note:
  
  # Private Vars
  midi_note = [ "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B" ]
  EPS = 0.1

  # Constructor
  def __init__(self, frequency = 0, mode = 0):
    def r2f(radian):
      # This is an approximation for the analytical assistant
      #  (still need to mathematically evaulate a better ver.)
      f_fac = 39.5

      frq = 2 * math.pi * radian
      if (frq < self.EPS):
        frq = 0
      
      frq /= f_fac

      return frq

    def f2m(frequency):
      return ( 12*math.log2(frequency/440) + 69 )

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
        self.rads = 0
        self.freq = frequency
        self.midi = f2m(self.freq)
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

  def find_value_harmonics(self, all_notes, tolerance):

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

        if ( (curr <= tolerance) or ( (10 - curr) <= tolerance) ):
          return round(intr/10)

    harm_notes = []

    for n in range(len(all_notes)):
      if ( self != all_notes[n] ):
        base = find_base_frequency(self.freq, all_notes[n].freq, tolerance)
        if (base):
          harm_notes.append(all_notes[n])

    return harm_notes

  # def __eq__(self, other):
  #   return (self.freq == other.freq)

  def __str__(self):
    return self.notation()

  def __repr__(self):
    return self.notation()


# main()
f_data = get_input_from_fusion()
rads = get_rad_column(f_data)

tol_fac = 16
tol = 1/tol_fac

"""
rads2 = [
  0.043308840000000, 0.090855600000000, 0.151840500000000, 
  0.153222000000000, 0.196463300000000, 0.213156500000000, 
  0.268481500000000, 0.456993200000000, 0.539292500000000, 
  0.669896100000000, 0.778650300000000, 0.795880900000000, 
  0.930494400000000, 0.970244600000000, 1.025362000000000, 
  1.274542000000000, 1.344059000000000, 1.395609000000000, 
  1.479782000000000, 1.613111000000000, 1.649877000000000, 
  1.730639000000000, 1.857378000000000, 2.469065000000000, 
  2.630674000000000, 2.699105000000000, 2.756241000000000, 
  3.087657000000000, 3.217560000000000, 3.443789000000000, 
  3.498719000000000, 3.702996000000000, 3.818635000000000, 
  3.975403000000000, 4.072206000000000, 4.114818000000000, 
  4.408462000000000, 4.520879000000000, 4.790317000000000, 
  5.127406000000000, 5.375454000000000, 5.448368000000000, 
  5.720190000000001, 5.784008000000000, 5.883911000000000, 
  5.987839000000000, 6.229888000000000, 6.471439000000000, 
  6.593323000000000, 6.660578999999999
]
for n in range(len(rads2)):
  rads2[n] *= 10000
frqs = [
  246.94, 261.6255653006, 277.18, 
  293.66, 311.13, 329.63, 
  349.23, 369.99, 391.99, 
  415.30, 440.00, 466.16, 
  493.8833012561, 520.00, 
  523.2511306012,
]
"""

notes = []
for r in rads:
  notes.append(Note(r))

# for f in frqs:
#   notes.append(Note(f,1))

# for n in range(len(notes)):
#   print("For mode " + str(n+1) + ":")
#   print(notes[n].notation())
#   print()

scale_harmonics = get_all_scale_harmonics(notes, tol)
value_harmonics = get_all_value_harmonics(notes, tol)

# print(scale_harmonics)
# print(value_harmonics)

# make_harmonic_plot(scale_harmonics)
# make_harmonic_plot(value_harmonics)



plotput = {}
for k,v in scale_harmonics.items():
  plotput[k.notation()] = count_num(v)

f = plt.figure(1)
plt.bar(list(plotput.keys()), plotput.values(), color='g')



plotput = {}
for k,v in value_harmonics.items():
  plotput[k.notation()] = count_num(v)

g = plt.figure(2)
plt.bar(list(plotput.keys()), plotput.values(), color='g')



plt.show()