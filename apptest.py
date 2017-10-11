import curses
import npyscreen
import sqlite3


db_name = None


class dbpageform(npyscreen.Form):
    def afterEditing(self):
        # with open('k.txt','w') as f:
        #     f.write(" ".join(str(x) for x in self.options.value))
        self.parentApp.setNextForm('db2')
        self.parentApp.mode = self.options.value[0]


    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, name='Select Action', values = ['Add', 'Edit', 'Delete','Execute'])


class dbpage2form(npyscreen.Form):
    def afterEditing(self):
        # with open('k.txt','w') as f:
        #     f.write(" ".join(str(x) for x in self.options.value))
        if self.options.value[0]==0:
            self.parentApp.setNextForm('flowform')
        else:
            self.parentApp.setNextForm(None)


    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, name='Select Action', values = ['Flows', 'Pages'])


class flowform(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('db')
        with open('k.txt','w') as f:
             #f.write(" ".join(str(x) for x in self.grid.edit_cell))
             f.write(self.grid.cell_display_value)

    def create(self):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("SELECT DISTINCT FLOW from flowdata")
        rows = cur.fetchall()
        lista =[]
        for r in range(len(rows)):
            lista.append(rows[r][0])
        # with open('k.txt','w') as f:
        #     f.write(rows[0][0])

        self.grid = self.add(npyscreen.SimpleGrid)
        self.grid.set_grid_values_from_flat_list(lista, max_cols=1, reset_cursor=False)
        self.grid.add_handlers({curses.ascii.NL:self.h_exit_down})

    def _test_safe_to_exit(self):
        self.parentApp.switchForm('db')
        #self.parentApp.search = ""






class loadpageform(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('db')

    def create(self):
        global db_name
        self.fn = self.add(npyscreen.TitleFilenameCombo, name = "Load Database:")
        db_name = self.fn.value


class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.mode = None
       self.addForm('MAIN', loadpageform, name='rMinusDB')
       self.addForm('db',dbpageform,name='Database')
       self.addForm('db2',dbpage2form,name='Page/Flow')
       self.addForm('flowform',flowform,name='Flow Selector')

       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = MyApplication().run()
