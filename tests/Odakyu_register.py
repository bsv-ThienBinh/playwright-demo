import pytest
import re
import os
from playwright.sync_api import expect, Error as PlaywrightError

BASE_URL = "https://admin.odakyu.bravesoft.vn/login"
EMAIL = "kimtran@bravesoft.com.vn"
PASSWORD = "brave0404"


def debug_delay(page, ms=2000):
    if os.getenv("SLOW_MO") == "1":
        page.wait_for_timeout(ms)


def open_screen(page):
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=60000)

    email = page.locator("input#mail_address, input[name='email']").first
    password = page.locator("input#password, input[name='password']").first

    expect(email).to_be_visible(timeout=15000)
    email.fill(EMAIL)
    password.fill(PASSWORD)

    login_btn = page.get_by_role("button", name="ログイン")
    expect(login_btn).to_be_visible(timeout=10000)
    login_btn.click()
    debug_delay(page, 3000)

    expect(page).to_have_url(
        re.compile(r"^https://admin\.odakyu\.bravesoft\.vn/account-management/?$"),
        timeout=30000,
    )

    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)

    new_btn = page.locator("button.common-submit-btn.primary:has-text('新規追加')").first
    expect(new_btn).to_be_visible(timeout=20000)
    expect(new_btn).to_be_enabled(timeout=20000)
    new_btn.scroll_into_view_if_needed()
    # Wait for transient loading mask to disappear before clicking.
    overlay = page.locator("div.loading-overlay")
    if overlay.count() > 0:
        try:
            expect(overlay.first).to_be_hidden(timeout=15000)
        except Exception:
            page.wait_for_timeout(1000)

    try:
        new_btn.click(timeout=10000)
    except Exception:
        # Fallback for rare overlay race where pointer events are still blocked.
        new_btn.click(force=True, timeout=10000)
    debug_delay(page, 5000)

    # Fallback click if first click is swallowed by overlay/state transition.
    popup = page.locator("div.modify-account-modal-content")
    try:
        expect(popup).to_be_visible(timeout=5000)
    except Exception:
        new_btn.click(force=True, timeout=10000)
        debug_delay(page, 5000)
    if os.getenv("DEBUG_POPUP") == "1":
        page.pause()
        expect(popup).to_be_visible(timeout=15000)

    # Assert title specifically inside the opened modal to avoid false positives.
    expect(popup.locator("div.title-confirm")).to_have_text("新規アカウント追加")
    page.screenshot(path="popup_opened_debug.png", full_page=True)


@pytest.fixture(autouse=True)
def setup_each_test(page):
    open_screen(page)


@pytest.fixture(autouse=True)
def pause_10s_each_test(page):
    yield
    if os.getenv("PAUSE_EACH_TEST", "1") != "1":
        return
    try:
        if not page.is_closed():
            page.wait_for_timeout(5000)
    except PlaywrightError:
        # Ignore teardown delay when page/context was already closed by browser/runtime.
        pass


def test_01_title(page):
    modal_title = page.locator("div.modify-account-modal-content div.title-confirm")
    expect(modal_title).to_be_visible()
    expect(modal_title).to_have_text("新規アカウント追加")
    debug_delay(page, 5000)


def test_02_url(page):
    expect(page).to_have_url(
        re.compile(r"^https://admin\.odakyu\.bravesoft\.vn/account-management/?$"),
        timeout=30000,
    )


def test_03_account_label(page):
    label = page.locator("div.label-title", has_text="アカウント名").first
    expect(label).to_be_visible()
    expect(label).to_contain_text("アカウント名")
    expect(label).to_contain_text("255文字以内")
    debug_delay(page, 15000)

def test_04_account_name_input(page):
    page.locator("input[name='userName']").fill("Thomas")
    expect(page.locator("input[name='userName']")).to_have_value("Thomas")

def test_05_email_label(page):
    label = page.locator("div.label-title", has_text="メールアドレス").first
    expect(label).to_be_visible()
    expect(label).to_contain_text("メールアドレス")

def test_06_email_input(page):
    page.locator("input[name='email']").fill("Thomas@gmail.com")
    expect(page.locator("input[name='email']")).to_have_value("Thomas@gmail.com")

def test_07_password_label(page):
    label = page.locator("div.label-title", has_text="パスワード").first
    expect(label).to_be_visible()
    expect(label).to_contain_text("パスワード")
    expect(label).to_contain_text("半角英数字 8文字以上32文字以内）")


from playwright.sync_api import expect

def test_08_password_placeholder(page):
    password_input = page.locator('input[type="password"]').first
    expect(password_input).to_be_visible()
    expect(password_input).to_have_attribute("placeholder", "**********")


