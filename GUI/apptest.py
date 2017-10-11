import npyscreen

db_name = None


class dbpageform(npyscreen.Form):
    def afterEditing(self):
        if self.options.value=="Edit":
            self.parentApp.setNextForm('flowedit')
        else:
            self.parentApp.setNextForm(None)


    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, name='Select Action', values = ['Add', 'Edit', 'Delete','Execute'])


class flowform(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
       self.options = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=4, name='Select Action', values = ['Add', 'Edit', 'Delete','Execute'])

class loadpageform(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm('db')

    def create(self):
        global db_name
        self.fn = self.add(npyscreen.TitleFilenameCombo, name = "Load Database:")
        db_name = self.fn.value


class MyApplication(npyscreen.NPSAppManaged):
   def onStart(self):
       self.addForm('MAIN', loadpageform, name='rMinusDB')
       self.addForm('db',dbpageform,name='Database')
       self.flowForm('flowedit',floweform,name='Flow Editor')
       # A real application might define more forms here.......

if __name__ == '__main__':
   TestApp = MyApplication().run()
