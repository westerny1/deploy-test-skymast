from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from mastodon import Mastodon
from datetime import datetime
from atproto import Client
import os

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skymast.db'
db = SQLAlchemy(app)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_email = db.Column(db.String(200), nullable=False)
    db_password = db.Column(db.String(200), nullable=False)
    db_website = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Account %r>' % self.id

with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        post_text = request.form['post-text']
        email = request.form['email']
        password = request.form['password']
        post_to = request.form['post-to']

        
        if post_text != "" and post_to == "mastodon":
            for account in Accounts.query.all():
                if account.db_website == 'mastodon':
                    try:
                        # create an application
                        Mastodon.create_app(
                            'skymast',
                            api_base_url = 'https://mastodon.social',
                            to_file = 'pytooter_clientcred.secret'
                        )
                        print('created application in mastodon')

                        # login
                        mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
                        mastodon.log_in(
                            account.db_email, 
                            account.db_password, 
                            to_file = 'pytooter_usercred.secret'
                        )
                        print('logged-in in mastodon')

                        # posting
                        mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
                        mastodon.toot(post_text)
                        print('posted text in mastodon')

                    except:
                        return 'There was an issue in posting in mastodon'
                else:
                    pass
            print('Done posting in mastodon')
            return redirect('/')
        
        elif post_text != "" and post_to == "bluesky":
            for account in Accounts.query.all():
                if account.db_website == 'bluesky':
                    try:
                        # creating session
                        client = Client(base_url='https://bsky.social')
                        client.login(account.db_email, account.db_password)
                        print('created session in bluesky')

                        # posting 
                        post = client.send_post(post_text)
                    except:
                        return 'There was an issue in posting in bluesky'
                else:
                    pass
            print('Done posting in bluesky')
            return redirect('/')
        
        elif post_text != "" and post_to == 'both':
            for account in Accounts.query.all():
                if account.db_website == 'mastodon':
                    try:
                        # create an application
                        Mastodon.create_app(
                            'skymast',
                            api_base_url = 'https://mastodon.social',
                            to_file = 'pytooter_clientcred.secret'
                        )
                        print('created application in mastodon')

                        # login
                        mastodon = Mastodon(client_id = 'pytooter_clientcred.secret',)
                        mastodon.log_in(
                            account.db_email, 
                            account.db_password, 
                            to_file = 'pytooter_usercred.secret'
                        )
                        print('logged-in in mastodon')

                        # posting
                        mastodon = Mastodon(access_token = 'pytooter_usercred.secret')
                        mastodon.toot(post_text)
                        print('posted text in mastodon')

                    except:
                        return 'There was an issue in posting in mastodon'
                elif account.db_website == 'bluesky':
                    try:
                        # creating session
                        client = Client(base_url='https://bsky.social')
                        client.login(account.db_email, account.db_password)
                        print('created session in bluesky')

                        # posting 
                        post = client.send_post(post_text)
                        print('posted text in bluesky')
                    except:
                        return 'There was an issue in posting in bluesky'
                else:
                    pass
            print('Done posting in both mastodon and bluesky')
            return redirect('/')

        
        # add mastodon account  
        elif "mastodon_login" in request.form and email != '' and password != '':
            print("mastodon login")
            account = Accounts(db_email = email, db_password = password, db_website = "mastodon")
            db.session.add(account)
            db.session.commit()
            return redirect('/')
        
        # add bluesky account
        elif "bluesky_login" in request.form and email != '' and password != '':
            print("bluesky login")
            account = Accounts(db_email = email, db_password = password, db_website = "bluesky")
            db.session.add(account)
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/')
    
    else:
        account_list = Accounts.query.order_by(Accounts.date_created).all()
        return render_template("index.html", account_list = account_list)

if __name__ == "__main__":
    app.run(debug=True)

