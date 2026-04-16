from pages.base_page import CommonPage
class UserLoginPage(CommonPage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = "//input[@id='mail_address']"
        self.password_input = "//input[@id='password']"
        self.login_button = "//button[@id='login_button']"
    
    def input_email(self, email):
        self.fill(self.email_input, email)
    
    def input_password(self, password):
        self.fill(self.password_input, password)
    
    def click_login(self):
        self.click(self.login_button)   

    
    def login(self, email, password):
        self.input_email(email)
        self.input_password(password)
        self.click(self.login_button)