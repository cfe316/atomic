import os
import urllib


class OpenADAS(object):
    search_url = ('http://open.adas.ac.uk/adf11.php?'
            'element=%(element)s&'
            'year=%(year)d&'
            'metastable=%(metastable)s&'
            'searching=1')
    fetch_url = r'http://open.adas.ac.uk/download.php?id=%d'

    def __init__(self):
        self.data = 0

    def search(self, element, year):
        self._retrieve_search_page(element, year)
        return self._parse_data()

    def _retrieve_search_page(self, element, year):
        options = dict(element=element, year=year, metastable='unresolved')
        res, msg = urllib.urlretrieve(self.search_url % options)
        self.data = open(res).read()
        os.remove(res)

    def _parse_data(self):
        parser = SearchPageParser()
        parser.feed(self.data)
        lines = parser.lines

        if lines == []: return {}
        header = lines.pop(0)

        db = {}
        for l in lines:
            element, class_, comment, year, resolved, url, name = l
            id_ = self._strip_url(url)
            db[class_.lower()] = (id_, name)

        return db

    def _strip_url(self, url):
        _, id_ = url.split('=')
        return int(id_)

    def fetch(self, id_filename, dst_directory=None):
        if dst_directory == None:
            dst_directory = os.curdir
        self.dst_directory = dst_directory

        id_, filename = id_filename

        url = self.fetch_url % id_

        dst_filename = os.path.join(self.dst_directory, filename)

        tmpfile, msg = urllib.urlretrieve(url)
        lines = open(tmpfile).readlines()

        # Write all lines in the destination file but the first.  Files, incorrectly,
        # contain an empty first line. This is a bug in the Open-ADAS database.
        dst = open(dst_filename, 'w')
        dst.writelines(lines[1:])

        os.remove(tmpfile)


class Sniffer(object):
    def __init__(self, file_):
        self.file_ = file_
        self.name = os.path.basename(file_)

        self._sniff_name()
        self._check()

    def _sniff_name(self):
        name, extension = self.name.split(os.path.extsep)

        type_, element = name.split('_')
        class_ = type_[:3]
        year = type_[3:]
        resolved = year.endswith('r')

        self.element = element
        self.year = year
        self.class_ = class_
        self.extension = extension
        self.resolved = resolved

    def _check(self):
        assert self.extension == 'dat'
        assert self.resolved == False, 'metastable resolved data not supported.'


from HTMLParser import HTMLParser
class SearchPageParser(HTMLParser):
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
    from atomic_data import _full_path

    dst_directory = _full_path('')

    data = [('carbon', 96), ('argon', 89), ('neon', 96)]

    adas = OpenADAS()
    for element, year in data:
        res = adas.search(element, year)

        for key in ['acd', 'scd', 'plt', 'prc', 'prb']:
            if key in res.keys():
                adas.fetch(res[key], dst_directory)
            else:
                print 'Warning: %s file is missing in %s %d dataset.'\
                        % (key, element, year)

