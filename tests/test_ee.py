import unittest

from utilities.event_emitter import EventEmitter


class TestEventEmitter(unittest.TestCase):
    def setUp(self):
        self.emitter = EventEmitter()

    def test_call_on(self):
        called = False

        def test():
            nonlocal called
            called = True

        self.emitter.on("test", test)

        self.emitter.emit("test")

        self.assertTrue(called)

    def test_call_once(self):
        called = 0

        def test():
            nonlocal called
            called += 1

        self.emitter.once("test", test)

        self.emitter.emit("test")
        self.emitter.emit("test")

        self.assertEqual(called, 1)


if __name__ == '__main__':
    unittest.main()