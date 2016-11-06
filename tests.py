import os
import vgmdb
import unittest
import tempfile

class VGMdbTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, vgmdb.app.config['DATABASE'] = tempfile.mkstemp()
        vgmdb.app.config['TESTING'] = True
        self.app = vgmdb.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(vgmdb.app.config['DATABASE'])

    def albumtag(self, albuminput):
        return self.app.post('/album-tagging', data=dict(
          albuminput=albuminput
        ), follow_redirects=True)

    def test_albumtag_success(self):
        rv = self.albumtag('vgmdb.net/album/42848')
        assert 'Ryu ga Gotoku Series Best Soundtrack' in rv.data
        rv = self.albumtag('http://vgmdb.net/album/10065')
        assert 'Umineko no Naku Koro ni' in rv.data
        rv = self.albumtag('20847')
        assert 'Millennium Actress Original Soundtrack' in rv.data

    def test_albumtag_fail(self):
        rv = self.albumtag('')
        assert 'Error' in rv.data
        rv = self.albumtag('2')
        assert 'Error' in rv.data
        rv = self.albumtag('not an album')
        assert 'Error' in rv.data

if __name__ == '__main__':
    unittest.main()
