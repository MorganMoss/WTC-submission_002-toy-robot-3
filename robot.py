from robot_toy import ToyRobot

def robot_start():
    """This is the entry point for starting my robot"""
    toy_robot = ToyRobot()
    toy_robot.start()
    while True:
        try:
            toy_robot.cmd()
        except SystemExit:
            break

if __name__ == "__main__":
    robot_start()
