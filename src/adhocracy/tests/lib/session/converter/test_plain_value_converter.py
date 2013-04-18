from adhocracy.tests import TestController
from adhocracy.lib.session.converter import PlainValueConverter

class PlainValueConverterTestController(TestController):

    def plain_value_with_no_secret(self):
        converter = PlainValueConverter()
        self.assertEqual( converter.encode("Gucky"), "\"Gucky\"}")

