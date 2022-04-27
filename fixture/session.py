from selenium.webdriver.common.by import By


class SessionHelper:

    def __init__(self, app):
        self.app = app
        self.driver = self.app.driver

    def login(self, user_name, password):
        self.app.open_home_page()
        self.driver.find_element(By.NAME, "username").click()
        self.driver.find_element(By.NAME, "username").clear()
        self.driver.find_element(By.NAME, "username").send_keys(user_name)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()
        self.driver.find_element(By.NAME, "password").click()
        self.driver.find_element(By.NAME, "password").clear()
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]').click()

    def logout(self):
        self.driver.find_element(By.LINK_TEXT, "administrator").click()
        self.driver.find_element(By.LINK_TEXT, " Выход").click()

    def is_logged_in(self):
        self.driver.find_element(By.LINK_TEXT, "administrator").click()
        return len(self.driver.find_elements(By.LINK_TEXT, "Logout")) > 0

    def is_logged_in_as(self, username):
        return self.get_logged_user() == username

    def get_logged_user(self):
        return self.driver.find_element(By.CSS_SELECTOR, '#breadcrumbs > ul > li > a').text

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def ensure_login(self, username, password):
        if self.is_logged_in():
            if self.is_logged_in_as(username):
                return
            else:
                self.logout()
        self.login(username, password)
