from random import randint

from models.projects import Projects


def test_add_project(app):
    project_name = str(randint(-1000000000, 1000000000))
    add_project = Projects(name=project_name,
                           status='в разработке',
                           view_state='публичный',
                           description="описание, очень подробное и интересное")
    app.session.login("administrator", "root")
    old_list_projects = app.mantis_projects.get_project_list()
    old_list_count = app.mantis_projects.count()
    app.mantis_projects.create_new_project(add_project)
    assert old_list_count + 1 == app.mantis_projects.count()
    new_list_projects = app.mantis_projects.get_project_list()
    old_list_projects.append(add_project)
    assert sorted(old_list_projects, key=Projects.name_or_max) == sorted(new_list_projects, key=Projects.name_or_max)
