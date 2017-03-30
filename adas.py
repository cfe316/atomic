import os
import errno
import shutil
import urllib

open_adas = 'http://open.adas.ac.uk/'

class OpenAdas(object):
    def search_adf11(self, element, year='', ms='metastable_unresolved'):
        p = [('element', element), ('year', year), (ms, 1),
                ('searching', 1)]
        s = AdasSearch('adf11')
        return s.search(p)

    def search_adf15(self, element, charge=''):
        p = [('element', element), ('charge', charge), ('resolveby', 'file'),
                ('searching', 1)]
        s = AdasSearch('adf15')
        return s.search(p)

    def fetch(self, url_filename, dst_directory=None):
        if dst_directory == None:
            dst_directory = os.curdir
        self.dst_directory = dst_directory

        url = self._construct_url(url_filename)
        nested = False # this switch makes files save flat
        if nested:
            path = self._construct_path(url_filename)
        else:
            __, path = url_filename

        tmpfile, __ = urllib.urlretrieve(url)

        dst_filename = os.path.join(self.dst_directory, path)
        self._mkdir_p(os.path.dirname(dst_filename))


        shutil.move(tmpfile, dst_filename)

    def _construct_url(self, url_filename):
        """
        >>> db = OpenAdas()
        >>> db._construct_url(('detail/adf11/prb96/prb96_c.dat', 'foo.dat'))
        'http://open.adas.ac.uk/download/adf11/prb96/prb96_c.dat'
        """
        url, __ = url_filename
        query = url.replace('detail','download')
        return open_adas + query

    def _construct_path(self, url_filename):
        """
        This function constructs a path to store the file in.
        >>> db = OpenAdas()
        >>> db._construct_path(('detail/adf11/prb96/prb96_c.dat', 'foo.dat'))
        'adf11/prb96/prb96_c.dat'
        """
        url, filename = url_filename
        path = url.replace('detail/','')
        path = path.replace('][','#')
        return path

    def _mkdir_p(self,path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise


class AdasSearch(object):
    def __init__(self, class_):
        if class_ not in ['adf11', 'adf15']:
            raise NotImplementedError('ADAS class %s is not supported.' %s)

        self.url = open_adas + '%s.php?' % class_
        self.class_ = class_
        self.data = 0
        self.parameters = []

    def search(self, parameters):
        self.parameters = parameters
        self._retrieve_search_page()
        return self._parse_data()

    def _retrieve_search_page(self):
        search_url =  self.url + urllib.urlencode(self.parameters)
        res, __ = urllib.urlretrieve(search_url)
        self.data = open(res).read()
        os.remove(res)

    def _parse_data(self):
        parser = SearchPageParser()
        parser.feed(self.data)
        lines = parser.lines

        if lines == []: return {}
        header = lines.pop(0)

        db = []
        for l in lines:
            if self.class_ == 'adf11':
                element, class_, comment, year, resolved, url, cl, typ, name = l
                name = name.strip()
                db.append((url, name))
            elif self.class_ == 'adf15':
                element, ion, w_lo, w_hi, url, cl, typ, name = l
                name = name.strip()
                db.append((url, name))
            else:
                raise NotImplementedError('this should never happen')

        return db

    def _strip_url(self, url):
        __, id_ = url.split('=')
        return int(id_)


from HTMLParser import HTMLParser
class SearchPageParser(HTMLParser):
    """
    Filling in a search form on http://open.adas.ac.uk generates a HTML document
    with a table that has the following structure:

    >>> html = '''
    ... <table summary='Search Results'>
    ...     <tr>
    ...     <td>Ne</td> <td><a href='filedetail.php?id=32147'>rc89_ne.dat</a></td>
    ...     <tr>
    ...     </tr>
    ...     <td>C</td> <td><a href='filedetail.php?id=32154'>rc89_c.dat</a></td>
    ...     </tr>
    ... </table>'''

    The SearchPageParser can parse this document looking for a table with a
    class `searchresults`.
    >>> parser = SearchPageParser()
    >>> parser.feed(html)
    >>> for l in parser.lines: print l
    ['Ne', 'filedetail.php?id=32147', 'rc89_ne.dat']
    ['C', 'filedetail.php?id=32154', 'rc89_c.dat']
    """
    def reset(self):
        self.search_results = False
        self.line = []
        self.lines = []

        HTMLParser.reset(self)

    #def handle_starttag(self, tag, attrs):
    #    attrs = dict(attrs)
    #    if tag == 'table' and attrs.get('class') == 'searchresults':
    #        self.search_results = True
    #    if not self.search_results: return
    #
    #    if tag == 'a' and self.line != None:
    #        self.line.append(attrs['href'])

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if (tag == 'table'
                and 'summary' in attrs
                and 'Results' in attrs['summary']):
            self.search_results = True
        if not self.search_results: return

        if tag == 'a' and self.line != None:
            self.line.append(attrs['href'])

    def handle_endtag(self, tag):
        if tag == 'table':
            self.search_results = False
        if not self.search_results: return

        if tag == 'tr':
            self.lines.append(self.line)
            self.line = []

    def handle_data(self, data):
        if not self.search_results: return

        if data.strip() != '':
            self.line.append(data)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
