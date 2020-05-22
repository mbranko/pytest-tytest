# -*- coding: utf-8 -*-

import pytest
from xray_api import make_initial_test_result, send_test_results
from runtime_settings import Cfg, Settings, Stats


def pytest_addoption(parser):
    group = parser.getgroup('tytest')
    group.addoption(
        '--runconfig', 
        dest='runconfig', 
        default='runconfig.py', 
        help='Test parameters script')
    group.addoption(
        '--secrets-file',
        dest='secrets',
        default='/private/secrets',
        help='Full path to secrets file')
    group.addoption(
        '--xray-plan-key',
        dest='xray_plan_key', 
        help='Key of the Xray issue that represents the test plan that is being run')
    group.addoption(
        '--xray-fail-silently',
        dest='xray_fail_silently', 
        default='yes', 
        help='Ignore Xray communication errors')


@pytest.fixture
def runconfig(request):
    return request.config.option.runconfig


@pytest.fixture
def secrets(request):
    return request.config.option.secrets


@pytest.fixture
def xray_plan_key(request):
    return request.config.option.xray_plan_key


@pytest.fixture
def xray_fail_silently(request):
    return request.config.option.xray_fail_silently


def pytest_configure(config):
    # import runtime configuration module
    file_name = config.getoption('runconfig') 
    if file_name.endswith('.py'):
        file_name = os.path.splitext(file_name)[0]
    Settings.RUN_CONFIG = file_name
    module = importlib.import_module(file_name)
    if module:
        for key, value in module.__dict__.items():
            if not key.startswith('_'):
                setattr(Cfg, key, value)

    # register mark for Xray
    config.addinivalue_line('markers', 'xray(test_key): Issue key of the test in Xray')

    Settings.XRAY_PLAN_KEY = config.getoption('xray_plan_key')
    Settings.XRAY_FAIL_SILENTLY = bool(config.getoption('xray_fail_silently'))

    # initialize secret params
    secrets = config.getoption('secrets')
    Settings.XRAY_HOST = read_or_get(secrets, 'XRAY_HOST', 'https://xray.cloud.xpand-it.com')
    Settings.XRAY_CLIENT_ID = read_or_get(secrets, 'XRAY_CLIENT_ID', '')
    Settings.XRAY_CLIENT_SECRET = read_or_get(secrets, 'XRAY_CLIENT_SECRET', '')
    Settings.JIRA_HOST = read_or_get(secrets, 'JIRA_HOST', '')
    Settings.JIRA_USER = read_or_get(secrets, 'JIRA_USER', '')
    Settings.JIRA_PASSWORD = read_or_get(secrets, 'JIRA_PASSWORD', '')
    Settings.JIRA_AUTH = (Settings.JIRA_USER, Settings.JIRA_PASSWORD)

    Stats.START_TIME = datetime.now()


def pytest_collection_modifyitems(config, items):
    for item in items:
        _store_item(item)


def pytest_terminal_summary(terminalreporter):
    Stats.END_TIME = datetime.now()
    result = make_initial_test_result(start_time=Stats.START_TIME, end_time=Stats.END_TIME)
    _fill_keys(terminalreporter.stats, 'passed')
    _fill_keys(terminalreporter.stats, 'failed')
    _fill_keys(terminalreporter.stats, 'skipped')

    for key, values in TestExecutionResult.xray_keys.items():
        test = { 'testKey': key, 'status': 'PASSED', 'steps': [] }
        for item in values:
            if test['status'] =='PASSED' and item.outcome == 'failed':
                test['status'] = 'FAILED'
            step = {
                'status': item.outcome.upper(), 
                'comment': item.nodeid,
            }
            if item.outcome == 'failed':
                step['actualResult'] = str(item.longrepr)
            test['steps'].append(step)
        result['tests'].append(test)
    # print(json.dumps(result, indent=2))
    send_test_results(result)


def _fill_keys(stats, outcome):
    if outcome in stats:
        for stat in stats[outcome]:
            try:
                xray_key = TestExecutionResult.functions[stat.nodeid]
            except KeyError:
                continue
            try:
                TestExecutionResult.xray_keys[xray_key].append(stat)
            except KeyError:
                TestExecutionResult.xray_keys[xray_key] = [stat]


def _get_xray_marker(item):
    return item.get_closest_marker('xray')


def _store_item(item):
    marker = _get_xray_marker(item)
    if not marker:
        return
    test_key = marker.kwargs['test_key']
    TestExecutionResult.functions[item.nodeid] = test_key
