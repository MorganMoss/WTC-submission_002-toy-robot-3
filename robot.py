from robot_toy import ToyRobot

def robot_start():
    """This is the entry point for starting my robot"""
    t = ToyRobot()
    t.start()
    while True:
        try:
            t.cmd()
        except SystemExit:
            break

if __name__ == "__main__":
    robot_start()
