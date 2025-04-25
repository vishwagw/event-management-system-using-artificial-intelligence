# idea : build an AI based parking lot management system:

# intro:
in todays's world, there are many parking lots in a specific area. for example, there are parking lots infront of a mall or large building. other buildings such as shared houses and apartment building have parking lots. As some one whob lived in an apartment building for two years, I have seen many parking lots and how their management system can be.

# idea : 
By using AI, we can build a automatic system that can help the user with parking in a public parking area.
basic system standard is follows:
1. a car user will drive toward the entrance. 
2. in the entrance their is an automatic detection system and counter will release a tickect for the driver.then it will give a slot number for the parking lot or show the available slots. when user park in the slot. there will be an automatic detector on the bumper to detect the vehicle.
3. the detector on the bumper will also help to measure how much time the vehicle is on the slot. this is going to help with the parking fee or parking fine if vehicle is over-parked. 

4. the system is also using computer vision to identify vehicles by the registered number plate, detect abnormal activites, detect thieves and respond in real-time.
this is the basic structure for parking management system.


# LIRARIES:
pyzbar - for scanning QR codes
imutils - for basic image processing

# system structure:

- QR_scan.py - for scanning QR codes from the cardrivers for parking invitation.
- empty_slot_detect.py - for detecting empty slots
- b.py - basic functionalities
- test.py - testing program
- email_test.py - 

