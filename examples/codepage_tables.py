"""Prints code page tables.
"""

import sys

from escpos import printer
from escpos.constants import *


def main():
    dummy = printer.Dummy()

    dummy.hw('init')

    for codepage in sys.argv[1:] or ['USA']:
        dummy.set(height=2, width=2)
        dummy.text(codepage+"\n\n\n")
        print_codepage(dummy, codepage)
        dummy.text("\n\n")

    dummy.cut()

    print dummy.output


def print_codepage(printer, codepage):
    printer.charcode(codepage)

    # Table header
    printer.set(text_type='B')
    printer._raw("  %s\n" % " ".join(map(lambda s: hex(s)[2:], range(0,16))))
    printer.set()

    # The table
    for x in range(0,16):
      # First column
      printer.set(text_type='B')
      printer._raw("%s " % hex(x)[2:])
      printer.set()

      for y in range(0,16):
        byte = six.int2byte(x*16+y)

        if byte in (ESC, CTL_LF, CTL_FF, CTL_CR, CTL_HT, CTL_VT):
          byte = ' '

        printer._raw(byte)
        printer._raw(" ")
      printer._raw('\n')

main()