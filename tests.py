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


if __name__ == '__main__':
  unittest.main()