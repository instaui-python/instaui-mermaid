import pytest
import os


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=None,
        help="Run browser in headless mode",
    )


@pytest.fixture(scope="session")
def browser(request):
    from playwright.sync_api import sync_playwright

    cli_headless = request.config.getoption("--headless")
    if cli_headless is None:
        headless = "GITHUB_ACTION" in os.environ
    else:
        headless = cli_headless

    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless)
    yield browser
    browser.close()
    pw.stop()
