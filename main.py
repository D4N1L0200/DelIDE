from core.ide import IDE
from core.signal_manager import SignalManager

if __name__ == "__main__":
    SignalManager.register_signals()
    ide: IDE = IDE()
    ide.run()
