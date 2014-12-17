#-----------------------------------------------------------------------------
#  Copyright (C) 2013 The IPython Development Team
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

import requests

from .base import NBViewerTestCase

class GistTestCase(NBViewerTestCase):
    def test_gist(self):
        url = self.url('2352771')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)

    def test_gist_not_nb(self):
        url = self.url('6689377')
        r = requests.get(url)
        self.assertEqual(r.status_code, 400)

    def test_gist_no_such_file(self):
        url = self.url('6689377/no/file.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 404)

    def test_gist_list(self):
        url = self.url('7518294')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('<th>Name</th>', html)
    
    def test_multifile_gist(self):
        url = self.url('7518294', 'Untitled0.ipynb')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('Download Notebook', html)
    
    def test_anonymous_gist(self):
        url = self.url('gist/4465051')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('Download Notebook', html)
    
    def test_gist_unicode(self):
        url = self.url('gist/amueller/3974344')
        r = requests.get(url)
        self.assertEqual(r.status_code, 200)
        html = r.text
        self.assertIn('<th>Name</th>', html)
