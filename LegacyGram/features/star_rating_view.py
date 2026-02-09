from base_plugin import MethodHook
from hook_utils import find_class

class StarRatingHiderHook(MethodHook):
    def __init__(self, plugin):
        self.plugin = plugin

    def before_hooked_method(self, param):
        if self.plugin.get_setting("stars_rating_in_profile", False):
            # public void set(TL_stars.Tl_starsRating starsRating)
            # just saying that user don't have any starsRating
            param.args[0] = None

def register_star_rating_hook(plugin):
    StarRatingView = find_class("org.telegram.ui.Components.StarRatingView")
    if StarRatingView:
        plugin.hook_all_methods(StarRatingView, "set", StarRatingHiderHook(plugin))