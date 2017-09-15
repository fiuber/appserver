## @file doxygentest.py
## \brief An example Python program.

# Demo class
class Demo:
    """\brief A demo class, it's really just for demonstration.

    The detailed description of the class would appear right here.
    However, as this class is utterly useless when talking about its
    functionality it actually has no detailed description which is
    sort of a pity, since a couple of lines of documentation would
    make it look like a real documentation. But as this is just an
    example of how the doxygen output might look like a one-liner has
    to be enough. Insert your documentation here as appropriate. You
    get the idea now, don't you? If not, I can't help it but I
    certainly won't type in a lot of nonsense just to make it look \em
    real.  No, definitely not.
    """

    def __init__(self):
        """The constructor."""

    def foo(self, bar):
        """The infamous foo method.

        There's no detailed description necessary for the \em foo()
        function as everybody know what it does.

        \param bar The \a bar argument is compulsory, never leave it out.
        \return The \a bar input after processing by the \em foo() function.
        """
        pass

    ## protected:

    def spam(self, amount):
        """Return an amount of spam.

        \param amount (\c int) The amount of spam.
        \return An amount of spam.
        """

        return amount*"spam"


# Another demo class
class AnotherDemo(Demo):
    """\brief This class is derived from the demo class."""

    def __init__(self):
        pass
