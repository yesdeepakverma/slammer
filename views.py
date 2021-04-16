import flask
from flask import request
from flask.views import MethodView

from slammer import Slammer
from flask import render_template, redirect
import uuid
import json

slm = Slammer()


class Login(MethodView):
    section = "login"

    def get(self):
        return render_template('slam.html', section=self.section)

    def post(self):
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            return render_template('slam.html', message="Pass the username and password", section="login")
        user = slm.get_user(username)

        if not user:
            return render_template('slam.html', message="User not found", section=self.section)
        else:
            _password = user.pop('password', None)
            if _password and _password == password:
                login_key = slm.update_login_key(username)
                return redirect("/dashboard?login_key="+login_key)
            else:
                return render_template('slam.html', message="Invalid password", section=self.section)


class Register(MethodView):
    def get(self):
        return render_template('slam.html', section="register")

    def post(self):
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        password = request.form['password']
        username = request.form['username']
        if not (username and password and firstname and lastname):
            return render_template('slam.html', message="Pass the all the fields", section="register")
        user = slm.add_user(username, {"password": password, "firstname": firstname, "lastname": lastname})
        if not user:
            return render_template('slam.html', message="User Already Exists", section="register")
        else:
            login_key = slm.update_login_key(username)
            return redirect("/dashboard?login_key="+login_key)


class Dashboard(MethodView):
    def get(self):
        login_key = request.args.get('login_key')
        user = slm.get_user_by_key(login_key)
        if not user:
            return redirect("/login")
        username = user['username']
        message = request.args.get('message', '')
        users = slm.list_user(username)

        notes = slm.list_notes(username)
        context = dict(section="dashboard", login_key=login_key, user=user, users=users, message=message, notes=notes)
        return render_template('slam.html', **context)


class AddSlam(MethodView):
    def post(self):
        to_slam = request.form['to_slam']
        login_key = request.form['login_key']
        from_user = slm.get_user_by_key(login_key)
        note = request.form['note']
        _note = slm.add_notes(to_slam, from_user, note)
        return redirect(f"/dashboard?login_key={login_key}&message=Note with message <small>'{note}'</small> sent")

    def get(self):
        return redirect('/login')


class ListSlam(MethodView):
    def get(self):
        to_slam = request.form['to_slam']
        login_key = request.form['login_key']
        from_user = slm.get_user_by_key(login_key)
        note = request.form['note']
        _note = slm.add_notes(to_slam, from_user, note)
        return redirect(f"/dashboard?login_key={login_key}&message=Note with message <small>'{note}'</small> sent")
