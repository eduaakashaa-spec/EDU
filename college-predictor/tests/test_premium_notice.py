import os,sys,tempfile
sys.path.insert(0,r"C:\Users\KALIL\EDU\college-predictor"); os.chdir(r"C:\Users\KALIL\EDU\college-predictor")
fd,db=tempfile.mkstemp(suffix='.db'); os.close(fd)
os.environ.update(DATABASE_URL='sqlite:///'+db,SECRET_KEY='x',FLASK_DEBUG='0')
from app import create_app
from app.extensions import db as DB, bcrypt
from app.models import User
a=create_app(); a.config['TESTING']=True
with a.app_context():
    DB.create_all()
    for n,e,t in [('Free','free@ex.com','free'),('Prem','prem@ex.com','premium')]:
        DB.session.add(User(name=n,email=e,tier=t,password_hash=bcrypt.generate_password_hash('x').decode()))
    DB.session.commit()
M='id="premiumNotice"'
anon=a.test_client()
show=['/','/josaa','/nri-admission','/dasa-2026','/tnea2026','/nirf-ranking','/career-path']
hide=['/members-registration','/premium-membership','/login','/contact','/members-login']
for u in show: r=anon.get(u); assert r.status_code==200 and M in r.get_data(as_text=True), ('should show',u)
for u in hide:
    r=anon.get(u, follow_redirects=True); assert r.status_code==200 and M not in r.get_data(as_text=True), ('should hide',u)
fc=a.test_client(); fc.post('/login',data={'email':'free@ex.com','password':'x'})
assert M in fc.get('/josaa').get_data(as_text=True)
r=fc.get('/why-cse'); assert r.status_code==403 and M not in r.get_data(as_text=True), 'locked page'
pc=a.test_client(); pc.post('/login',data={'email':'prem@ex.com','password':'x'})
assert M not in pc.get('/josaa').get_data(as_text=True), 'premium user'
print('premium notice checks passed')
