import unittest
from content_provider import ContentProvider

class TestContentProvider(unittest.TestCase):
    def setUp(self):
        self.provider = ContentProvider()

    def test_get_content(self):
        prompt = 'Tell a joke about a technology company.'
        content = self.provider.get_content(prompt)
        print(content)
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()