import os
import urllib

open_adas = 'http://open.adas.ac.uk/'

class OpenAdas(object):
    def search_adf11(self, element, year='', metastable='unresolved'):
        p = [('element', element), ('year', year), ('metastable', metastable),
                ('searching', 1)]
        s = AdasSearch('adf11')
        return s.search(p)

    def search_adf15(self, element, charge=''):
        p = [('element', element), ('charge', charge), ('resolveby', 'file'),
                ('searching', 1)]
        s = AdasSearch('adf15')
        return s.search(p)

    def fetch(self, id_filename, dst_directory=None):
        if dst_directory == None:
            dst_directory = os.curdir
        self.dst_directory = dst_directory

        dst_filename = os.path.join(self.dst_directory, id_filename[1])

        url = self._construct_url(id_filename)
        tmpfile, msg = urllib.urlretrieve(url)
        lines = open(tmpfile).readlines()

        # Write all lines in the destination file but the first.  Files, incorrectly,
        # contain an empty first line. This is a bug in the Open-ADAS database.
        dst = open(dst_filename, 'w')
        dst.writelines(lines[1:])

        os.remove(tmpfile)

    def _construct_url(self, id_filename):
        """
        >>> db = OpenADAS()
        >>> db._construct_url((12345, 'foo.dat'))
        'http://open.adas.ac.uk/download.php?id=12345'
        """
        id_, filename = id_filename
        query = [('id', id_)]
        return open_adas + 'download.php?' + urllib.urlencode(query)


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
        res, msg = urllib.urlretrieve(search_url)
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
                element, class_, comment, year, resolved, url, name = l
                id_ = self._strip_url(url)
                class_ = class_.lower()
                db.append((id_, name))
            elif self.class_ == 'adf15':
                element, ion, w_lo, w_hi, url, name = l
                id_ = self._strip_url(url)
                db.append((id_, name))
            else:
                raise NotImplementedError('this should never happen')

        return db

    def _strip_url(self, url):
        _, id_ = url.split('=')
        return int(id_)



from HTMLParser import HTMLParser
class SearchPageParser(HTMLParser):
    """
    Filling in a search form on http://open.adas.ac.uk generates a HTML document
    with a table that has the following structure:

    >>> html = '''
    ... <table class='searchresults'>
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

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table' and attrs.get('class') == 'searchresults':
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
