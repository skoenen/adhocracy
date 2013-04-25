try:
    import json
except:
    raise ImportError("Python version >= 2.6 needed")

import hashlib
import logging


log = logging.getLogger(name=__name__)


__all__ = ["ValueConverter", "PlainValueConverter", "SignedValueConverter"]

class ValueConverter(object):
    def __init__(self):
        raise NotImplementedError("This is an abstract class.")

    def _serialize(self, value):
        try:
            return json.dumps(value)
        except:
            return None

    def _unserialize(self, value):
        try:
            return json.loads(value)
        except:
            return None

    def encode(self, value):
        raise NotImplementedError("This is an abstract class.")

    def decode(self, value):
        raise NotImplementedError("This is an abstract class.")

class PlainValueConverter(ValueConverter):
    def encode(self, value):
        return self._serialize(value)

    def decode(self, value):
        return self._unserialize(value)

class SignedValueConverter(ValueConverter):
    _algorithm = "sha256"

    def __init__(self, secret):
        if secret is None:
            raise ValueError("Secret could not be \"None\".")

        self._secret = secret

    def _sign_value(self, value):
        return self._serialize({"value": value, "secret": self._secret})

    def sign(self, value):
        return getattr(hashlib, self._algorithm)(
                self._sign_value(value)).hexdigest()

    def sign_valid(self, value, sign):
        return sign == self.sign(value)

    def encode(self, value):
        return self._serialize({
                "algo": self._algorithm,
                "value": value,
                "sign": self.sign(value)})

    def decode(self, value):
        obj = self._unserialize(value)
        if obj is not None:
            if self.sign_valid(obj["value"], obj["sign"]):
                obj = obj["value"]
            else:
                log.info("Validation of signature for \"{}\" failed."
                        .format(obj))
                obj = None

        return obj

