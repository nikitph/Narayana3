from flask import Blueprint, request, session, redirect, url_for, flash, g
from flask.ext.security import login_required, logout_user, login_user, current_user
from flask.templating import render_template
from models import User
from public.models import Thought

bp_user = Blueprint('users',__name__,static_folder='../static')


@bp_user.before_request
def before_request():
    g.user = current_user


@bp_user.route('/')
def index():
    return render_template('index.html')

@bp_user.route('/about/')
def about():
    return render_template('about.html')

@bp_user.route('/hiw')
def hiw():
    return render_template('hiw.html')

@bp_user.route('/disclaimer')
def disclaimer():
    return render_template('dis.html')

@bp_user.route('/account/')
@login_required
def account():
    return render_template('account.html')

@bp_user.route('/record', methods=['GET'])
@login_required
def record_get():
    distortions = {'All or nothing - thinking', 'Overgeneralization', 'Mental filter', 'Discounting the positive', 'Jumping to conclusions',
                   'Magnification', 'Emotional reasoning', 'Should statements', 'Labeling', 'Personalization and blame'}
    return render_template('record.html', dist=distortions)

@bp_user.route('/record', methods=['POST'])
@login_required
def record_post():
    data = request.form
    thoughts = data['thoughts']
    usr = g.user.get_id()
    level = data['level']
    distr = data['dist']
    rtn = data['rational']
    thgt = Thought(dys_thought=thoughts, user=usr, distress=int(level), distortion=distr, rational=rtn).save()
    return render_template('confirm.html')

@bp_user.route('/access', methods=['GET'])
@login_required
def access_get():
    custsubs = Thought.objects(user=g.user.get_id())
    return render_template('accessresults.html', thoughts=custsubs.to_json())
