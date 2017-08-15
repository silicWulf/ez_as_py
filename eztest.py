import ez_as_py
import pygame


class ControlThread:
    def __init__(self):
        pass

    def main(self):
        ez_as_py.init(self)
        self.sloc = (100, 100)
        self.sid_orig = self.window.addObject('hmm.png', self.sloc)
        currentFrame = self.window.onFrame()
        while currentFrame != -1:
            currentFrame = self.window.onFrame()
            self.mainLoop(currentFrame)

    def mainLoop(self, currentFrame):

        if self.window.getObject(self.sid_orig):
            self.window.changeID(self.sid_orig, 'newIDlol')
            self.sid = 'newIDlol'
        if self.sid is not None:
            pos = self.window.getObject(self.sid)[1]
            x = pos[0]
            y = pos[1]

            speed = 6

            keys = self.window.getKeys()

            str_fps = str(self.window.getFPS())
            self.window.changeWindowName(str_fps)

            try:
                if self.ez_keysReady:
                    if keys[self.ez_w]:
                        self.window.moveObject(self.sid, (x, y - speed))
                    if keys[self.ez_s]:
                        self.window.moveObject(self.sid, (x, y + speed))
                    if keys[self.ez_a]:
                        self.window.moveObject(self.sid, (x - speed, y))
                    if keys[self.ez_d]:
                        self.window.moveObject(self.sid, (x + speed, y))
            except TypeError:
                pass
            except NameError:
                pass

    def _getTypeName(self, var):
        t = str(type(var))
        t = t.split('\'')[1]
        t = t.split('\'')[0]
        return t


if __name__ == '__main__':
    c = ez_as_py.startControlThread(ControlThread)
    ez_as_py.Window((500, 500), 30, c)
