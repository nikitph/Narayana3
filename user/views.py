from datetime import datetime
from flask import Blueprint, request, session, redirect, url_for, flash, g
from flask.ext.security import login_required, logout_user, login_user, current_user
from flask.templating import render_template
from models import User
from public.models import Thought, Dcheck

bp_user = Blueprint('users', __name__, static_folder='../static')


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
    distortions = {'All or nothing - thinking', 'Overgeneralization', 'Mental filter', 'Discounting the positive',
                   'Jumping to conclusions',
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
    thgt = Thought(dys_thought=thoughts, user=usr, distress=int(level), distortion=distr, rational=rtn,
                   timestamp=str(datetime.now())).save()
    return render_template('confirm.html')


@bp_user.route('/access', methods=['GET'])
@login_required
def access_get():
    custsubs = Thought.objects(user=g.user.get_id())
    return render_template('accessresults.html', thoughts=custsubs.to_json())


@bp_user.route('/dcl', methods=['GET'])
@login_required
def dcl_get():
    questns = {'Feeling sad or down in the dumps',
               'Feeling unhappy or blue',
               'Crying spells or tearfulness',
               'Feeling discouraged',
               'Feeling hopeless',
               'Low self-esteem',
               'Feeling worthless or inadequate',
               'Guilt or shame',
               'Criticizing yourself or blaming others',
               'Difficulty making decisions',
               'Loss of interest in family, friends or colleagues',
               'Loneliness',
               'Spending less time with family or friends',
               'Loss of motivation',
               'Loss of interest in work or other activities',
               'Avoiding work or other activities',
               'Loss of pleasure or satisfaction in life',
               'Feeling tired',
               'Difficulty sleeping or sleeping too much',
               'Decreased or increased appetite',
               'Loss of interest in sex',
               'Worrying about your health',
               'Do you have any suicidal thoughts?',
               'Would you like to end your life?',
               'Do you have a plan for harming yourself?'}
    return render_template('dcl.html', questions=questns)


@bp_user.route('/dcl', methods=['POST'])
@login_required
def dcl_post():
    val = 0
    for d in request.form:
        val += int(request.form[d])
    usr = g.user.get_id()
    dc = Dcheck(user=usr, score=val,
                timestamp=str(datetime.now())).save()
    return render_template('dclresults.html', score=val)


@bp_user.route('/changei', methods=['GET'])
@login_required
def changei_get():
    kmap = {'Death of a spouse': 100,
            'Divorce': 73,
            'Marital separation': 65,
            'Imprisonment': 63,
            'Death of a close family member': 63,
            'Personal injury or illness': 53,
            'Marriage': 50,
            'Dismissal from work': 47,
            'Marital reconciliation': 45,
            'Retirement': 45,
            'Change in health of family member': 44,
            'Pregnancy': 40,
            'Sexual difficulties': 39,
            'Gain a new family member': 39,
            'Business readjustment': 39,
            'Change in financial state': 38,
            'Death of a close friend': 37,
            'Change to different line of work': 36,
            'Change in frequency of arguments': 35,
            'Major mortgage': 32,
            'Foreclosure of mortgage or loan': 30,
            'Change in responsibilities at work': 29,
            'Child leaving home': 29,
            'Trouble with in-laws': 29,
            'Outstanding personal achievement': 28,
            'Spouse starts or stops work': 26,
            'Beginning or end school': 26,
            'Change in living conditions': 25,
            'Revision of personal habits': 24,
            'Trouble with boss': 23,
            'Change in working hours or conditions': 20,
            'Change in residence': 20,
            'Change in schools': 20,
            'Change in recreation': 19,
            'Change in church activities': 19,
            'Change in social activities': 18,
            'Minor mortgage or loan': 17,
            'Change in sleeping habits': 16,
            'Change in number of family reunions': 15,
            'Change in eating habits': 15,
            'Vacation': 13,
            'Major Holiday': 12,
            'Minor violation of law': 11}
    return render_template('changei.html', keym=kmap)


@bp_user.route('/changei', methods=['POST'])
@login_required
def changei_post():
    val = 0
    for d in request.form:
        val += int(request.form[d])
    usr = g.user.get_id()
    return render_template('changeiresults.html', score=val)


@bp_user.route('/changeina', methods=['GET'])
@login_required
def changeina_get():
    kmap = {'Death of parent': 100,
            'Unplanned pregnancy/abortion': 100,
            'Getting married': 95,
            'Divorce of parents': 90,
            'Acquiring a visible deformity': 80,
            'Fathering a child': 70,
            'Jail sentence of parent for over one year': 70,
            'Marital separation of parents': 69,
            'Death of a brother or sister': 68,
            'Change in acceptance by peers': 67,
            'Unplanned pregnancy of sister': 64,
            'Discovery of being an adopted child': 63,
            'Marriage of parent to stepparent': 63,
            'Death of a close friend': 63,
            'Having a visible congenital deformity': 62,
            'Serious illness requiring hospitalization': 58,
            'Failure of a grade in school': 56,
            'Not making an extracurricular activity': 55,
            'Hospitalization of a parent': 55,
            'Jail sentence of parent for over 30 days': 53,
            'Breaking up with boyfriend or girlfriend': 53,
            'Beginning to date': 51,
            'Suspension from school': 50,
            'Becoming involved with drugs or alcohol': 50,
            'Birth of a brother or sister': 50,
            'Increase in arguments between parents': 47,
            'Loss of job by parent': 46,
            'Outstanding personal achievement': 46,
            'Change in parents financial status': 45,
            'Accepted at college of choice': 43,
            'Being a senior in high school': 42,
            'Hospitalization of a sibling': 41,
            'Increased absence of parent from home': 38,
            'Brother or sister leaving home': 37,
            'Addition of third adult to family': 34,
            'Becoming a full fledged member of a church': 31,
            'Decrease in arguments between parents': 27,
            'Decrease in arguments with parents': 26,
            'Mother or father beginning work': 26}
    return render_template('changei.html', keym=kmap)
