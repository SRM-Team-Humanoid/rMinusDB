import curses
import npyscreen
import sqlite3


db_name = None
flow_name = ""
page_ID = ""

class dbpageform(npyscreen.Form):
    def afterEditing(self):
        # with open('k.txt','w') as f:
        #     f.write(" ".join(str(x) for x in self.options.value))
        self.parentApp.setNextForm('db2')
        self.parentApp.mode = self.options.value[0]
        if self.options.value[0]==4:
            exit()


    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=5, name='Select Action', values = ['Add', 'Edit', 'Delete','Execute','Exit'])


class dbpage2form(npyscreen.Form):
    def afterEditing(self):
        # with open('k.txt','w') as f:
        #     f.write(" ".join(str(x) for x in self.options.value))
        if self.options.value[0]==0 and self.parentApp.mode==0:
            self.parentApp.setNextForm('flowadder')
        elif self.options.value[0]==0 and self.parentApp.mode==1:
            self.parentApp.setNextForm('flowform')
        elif self.options.value[0]==0 and self.parentApp.mode==2:
            self.parentApp.setNextForm('flowform')
        else:
            self.parentApp.setNextForm(None)


    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, name='Select Action', values = ['Flows', 'Pages'])


class flowform(npyscreen.Form):
    def afterEditing(self):
        global flow_name
        self.parentApp.setNextForm('flowpageid')
        flow_name = str(self.lista[self.grid.edit_cell[0]])

    def getRows(self):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("SELECT DISTINCT FLOW from flowdata")
        rows = cur.fetchall()
        self.lista =[]
        for r in range(len(rows)):
            self.lista.append(rows[r][0])

    def beforeEditing(self):
        if flow_name!="":
            self.getRows()
            self.grid.set_grid_values_from_flat_list(self.lista, max_cols=1, reset_cursor=False)
        self.display()


    def create(self):
        self.getRows()
        # with open('k.txt','w') as f:
        #     f.write(rows[0][0])

        self.grid = self.add(npyscreen.SimpleGrid)
        self.grid.set_grid_values_from_flat_list(self.lista, max_cols=1, reset_cursor=False)
        self.grid.add_handlers({curses.ascii.NL:self.h_exit_down})

    def _test_safe_to_exit(self):
        self.parentApp.switchForm('flowpageid')
        #self.parentApp.search = ""

class flowpageid(npyscreen.Form):
    def afterEditing(self):
        global page_ID
        self.parentApp.setNextForm('floweditor')
        page_ID = str(self.lista[self.grid.edit_cell[0]])

    def getRows(self):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("SELECT PageID from flowdata where Flow = \'"+flow_name+"\'")
        rows = cur.fetchall()
        self.lista =[]
        for r in range(len(rows)):
            self.lista.append(rows[r][0])

    def beforeEditing(self):
        if flow_name!="":
            self.getRows()
            self.grid.set_grid_values_from_flat_list(self.lista, max_cols=1, reset_cursor=False)
        self.display()

    def create(self):

        # with open('k.txt','w') as f:
        #     f.write(rows[0][0])

        self.grid = self.add(npyscreen.SimpleGrid)
        self.grid.add_handlers({curses.ascii.NL:self.h_exit_down})

    def _test_safe_to_exit(self):
        self.parentApp.switchForm('db')
        #self.parentApp.search = ""


class floweditor(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('db')

    def getRows(self):
        con = sqlite3.connect("test.db")
        cur = con.cursor()
        cur.execute("SELECT PageName,Speed from flowdata where Flow = \'"+flow_name+"\' and PageID = \'"+page_ID+"\'")
        rows = cur.fetchall()
        self.lista = [str(rows[0][0]),str(rows[0][1])]
        # with open('k.txt','w') as f:
        #      f.write(str(len(rows[0])))

    def beforeEditing(self):
        if page_ID!="":
            self.getRows()
            self.pagename.value = self.lista[0]
            self.speed.value = self.lista[1]
        self.display()

    def create(self):

        # with open('k.txt','w') as f:
        #     f.write(rows[0][0])

        self.pagename = self.add(npyscreen.TitleText, name = "PageName:",)
        self.speed = self.add(npyscreen.TitleText, name = "Speed:",)




class flowadder(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('db')

    def beforeEditing(self):
        if page_ID!="":
            self.flow.value = ""
            self.pageid.value = ""
            self.pagename.value = ""
            self.speed.value = ""
        self.display()

    def create(self):

        # with open('k.txt','w') as f:
        #     f.write(rows[0][0])
        self.flow = self.add(npyscreen.TitleText, name = "Flow Name:",)
        self.pageid = self.add(npyscreen.TitleText, name = "Page Id:",)
        self.pagename = self.add(npyscreen.TitleText, name = "PageName:",)
        self.speed = self.add(npyscreen.TitleText, name = "Speed:",)







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
       self.addForm('flowpageid',flowpageid,name='Page Selector')
       self.addForm('floweditor',floweditor,name='Flow Editor')
       self.addForm('flowadder',flowadder,name='Flow Adder')


       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = MyApplication().run()
