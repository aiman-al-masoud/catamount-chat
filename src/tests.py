from playwright.sync_api import Page #,expect



def test_001(page: Page):
    page.goto("http://127.0.0.1:5000/login")
    page.type('css=#input_username', 'capra')
    page.type('css=#input_password', 'password')
    page.click('css=#button_login')
    page.click('css=#capra')
