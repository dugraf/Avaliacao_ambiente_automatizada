from views.gui import AvaliacaoGUI
from multiprocessing import freeze_support

if __name__ == '__main__':
    freeze_support()
    app = AvaliacaoGUI()
    app.run()