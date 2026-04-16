from pages.base_page import CommonPage
from pages.login_page import UserLoginPage
import pytest

URL = "https://playwright-demo.eventos.work/web/portal/529/event/3988/users/login"


@pytest.fixture
def access_to_login_page(page):
    login_page = UserLoginPage(page)
    login_page.navigate(URL)
    return login_page