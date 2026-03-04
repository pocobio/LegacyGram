from hook_utils import find_class, get_private_field

from LegacyGram.data.constants import Keys
from LegacyGram.utils.xposed_utils import BaseHook

# Telegram R class for string resources
R = None

"""
EXPLANATION
MessageCell.GetAuthorStatus() # WORKS ONLY IN CHATS!
    -> if user not null -> call UserObject.GetEmojiStatusDocumentId & exteraBadge
        -> if EmojiStatusDocumentId not null -> return it
        -> if exteraBadge not null -> return badge
        -> if user.premium -> return msg_premium_liststar
    else logic for chat / channels (or idk)
    not checked for exteraBadge

UserObject.GetEmojiStatusDocumentIdHook() # Only 5 calls
    called in ChatMessageCell, DrawerUserCell, DrawerProfileCell
    so it's removes emoji status from (you will see msg_premium_liststar):
        messages in chats, drawer menu, chat list, title in chat list (search is not effected)

DialogObject.GetEmojiStatusDocumentIdHook() has over then 52 calls
"""

"""
TODO: if you click on badge, you got wrong logic.
Solution: see didPressUserStatus in ChatActivity using JADX

if (!user.premium || DialogObject.getEmojiStatusDocumentId(user.emoji_status) == 0) {
    BadgesController badgesController = BadgesController.INSTANCE;
    BadgeDTO badge = badgesController.getBadge(user);
    if (badge != null) {
        boolean zIsDeveloper = badgesController.isDeveloper(user);
        BulletinFactory bulletinFactoryOf = BulletinFactory.of(ChatActivity.this);
        TLRPC.Document documentFindDocument = AnimatedEmojiDrawable.findDocument(((BaseFragment) ChatActivity.this).currentAccount, badge.getDocumentId());
        if (badge.getText() != null) {
            string = LocaleUtils.formatWithUsernames(badge.getText());
        } else {
            string = LocaleController.formatString(zIsDeveloper ? R.string.Developer : R.string.Supporter, user.first_name);
        }
        bulletinFactoryOf.createEmojiBulletin(documentFindDocument, string, zIsDeveloper ? null : LocaleController.getString(R.string.FragmentUsernameOpen),
        new Runnable() {
            @Override
            public final void run() {
                this.f$0.lambda$didPressUserStatus$6();
            }
        }).show();
        return;
    }
    return;
}
"""


class ChatMessageCellGetAuthorStatusHook(BaseHook):
    """
    This hook remain only exteraGram badge
    ref: see original method using JADX

    java:
        private Object getAuthorStatus() {
        MessageObject messageObject;
        TLRPC.User user = this.currentUser;
        if (user != null) {
            BadgeDTO badge = BadgesController.INSTANCE.getBadge(this.currentUser);
            if (badge != null) {
                return badge
            }
            return null
        }
        return null
    """

    _BadgesController = None

    def before_hooked_method(self, param):
        if not self.is_enabled():
            return

        current_user = get_private_field(param.thisObject, "currentUser")

        if current_user:
            if self._BadgesController is None:
                self._BadgesController = find_class("com.exteragram.messenger.badges.BadgesController")
            badge = self._BadgesController.INSTANCE.getBadge(current_user)
            param.setResult(badge)
        else:
            param.setResult(None)


class ProfileActivitySetCollectibleGiftStatusHook(BaseHook):
    def before_hooked_method(self, param):
        if not self.is_enabled():
            return
        param.setResult(None)


def register_premium_badge(plugin) -> None:
    ProfileActivity = find_class("org.telegram.ui.ProfileActivity")
    if ProfileActivity:
        plugin.hook_all_methods(ProfileActivity, "setCollectibleGiftStatus", ProfileActivitySetCollectibleGiftStatusHook(plugin, Keys.hide_gift_hint))

    ChatMessageCell = find_class("org.telegram.ui.Cells.ChatMessageCell")
    if ChatMessageCell:
        plugin.hook_all_methods(ChatMessageCell, "getAuthorStatus", ChatMessageCellGetAuthorStatusHook(plugin, Keys.hide_premium_badge))
