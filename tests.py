import unittest
from notes import *

class TestNotesObject(unittest.TestCase):

  def test_has_midi_notes(self):

    # Make a note object
    n = Note(0.64)

    # Try accessing value
    resl = n.midi_note[9]

    # Expected value
    expt = "A"

    # Check
    self.assertEqual(resl, expt)
  
  def test_has_epsilon(self):

    # Make a note object
    n = Note(0.42)

    # Try accessing value
    resl = n.EPS

    # Expected value
    expt = 0.1

    # Check
    self.assertEqual(resl, expt)
  
  def test_object_exists(self):
  
    # Make a note object
    n = Note(0.42)

    # Check
    self.assertIsInstance(n, Note)
    self.assertFalse(isinstance(n, int))
    self.assertFalse(isinstance(n, float))

  def test_silly(self):
    
    # Make a note object
    n0 = Note(0.42)
    n1 = Note(0.64)
    n2 = Note(0.50)

    # Check
    self.assertEqual(str(n0), "Db-8 - 22 cents")
    self.assertNotEqual(str(n1), "Db-8 - 22 cents")
    self.assertNotEqual(str(n2), "Db-8 0 22 cents")

class TestFrequencies(unittest.TestCase):

  def test_init_modes(self):

    # Make notes using different modes
    note0 = Note(4840.697)
    note1 = Note(4840.697, 0)
    note2 = Note(770, 1)
    note3 = Note(78.688, 2)

    # Expected notation
    expt = "G5 - 31 cents"

    # Check
    self.assertEqual(note0.notation(), expt)
    self.assertEqual(note1.notation(), expt)
    self.assertEqual(note2.notation(), expt)
    self.assertEqual(note3.notation(), expt)

  def test_octaves(self):

    # Input Frequencies 
    freqs = [
      8.1757989156,
      8.6619572180,
      9.1770239974,
      9.7227182413,
      10.3008611535,
      10.9133822323,
      11.5623257097,
      12.2498573744,
      12.9782717994,
      13.7500000000,
      14.5676175474,
      15.4338531643,
      16.3515978313,
      27.5000000000,
      30.8677063285,
      32.7031956626,
      55.0000000000,
      61.7354126570,
      65.4063913251,
      110.0000000000,
      220.0000000000,
      440.0000000000
    ]

    # Make Notes from Frequencies (using mode=1)
    notes = []
    for f in freqs:
      notes.append(Note(f, 1))
    
    # Find each note's octave
    resl = []
    for n in notes:
      resl.append(n.octv)

    # Expected Octaves
    expt = [
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 
      0, 0, 0, 
      1, 1, 1, 
      2, 2, 
      3, 
      4
    ]

    # Check
    self.assertEqual(resl, expt)

