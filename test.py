import struct
from pprint import pprint
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d

class PacketHeader:
    format = '<HBBBBBQfIIBB'
    size = struct.calcsize(format)
    def __init__(self, data):
        self.m_packetFormat, \
        self.m_gameYear, \
        self.m_gameMajorVersion, \
        self.m_gameMinorVersion, \
        self.m_packetVersion, \
        self.m_packetId, \
        self.m_sessionUID, \
        self.m_sessionTime, \
        self.m_frameIdentifier, \
        self.m_overallFrameIdentifier, \
        self.m_playerCarIndex, \
        self.m_secondaryPlayerCarIndex = struct.unpack(self.format, data)


class CarDamageData:
    size = 42
    def __init__(self, data):
        self.m_tyresWear = struct.unpack('4f', data[:16])  # 4 floats, each 4 bytes
        self.m_tyresDamage = struct.unpack('4B', data[16:20])  # 4 uint8, each 1 byte
        self.m_brakesDamage = struct.unpack('4B', data[20:24])  # 4 uint8, each 1 byte
        self.m_frontLeftWingDamage = struct.unpack('B', data[24:25])[0]
        self.m_frontRightWingDamage = struct.unpack('B', data[25:26])[0]
        self.m_rearWingDamage = struct.unpack('B', data[26:27])[0]
        self.m_floorDamage = struct.unpack('B', data[27:28])[0]
        self.m_diffuserDamage = struct.unpack('B', data[28:29])[0]
        self.m_sidepodDamage = struct.unpack('B', data[29:30])[0]
        self.m_drsFault = struct.unpack('B', data[30:31])[0]
        self.m_ersFault = struct.unpack('B', data[31:32])[0]
        self.m_gearBoxDamage = struct.unpack('B', data[32:33])[0]
        self.m_engineDamage = struct.unpack('B', data[33:34])[0]
        self.m_engineMGUHWear = struct.unpack('B', data[34:35])[0]
        self.m_engineESWear = struct.unpack('B', data[35:36])[0]
        self.m_engineCEWear = struct.unpack('B', data[36:37])[0]
        self.m_engineICEWear = struct.unpack('B', data[37:38])[0]
        self.m_engineMGUKWear = struct.unpack('B', data[38:39])[0]
        self.m_engineTCWear = struct.unpack('B', data[39:40])[0]
        self.m_engineBlown = struct.unpack('B', data[40:41])[0]
        self.m_engineSeized = struct.unpack('B', data[41:42])[0]        


class LapData:
    size = 4+4+2+1+2+1+2+2+4+4+4+1+1+1+1+1+1+1+1+1+1+1+1+1+1+1+2+2+1
    def __init__(self, data):
        self.m_lastLapTimeInMS, \
        self.m_currentLapTimeInMS,\
        self.m_sector1TimeInMS, \
        self.m_sector1TimeMinutes, \
        self.m_sector2TimeInMS, \
        self.m_sector2TimeMinutes, \
        self.m_deltaToCarInFrontInMS, \
        self.m_deltaToRaceLeaderInMS, \
        self.m_lapDistance, \
        self.m_totalDistance, \
        self.m_safetyCarDelta, \
        self.m_carPosition, \
        self.m_currentLapNum, \
        self.m_pitStatus, \
        self.m_numPitStops, \
        self.m_sector, \
        self.m_currentLapInvalid , \
        self.m_penalties, \
        self.m_totalWarnings, \
        self.m_cornerCuttingWarnings, \
        self.m_numUnservedDriveThroughPens, \
        self.m_numUnservedStopGoPens, \
        self.m_gridPosition, \
        self.m_driverStatus, \
        self.m_resultStatus, \
        self.m_pitLaneTimerActive, \
        self.m_pitLaneTimeInLaneInMS, \
        self.m_pitStopTimerInMS, \
        self.m_pitStopShouldServePen = struct.unpack('<IIHBHBHHfffBBBBBBBBBBBBBBBHHB', data)



class CarMotionData:
    format = '<6f6h6f'
    size = struct.calcsize(format)
    def __init__(self, data):
        self.m_worldPositionX, \
        self.m_worldPositionY, \
        self.m_worldPositionZ, \
        self.m_worldVelocityX, \
        self.m_worldVelocityY, \
        self.m_worldVelocityZ, \
        self.m_worldForwardDirX, \
        self.m_worldForwardDirY, \
        self.m_worldForwardDirZ, \
        self.m_worldRightDirX, \
        self.m_worldRightDirY, \
        self.m_worldRightDirZ, \
        self.m_gForceLateral, \
        self.m_gForceLongitudinal, \
        self.m_gForceVertical, \
        self.m_yaw, \
        self.m_pitch, \
        self.m_roll = struct.unpack(self.format, data)


def skip_to_next(pos, data ):
    while pos+3 < len(data):
        # print(pos, data[pos:pos+3])
        if data[pos:pos+3] == b'\xe7\x07\x17':
            break
        pos += 1
    return pos 

with open("f1.dump", "rb") as f:
    data = f.read()
    pos = 0
    X = []
    Y = []
    Z = []
    while pos + PacketHeader.size < len(data):
        packet_header = PacketHeader(data[pos:pos+PacketHeader.size]) 
        skip = PacketHeader.size
        # pprint(vars(packet_header))
        # print(packet_header.m_packetId)
        if (packet_header.m_packetId == 0):
            start = pos + PacketHeader.size
            end = start + CarMotionData.size
            if data.__len__() < end:
                break
            print(packet_header.m_packetId, "CAR MOTION DATA")
            car_motion_data = CarMotionData(data[start:end])
            # pprint(vars(car_motion_data))
            # print(car_motion_data.m_worldPositionX, car_motion_data.m_worldPositionY, car_motion_data.m_worldPositionZ)
            X.append(car_motion_data.m_worldPositionX)
            Y.append(car_motion_data.m_worldPositionY)
            Z.append(car_motion_data.m_worldPositionZ)

            skip += CarMotionData.size


        elif (packet_header.m_packetId == 10):
            start = pos + PacketHeader.size
            end = start + CarDamageData.size
            if data.__len__() < end:
                break
            print(packet_header.m_packetId, "CAR DAMAGE DATA")
            car_damage_data = CarDamageData(data[start:end])
            # pprint(vars(car_damage_data))
            skip += CarDamageData.size

        elif (packet_header.m_packetId == 2):
            start = pos + PacketHeader.size
            end = start + LapData.size
            if data.__len__() < end:
                break
            print(packet_header.m_packetId, "LAP DATA")
            lap_data = LapData(data[start:end])
            # pprint(vars(lap_data))
            skip += LapData.size

        else:
            print(packet_header.m_packetId)
        # print("====================================")
        pos = skip_to_next(pos+skip, data)


    # plt.plot(X, Y)
    # plt.xlabel('X-axis')
    # plt.ylabel('Y-axis')
    


    ax = plt.figure().add_subplot(projection='3d')
    ax.contour(X, Y, Z, cmap=cm.coolwarm)  # Plot contour curves
    plt.show()
