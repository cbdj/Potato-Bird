from pythonforandroid.recipe import PythonRecipe

class PygameMenuRecipe(PythonRecipe):
    """
    Recipe to build apps based on SDL2-based pygame.

    .. warning:: Some pygame functionality is still untested, and some
        dependencies like freetype, postmidi and libjpeg are currently
        not part of the build. It's usable, but not complete.
    """

    url = 'https://github.com/cbdj/pygame-menu/archive/refs/tags/fix_sdl2.tar.gz'

    site_packages_name = 'pygame_menu'
    name = 'pygame_menu'
    depends = ['setuptools']
    call_hostpython_via_targetpython = False
    
    for i in range(10):
        print("HELLO FROM MY CUSTOM pygame_menu RECIPE !!!!")

recipe = PygameMenuRecipe()
