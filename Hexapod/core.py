from .Servo.pwm import PWM
from time import sleep

""" joint_key convention:
    R - right, L - left
    F - front, M - middle, B - back
    H - hip, K - knee, A - Ankle
    key : (channel, minimum_pulse_length, maximum_pulse_length) """

joint_properties = {

    'LFH': (0, 110, 630), 'LFK': (1, 110, 630), 'LFA': (2, 110, 630),
    'RFH': (3, 110, 630), 'RFK': (4, 110, 630), 'RFA': (5, 110, 630),
    'LMH': (6, 110, 630), 'LMK': (7, 110, 630), 'LMA': (8, 110, 630),
    'RMH': (9, 110, 630), 'RMK': (10, 110, 630), 'RMA': (11, 110, 630),
    'LBH': (12, 110, 630), 'LBK': (13, 110, 630), 'LBA': (14, 110, 630),
    'RBH': (15, 110, 630), 'RBK': (16, 110, 630), 'RBA': (17, 110, 630),
    'N': (18, 150, 650)
}

driver1 = PWM(0x40)
driver2 = PWM(0x41)

driver1.setPWMFreq(60)
driver2.setPWMFreq(60)


def drive(ch, val):
    driver = driver1 if ch < 16 else driver2
    ch = ch if ch < 16 else ch - 16
    driver.setPWM(ch, 0, val)


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def remap(old_val, old_min, old_max, new_min, new_max):
    new_diff = (new_max - new_min) * (old_val - old_min) / float((old_max - old_min))
    return int(round(new_diff)) + new_min


class HexapodCore:

    def __init__(self):

        self.neck = Joint("neck", 'N')

        self.left_front = Leg('left front', 'LFH', 'LFK', 'LFA')
        self.right_front = Leg('right front', 'RFH', 'RFK', 'RFA')

        self.left_middle = Leg('left middle', 'LMH', 'LMK', 'LMA')
        self.right_middle = Leg('right middle', 'RMH', 'RMK', 'RMA')

        self.left_back = Leg('left back', 'LBH', 'LBK', 'LBA')
        self.right_back = Leg('right back', 'RBH', 'RBK', 'RBA')

        self.legs = [self.left_front, self.right_front,
                     self.left_middle, self.right_middle,
                     self.left_back, self.right_back]

        self.right_legs = [self.right_front, self.right_middle, self.right_back]
        self.left_legs = [self.left_front, self.left_middle, self.left_back]

        self.tripod1 = [self.left_front, self.right_middle, self.left_back]
        self.tripod2 = [self.right_front, self.left_middle, self.right_back]

        self.hips, self.knees, self.ankles = [], [], []

        for leg in self.legs:
            self.hips.append(leg.hip)
            self.knees.append(leg.knee)
            self.ankles.append(leg.ankle)

    def off(self):

        self.neck.off()

        for leg in self.legs:
            leg.off()


class Leg:

    def __init__(self, name, hip_key, knee_key, ankle_key):
        # Maximale graden van de servos.
        max_hip, max_knee, knee_leeway = 45, 30, 10

        self.hip = Joint("hip", hip_key, max_hip)
        self.knee = Joint("knee", knee_key, max_knee, leeway=knee_leeway)
        self.ankle = Joint("ankle", ankle_key)
        print("hip: " + self.hip)
        print("Knee: " + self.knee)
        print("ankle: "+ self.ankle)

        self.name = name
        self.joints = [self.hip, self.knee, self.ankle]

    def pose(self, hip_angle=0, knee_angle=0, ankle_angle=0):

        self.hip.pose(hip_angle)
        self.knee.pose(knee_angle)
        self.ankle.pose(ankle_angle)

    def move(self, knee_angle=None, hip_angle=None, offset=100):
        """ knee_angle < 0 means thigh is raised, ankle's angle will be set to the specified 
            knee angle minus the offset. offset best between 80 and 110 """
        print("knee_angle: " + knee_angle)
        print("hip_angle: " + hip_angle )
        if knee_angle == None: knee_angle = self.knee.angle
        if hip_angle == None: hip_angle = self.hip.angle

        self.pose(hip_angle, knee_angle, knee_angle - offset)

    def replant(self, raised, floor, offset, t=0.1):

        self.move(raised)
        sleep(t)

        self.move(floor, offset)
        sleep(t)

    def off(self):
        for joint in self.joints:
            joint.off()

    def __repr__(self):
        return 'leg: ' + self.name


class Joint:

    def __init__(self, joint_type, jkey, maxx=90, leeway=0):
        self.joint_type, self.name = joint_type, jkey
        self.channel, self.min_pulse, self.max_pulse = joint_properties[jkey]
        self.max, self.leeway = maxx, leeway

        self.off()

    def pose(self, angle=0):
        angle = constrain(angle, -(self.max + self.leeway), self.max + self.leeway)
        pulse = remap(angle, -self.max, self.max, self.min_pulse, self.max_pulse)

        print("Angle: " + angle)
        print("Pulse: " + pulse)
        print("Channel: " + self.channel)

        drive(self.channel, pulse)
        self.angle = angle

        # print repr(self), ':', 'pulse', pulse

    def off(self):
        drive(self.channel, 0)
        self.angle = None

    def __repr__(self):
        return 'joint: ' + self.joint_type + ' : ' + self.name + ' angle: ' + str(self.angle)
