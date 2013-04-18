from adhocracy.tests import TestController
from adhocracy.lib.session.converter import CryptValueConverter


class CryptValueConverterTestController(TestController):

    def crypt_value_with_no_secret(self):
        encryptor = CryptValueConverter()
        decryptor = CryptValueConverter()

        enval = encryptor.encode("Perry Rhodan")
        deval = decryptor.encode("Perry Rhodan")

        self.assertEqual(
                encryptor.encode("Gucky"),
                decryptor.encode("Gucky"))

        self.assertEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

    def crypt_value_with_same_secret(self):
        encryptor = CryptValueConverter("secret")
        decryptor = CryptValueConverter("secret")

        enval = encryptor.encode("Atlan")
        deval = decryptor.encode("Atlan")

        self.assertEqual(
                encryptor.encode("Reginald Bull"),
                decryptor.encode("Reginald Bull"))

        self.assertEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

    def crypt_value_with_different_secret(self):
        encryptor = CryptValueConverter("secret")
        decryptor = CryptValueConverter("Setec Astronomy")

        enval = encryptor.encode("Goeffry Abel Waringer")
        deval = decryptor.encode("Goeffry Abel Waringer")

        self.assertNotEqual(
                encryptor.encode("Lord Zwiebus"),
                decryptor.encode("Lord Zwiebus"))

        self.assertNotEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

