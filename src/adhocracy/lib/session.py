try:
    from paste.registry import StackedObjectProxy
    adhocarcy_session = StackedObjectProxy(name="adhocarcy.session.stack")
except:
    adhocarcy_session = None

try:
    from Cookie import SimpleCookie
except ImportError:
    from http.cookies import SimpleCookie

try:
    import hashlib
except Exception:
    raise ImportError('Python version >= 2.5 needed')

from datetime import utcnow

session_key = "adhocracy_session"

class SessionMiddleware(object)
    _session_stack = adhocarcy_session
    _env_key = 'adhocracy.session.key'
    _secret_key = 'adhocarcy.session.secret'

    def __init__(self, app, config, **kwargs):
        self._app = app
        self._config = config or {}

        session_key = self._config[self._env_key] or 'adhocracy_session'
        self._session_secret = self._config[self.secret_key] or ''

    def __call__(self, environ, start_response):
        session = Session(environ, **self._config)

        if environ.get('paste.registry'):
            if environ['paste.registry'].reglist:
                environ['paste.registry'].register(
                        self._session_stack,
                        session)

        environ[session_key] = session

        def session_start_response(status, headers, exc_info=None):
            if session.changed():
                headers.append(('Set-cookie', session.cookie()))
            return start_response(status, headers, exc_info)

        return self.wrap_app(environ, session_start_response)

class Session(object):
    _hash_key = 'adhocracy.session.hash_function'

    def __init__(self, environ, config, **kwargs):
        self._config = config
        self._environ = environ
        self._header = {}
        self._values = {}

        if 'HTTP_COOKIE' in environ:
            self._cookie = SimpleCookie(environ.get('HTTP_COOKIE'))
            self._update_session()
        else:
            self._cookie = SimpleCookie()
            self._update_cookie()

    def __setitem__(self, key, value):
        self._values.__setitem__(key, value)
        self._changed = True
        self._dirty = True

    def __getitem__(self, key):
        return self._values.__getitem__(key)

    def __iter__(self):
        return iter(self._values)

    def _update_cookie(self):
        if not self._cookie:
            self._cookie = SimpleCookie()
            self._dirty = True

        if self._dirty:
            for key, value in self._values:
                self._cookie[key] = value

            self._dirty = False

    def _update_session(self):
        for key, value in self._cookie:
            self._values[key] = value

    def keys(self):
        return self._values.keys()

    def values(self):
        return self._values.values()

    def accessed(self):
        return self._changed

    def set_hashed(self, key, value):
        if hash_key not in hashlib.__dict__:
            raise ConfigurationException(
                "The configured hash function {0} is not implemented.".format(hash_key))

        hash_func = hashlib.__dict__[self._config[hash_key]]

        clear_val = "{0}{1}{2}" .format(value,
                            self._values['created_at'].isoformat(),
                            self._secret)
        enc_val = "{0}!!!{1}" .format(hash_func(clear_val), value)

        self.__setitem__(key, hash_func(value))
        self._changed = True

    def get_hashed(self, key):
        if hash_key not in hashlib.__dict__:
            raise ConfigurationException(
                "The configured hash function {0} is not implemented.".format(hash_key))

        hash_func = hashlib.__dict__[self._config[hash_key]]

        enc_val, value = self._values[key].split("!!!")
        clear_val = "{0}{1}{2}" .format(value,
                            self._values['created_at'].isoformat(),
                            self._secret)
        if enc_val == hash_func(clear_val):
            return value
        else:
            return None

    def get(key, default = None):
        return self._values.get(key, default)

    def cookie(self):
        self._update_cookie()
        return self._cookie

