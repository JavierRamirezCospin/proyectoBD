# Main class definition and init



import psycopg2
from tkinter import *

class Notification(Toplevel):

    def __init__(self, message, title='Notification', w=165, h=150, but_text='Ok'):
        Toplevel.__init__(self)
        self.title(title)
        self.title_name = title
        
        x = self.winfo_screenheight() / 2
        y = self.winfo_screenheight() / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x - (w / 2), y - (h / 2)))
        self.label = Label(self, text=message, wraplength=w - (w * 0.1), justify='center')
        self.label.grid(row=0, columnspan=10, sticky=W + E + S + N)
        self.button = Button(self, text=but_text, command=self.destroy, width=7)
        self.button.grid(row=10, sticky=W + E, padx=5, pady=5)

class App:

    def __init__(self, master, screenx, screeny, con=None):
        self.root = master
        self.scy = screeny
        self.scx = screenx

        #   db connection
        self.con = con

        #   frames
        self.topFrame = Frame(self.root, height=10, bd=2)
        self.topFrame.grid(row=0)
        self.loginFrame = Frame(self.root)
        self.loginFrame.grid(row=1)
        self.mainFrame = Frame(self.root)
        self.adminFrame = Frame(self.root)


        #   login vars and butts
        self.loginUsernameEntryVar = StringVar()
        self.loginPasswordEntryVar = StringVar()

        self.loginButton = Button(self.loginFrame, text='Login',)
        self.loginButton.grid(row=0, pady=2)

        self.signUpButton = Button(self.loginFrame, text='Sign Up',)
        self.signUpButton.grid(row=1, pady=2)
        self.notifButton = Button(self.loginFrame, text='Notification', )
        self.notifButton.grid(row=2, pady=2)

        self.showLoginButton = Button(self.topFrame, text='Show Login', command=self.showLogin)
        self.showLoginButton.grid(padx=3, row=0, column=0)
        self.hideLoginButton = Button(self.topFrame, text='Hide Login', command=self.hideLogin)
        self.hideLoginButton.grid(padx=3, row=0, column=1)

    def hideLogin(self):
        self.loginFrame.grid_remove()

    def showLogin(self):
        self.loginFrame.grid()

    def login(self):
        pass
    
    def logout(self):
        pass
    
    def signup(self):
        pass

    def notification(self, message):
        print('Notifying: ', message)
        n = Notification(message)
        print('Done')



if __name__ == '__main__':
    root = Tk()
    con = ''
    # con = psycopg2.connect(
    #     host = "127.0.0.1",
    #     database = "basesdb",
    #     user = "postgres",
    #     password = "7654321.",
    #     port = 5432
    # )

    root.title('CloudSound')
    root.minsize(485, 590)  # for now.
    
    x = (root.winfo_screenwidth() / 2) - (430 / 2)
    y = (root.winfo_screenheight()/ 2) - (555 / 2)
    # root.geometry('%dx%d+%d+%d' % (450, 575, x, y))
    
    app = App(root, root.winfo_screenwidth(), root.winfo_screenheight(), con)
    # app.killswitch()
    # root.config(menu=app.menubar)
    mainloop()


