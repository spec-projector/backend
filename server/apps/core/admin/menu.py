from admin_tools.menu import Menu, items, reverse


class AdminMenu(Menu):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.children += [
            items.MenuItem('Home', reverse('admin:index')),
            items.AppList(title='Applications')
        ]
