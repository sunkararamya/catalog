from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
# importing all database models from ModelDataSetup file
from ModelDataSetup import *

engine = create_engine('sqlite:///filmcameras.db')
''' Bind the engine to the metadata of the Base class so that the
 declaratives can be accessed through a DBSession instance'''
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# If there is any  existing Filmy_Cameras then delete it.
session.query(Filmy_Cameras).delete()
# If there is any  existing Filmy_cam_Name then delete it.
session.query(Filmy_cam_Name).delete()
# If there is any  existing GoogleMailuser then delete it
session.query(GoogleMailuser).delete()

# Sample data creation of user
user1 = GoogleMailuser(r_name="ramya reddy", email="ramyasunkara52@gmail.com",
                       picture='http://www.enchanting-costarica.com/wp-/'
                       'content uploads/2018/02/jcarvaja17-min.jpg')
session.add(user1)
session.commit()
print ("user1 is successfully added")
user2 = GoogleMailuser(r_name="priya reddy", email="sharipriya71@gmail.com",
                       picture='http://www.enchanting-costarica.com/wp-/'
                       'content uploads/2018/02/jcarvaja17-min.jpg')
session.add(user2)
session.commit()
print ("user2 is successfully added")

# Create sample  film Camera names
Cam_type1 = Filmy_Cameras(r_name="SingleLensReflex Camera",
                          user_id=1)
session.add(Cam_type1)
session.commit()

Cam_type2 = Filmy_Cameras(r_name="Range-Finder", user_id=1)
session.add(Cam_type2)
session.commit

Cam_type3 = Filmy_Cameras(r_name="TwinLens Reflex", user_id=1)
session.add(Cam_type3)
session.commit()
Cam_type4 = Filmy_Cameras(r_name="Stereo Cameras", user_id=1)
session.add(Cam_type4)
session.commit()

Cam_type5 = Filmy_Cameras(r_name="Instant Cameras", user_id=1)
session.add(Cam_type5)
session.commit()
Cam_type6 = Filmy_Cameras(r_name="Panoramic Cameras", user_id=1)
session.add(Cam_type6)
session.commit()
Cam_type7 = Filmy_Cameras(r_name="Folding Cameras", user_id=1)
session.add(Cam_type7)
session.commit()
Cam_type8 = Filmy_Cameras(r_name="Box Cameras",  user_id=1)
session.add(Cam_type8)
session.commit()

# Adding different cam_Models into Cameras .................................
Cam1 = Filmy_cam_Name(r_name="Canon",
                      cam_Model="EOS 1300D",
                      Dimension="7.8x12.9x10.1cm",
                      Batteries="1 Lithium batterie",
                      resolution="18megapixels",
                      screen_size="3 Inches",
                      conector_type="Wi-Fi,NFC",
                      camera_cost="40,000Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=1,
                      user_id=1)
session.add(Cam1)
session.commit()
Cam2 = Filmy_cam_Name(r_name="Nikon",
                      cam_Model="Nik_D5300_18_55",
                      Dimension="7.6 x 12.5 x 9.8 cm",
                      Batteries="1 Lithium batterie",
                      resolution="24.2 Megapixels",
                      screen_size="3.2 Inches",
                      conector_type="Wi-Fi",
                      camera_cost="42,798Rs",
                      voltage="7.6 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=1,
                      user_id=1)
session.add(Cam2)
session.commit()
Cam3 = Filmy_cam_Name(r_name="Sony",
                      cam_Model="DSC-H300B",
                      Dimension="9.2x12.8x8.9 cm",
                      Batteries="2 AA batteries",
                      resolution="20.1 megapixels",
                      screen_size="3 Inches",
                      conector_type="usb",
                      camera_cost="14,400Rs",
                      voltage="7.2 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=1,
                      user_id=1)
session.add(Cam3)
session.commit()
Cam4 = Filmy_cam_Name(r_name="Nikon",
                      cam_Model="BKA130YA",
                      Dimension="11 x 13 x 8 cm",
                      Batteries="1 CR2 batterie",
                      resolution="18.1 megapixels",
                      screen_size="3.1Inches",
                      conector_type="Wi-fi",
                      camera_cost="17,987Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=2,
                      user_id=1)
session.add(Cam4)
session.commit()
Cam5 = Filmy_cam_Name(r_name="Xummy",
                      cam_Model="198160",
                      Dimension="7.9x12.9x10.2 cm",
                      Batteries="1 Lithium batterie",
                      resolution="19.2 megapixels",
                      screen_size="3 Inches",
                      conector_type="usb",
                      camera_cost="20,000Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=2,
                      user_id=1)
session.add(Cam5)
session.commit()
Cam6 = Filmy_cam_Name(r_name="Fotodiox",
                      cam_Model="B-III-Cap-zetal",
                      Dimension="5 x 5 x 2.5 cm",
                      Batteries="No batteries",
                      resolution="18.1mega pixels",
                      screen_size="3 Inches",
                      conector_type="Wi-fi",
                      camera_cost="16,000Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=3,
                      user_id=1)
