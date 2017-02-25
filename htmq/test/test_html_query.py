from unittest import TestCase, main as ut_main
from os.path import dirname, abspath, join as joinpath

from redlib.api.http import HttpRequest, GlobalOptions

from ..html_query import HtmlQuery, htmq


go = GlobalOptions(cache_dir='test_cache')
hr = HttpRequest(global_options=go)
this_file_dir = dirname(abspath(__file__))


def readfile(f): 
        with open(joinpath(this_file_dir, f), 'r') as f:
                return f.read()


class TestHtmlQuery(TestCase): 

        def get_page(self, url):
                return hr.get(url)


        def test_title(self):
                html = self.get_page("https://google.com")
                self.assertEqual(htmq(html).title().text().q(), 'Google')


        def test_div(self):
                html = readfile('1.html')
                self.assertEqual(htmq(html).all().div(cls='test').first().text().q(), 'first div')
                self.assertEqual(htmq(html).all().div(cls='test').second().text().q(), 'second div')
                self.assertEqual(htmq(html).all().div(cls='test', id='second').one().text().q(), 'second div')
                self.assertEqual(htmq(html).all().div(cls='test').last().text().q(), 'second div')
                self.assertEqual(htmq(html).all().div(cls='test_no_exist').last().text().on_exc(ret=None).q(), None)

                class TestException(Exception):
                        pass

                with self.assertRaises(TestException):
                        htmq(html).all().div(cls='test_no_exist').last().text().on_exc(exc_cls=TestException).q()


        def test_a(self):
                html = readfile('1.html')
                self.assertEqual(htmq(html).all().a().one().attr('href').q(), 'test_target')
                self.assertEqual(htmq(html).all().a().one().text().q(), 'test link')
                self.assertEqual(htmq(html).all().a().one().attrs('href,class').q(), ('test_target', 'test'))
                

if __name__ == '__main__':
        ut_main()
