from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ModelDataSetup import Base, Filmy_Cameras, Filmy_cam_Name, GoogleMailuser
from flask import session as gmail_signin_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime
# creating filmcameras database in sqlite
engine_1 = create_engine('sqlite:///filmcameras.db',
                         connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine_1)
DBSession = sessionmaker(bind=engine_1)
session = DBSession()
# for flask instance....................... .............................
app = Flask(__name__)
# client id for gconnect in client_secrets.json .............................

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Film Camera Hub"
# creating session
DBSession = sessionmaker(bind=engine_1)
session = DBSession()
#  It is for Creating anti-forgery state token
fct_tcs = session.query(Filmy_Cameras).all()


# Route for signin
@app.route('/signin')
def displaysignin():
    ''' google mail user signin'''
    cur_state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
    gmail_signin_session['cur_state'] = cur_state
    # return "current session state is %s" % gmail_signin_session['cur_state']
    fct_tcs = session.query(Filmy_Cameras).all()
    fctes = session.query(Filmy_cam_Name).all()
    return render_template('signin.html',
                           STATE=cur_state, fct_tcs=fct_tcs, fctes=fctes)
    # return render_template('myhome.html', STATE=cur_state
    # fct_tcs=fct_tcs,fctes=fctes)

# Route for gconnect


@app.route('/gconnect', methods=['POST'])
def gconnect():
    '''this function will handles the google signin process on server side'''
    # current state token validating
    if request.args.get('cur_state') != gmail_signin_session['cur_state']:
        g_response = make_response(json.dumps('Invalid state parameter.'), 401)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response
    # when the above if condition  is not true then I can collect the
    # one-time code from the server with the function request.data
    code = request.data

    try:
        ''' creating oauth_flow object and adding clients secret  information to
         it.'''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        g_response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response

    # Checking that the access token is valid or not.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If access token info is invalid, abort.
    if result.get('error') is not None:
        g_response = make_response(json.dumps(result.get('error')), 500)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response

    # Verify if that the access token is used for the intended user or not.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        g_response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response

    # Verifying that the access token is valid or not for this itemapp.
    if result['issued_to'] != CLIENT_ID:
        g_response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client  ID is does not matching app's.")
        g_response.headers['Content-Type'] = 'application/json'
        return g_response

    stored_access_token = gmail_signin_session.get('access_token')
    stored_gplus_id = gmail_signin_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        g_response = \
            make_response(json.dumps('Current user is already connected.'),
                          200)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response

    # Store the access token in the session for later use.
    gmail_signin_session['access_token'] = credentials.access_token
    gmail_signin_session['gplus_id'] = gplus_id

    # Getting  user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    gmail_signin_session['username'] = data['name']
    gmail_signin_session['picture'] = data['picture']
    gmail_signin_session['email'] = data['email']

    # see if user exists, if it dosesn't make a new one
    user_id = getUserID(gmail_signin_session['email'])
    if not user_id:
        user_id = generateUser(gmail_signin_session)
    gmail_signin_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += gmail_signin_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += gmail_signin_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % gmail_signin_session['username'])
    print ("done!")
    return output


# User Helper Functions
def generateUser(gmail_signin_session):
    camUser1 = GoogleMailuser(r_name=gmail_signin_session[
                              'username'], email=gmail_signin_session[
                              'email'], picture=gmail_signin_session[
                              'picture'])
    session.add(camUser1)
    session.commit()
    user = session.query(GoogleMailuser).filter_by(email=gmail_signin_session[
                                                   'email']).one()
    return user.r_id


