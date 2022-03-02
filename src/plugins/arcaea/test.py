
import time


def test():
    def on_start(app):
        print('Starting...')

    def on_receive(app):
        print('Receiving...')

    def on_error(app, e):
        print('Error on' + str(app) + ':')
        print(e)

    def on_stop(app, result):
        print('Stop')
        print(result)
        breakpoint()

    app = arc.Application('750248806',
                          on_start=on_start,
                          on_receive=on_receive,
                          on_error=on_error,
                          on_stop=on_stop)

    app.start()
    while not app.stop_flag:
        print(time.localtime(time.time()))
        time.sleep(3)
    print('MainThread stop')
    breakpoint()


if __name__ == '__main__':
    test()
