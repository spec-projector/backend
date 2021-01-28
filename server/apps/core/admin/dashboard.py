from jnt_admin_tools.dashboard import Dashboard as BaseDashboard, modules
from jnt_admin_tools.dashboard.modules import RecentActions


class Dashboard(BaseDashboard):
    """Base class for dashboards."""

    def init_with_context(self, context):
        """Define what we need to see in admin dashboard here."""
        self.children.append(
            modules.AppList("Applications", exclude=["constance.*"]),
        )
        self.children.append(RecentActions("Recent actions", 5))
