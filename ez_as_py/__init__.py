import os
import time
import random
import pygame
import threading
import pygame.font


class Window:
    """ez_as_py.Window(resolution, framerate, control_thread, resizable=False, debug=True)
    A wrapper class for pygame's display."""

    def __init__(self, resolution, framerate, control_class, resizable=False, debug=False):
        self._main(resolution, framerate, control_class, resizable, debug)

    def _main(self, resolution, framerate, control_class, resizable, debug):
        control_class.window = self
        self.inFrame = False

        self._frameCount = 0
        self._changeName = None

        self._objects = {}

        if debug:
            print('initialized main')
        pygame.init()
        if debug:
            print('pygame initialized')
        self._generateWindow(resolution, resizable)

        self._exit = False
        self._objHash = self._objects
        self._objList = self._objects.items()

        self._clock = pygame.time.Clock()

        self.inFrame = False

        if debug:
            print('created variables')

        frame = 0

        while not self._exit:
            try:
                self.inFrame = True
                self._clock.tick(framerate)
                self._frameCount += 1
                if debug:
                    frame += 1
                    if frame == framerate:
                        frame = 1
                        print(str(time.time()))
                        pygame.display.set_caption(str(self._clock.get_fps()))

                if self._changeName is not None:
                    pygame.display.set_caption(self._changeName)
                    self._changeName = None

                self.events = pygame.event.get()
                for event in self.events:
                    if event.type == pygame.QUIT:
                        os._exit(1)

                self._window.fill((255, 255, 255))

                for name, tup in self._objects.items():
                    if debug:
                        print('obj cycle')
                    obj = tup[0]
                    loc = tup[1]
                    self._window.blit(obj, loc)

                pygame.display.update()
            except KeyboardInterrupt:
                os._exit(0)

    def getMousePos(self):
        """ez_as_py.Window.getMousePos()

        Returns a tuple representing the current position
        of the mouse."""

        return pygame.mouse.get_pos()

    def getMouseState(self):
        """ez_as_py.Window.getMouseState()

        Returns the current mouse state as a dict,
        with key names 'mouse1', 'mouse2', and
        'mouse3', all of which represent boolean
        values stating if they are pressed."""

        state = pygame.mouse.get_pressed()
        statedict = {'mouse1': False, 'mouse2': False, 'mouse3': False}
        if state[0] is True:
            statedict['mouse1'] = True
        if state[1] is True:
            statedict['mouse2'] = True
        if state[2] is True:
            statedict['mouse3'] = True
        return statedict

    def changeWindowName(self, name):
        """ez_as_py.Window.changeWindowName()

        Changes the window's name to a string 'name.'"""

        try:
            if self._getTypeName(name) == 'str':
                self._changeName = name
            else:
                raise ValueError
        except ValueError:
            raise ValueError('\'name\' argument must be str, was ' + self._getTypeName(name))

    def getWindowName(self):
        """ez_as_py.Window.getWindowName()

        Returns the current name of the window."""

        return str(pygame.display.get_caption()[0])

    def getFPS(self):
        """ez_as_py.Window.getFPS()

        Returns a float representing the current framerate."""

        return self._clock.get_fps()

    def setFramerate(self, framerate):
        """ez_as_py.Window.setFramerate(framerate)

        Sets the framerate cap to an int 'framerate.'"""

        self.framerate = framerate

    def onFrame(self):
        """ez_as_py.Window.onFrame()

        Acts as the window's clock, returning the current
        frame count every frame."""

        while self.inFrame is False:
            time.sleep(0.0001)
        self.inFrame = False
        return self._frameCount

    def getKeys(self):
        """ez_as_py.Window.getKeys()

        Return a dictionary of keys with characters with
        a boolean state relating to whether or not they
        are pressed."""
        return pygame.key.get_pressed()

    def makeSurface(self, size, color=(255, 255, 255)):
        """ez_as_py.Window.makeSurface(size, color=(255, 255, 255))

        Returns a surface with the size 'size' (tuple) and the color
        'color' (tuple)."""

        try:
            foo = pygame.Surface(size)
        except ValueError:
            raise ValueError('\'size\' argument must be tuple, was ' + self._getTypeName(size))
        try:
            foo.fill(color)
        except ValueError:
            raise ValueError('\'color\' argument must be tuple, was ' + self._getTypeName(color))
        return foo

    def moveObject(self, obj_name, location):
        """ez_as_py.Window.moveObject(obj_name, location)

        Moves the object named 'obj_name' to the location 'location'.

        Does nothing if object by the name of 'obj_name' is not found."""

        try:
            self._objects[obj_name] = (self._objects[obj_name][0], location)
        except KeyError:
            pass

    def getObject(self, obj_name):
        """ez_as_py.Window.getObject(obj_name)

        Returns the object and its rect that was added by
        ez_as_py.Window.addObject(surf, location), using
        the object ID returned by the mentioned function.

        Returns None if object not found."""

        try:
            return self._objects[obj_name]
        except KeyError:
            return None

    def removeObject(self, obj_name):
        """ez_as_py.Window.removeObject(obj_name)

        Removes an object from the screen, using 'obj_name' as
        the returned name from
        ez_as_py.Window.addObject(surf, location)."""

        try:
            del self._objects[obj_name]
        except KeyError:
            pass

    def addObject(self, surf, location):
        """ez_as_py.Window.addObject(surf, location)

        Adds an object onto the screen.

        The argument 'surf' must be an object that pygame.Surface is able to
        blit (this may be a sprite or another surface,
        for example), or a       # confirm which types pygame.display accepts
        string that contains the path of an image file.

        The argument 'location' must be a tuple of coordinates at which to
        place the object.

        Returns the ID of the object."""

        try:
            if self._getTypeName(surf) == 'str':
                try:
                    surf = pygame.image.load(surf)
                except FileNotFoundError:
                    raise FileNotFoundError('file not found')
            surfID = str(hash(surf) + random.randint(0, 9999999999))[-8:]
            if len(surfID) != 8:
                repID = surfID
                while len(repID) != 8:
                    repID += str(random.randint(0, 9))
                surfID = repID
            while True:
                time.sleep(0.001)
                try:
                    self._objects[surfID] = (surf.convert_alpha(), location)
                    break
                except pygame.error:
                    pass
            return surfID
        except TypeError:
            raise TypeError('\'surf\' argument must be a pygame.Surface or str object, was ' + self._getTypeName(surf))

    def changeID(self, from_id, to_id):
        try:
            self._objects[to_id] = self._objects[from_id]
            del self._objects[from_id]
        except KeyError:
            pass

    def _getTypeName(self, var):
        t = str(type(var))
        t = t.split('\'')[1]
        t = t.split('\'')[0]
        return t

    def get_rect(self):
        """ez_as_py.Window.get_rect()

        Returns the dimensions of the window."""

        return self._window.get_rect()

    def _generateWindow(self, resolution, resizable):
        if not resizable:
            try:
                self._window = pygame.display.set_mode(resolution)
            except TypeError:
                t = str(type(resolution))
                t = t.split('\'')[1]
                t = t.split('\'')[0]
                raise TypeError('\'resolution\' argument must be tuple (width, height), was ' + t)
            except:
                print('Unknown exception, check console.')
                raise Exception('limit break!')
        else:
            try:
                self._window = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            except TypeError:
                t = str(type(resolution))
                t = t.split('\'')[1]
                t = t.split('\'')[0]
                raise TypeError('\'resolution\' argument must be tuple (width, height), was ' + t)
            except:
                print('Unknown exception, check console.')
                raise Exception('limit break!')


