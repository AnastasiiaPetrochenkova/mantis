def test_del_project(app):
    app.session.login("administrator", "root")
    old_list_count = app.mantis_projects.count()
    if old_list_count == 0:
        app.mantis_projects.create_new_project()
        old_list_count = app.mantis_projects.count()
    app.mantis_projects.delete_project()
    assert old_list_count - 1 == app.mantis_projects.count()
    app.mantis_projects.get_project_list()
