from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, checkout


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # Создаем объект DB на основе класса SQLAlchemy, внутри объекта app


class Item(db.Model):  # создаем класс Item,   Создаем запись в БД при помощи метода Model
    id = db.Column(db.Integer, primary_key=True) # добавляем колонки в БД db, 
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True) # default - значение записи по умолчанию
    #text = title = db.Collumn(db.Text)
    
    def __repr__(self):
        return self.title
    

@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    # с помощью render template выводим файл
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    # с помощью render template выводим файл
    return render_template('about.html')


@app.route('/create', methods =["POST", "GET"])
def create():
    if request.method=='POST': # Если данные получены методом POST, значит они получены из формы и записываем их в БД
        title= request.form['title']
        price= request.form['price']   
        
        item = Item(title=title, price=price)
        
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')         
        except:
            return 'Ошибка ввода'
    else:
        
    # с помощью render template выводим файл
         return render_template('create.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    # с помощью render template выводим файл
    item= Item.query.get(id)
    
    from cloudipsp import Api, Checkout
    api = Api(merchant_id=1396424,
          secret_key='test')
    checkout = Checkout(api=api)
    data = {
    "currency": "USD",
    "amount": str(item.price)+'00'
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)




if __name__ == '__main__':

    app.run(debug=True)
