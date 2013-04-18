from adhocracy.tests import TestController
from adhocracy.lib.session.converter import SignedValueConverter


class SignedValueConverterTestController(TestController):

    def signed_value_with_no_secret(self):
        ensigner = SignedValueConverter()
        designer = SignedValueConverter()

        enval = ensigner.encode("Julian Tifflor")
        deval = designer.encode("Julian Tifflor")

        self.assertEqual(
                encryptor.encode("Fellmer Lyod"),
                decryptor.encode("Fellmer Lyod"))

        self.assertEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

    def signed_value_with_same_secret(self):
        encryptor = CryptValueConverter("secret")
        decryptor = CryptValueConverter("secret")

        enval = encryptor.encode("Alaska Sadelaere")
        deval = decryptor.encode("Alaska Sadelaere")

        self.assertEqual(
                encryptor.encode("Melbar Kasom"),
                decryptor.encode("Melbar Kasom"))

        self.assertEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

    def signed_value_with_different_secret(self):
        encryptor = CryptValueConverter("secret")
        decryptor = CryptValueConverter("Setec Astronomy")

        enval = encryptor.encode("Roi Danton")
        deval = decryptor.encode("Roi Danton")

        self.assertNotEqual(
                encryptor.encode("Homer G. Adams"),
                decryptor.encode("Homer G. Adams"))

        self.assertNotEqual(
                encryptor.decode(deval),
                decryptor.decode(enval))

