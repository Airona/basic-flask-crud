
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///xubuntu'
#app.config['SECRET_KEY'] = ''

def sql(rawSql, sqlVars={}):
 "Execute raw sql, optionally with prepared query"
 assert type(rawSql)==str
 assert type(sqlVars)==dict
 res=db.session.execute(rawSql, sqlVars)
 db.session.commit()
 return res

@app.before_first_request
def initDBforFlask():
 sql("CREATE TABLE IF NOT EXISTS programs (id SERIAL PRIMARY KEY, name VARCHAR(200) UNIQUE);")
 sql("INSERT INTO programs(name) VALUES ('Flask') ON CONFLICT (name) DO NOTHING;")
 sql("INSERT INTO programs(name) VALUES ('Apache') ON CONFLICT (name) DO NOTHING;")
 sql("INSERT INTO programs(name) VALUES ('Python3') ON CONFLICT (name) DO NOTHING;")
 sql("INSERT INTO programs(name) VALUES ('PostgreSQL') ON CONFLICT (name) DO NOTHING;")

class Program (db.Model):
 __tablename__ = 'programs'
 id = db.Column(db.Integer, primary_key=True)
 name = db.Column(db.String(200))

@app.route("/")
def hello():
 return render_template("index.html")

@app.route("/programs")
def programs():
 programs=sql("SELECT * FROM programs;")
 return render_template("programs.html", programs=programs)

@app.route("/programs/add", methods = ["GET", "POST"])
def add():
 if request.method == "GET":
  return render_template("add_program.html")
 else:
  name = request.form["name"]
  program=Program(name=name)
  db.session.add(program)
 try:
  db.session.commit()
  return render_template("add_program.html", alert="Succesfull Create!")
 except:
  pass
  return render_template("add_program.html", alert="Error while creating new program!")

@app.route("/programs/delete/<id>")
def delete(id):
 try:
  id = int(id)
  Program.query.filter_by(id=id).delete()
  db.session.commit()
 except:
  pass
 return redirect("/programs")

@app.route("/programs/update/<id>", methods = ["GET", "POST"])
def update(id):
 id = int(id)
 program = Program.query.filter_by(id=id).first()
 if request.method == "GET":
  return render_template("update_program.html", program=program)
 else:
  name = request.form["name"]
  try:
   program.name = name
   db.session.commit()
  except:
   pass
  return redirect("/programs")


#debugging testserver python3
if __name__ == "__main__":
 from flask_sqlalchemy import get_debug_queries
 app.run(debug=True)
