from django_webtest import DjangoTestApp, WebTest

from affinity.wsgi import application


class ViewTestApp(DjangoTestApp):

    def get_wsgi_handler(self):
        return application


class ViewTestCase(WebTest):
    app_class = ViewTestApp

    def _patch_settings(self):
        """
        Disables magic.
        """

    def _unpatch_settings(self):
        """
        Disables magic.
        """
