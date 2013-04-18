from adhocracy.tests import TestController
from adhocracy.lib.session import Session

# Use the PlainValueConverter to make it easier to test the session
from adhocracy.lib.session.converter import PlainValueConverter


class SessionTestController(TestController):
    _domain = "adhocracy.lan"

    def _config(self, **add_config):
        config = {}

        config["adhocracy.domain"] = self._domain

        config.update(add_config)
        return config

    def _environ(self, **add_environ):
        environ = {}

        environ["HTTP_COOKIE"] = "Cookie: President=\"Perry Rhodan\";
        Domain=.adhocray.lan"

        environ.update(add_environ)
        return environ

    def _check_with_session(self, session, *add_tests):
        cookie_header = "Set-Cookie: President=\"Perry Rhodan\";
        Domain=.adhocracy.lan"
        session["President"] = "Perry Rhodan"

        # Check that we get what we put into
        self.assertEqual(session["President"], "Perry Rhodan")

        # Check that it produces the correct `Set-Cookie` header
        self.assertEqual(session._cookie["President"], cookie_header)

        if "path_check" in add_tests:
            self.assertTrue("Path=/test" in session._cookie["President"])

        if "http_only_check" in add_tests:
            self.assertTrue("HttpOnly" in session._cookie["President"])

    def session_with_no_extra_config(self):
        session = Session({}, self._config(),
                value_converter=PlainValueConverter)
        self._check_with_session(session)

    def session_with_path(self):
        session = Session({}, self._config(), path="/test",
                value_converter=PlainValueConverter)
        self._check_with_session(session, "path_check")

    def session_with_http_only(self):
        session = Session({}, self._config(), http_only=True,
                value_converter=PlainValueConverter)
        self._check_with_session(session, "http_only_check")

    def session_with_path_and_http_only(self):
        session = Session({}, self._config(), path="/test", http_only=True,
                value_converter=PlainValueConverter)
        self._check_with_session(session, "path_check", "http_only_check")

    def session_load_from_cookie(self):
        session = Session(self._environ(), self._config(),
                value_converter=PlainValueConverter)
        self._check_with_session(session)

