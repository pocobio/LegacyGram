from client_utils import get_last_fragment
from hook_utils import find_class
from ui.bulletin import BulletinHelper


def get_client_version() -> str:
    try:
        BuildVars = find_class("org.telegram.messenger.BuildVars")
        if BuildVars:
            return str(BuildVars.BUILD_VERSION_STRING)
    except Exception as e:
        BulletinHelper.show_error(f"Failed to get client version: {e}")

    return "Unknown"


def open_url(url: str):
    try:
        current_fragment = get_last_fragment()
        if not current_fragment:
            return
        context = current_fragment.getParentActivity()
        if not context:
            return
        Browser = find_class("org.telegram.messenger.browser.Browser")
        if Browser:
            # or we can use openUrlInSystemBrowser,
            Browser.openUrl(context, url)
    except Exception as e:
        BulletinHelper.show_error(f"Failed to open url {url}: {e}")
