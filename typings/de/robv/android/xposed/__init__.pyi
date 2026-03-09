from typing import Any

from java.lang.reflect import Member

class XC_MethodHook:
    """
    Callback class for method hooks.

    Usually, anonymous subclasses of this class are created which override
    `beforeHookedMethod` and/or `afterHookedMethod`.
    """

    def __init__(self, priority: int = 50) -> None:
        """
        Creates a new callback with a specific priority.

        Note that `afterHookedMethod` will be called in reversed order, i.e.
        the callback with the highest priority will be called last. This way, the callback has the
        final control over the return value. `beforeHookedMethod` is called as usual, i.e.
        highest priority first.
        """
        ...

    class MethodHookParam:
        """
        Wraps information about the method call and allows to influence it.
        """

        method: Member
        """The hooked method/constructor."""

        thisObject: Any
        """The `this` reference for an instance method, or `None` for static methods."""

        args: list[Any]
        """Arguments to the method call."""

        def getResult(self) -> Any:
            """
            Returns the result of the method call.
            """
            ...

        def setResult(self, result: Any) -> None:
            """
            Modify the result of the method call.

            If called from `beforeHookedMethod`, it prevents the call to the original method.
            """
            ...

        def getThrowable(self) -> Any:
            """
            Returns the `Throwable` thrown by the method, or `None`.
            """
            ...

        def hasThrowable(self) -> bool:
            """
            Returns true if an exception was thrown by the method.
            """
            ...

        def setThrowable(self, throwable: Any) -> None:
            """
            Modify the exception thrown of the method call.

            If called from `beforeHookedMethod`, it prevents the call to the original method.
            """
            ...

        def getResultOrThrowable(self) -> Any:
            """
            Returns the result of the method call, or throws the Throwable caused by it.
            """
            ...
