# https://docs.djangoproject.com/en/1.11/topics/testing/advanced/#defining-a-test-runner
# python ./manage.py test --testrunner=runtests.TestsRunner
# python ./manage.py test --testrunner=runtests.TestsRunner --settings=mollys.settings-test tests
from django.test.runner import DiscoverRunner

class TestsRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
