#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
Bereitet die Gliederung einer GuV und Bilanz ordentlich auf.

Regeln:
* Da alphabetisch sortiert wird (nicht nummerisch), müssen

  - die Nummern eines Abschnittes gleich viele Stellen haben,
    also bei Bedarf führenden Nullen verwenden. Dieser werden
    für die Ausgabe automatisch entfernt.

  - Für Unterpunkte, die mit Spiegelstrichen dargestellt werden gilt:
    Gibt es in einem Abschnitt mehrere, dann werden diese mit Ziffern
    direkt hinter dem Spiegelstrich nummeriert. Bei nur einem
    Spiegelstrich im Abschnitt, ist die zusätliche Nummerierung nicht
    nötig. Beispiel::

         C. 07: ...
         C. 07 -: ...
         C. 08: ...
         C. 08 -1: ...
         C. 08 -2: ...
  
"""

# files to use for testing
__infiles = ['gliederung-bilanz.cfg',
           'gliederung-guv.cfg']

from ConfigParser import ConfigParser
import re

pat_number = re.compile(r'(?:(\S+)\s?)')
pat_davon = re.compile(r'-\d+$')

def readGrouping(infile, abschnitt=None):
    """
    Iterate over the items of a grouping.
    The grouping is

    Item numbers are 
    """

    def readItems(cfg, section):
        for num, text in cfg.items(section):
            num = pat_number.findall(num)
            text = ' '.join(text.splitlines())
            num = map(lambda x: x.upper(), num)
            yield num, text

    cfg = ConfigParser()
    cfg.readfp(open(infile))

    if abschnitt:
        sections = [abschnitt]
    else:
        sections = cfg.sections()

    for section in sections:
        yield None, section
        for num, text in sorted(readItems(cfg, section)):
            num = map(lambda n: n.lstrip('0'), num)
            yield num, text


def iterPrettyItems(infile, abschnitt=None):
    """
    """

    def canonifyNum(num):
        num[-1] = pat_davon.sub('-', num[-1].strip())
        return ' '.join(num)

    laststack = []

    for num, text in readGrouping(infile, abschnitt=None):
        if num is None:
            yield None, None, text
            continue

        printNum = canonifyNum(num)

        while laststack:
            last, lastlen = laststack.pop()
            if num[:len(last)] == last:
                # put last entry back on stack
                laststack.append((last, lastlen))
                printNum = ' ' * lastlen + printNum[lastlen:]
                break

        laststack.append((num, len(printNum)))

        yield num, printNum, text

def prettyPrintItems(infile, abschnitt=None):
    """
    """
    # this is mostly meant a an example
    for num, num1, text in iterPrettyItems(f, abschnitt):
        if num is None: # section
            print
            print text
            print max(10, len(text))*'-'
        else:
            print num1, text

            
if __name__ == '__main__':
    for f in __infiles:
        print '=====', f, '====='
        prettyPrintItems(f)
        print
        print
        
del __infiles
