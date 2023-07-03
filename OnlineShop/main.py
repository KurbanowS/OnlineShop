from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///onlineshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

if __name__ == "__main__":
    app.run(debug=True)


class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False )
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False )
    isActive = db.Column(db.Boolean, default=True )

    def __repr__(self):
        return self.name


@app.route('/')
def home_page():
    stuffs = Stuff.query.order_by(Stuff.price).all()
    return render_template('home_page.html', data=stuffs)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':    
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        stuff = Stuff(name=name, price=price, description=description)

        try:
            db.session.add(stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "Возникла ошибка"

    return render_template('add.html')

@app.route('/<int:id>/delete')
def stuff_delete(id):
    stuff = Stuff.query.get_or_404(id)

    try:
        db.session.delete(stuff)
        db.session.commit()
        return redirect('/')
    except:
        return 'При покупке товара произошла ошибка'