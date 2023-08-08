from rktellolib import Tello

drone = Tello(debug=True, has_video=False)

# def system_info(drone):
#     # Retrieve System & Environment States
#     print(drone.get_battery())
#     print(drone.get_flight_time())
#     print(drone.get_temp())
#     print(drone.get_barometer())

#     # Retrieve Positional States
#     print(drone.get_height())
#     print(drone.get_distance_tof())
#     print(drone.get_ax())
#     print(drone.get_ay())
#     print(drone.get_az())
#     print(drone.get_vx())
#     print(drone.get_vy())
#     print(drone.get_vz())

drone.connect()
drone.takeoff()

drone.forward(100)
print(drone.get_vx())
print(drone.get_vy())
print(drone.get_vz())

drone.cw(90)
drone.forward(100)
print(drone.get_vx())
print(drone.get_vy())
print(drone.get_vz())

drone.cw(90)
drone.forward(100)
drone.get_states()
drone.get_state('vgx')
print(drone.get_vx())
print(drone.get_vy())
print(drone.get_vz())

drone.cw(90)
drone.forward(100)
print(drone.get_vx())
print(drone.get_vy())
print(drone.get_vz())

drone.cw(90)

drone.land()
drone.disconnect()

