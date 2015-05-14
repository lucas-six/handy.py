#!/usr/bin/env python

'''A tiny Python library.


Copyright 2015 Li Yun <leven.cn@gmail.com>.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import sys
import unittest

import pep8


# POSIX conformance
import os
if os.name != 'posix':
    sys.exit('POSIX-conformance system required')

if sys.version_info < (3, 4):
    sys.exit("Python 3.4+ required")


class GeneralTestCase(unittest.TestCase):
    '''General test case for module.

    Includes:

        - PEP 8 conformance (pep8 required)

    '''

    def setUp(self):
        '''Subclasses must provide `test_modules` and could configure
        `pep8_quiet`.'''
        self.test_modules = [__file__]
        self.pep8_quiet = False

    def test_pep8_conformance(self):
        pep8_style = pep8.StyleGuide(quiet=self.pep8_quiet)
        result = pep8_style.check_files(self.test_modules)
        self.assertEqual(result.total_errors, 0,
                         'Found {0} code style errors (and warnings)'
                         .format(result.total_errors))


if __name__ == '__main__':
    unittest.main(verbosity=2, catchbreak=True)