def test_09_password_mask_display(page):
    password_input = page.locator('input[type="password"]').first
    expect(password_input).to_be_visible()

    password_input.fill("abc12XYZ")
    expect(password_input).to_have_value("abc12XYZ")  # 実値は保持される
    expect(password_input).to_have_attribute("type", "password")  # マスク表示条件  


def test_10_role_select_initial_display(page):
    # Khu vuc "権限"
    role_box = page.locator("div.label-input", has_text="権限").first

    # Co o select hien thi
    expect(role_box.locator(".multiselect-wrapper")).to_be_visible()

    # Co icon muoi ten (pull-down)
    expect(role_box.locator(".multiselect-caret")).to_be_visible()

    # Chua chon gi luc dau
    expect(role_box.locator(".multiselect-single-label")).to_have_count(0)


def test_11_role_select_option_master_admin(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    select = role_box.locator(".multiselect-wrapper")

    # Mo dropdown
    select.click()

    # Chon "マスター管理者"
    role_box.locator("li.multiselect-option", has_text="マスター管理者").click()

    # Kiem tra gia tri da hien thi trong box
    expect(role_box.locator(".multiselect-single-label")).to_have_text("マスター管理者")


def test_12_role_select_option_tenant_admin(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    select = role_box.locator(".multiselect-wrapper")

    # Mo dropdown
    select.click()

    # Chon "テナント管理者"
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()

    # Kiem tra gia tri da hien thi trong box
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")


def test_13_role_select_cannot_choose_both(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    select = role_box.locator(".multiselect-wrapper")

    # Chon gia tri thu 1
    select.click()
    role_box.locator("li.multiselect-option", has_text="マスター管理者").click()
    expect(role_box.locator(".multiselect-single-label")).to_have_text("マスター管理者")

    # Chon tiep gia tri thu 2
    select.click()
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()

    # Ket qua: chi con 1 gia tri (gia tri moi de len gia tri cu)
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")
    expect(role_box.locator(".multiselect-tag")).to_have_count(0)


def test_14_ticket_point_permission_display(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    role_select = role_box.locator(".multiselect-wrapper")
    role_select.click()
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")

    section = page.locator(
        "div.label-input:has(div.label-title:has-text('チケット組成時のポイント付与パラメータの変更権限'))"
    ).first
    expect(section).to_be_visible(timeout=10000)
    expect(
        section.locator(
            "div.label-title", has_text="チケット組成時のポイント付与パラメータの変更権限"
        )
    ).to_be_visible()
    expect(section.locator("label.custom-radio-input", has_text="有")).to_be_visible()
    expect(section.locator("label.custom-radio-input", has_text="無")).to_be_visible()


def test_15_ticket_point_permission_select_yes(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    role_select = role_box.locator(".multiselect-wrapper")
    role_select.click()
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")

    box = page.locator(
        "div.label-input:has(div.label-title:has-text('チケット組成時のポイント付与パラメータの変更権限'))"
    ).first
    yes_radio = box.locator("input#authority1")

    # Chon "有"
    yes_radio.check()

    # Kiem tra "有" da duoc chon
    expect(yes_radio).to_be_checked()


def test_16_ticket_point_permission_select_no(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    role_select = role_box.locator(".multiselect-wrapper")
    role_select.click()
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")

    box = page.locator(
        "div.label-input:has(div.label-title:has-text('チケット組成時のポイント付与パラメータの変更権限'))"
    ).first
    no_radio = box.locator("input#authority2")

    # Chon "無"
    no_radio.check()

    # Kiem tra "無" da duoc chon
    expect(no_radio).to_be_checked()


def test_17_ticket_point_permission_cannot_select_both(page):
    role_box = page.locator("div.label-input", has_text="権限").first
    role_select = role_box.locator(".multiselect-wrapper")
    role_select.click()
    role_box.locator("li.multiselect-option", has_text="テナント管理者").click()
    expect(role_box.locator(".multiselect-single-label")).to_have_text("テナント管理者")
    box = page.locator("div.label-input", has_text="チケット組成時のポイント付与パラメータの変更権限").first
    
    yes_radio = box.locator("input#authority1")
    no_radio = box.locator("input#authority2")

    # Chon "有"
    yes_radio.check()
    expect(yes_radio).to_be_checked()
    expect(no_radio).not_to_be_checked()

    # Chon tiep "無" -> chi 1 lua chon duoc giu
    no_radio.check()
    expect(no_radio).to_be_checked()
    expect(yes_radio).not_to_be_checked()