from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from models.projects import Projects


class ProjectHelper:
    project_cache = None

    def __init__(self, app):
        self.app = app
        self.driver = self.app.driver

    def open_home_page(self):
        if not (self.driver.current_url.endswith("/mantisbt-2.25.3/")) or not \
                (self.driver.current_url.endswith("/mantisbt-2.25.3/my_view_page.php")):
            self.driver.find_element(By.LINK_TEXT, "MantisBT").click()

    def manage(self):
        self.open_home_page()
        self.driver.find_element(By.LINK_TEXT, "Управление").click()

    def manage_projects(self):
        self.manage()
        self.driver.find_element(By.LINK_TEXT, "Управление проектами").click()

    def create_new_project(self, projects):
        self.manage_projects()
        create_new_project_button = "#main-container > div.main-content > div.page-content > div > div > div.widget-box.widget-color-blue2 > div.widget-body > div > div.widget-toolbox.padding-8.clearfix > form > button"
        self.driver.find_element(By.CSS_SELECTOR, create_new_project_button).click()
        self.fill_in_form_project(Projects(name=projects.name, status=projects.status,
                                           inherit_global=projects.inherit_global, view_state=projects.view_state,
                                           description=projects.description))
        self.driver.find_element(By.CSS_SELECTOR, '[value="Добавить проект"]').click()
        self.open_home_page()
        self.project_cache = None

    def change_field_value(self, field_name, text):
        if text is not None and field_name != 'project-inherit-global':
            self.driver.find_element(By.ID, field_name).click()
            self.driver.find_element(By.ID, field_name).clear()
            self.driver.find_element(By.ID, field_name).send_keys(text)

    def fill_in_form_project(self, projects):
        self.change_field_value("project-name", projects.name)
        self.select_by_name("project-status", projects.status)
        self.change_field_value("project-inherit-global", projects.inherit_global)
        self.select_by_name("project-view-state", projects.view_state)
        self.change_field_value("project-description", projects.description)

    def select_by_name(self, field_name, text):
        if text is not None:
            Select(self.driver.find_element(By.ID, field_name)).select_by_value('10')

    def get_project_list(self):
        if self.project_cache is None:
            self.manage_projects()
            self.project_cache = []
            project_list = "#main-container > div.main-content > div.page-content > div > div > div.widget-box.widget-color-blue2 > div.widget-body > div > div.table-responsive > table > tbody > tr"
            elements = self.driver.find_elements(By.CSS_SELECTOR, project_list)
            for element in elements:
                cells = element.find_elements_by_tag_name("td")
                name = cells[0].text
                status = cells[1].text
                enabled = cells[2].text
                view_state = cells[3].text
                description = cells[4].text
                self.project_cache.append(Projects(name=name, status=status, enabled=enabled,
                                                   view_state=view_state, description=description))
        return list(filter(None, self.project_cache))

    def open_first_project_from_row(self):
        first_project = "#main-container > div.main-content > div.page-content > div > div > div.widget-box.widget-color-blue2 > div.widget-body > div > div.table-responsive > table > tbody > tr:nth-child(1) > td:nth-child(1) > a"
        self.driver.find_element(By.CSS_SELECTOR, first_project).click()

    def count(self):
        self.open_home_page()
        self.manage_projects()
        project_list = "#main-container > div.main-content > div.page-content > div > div > div.widget-box.widget-color-blue2 > div.widget-body > div > div.table-responsive > table > tbody > tr"
        return len(self.driver.find_elements(By.CSS_SELECTOR, project_list))

    def delete_project(self):
        self.open_home_page()
        self.manage_projects()
        if self.count() == 0:
            self.create_new_project()
        self.open_first_project_from_row()
        self.driver.find_element(By.CSS_SELECTOR, '[value="Удалить проект"]').click()
        self.driver.find_element(By.CSS_SELECTOR, '[value="Удалить проект"]').click()
