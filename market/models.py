from market import db, bcrypt, login_manager

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_adress = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    

    # Mejora la forma en como despliega el presupuesto en la pantalla con valores altos
    @property
    def prettier_budget(self):
        ''' Improves the way we can see high values on the screen '''
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]}.{str(self.budget)[-3:]}$'
        else:
            return f'{self.budget}$'
    
    
    @property
    def password(self):
        return self.password

    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def verify_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    
    def can_purchase(self, ram_obj):
        ''' Returns True or False if the current user can buy this ram or not '''
        return self.budget >= ram_obj.price


    def __repr__(self):
        return f'User id:{self.id} is:{self.name}'


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1042))
    owner = db.Column(db.Integer(), db.ForeignKey('users.id'))
    

    def buy(self, user):
        ''' Method that allows us to buy a ram '''
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
    

    def __repr__(self):
        return f'Item id:{self.id} nombre:{self.name}'
    