def getUserInfo(user_id):
    user = session.query(GoogleMailuser).filter_by(r_id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(GoogleMailuser).filter_by(email=email).one()
        return user.r_id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their signin_session
# Route for home


@app.route('/')
@app.route('/home')
def home():
    fct_tcs = session.query(Filmy_Cameras).all()
    return render_template('myhome.html', fct_tcs=fct_tcs)


# Route for camera hub


@app.route('/CameraHub')
def CameraHub():
    ''' camera hub  for admins'''
    try:
        if gmail_signin_session['username']:
            r_name = gmail_signin_session['username']
            fct_tcs = session.query(Filmy_Cameras).all()
            fcts = session.query(Filmy_Cameras).all()
            fctes = session.query(Filmy_cam_Name).all()
            return render_template('myhome.html', fct_tcs=fct_tcs,
                                   fcts=fcts, fctes=fctes, uname=r_name)
    except:
        return redirect(url_for('displaysigsnin'))
# Route for displayCameras .......................................


@app.route('/CameraHub/<int:fctid>/AllCompanys')
def displayCameras(fctid):
    ''' Showing film_cameras based on Camera category'''
    fct_tcs = session.query(Filmy_Cameras).all()
    fcts = session.query(Filmy_Cameras).filter_by(r_id=fctid).one()
    fctes = session.query(Filmy_cam_Name).filter_by(
                                                 filmcameratypeid=fctid).all()
    try:
        if gmail_signin_session['username']:
            return render_template('displayCameras.html', fct_tcs=fct_tcs,
                                   fcts=fcts, fctes=fctes,
                                   uname=gmail_signin_session['username'])
    except:
        return render_template('displayCameras.html',
                               fct_tcs=fct_tcs, fcts=fcts, fctes=fctes)


# Route for addCameraType
@app.route('/CameraHub/addCameraType', methods=['POST', 'GET'])
def addCameraType():
    '''# Add New Camera Name'''
    if request.method == 'POST':
        company = Filmy_Cameras(r_name=request.form['r_name'],
                                user_id=gmail_signin_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('CameraHub'))
    else:
        return render_template('addCameraType.html', fct_tcs=fct_tcs)


# Route for editCameraCategory
@app.route('/CameraHub/<int:fctid>/edit', methods=['POST', 'GET'])
def editCameraCategory(fctid):
    ''' edit camera names'''
    editCamera = session.query(Filmy_Cameras).filter_by(r_id=fctid).one()
    cam_creator = getUserInfo(editCamera.user_id)
    user = getUserInfo(gmail_signin_session['user_id'])
    # If logged in user != item owner redirect them
    if cam_creator.r_id != gmail_signin_session['user_id']:
        flash("You cannot edit this Film Camera Type."
              "This is belongs to %s" % cam_creator.r_name)
        return redirect(url_for('CameraHub'))
    if request.method == "POST":
        if request.form['r_name']:
            editCamera.r_name = request.form['r_name']
        session.add(editCamera)
        session.commit()
        flash("Film Camera Type is edited successfully ")
        return redirect(url_for('CameraHub'))
    else:
        # fct_tcs is a globla variable we can use this ....................
        return render_template('editCameraCategory.html',
                               fct=editCamera, fct_tcs=fct_tcs)


# Route for deleteCameraCategory
@app.route('/CameraHub/<int:fctid>/delete', methods=['POST', 'GET'])
def deleteCameraCategory(fctid):
    ''' Deleting Camera Category'''
    fct = session.query(Filmy_Cameras).filter_by(r_id=fctid).one()
    cam_creator = getUserInfo(fct.user_id)
    user = getUserInfo(gmail_signin_session['user_id'])
    # If logged in user != item owner redirect them
    if cam_creator.r_id != gmail_signin_session['user_id']:
        flash("You cannot Delete this Film Camera Type."
              "This is belongs to %s" % cam_creator.r_name)
        return redirect(url_for('CameraHub'))
    if request.method == "POST":
        session.delete(fct)
        session.commit()
        flash("Film Camera Type is deleted successfully")
        return redirect(url_for('CameraHub'))
    else:
        return render_template(
               'deleteCameraCategory.html', fct=fct, fct_tcs=fct_tcs)

# Route for addCameraDetails


@app.route('/CameraHub/addCompany/addCameraDetails/<string:fctname>/add',
           methods=['GET', 'POST'])
def addCameraDetails(fctname):
    ''' Add New Camera Details'''
    fcts = session.query(Filmy_Cameras).filter_by(r_name=fctname).one()
    # See if the logged in user is not the owner of camera
    cam_creator = getUserInfo(fcts.user_id)
    user = getUserInfo(gmail_signin_session['user_id'])
    # If logged in user != item owner redirect them
    if cam_creator.r_id != gmail_signin_session['user_id']:
        flash("You cannot add new camera details"
              "This is belongs to %s" % cam_creator.r_name)
        return redirect(url_for('displayCameras', fctid=fcts.r_id))
    if request.method == 'POST':
        r_name = request.form['r_name']
        cam_Model = request.form['cam_Model']
        Dimension = request.form['Dimension']
        Batteries = request.form['Batteries']
        resolution = request.form['resolution']
        screen_size = request.form['screen_size']
        conector_type = request.form['conector_type']
        camera_cost = request.form['camera_cost']
        voltage = request.form['voltage']
        cameraDetails = Filmy_cam_Name(r_name=r_name,
                                       cam_Model=cam_Model,
                                       Dimension=Dimension,
                                       Batteries=Batteries,
                                       resolution=resolution,
                                       screen_size=screen_size,
                                       conector_type=conector_type,
                                       camera_cost=camera_cost,
                                       voltage=voltage,
                                       date=datetime.datetime.now(),
                                       filmcameratypeid=fcts.r_id,
                                       user_id=gmail_signin_session['user_id'])
        session.add(cameraDetails)
        session.commit()
        return redirect(url_for('displayCameras', fctid=fcts.r_id))
    else:
        return render_template('addCameraDetails.html',
                               fctname=fcts.r_name, fct_tcs=fct_tcs)


# Route for editCameradetails

@app.route('/CameraHub/<int:fctid>/<string:fctename>/edit',
           methods=['GET', 'POST'])
def editCameradetails(fctid, fctename):
    '''Edit camera details'''
    fct = session.query(Filmy_Cameras).filter_by(r_id=fctid).one()
    cameraDetails = session.query(Filmy_cam_Name).filter_by(
                    r_name=fctename).one()
    # See if the logged in user is not the owner of camera
    cam_creator = getUserInfo(fct.user_id)
    user = getUserInfo(gmail_signin_session['user_id'])
    # If logged in user != item owner redirect them
    if cam_creator.r_id != gmail_signin_session['user_id']:
        flash("You can't edit camera details"
              "This is belongs to %s" % cam_creator.r_name)
        return redirect(url_for('displayCameras', fctid=fct.id))
    # POST methods
    if request.method == 'POST':
        cameraDetails.r_name = request.form['r_name']
        cameraDetails.cam_Model = request.form['cam_Model']
        cameraDetails.Dimension = request.form['Dimension']
        cameraDetails.Batteries = request.form['Batteries']
        cameraDetails.resolution = request.form['resolution']
        cameraDetails.screen_size = request.form['screen_size']
        cameraDetails.conector_type = request.form['conector_type']
        cameraDetails.camera_cost = request.form['camera_cost']
        cameraDetails.voltage = request.form['voltage']
        cameraDetails.date = datetime.datetime.now()
        session.add(cameraDetails)
        session.commit()
        flash("film_camera Edited Successfully")
        return redirect(url_for('displayCameras', fctid=fctid))
    else:
        return render_template(
               'editCameradetails.html',
               fctid=fctid, cameraDetails=cameraDetails, fct_tcs=fct_tcs)

# Route for deleteCameradetails


@app.route('/CameraHub/<int:fctid>/<string:fctename>/delete',
           methods=['GET', 'POST'])
def deleteCameradetails(fctid, fctename):
    ''' Delete camera details'''
    fct = session.query(Filmy_Cameras).filter_by(r_id=fctid).one()
    cameraDetails = session.query(Filmy_cam_Name).filter_by(
                    r_name=fctename).one()
    # See if the logged in user is not the owner of camera
    cam_creator = getUserInfo(fct.user_id)
    user = getUserInfo(gmail_signin_session['user_id'])
    # If logged in user != item owner redirect them
    if cam_creator.r_id != gmail_signin_session['user_id']:
        flash("You can't delete Camera details"
              "This is belongs to %s" % cam_creator.r_name)
        return redirect(url_for('displayCameras', fctid=fct.r_id))
    if request.method == "POST":
        session.delete(cameraDetails)
        session.commit()
        flash("Camera details deleted Successfully")
        return redirect(url_for('displayCameras', fctid=fctid))
    else:
        return render_template(
               'deleteCameradetails.html',
               fctid=fctid, cameraDetails=cameraDetails, fct_tcs=fct_tcs)


# Route for logout
@app.route('/logout')
def logout():
    ''' Logout from current user'''
    access_token = gmail_signin_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (gmail_signin_session['username'])
    if access_token is None:
        print ('Access Token is None')
        g_response = make_response(
            json.dumps('Current user not connected....'), 401)
        g_response.headers['Content-Type'] = 'application/json'
        return g_response
    access_token = gmail_signin_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del gmail_signin_session['access_token']
        del gmail_signin_session['gplus_id']
        del gmail_signin_session['username']
        del gmail_signin_session['email']
        del gmail_signin_session['picture']
        g_response = make_response(json.dumps('Successfully disconnected/'
                                              'user..'), 200)
        g_response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('displaysignin'))
        # return g_response
    else:
        g_response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        g_response.headers['Content-Type'] = 'application/json'
        return g_response


