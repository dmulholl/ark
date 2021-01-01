import ivy

try:
    import syntext
except ImportError:
    pass
else:
    @ivy.renderers.register('stx')
    def render(text):
        return syntext.render(text, pygmentize=True)
