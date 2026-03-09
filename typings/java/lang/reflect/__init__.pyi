from typing import Any

from java.lang import Class, String

class Modifier:
    """Java reflection Modifier constants"""

    PUBLIC: int = 1
    PRIVATE: int = 2
    PROTECTED: int = 4
    STATIC: int = 8
    FINAL: int = 16
    SYNCHRONIZED: int = 32
    VOLATILE: int = 64
    TRANSIENT: int = 128
    NATIVE: int = 256
    INTERFACE: int = 512
    ABSTRACT: int = 1024
    STRICTFP: int = 2048

class Member:
    """
    Member is an interface that reflects identifying information about
    a single member (a field or a method) or a constructor.
    """

    PUBLIC: int = 0
    DECLARED: int = 1

    def getDeclaringClass(self) -> Class:
        """Returns the Class object representing the class or interface that declares the member or constructor represented by this Member."""
        ...

    def getName(self) -> String:
        """Returns the simple name of the underlying member or constructor represented by this Member."""
        ...

    def getModifiers(self) -> int:
        """Returns the Java language modifiers for the member or constructor represented by this Member, as an integer."""
        ...

    def isSynthetic(self) -> bool:
        """Returns true if this member was introduced by the compiler; returns false otherwise."""
        ...

class AccessibleObject:
    def setAccessible(self, flag: bool) -> None: ...
    def isAccessible(self) -> bool: ...

class Executable(AccessibleObject, Member):
    def getParameterTypes(self) -> Any: ...
    def getParameterCount(self) -> int: ...

class Method(Executable):
    def invoke(self, obj: Any, *args: Any) -> Any: ...
    def getReturnType(self) -> Class: ...

class Constructor(Executable):
    def newInstance(self, *initargs: Any) -> Any: ...

class Field(AccessibleObject, Member):
    def get(self, obj: Any) -> Any: ...
    def set(self, obj: Any, value: Any) -> None: ...
    def getType(self) -> Class: ...
