import sys


if __name__ == "__main__":
    if "--demo" in sys.argv:
        from model.main import demo
        demo()
    elif "--terminal" in sys.argv:
        from model.main import main
        main()
    else:
        # Běžné spuštění otevře okno. Terminál a demo zůstávají dostupné.
        from gui import main
        main()
