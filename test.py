import tkinter

root = tkinter.Tk()
root.eval('tk::PlaceWindow . center')

second_win = tkinter.Toplevel(root)
root.eval(f'tk::PlaceWindow {str(second_win)} center')

root.mainloop()