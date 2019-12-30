from flask import Flask, render_template, url_for, redirect, request, session
from f5.bigip import ManagementRoot
app = Flask(__name__)
app.secret_key = 'loginner'
users = {
    'konsolidasi' : 'konsolidasi123',
    'foo'   : 'myfoo',
}

@app.route('/', methods=['GET','POST'])
def login():
    session['logged_in'] = False
    username = request.form.get('username')
    password = request.form.get('password')
    partition = request.form.get('partition')
    wideip = request.form.get('wideip')
    ip = request.form.get('ip')
    if username and password and username in users and users[username] == password:
        session['logged_in'] = True
        session['user'] = username
        session['pass'] = password
        session['part'] = partition
        session['wideip'] = wideip
        session['ip'] = ip
        return redirect(url_for('account'))
    return render_template('D:/login.html')

@app.route("/account")
def account():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    x = str(session.get('user', None))
    y = str(session.get('pass', None))
    z = str(session.get('part', None))
    w = str(session.get('wideip', None))
    v = str(session.get('ip',None))
    mgmt = ManagementRoot(v, x, y)
    pool = mgmt.tm.gtm.wideips.a_s.a.load(partition=z, name=w)
    a=pool.name
    b=pool.persistence
    c=pool.pools[0].get('ratio')
    d=pool.pools[1].get('ratio')
    return render_template('D:/akun.html', variable=a, variable1=b, variable2=c, variable3=d)

@app.route('/join')
def my_form_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    x = str(session.get('user', None))
    y = str(session.get('pass', None))
    z = str(session.get('part', None))
    w = str(session.get('wideip', None))
    v = str(session.get('ip',None))
    mgmt = ManagementRoot(v, x, y)
    pool = mgmt.tm.gtm.wideips.a_s.a.load(partition=z, name=w)
    c=pool.pools[0].get('ratio')
    d=pool.pools[1].get('ratio')
    b=pool.persistence
    if b == 'enabled':
        e = pool.ttlPersistence
        f = pool.persistCidrIpv4
        return render_template('D:/join1.html', variable4=e, variable5=f, variable6=c, variable7=d, variable8=b)
    if b == 'disabled':
        return render_template('D:/join.html', variable6=c, variable7=d)

@app.route('/pos', methods=['GET','POST'])
def my_form():
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    do_something(text1,text2,text3)
    return redirect(url_for('account'))

@app.route('/pos1', methods=['GET','POST'])
def my_form1():
    text1 = request.form['text1']
    text2 = request.form['text2']
    text3 = request.form['text3']
    text4 = request.form['text4']
    text5 = request.form['text5']
    do_something1(text1,text2,text3,text4,text5)
    return redirect(url_for('account'))

def do_something(text1,text2,text3):
    x = str(session.get('user', None))
    y = str(session.get('pass', None))
    z = str(session.get('part', None))
    w = str(session.get('wideip', None))
    v = str(session.get('ip',None))
    text1 = int(text1)
    text2 = int(text2)
    text3 = str(text3)
    mgmt = ManagementRoot(v, x, y)
    pool = mgmt.tm.gtm.wideips.a_s.a.load(partition=z, name=w)
    pool.pools[0].update({'ratio': text1})
    pool.pools[1].update({'ratio': text2})
    pool.persistence = text3
    pool.update()
    return redirect(url_for('account'))

def do_something1(text1,text2,text3,text4,text5):
    x = str(session.get('user', None))
    y = str(session.get('pass', None))
    z = str(session.get('part', None))
    w = str(session.get('wideip', None))
    v = str(session.get('ip',None))
    text1 = int(text1)
    text2 = int(text2)
    text3 = str(text3)
    text4 = int(text4)
    text5 = int(text5)
    mgmt = ManagementRoot(v, x, y)
    pool = mgmt.tm.gtm.wideips.a_s.a.load(partition=z, name=w)
    pool.pools[0].update({'ratio': text1})
    pool.pools[1].update({'ratio': text2})
    pool.persistence = text3
    if pool.persistence == 'enabled':
        pool.ttlPersistence = text4
        pool.persistCidrIpv4 = text5
    pool.update()
    return redirect(url_for('account'))



if __name__ == '__main__':
    app.run(debug=True, port='80')