def startControlThread(control_class):
    """ez_as_py.startControlThread(control_class)

    Prepares the class 'control_class' to be the controlling
    class over pygame, by shipping it to an alternate thread."""

    c = control_class()
    ctrl = threading.Thread(target=c.main, args=())
    ctrl.daemon = True
    ctrl.start()
    return c


def init(src_class):
    """ez_as_py.init(src_class)

    Initializes variables within the source class 'src_class.ez_'"""

    src_class.window = None
    while src_class.window is None:
        time.sleep(0.01)

    src_class.ez_zero = 48
    src_class.ez_one = 49
    src_class.ez_two = 50
    src_class.ez_three = 51
    src_class.ez_four = 52
    src_class.ez_five = 53
    src_class.ez_six = 54
    src_class.ez_seven = 55
    src_class.ez_eight = 56
    src_class.ez_nine = 57
    src_class.ez_ampersand = 38
    src_class.ez_asterisk = 42
    src_class.ez_at = 64
    src_class.ez_backquote = 96
    src_class.ez_backslash = 92
    src_class.ez_backspace = 8
    src_class.ez_pause = 318
    src_class.ez_capslock = 301
    src_class.ez_caret = 94
    src_class.ez_clear = 12
    src_class.ez_colon = 58
    src_class.ez_comma = 44
    src_class.ez_delete = 127
    src_class.ez_dollar = 36
    src_class.ez_down = 274
    src_class.ez_end = 279
    src_class.ez_equals = 61
    src_class.ez_escape = 27
    src_class.ez_euro = 321
    src_class.ez_exclaim = 33
    src_class.ez_f1 = 282
    src_class.ez_f10 = 291
    src_class.ez_f11 = 292
    src_class.ez_f12 = 293
    src_class.ez_f13 = 294
    src_class.ez_f14 = 295
    src_class.ez_f15 = 296
    src_class.ez_f2 = 283
    src_class.ez_f3 = 284
    src_class.ez_f4 = 285
    src_class.ez_f5 = 286
    src_class.ez_f6 = 287
    src_class.ez_f7 = 288
    src_class.ez_f8 = 289
    src_class.ez_f9 = 290
    src_class.ez_first = 0
    src_class.ez_greater = 62
    src_class.ez_hash = 35
    src_class.ez_help = 315
    src_class.ez_home = 278
    src_class.ez_insert = 277
    src_class.ez_kp0 = 256
    src_class.ez_kp1 = 257
    src_class.ez_kp2 = 258
    src_class.ez_kp3 = 259
    src_class.ez_kp4 = 260
    src_class.ez_kp5 = 261
    src_class.ez_kp6 = 262
    src_class.ez_kp7 = 263
    src_class.ez_kp8 = 264
    src_class.ez_kp9 = 265
    src_class.ez_kp_divide = 267
    src_class.ez_kp_enter = 271
    src_class.ez_kp_equals = 272
    src_class.ez_kp_minus = 269
    src_class.ez_kp_multiply = 268
    src_class.ez_kp_period = 266
    src_class.ez_kp_plus = 270
    src_class.ez_lalt = 308
    src_class.ez_last = 323
    src_class.ez_lctrl = 306
    src_class.ez_left = 276
    src_class.ez_leftbracket = 91
    src_class.ez_leftparen = 40
    src_class.ez_less = 60
    src_class.ez_lmeta = 310
    src_class.ez_lshift = 304
    src_class.ez_lsuper = 311
    src_class.ez_menu = 319
    src_class.ez_minus = 45
    src_class.ez_mode = 313
    src_class.ez_numlock = 300
    src_class.ez_pagedown = 281
    src_class.ez_pageup = 280
    src_class.ez_pause = 19
    src_class.ez_period = 46
    src_class.ez_plus = 43
    src_class.ez_power = 320
    src_class.ez_print = 316
    src_class.ez_question = 63
    src_class.ez_quote = 39
    src_class.ez_quotedbl = 34
    src_class.ez_ralt = 307
    src_class.ez_rctrl = 305
    src_class.ez_enter = 13
    src_class.ez_right = 275
    src_class.ez_rightbracket = 93
    src_class.ez_rightparen = 41
    src_class.ez_rmeta = 309
    src_class.ez_rshift = 303
    src_class.ez_rsuper = 312
    src_class.ez_scrollock = 302
    src_class.ez_semicolon = 59
    src_class.ez_slash = 47
    src_class.ez_space = 32
    src_class.ez_sysreq = 317
    src_class.ez_tab = 9
    src_class.ez_underscore = 95
    src_class.ez_unknown = 0
    src_class.ez_up = 273
    src_class.ez_a = 97
    src_class.ez_b = 98
    src_class.ez_c = 99
    src_class.ez_d = 100
    src_class.ez_e = 101
    src_class.ez_f = 102
    src_class.ez_g = 103
    src_class.ez_h = 104
    src_class.ez_i = 105
    src_class.ez_j = 106
    src_class.ez_k = 107
    src_class.ez_l = 108
    src_class.ez_m = 109
    src_class.ez_n = 110
    src_class.ez_o = 111
    src_class.ez_p = 112
    src_class.ez_q = 113
    src_class.ez_r = 114
    src_class.ez_s = 115
    src_class.ez_t = 116
    src_class.ez_u = 117
    src_class.ez_v = 118
    src_class.ez_w = 119
    src_class.ez_x = 120
    src_class.ez_y = 121
    src_class.ez_z = 122
    src_class.ez_keysReady = True
