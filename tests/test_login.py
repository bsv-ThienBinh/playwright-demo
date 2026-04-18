import pytest

@pytest.fixture(autouse=True)
def pause__seconds_each_case(page):
    """Pause 5 seconds after each test case for observation."""
    yield
    if not page.is_closed():
        page.wait_for_timeout(3_000)


def test_login_003_url_contains_login_path(access_to_login_page):
    """Case 3: URL should contain /login on login screen."""
    login_page = access_to_login_page
    assert "/login" in login_page.page.url


def test_login_004_login_title_is_visible(access_to_login_page):
    """Case 4: Login title should be visible on screen."""
    login_page = access_to_login_page
    assert login_page.is_text_visible("ログイン")


def test_login_005_email_label_and_input_are_visible(access_to_login_page):
    """Case 5: Email label and textbox should be visible."""
    login_page = access_to_login_page
    assert login_page.is_text_visible("メールアドレス")
    assert login_page.page.is_visible(login_page.email_input)


def test_login_006_input_fields(access_to_login_page):
    """Check if user can input text into username and password fields."""
    login_page = access_to_login_page
    login_page.input_email("binhbsv")
    login_page.input_password("xxxx")
    assert login_page.get_input_value(login_page.email_input) == "binhbsv"
    assert login_page.get_input_value(login_page.password_input) == "xxxx"

def test_login_007_password_masking(access_to_login_page):
    """Case 7: Password input should mask characters (type='password')."""
    login_page = access_to_login_page
    # Kiểm tra thuộc tính type của element password có phải là 'password' không
    password_type = login_page.page.get_attribute(login_page.password_input, "type")
    assert password_type == "password"

def test_login_008_email_uppercase(access_to_login_page):
    """Case 8: Uppercase email should be accepted."""
    login_page = access_to_login_page
    login_page.input_email("ABC@GMAIL.COM")
    assert login_page.get_input_value(login_page.email_input) == "ABC@GMAIL.COM"


def test_login_009_invalid_email_format_1(access_to_login_page):
    """Case 9: Invalid email format abc@gmail"""
    login_page = access_to_login_page
    login_page.input_email("abc@gmail")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスが正しくありません。")


def test_login_010_invalid_email_format_2(access_to_login_page):
    """Case 10: Invalid email format abc!@gmail.com"""
    login_page = access_to_login_page
    login_page.input_email("abc!@gmail.com")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスが正しくありません。")


def test_login_011_invalid_email_format_3(access_to_login_page):
    """Case 11: Invalid email format test.abc"""
    login_page = access_to_login_page
    login_page.input_email("test.abc")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスが正しくありません。")


def test_login_012_invalid_email_format_4(access_to_login_page):
    """Case 12: Invalid email format @gmail.com"""
    login_page = access_to_login_page
    login_page.input_email("@gmail.com")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスが正しくありません。")


def test_login_013_fullwidth_email(access_to_login_page):
    """Case 13: Full-width characters in email should show error."""
    login_page = access_to_login_page
    login_page.input_email("ａｂｃ＠gmail.com")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスが正しくありません。")


def test_login_014_empty_email(access_to_login_page):
    """Case 14: Empty email should show required error."""
    login_page = access_to_login_page
    login_page.input_email("")
    login_page.click_login()
    assert login_page.is_text_visible("メールアドレスを入力してください")


def test_login_015_password_label_and_input(access_to_login_page):
    """Case 15: Password label and textbox visible."""
    login_page = access_to_login_page
    assert login_page.is_text_visible("パスワード")
    assert login_page.page.is_visible(login_page.password_input)




def test_login_032_valid_credentials(access_to_login_page):
    """Check login with valid credentials"""

    login_page = access_to_login_page

    # input đúng data login
    login_page.input_email("binhbsv@gmail.com")
    login_page.input_password("brave0404")
     
    # click login
    login_page.click_login()
    # assert (ví dụ sau login thành công)
    assert login_page.page.url != "https://example.com/login"