session.add(Cam6)
session.commit()
Cam7 = Filmy_cam_Name(r_name="Superheadz Blackbird",
                      cam_Model="Sundome Camera",
                      Dimension="18.2x13x12.2 cm",
                      Batteries="No batteries",
                      resolution="21.1 megapixels",
                      screen_size="3.2 Inches",
                      conector_type="no connector",
                      camera_cost="33,345Rs",
                      voltage="7.3 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=3,
                      user_id=1)
session.add(Cam7)
session.commit()
Cam8 = Filmy_cam_Name(r_name="myTVS",
                      cam_Model="TAV-40 + Sensor",
                      Dimension="25 x 21 x 18 cm",
                      Batteries="No batteries",
                      resolution="18",
                      screen_size="3 Inches",
                      conector_type="Wi-Fi,NFC",
                      camera_cost="7,986Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=4,
                      user_id=1)
session.add(Cam8)
session.commit()
Cam9 = Filmy_cam_Name(r_name="DULCET",
                      cam_Model="DC-9911TC",
                      Dimension="21 x 16 x 9 cm",
                      Batteries="No ion batteries",
                      resolution="18",
                      screen_size="3 Inches",
                      conector_type="Wi-Fi,NFC",
                      camera_cost="5,568Rs",
                      voltage="7.4 Volts",
                      date=datetime.datetime.now(),
                      filmcameratypeid=4,
                      user_id=1)
session.add(Cam9)
session.commit()
Cam10 = Filmy_cam_Name(r_name="Woodman",
                       cam_Model="S1",
                       Dimension="45.7 x 30.5 x 25 cm",
                       Batteries="No ion batteries",
                       resolution="720p Megapixels",
                       screen_size="7 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="10,000Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=4,
                       user_id=1)
session.add(Cam10)
session.commit()
Cam11 = Filmy_cam_Name(r_name="V.T.I.",
                       cam_Model="VTI002",
                       Dimension="20 x 20 x 8 cm",
                       Batteries="No batteries",
                       resolution="1080p Full HD",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="4,678Rs",
                       voltage="7.4 Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=5,
                       user_id=1)
session.add(Cam11)
session.commit()
Cam12 = Filmy_cam_Name(r_name="Fuji",
                       cam_Model="Instax Square SQ6",
                       Dimension="15.5x15.5x10.4cm",
                       Batteries="2 CR2batteries",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="7,490Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=5,
                       user_id=1)
session.add(Cam12)
session.commit()
Cam13 = Filmy_cam_Name(r_name="YAOJIN",
                       cam_Model="YAOJINJAS130-F01",
                       Dimension="19 x 19 x 9 cm",
                       Batteries="No batteries required",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="7,490Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=6,
                       user_id=1)
session.add(Cam13)
session.commit()
Cam13 = Filmy_cam_Name(r_name="V380",
                       cam_Model="VR Cam V6-2",
                       Dimension="18 x 12 x 5 cm",
                       Batteries="No batteries required",
                       resolution="20megapixels",
                       screen_size="3.2 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="6,789Rs",
                       voltage="7.3Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=6,
                       user_id=1)
session.add(Cam13)
session.commit()

Cam14 = Filmy_cam_Name(r_name="MSE",
                       cam_Model="DigitalCameraBinocular-A2",
                       Dimension="19.2 x 19.2 x 9.4 cm",
                       Batteries="No batteries required",
                       resolution="21megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.1Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=7,
                       user_id=1)
session.add(Cam14)
session.commit()
Cam15 = Filmy_cam_Name(r_name="HOLGA",
                       cam_Model="120N",
                       Dimension="25.4x21.3x15.7cm",
                       Batteries="No batteries required",
                       resolution="19megapixels",
                       screen_size="3.1 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,890Rs",
                       voltage="7.1Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=7,
                       user_id=1)
session.add(Cam15)
session.commit()
Cam16 = Filmy_cam_Name(r_name="Fuji",
                       cam_Model="120N",
                       Dimension="20.1x16.8x14.1 cm",
                       Batteries="No batteries required",
                       resolution="0.1megapixels",
                       screen_size="3.2 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="8,878Rs",
                       voltage="7.2Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=8,
                       user_id=1)
session.add(Cam16)
session.commit()
Cam16 = Filmy_cam_Name(r_name="Fuji",
                       cam_Model="Mini 9",
                       Dimension="19 x 14 x 15.2 cm",
                       Batteries="2 CR2 batteries ",
                       resolution="0.1megapixels",
                       screen_size="3.2 Inches",
                       conector_type="Wi-Fi",
                       camera_cost="6,789Rs",
                       voltage="7.0Volts",
                       date=datetime.datetime.now(),
                       filmcameratypeid=8,
                       user_id=1)
session.add(Cam16)
session.commit()

print("Your films database has been inserted")
