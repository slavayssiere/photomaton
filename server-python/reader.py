import rethinkdb as r

# Database init
r.connect( "localhost", 28015).repl()

cursor = r.table("states").changes().run()
for document in cursor:
    print(document)

print('end')