class TestHarmonics(unittest.TestCase):

  def test_one(self):

    # Make note objects
    freqs = [
      13.75,
      20.00,
      27.50,
      30.00,
      40.00,
      50.00,
      55.00,
      60.00,
      70.00,
      80.00,
      90.00,
      100.00,
      110.00,
      120.00,
      130.00,
      140.00,
      150.00,
      160.00,
      170.00,
      180.00,
      190.00,
      200.00,
      210.00,
      220.00,
      440.00,
      880.00,
      1760.00,
      3520.00,
      7040.00
    ]

    # Make Notes from Frequencies (using mode=1)
    notes = []
    for f in freqs:
      notes.append(Note(f, 1))
    
    # Find scale harmonics for first note
    vals = get_all_scale_harmonics(notes, 1/8)
    vals = vals[notes[0]]

    # Convert to strings
    resl = []
    for n in vals:
      resl.append(n.notation())

    # Expected harmonizing notes
    expt = [
      'A0', 
      'A1', 
      'A2', 
      'A3', 
      'A4', 
      'A5', 
      'A6', 
      'A7', 
      'A8'
    ]

    # Check
    self.assertEqual(resl, expt)

  """
  def test_all_harmonic_searches_brief(self):

    # Make note objects
    freqs = [
      220,
      330,
      440,
      550,
      660,
      770,
      880
    ]

    # Set tolerance level
    tol = 1/8

    # Make Notes from Frequencies (using mode=1)
    notes = []
    for f in freqs:
      notes.append(Note(f, 1))
    
    # All with respect to the first note:
    # Find scale harmonics for first note
    valsA = get_all_scale_harmonics(notes, tol)
    valsA = valsA[notes[0]]

    # Convert to strings
    reslA = []
    for n in valsA:
      reslA.append(n.notation())

    
    # Find scale harmonics for first note
    valsB = get_all_value_harmonics(notes, tol, 0)
    valsB = valsB[notes[0]]

    # Convert to strings
    reslB = []
    for n in valsB:
      reslB.append(n.notation())

    
    # Find scale harmonics for first note
    valsC = get_all_value_harmonics(notes, tol, 1)
    valsC = valsC[notes[0]]

    # Convert to strings
    reslC = []
    for n in valsC:
      reslC.append(n.notation())

    # Expected harmonizing notes (by octave)
    exptA = [ 
      'A4', 
      'A5'
    ]
    # Expected harmonizing notes (by [common] multiple)
    exptB = [ 
      'E4 + 2 cents',
      'A4', 
      'Db5 - 14 cents', 
      'E5 + 2 cents', 
      'G5 - 31 cents', 
      'A5'
    ]
    # Expected harmonizing notes (by [strict] multiple)
    exptC = [ 
      'A4', 
      'E5 + 2 cents', 
      'A5'
    ]

    # Check
    self.assertEqual(reslA, exptA)
    self.assertEqual(reslB, exptB)
    self.assertEqual(reslC, exptC)
  """

  def test_all_harmonic_searches_full(self):

    # Make note objects
    freqs = [
      220,
      330,
      440,
      550,
      660,
      700,
      770,
      880
    ]

    # Set tolerance level
    tol = 1/8

    # Make Notes from Frequencies (using mode=1)
    notes = []
    for f in freqs:
      notes.append(Note(f, 1))
    
    # All with respect to the first note:
    # Find scale harmonics for first note
    valsA = get_all_scale_harmonics(notes, tol)

    
    # Find scale harmonics for first note
    valsB = get_all_value_harmonics(notes, tol, 0)

    
    # Find scale harmonics for first note
    valsC = get_all_value_harmonics(notes, tol, 1)

    # Check
    self.assertEqual(len(valsA[notes[0]]), 2)
    self.assertEqual(len(valsB[notes[0]]), 6)
    self.assertEqual(len(valsC[notes[0]]), 3)
    
    self.assertEqual(len(valsA[notes[1]]), 1)
    self.assertEqual(len(valsB[notes[1]]), 6)
    self.assertEqual(len(valsC[notes[1]]), 1)
    
    self.assertEqual(len(valsA[notes[2]]), 2)
    self.assertEqual(len(valsB[notes[2]]), 6)
    self.assertEqual(len(valsC[notes[2]]), 1)
    
    self.assertEqual(len(valsA[notes[3]]), 0)
    self.assertEqual(len(valsB[notes[3]]), 6)
    self.assertEqual(len(valsC[notes[3]]), 0)
    
    self.assertEqual(len(valsA[notes[4]]), 1)
    self.assertEqual(len(valsB[notes[4]]), 6)
    self.assertEqual(len(valsC[notes[4]]), 0)
    
    self.assertEqual(len(valsA[notes[5]]), 0)
    self.assertEqual(len(valsB[notes[5]]), 0)
    self.assertEqual(len(valsC[notes[5]]), 0)
    
    self.assertEqual(len(valsA[notes[6]]), 0)
    self.assertEqual(len(valsB[notes[6]]), 6)
    self.assertEqual(len(valsC[notes[6]]), 0)
    
    self.assertEqual(len(valsA[notes[7]]), 2)
    self.assertEqual(len(valsB[notes[7]]), 6)
    self.assertEqual(len(valsC[notes[7]]), 0)


if __name__ == '__main__':
  unittest.main()