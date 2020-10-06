import sys, os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(MODEL_DIR)
sys.path.append(SRC_DIR)


if __name__ == "__main__":
    import inspect, os.path

    filename = inspect.getframeinfo(inspect.currentframe()).filename
    path = os.path.dirname(os.path.abspath(filename))
    args = sys.argv
    print(args)
    print('cmdline use not supported yet, and json server is disabled for this release')
