import tkinter as tk
from game2048.ui import GameUI

def main():
    root = tk.Tk()
    game = GameUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
