import sys
class ModelInitializationException(Exception):
    def __init__(self, reason):
        self.reason = reason
        super().__init__(f"Model initialization failed: {reason}")



def exception_handler(exctype, value, traceback):
    if exctype == ModelInitializationException:
        print(f"Model initialization failed: {value.reason}")
        sys.exit(1)
    else:
        sys.__excepthook__(exctype, value, traceback)


sys.excepthook = exception_handler