import sys
import ast
import rclpy
from rclpy.node import Node
import os
from ament_index_python.packages import get_package_share_directory

#from example_interfaces.srv import AddTwoInts
from dobot_msgs_v4.srv import GetAngle, EnableRobot, DisableRobot, MovJ, MovL, ClearError, GetErrorID, RobotMode, StartDrag, StopDrag, RelJointMovJ
from .TwinCAT_Add_Route import ADS_Route



class MinimalClientAsync(Node, ADS_Route):
    def __init__(self):
        super().__init__('minimal_client_async')
        ADS_Route.__init__(self)
        '''# Get the package share directory
        package_share_directory = get_package_share_directory('py_srvcli')
        # Construct the path to the text file
        text_file_path = os.path.join(package_share_directory, 'resource', 'PLC_Info.txt')
        # Read and print the content of the file
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as file:
                content = file.read()
                self.get_logger().info(f"Content of the text file:\n{content}")
        else:
            self.get_logger().error(f"File not found: {text_file_path}")'''

        
        self.cliEnable = self.create_client(EnableRobot, 'dobot_bringup_ros2/srv/EnableRobot')
        self.cliDisable = self.create_client(DisableRobot, 'dobot_bringup_ros2/srv/DisableRobot')

        self.cliState = self.create_client(RobotMode, 'dobot_bringup_ros2/srv/RobotMode')
        self.cliErrorID = self.create_client(GetErrorID, 'dobot_bringup_ros2/srv/GetErrorID')
        self.cliClearError = self.create_client(ClearError, 'dobot_bringup_ros2/srv/ClearError')

        self.cliStartDrag = self.create_client(StartDrag, 'dobot_bringup_ros2/srv/StartDrag')
        self.cliStopDrag = self.create_client(StopDrag, 'dobot_bringup_ros2/srv/StopDrag')

        self.cliGetAngle = self.create_client(GetAngle, 'dobot_bringup_ros2/srv/GetAngle')

        self.cliMovJ = self.create_client(MovJ, 'dobot_bringup_ros2/srv/MovJ')
        self.cliMovL = self.create_client(MovL, 'dobot_bringup_ros2/srv/MovL')

        self.cliRelJointMovJ = self.create_client(RelJointMovJ, 'dobot_bringup_ros2/srv/RelJointMovJ')

        while not self.cliGetAngle.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        #---------------------------------------------------------
        #
        #---------------------------------------------------------
        self.reqEnable = EnableRobot.Request()
        self.reqDisable = DisableRobot.Request()

        self.reqState = RobotMode.Request()
        self.reqErrorID = GetErrorID.Request()
        self.reqErrorClear = ClearError.Request()

        self.reqStartDrag = StartDrag.Request()
        self.reqStopDrag = StopDrag.Request()

        self.reqGetAngle = GetAngle.Request()

        self.reqMovJ = MovJ.Request()
        self.reqMovL = MovL.Request()


    def send_Enable(self):
        return self.cliEnable.call_async(self.reqEnable)
    def send_Disable(self):
        return self.cliDisable.call_async(self.reqDisable)

    def get_State(self):
        return self.cliState.call_async(self.reqState)
    def get_ErrorID(self):
        return self.cliErrorID.call_async(self.reqErrorID)
    def send_ErrorClear(self):
        return self.cliClearError.call_async(self.reqErrorClear)

    def send_StartDrag(self):
        return self.cliStartDrag.call_async(self.reqStartDrag)
    def send_StopDrag(self):
        return self.cliStopDrag.call_async(self.reqStopDrag)    

    def send_GetAngle(self): #Get Angle
        return self.cliGetAngle.call_async(self.reqGetAngle)

    def send_MovJ(self, a ,b, c, d, e, f):
        self.reqMovJ.a = a
        self.reqMovJ.b = b
        self.reqMovJ.c = c
        self.reqMovJ.d = d
        self.reqMovJ.e = e
        self.reqMovJ.f = f
        return self.cliMovJ.call_async(self.reqMovJ)
    def send_MovL(self, a ,b, c, d, e, f):
        self.req.a = a
        self.req.b = b
        self.req.c = c
        self.req.d = d
        self.req.e = e
        self.req.f = f
        return self.cliMovL.call_async(self.reqMovL)

def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    #future = minimal_client.send_request(float(sys.argv[1]), float(sys.argv[2]),float(sys.argv[3]), float(sys.argv[4]),float(sys.argv[5]), float(sys.argv[6]))
    while True:
        # Sends Enable
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bEnable") == True: 
            future = minimal_client.send_Enable()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
        # Sends Disable
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bDisable")== True: 
            future = minimal_client.send_Disable()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()

        #------------------------------------------------
        # Sends Get State
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bGetState") == True: 
            future = minimal_client.get_State()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
            actual_list = list(ast.literal_eval(response.robot_return))
            print(actual_list)
        # Sends Get ErrorID
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bErrorID") == True: 
            future = minimal_client.get_ErrorID()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
            #actual_list = list(ast.literal_eval(response.robot_return))
            #print(actual_list)
        # Sends Error Clear
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bClearError")  == True: 
            future = minimal_client.send_ErrorClear()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
            #actual_list = list(ast.literal_eval(response.robot_return))
            #print(actual_list)
        
        #------------------------------------------------
        # Sends Disable
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bStartDrag")  == True: 
            future = minimal_client.send_StartDrag()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
        # Sends Disable
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bStopDrag")  == True: 
            future = minimal_client.send_StopDrag()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
        
        #------------------------------------------------
        # Sends Get Angle Request
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bGetJoints") == True: 
            future = minimal_client.send_GetAngle()
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()
            actual_list = list(ast.literal_eval(response.robot_return))
            print(actual_list)
            minimal_client.Write_Variable("MAIN.fb_Dobot.aCurrentJoints",actual_list)
        
        #minimal_client.get_logger().info(
        #    'Result:'+ response.robot_return)
        #actual_list = list(ast.literal_eval(response.robot_return))
        #print(actual_list)
        #minimal_client.Write_Variable("MAIN.fb_Dobot.aCurrentJoints",actual_list)
    
        #------------------------------------------------
        # Send Mov j
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bMovJ")  == True: 
            listVar=minimal_client.Read_Variable("MAIN.fb_Dobot.aMovJ")
            #print(listVar)
            future = minimal_client.send_MovJ(listVar[0],listVar[1],listVar[2],listVar[3],listVar[4],listVar[5])
            rclpy.spin_until_future_complete(minimal_client, future)
            #response = future.result()

        # Send Mov L
        if minimal_client.Read_Variable("MAIN.fb_Dobot.bMovL")  == True: 
            future = minimal_client.send_MovL(float(sys.argv[1]), float(sys.argv[2]),float(sys.argv[3]), float(sys.argv[4]),float(sys.argv[5]), float(sys.argv[6]))
            rclpy.spin_until_future_complete(minimal_client, future)
            response = future.result()





        '''future = minimal_client.send_GetAngle()
        rclpy.spin_until_future_complete(minimal_client, future)
        response = future.result()
        #minimal_client.get_logger().info(
        #    'Result:'+ response.robot_return)
        actual_list = list(ast.literal_eval(response.robot_return))
        print(actual_list)
        minimal_client.Write_Variable("MAIN.fb_Dobot.aCurrentJoints",actual_list)'''
    
    '''try:
        rclpy.spin(minimal_client)  # Keep the node running
    except KeyboardInterrupt:
        pass  # Allow the program to exit gracefully
    finally:
        minimal_client.destroy_node()
        rclpy.shutdown()  # Automatically cleans up the node on shutdown'''


if __name__ == '__main__':
    main()