# Json
# Route for allfilm_camerasJSON
@app.route('/CameraHub/JSON')
def allfilm_camerasJSON():
    '''It will display t all film cameras '''
    cameracategories = session.query(Filmy_Cameras).all()
    cam_category_dict = [db.serialize for db in cameracategories]
    for db in range(len(cam_category_dict)):
        film_cameras = [d.serialize for d in session.query(
                 Filmy_cam_Name).filter_by(
                 filmcameratypeid=cam_category_dict[db]["r_id"]).all()]
        if film_cameras:
            cam_category_dict[db]["film_camera"] = film_cameras
    return jsonify(Filmy_Cameras=cam_category_dict)

# Route for categoriesJSON


@app.route('/film_camerastore/cameracategories/JSON')
def categoriesJSON():
    '''Displays all Camera categories'''
    film_cameras = session.query(Filmy_Cameras).all()
    return jsonify(cameracategories=[db.serialize for db in film_cameras])

# Route for itemsJSON


@app.route('/film_camerastore/film_cameras/JSON')
def itemsJSON():
    '''Displays all Camera Models'''
    items = session.query(Filmy_cam_Name).all()
    return jsonify(film_cameras=[d.serialize for d in items])

# Route for categoryItemsJSON


@app.route('/film_camerastore/<path:film_camera_name>/film_cameras/JSON')
def categoryItemsJSON(film_camera_name):
    '''Displays camera models for a specific camera category'''
    film_cameraCategory = session.query(Filmy_Cameras).filter_by(
                          r_name=film_camera_name).one()
    film_cameras = session.query(Filmy_cam_Name).filter_by(
                   filmcameratype=film_cameraCategory).all()
    return jsonify(film_cameramodel=[d.serialize for d in film_cameras])

# Route for ItemJSON


@app.route('/film_camerastore/<path:film_camera_name>/<path:cam_model_name>/'
           'JSON')
def ItemJSON(film_camera_name, cam_model_name):
    '''Displays a specific Film_Camera category Model'''
    film_cameraCategory = session.query(Filmy_Cameras).filter_by(
                          r_name=film_camera_name).one()
    film_cameramodel = session.query(Filmy_cam_Name).filter_by(
           r_name=cam_model_name, filmcameratype=film_cameraCategory).one()
    return jsonify(film_cameramodel=[film_cameramodel.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
