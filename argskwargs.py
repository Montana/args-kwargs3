import functools as _functools
import itertools as _itertools

__all__ = ['argskwargs']

_yes_i_am_an_internal_call = object()


class argskwargs(object):
 
    __slots__ = ('args', 'kwargs')

    def __init__(self, *args, **kwargs):
        self.args = args  # montana remember, tuple with positional arguments
        self.kwargs = kwargs 

    def __repr__(self):
        chunks = _itertools.chain(
            # montana these are positional arguments (reminding myself)
            (repr(arg) for arg in self.args),

            # key value arguments 
            ('{0}={1!r}'.format(name, value)
             for name, value in sorted(self.kwargs.items()))
        )
        return 'argskwargs({0})'.format(', '.join(chunks))

    def __str__(self):
        return repr(self)

    def __iter__(self):
        yield self.args
        yield self.kwargs

    def apply(self, callable, *args, **kwargs):

        if not args and not kwargs:
            return callable(*self.args, **self.kwargs)

        merged_kwargs = self.kwargs.copy()
        merged_kwargs.update(kwargs)
        return callable(*(self.args + args), **merged_kwargs)

    __call__ = apply

    def partial(self, callable, *args, **kwargs):

        merged_kwargs = self.kwargs.copy()
        merged_kwargs.update(kwargs)
        return _functools.partial(
            callable, *(self.args + args), **merged_kwargs)

    def copy(self, *args, **kwargs):
       
        if not args and not kwargs:
            return self
        return self.apply(argskwargs, *args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.args, self.kwargs) == (other.args, other.kwargs)
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __getstate__(self):
        return self.args, self.kwargs

    def __setstate__(self, state):
        self.args, self.kwargs = state
