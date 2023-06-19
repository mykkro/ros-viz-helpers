from pathlib import Path

from rosbags.highlevel import AnyReader
import yaml

# Message definition: https://github.com/frankaemika/franka_ros/blob/develop/franka_msgs/msg/FrankaState.msg
# Meaning of individual fields explained here: https://frankaemika.github.io/docs/franka_ros.html
"""
std_msgs/Header header
float64[6] cartesian_collision
float64[6] cartesian_contact
float64[7] q
float64[7] q_d
float64[7] dq
float64[7] dq_d
float64[7] ddq_d
float64[7] theta
float64[7] dtheta
float64[7] tau_J
float64[7] dtau_J
float64[7] tau_J_d
float64[6] K_F_ext_hat_K
float64[2] elbow
float64[2] elbow_d
float64[2] elbow_c
float64[2] delbow_c
float64[2] ddelbow_c
float64[7] joint_collision
float64[7] joint_contact
float64[6] O_F_ext_hat_K
float64[6] O_dP_EE_d
float64[3] O_ddP_O
float64[6] O_dP_EE_c
float64[6] O_ddP_EE_c
float64[7] tau_ext_hat_filtered
float64 m_ee
float64[3] F_x_Cee
float64[9] I_ee
float64 m_load
float64[3] F_x_Cload
float64[9] I_load
float64 m_total
float64[3] F_x_Ctotal
float64[9] I_total
float64[16] O_T_EE
float64[16] O_T_EE_d
float64[16] O_T_EE_c
float64[16] F_T_EE
float64[16] F_T_NE
float64[16] NE_T_EE
float64[16] EE_T_K
float64 time
float64 control_command_success_rate
uint8 ROBOT_MODE_OTHER=0
uint8 ROBOT_MODE_IDLE=1
uint8 ROBOT_MODE_MOVE=2
uint8 ROBOT_MODE_GUIDING=3
uint8 ROBOT_MODE_REFLEX=4
uint8 ROBOT_MODE_USER_STOPPED=5
uint8 ROBOT_MODE_AUTOMATIC_ERROR_RECOVERY=6
uint8 robot_mode
franka_msgs/Errors current_errors
franka_msgs/Errors last_motion_errors
"""

# Example of a message:
"""
/franka_state_controller/franka_states
franka_msgs__msg__FrankaState(header=std_msgs__msg__Header(stamp=builtin_interfaces__msg__Time(sec=1686927206, nanosec=60444408, __msgtype__='builtin_interfaces/msg/Time'), frame_id='', __msgtype__='std_msgs/msg/Header'), cartesian_collision=array([0., 0., 0., 0., 0., 0.]), cartesian_contact=array([0., 0., 0., 0., 0., 0.]), q=array([ 0.05619502, -0.78893143, -0.20456323, -2.15522732, -0.15764751,
        1.3448016 ,  0.62206251]), q_d=array([ 0.05096279, -0.8394017 , -0.20461854, -2.16984654, -0.16232222,
        1.3067136 ,  0.6206096 ]), dq=array([ 7.95413632e-03,  1.90272328e-01, -2.45258671e-04,  8.02920036e-02,
        2.49678008e-02,  1.17084981e-01, -1.38674863e-06]), dq_d=array([0., 0., 0., 0., 0., 0., 0.]), ddq_d=array([0., 0., 0., 0., 0., 0., 0.]), theta=array([ 0.05615648, -0.78905737, -0.20434543, -2.15374756, -0.15754463,
        1.34509981,  0.62208676]), dtheta=array([0.        , 0.18829913, 0.        , 0.0742737 , 0.01723702,
       0.11733034, 0.        ]), tau_J=array([-0.57371199, -3.13336945,  3.10414028, 20.52121162,  0.79822433,
        2.15048265,  0.21825399]), dtau_J=array([-41.30597687, -73.77136993,  12.0943222 , -77.62652588,
        16.0581398 , -34.54545593,  22.32954407]), tau_J_d=array([0., 0., 0., 0., 0., 0., 0.]), K_F_ext_hat_K=array([-3.73503246, -0.36313525,  0.29415831, -0.03085724,  0.72257232,
        0.26007961]), elbow=array([-0.20456323, -1.        ]), elbow_d=array([-0.20461854, -1.        ]), elbow_c=array([-0.20461854, -1.        ]), delbow_c=array([0., 0.]), ddelbow_c=array([0., 0.]), joint_collision=array([0., 0., 0., 0., 0., 0., 0.]), joint_contact=array([0., 0., 0., 0., 0., 0., 0.]), O_F_ext_hat_K=array([-3.75536579,  0.19735837, -0.16392114, -0.1021628 , -2.75723639,
       -0.54828461]), O_dP_EE_d=array([0., 0., 0., 0., 0., 0.]), O_ddP_O=array([ 0.  ,  0.  , -9.81]), O_dP_EE_c=array([0., 0., 0., 0., 0., 0.]), O_ddP_EE_c=array([0., 0., 0., 0., 0., 0.]), tau_ext_hat_filtered=array([-0.61800653, -1.49244131, -0.26346881,  0.47900477, -0.00249462,
       -0.08851128,  0.2218687 ]), m_ee=0.7300000190734863, F_x_Cee=array([-0.01,  0.  ,  0.03]), I_ee=array([0.001 , 0.    , 0.    , 0.    , 0.0025, 0.   
 , 0.    , 0.    ,
       0.0017]), m_load=0.0, F_x_Cload=array([0., 0., 0.]), I_load=array([0.01, 0.  , 0.  , 0.  , 0.01, 0.  , 0.  , 0.  , 0.01]), m_total=0.7300000190734863, F_x_Ctotal=array([-0.01,  0.  ,  0.03]), I_total=array([0.001 , 0.    , 0.    , 0.    , 0.0025, 0.    , 0.    , 0.    ,
       0.0017]), O_T_EE=array([ 0.99840782,  0.04381944, -0.03524803,  0.        ,  0.04400161,
       -0.9990121 ,  0.00440886,  0.        , -0.03502069, -0.00595293,
       -0.99936886,  0.        ,  0.2713275 , -0.09218577,  0.55306261,
        1.        ]), O_T_EE_d=array([ 9.98446729e-01,  4.10314909e-02, -3.74338383e-02,  0.00000000e+00,
        4.10667730e-02, -9.99146754e-01,  1.73753669e-04,  0.00000000e+00,
       -3.73954886e-02, -1.71080366e-03, -9.99299080e-01,  0.00000000e+00,
        2.50827893e-01, -9.32509684e-02,  5.56569926e-01,  1.00000000e+00]), O_T_EE_c=array([ 9.98446729e-01,  4.10314909e-02, -3.74338383e-02,  0.00000000e+00,
        4.10667730e-02, -9.99146754e-01,  1.73753669e-04,  0.00000000e+00,
       -3.73954886e-02, -1.71080366e-03, -9.99299080e-01,  0.00000000e+00,
        2.50827893e-01, -9.32509684e-02,  5.56569926e-01,  1.00000000e+00]), F_T_EE=array([ 0.70709997, -0.70709997,  0.        ,  0.        ,  0.70709997,        0.70709997,  0.        ,  0.        ,  0.        ,  0.        ,
        1.        ,  0.        ,  0.        ,  0.        ,  0.1034    ,
        1.        ]), F_T_NE=array([ 0.70709997, -0.70709997,  0.        ,  0.        ,  0.70709997,
        0.70709997,  0.        ,  0.        ,  0.        ,  0.        ,
        1.        ,  0.        ,  0.        ,  0.        ,  0.1034    ,
        1.        ]), NE_T_EE=array([1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.]), EE_T_K=array([1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1., 0., 0., 0., 0., 1.]), time=28398.018, control_command_success_rate=0.0, robot_mode=3, current_errors=franka_msgs__msg__Errors(joint_position_limits_violation=False, cartesian_position_limits_violation=False, self_collision_avoidance_violation=False, joint_velocity_violation=False, cartesian_velocity_violation=False, force_control_safety_violation=False, joint_reflex=False, cartesian_reflex=False, max_goal_pose_deviation_violation=False, max_path_pose_deviation_violation=False, cartesian_velocity_profile_safety_violation=False, joint_position_motion_generator_start_pose_invalid=False, joint_motion_generator_position_limits_violation=False, joint_motion_generator_velocity_limits_violation=False, joint_motion_generator_velocity_discontinuity=False, joint_motion_generator_acceleration_discontinuity=False, cartesian_position_motion_generator_start_pose_invalid=False, cartesian_motion_generator_elbow_limit_violation=False, cartesian_motion_generator_velocity_limits_violation=False, cartesian_motion_generator_velocity_discontinuity=False, cartesian_motion_generator_acceleration_discontinuity=False, cartesian_motion_generator_elbow_sign_inconsistent=False, cartesian_motion_generator_start_elbow_invalid=False, cartesian_motion_generator_joint_position_limits_violation=False, cartesian_motion_generator_joint_velocity_limits_violation=False, cartesian_motion_generator_joint_velocity_discontinuity=False, cartesian_motion_generator_joint_acceleration_discontinuity=False, cartesian_position_motion_generator_invalid_frame=False, force_controller_desired_force_tolerance_violation=False, controller_torque_discontinuity=False, start_elbow_sign_inconsistent=False, communication_constraints_violation=False, power_limit_violation=False, joint_p2p_insufficient_torque_for_planning=False, tau_j_range_violation=False, instability_detected=False, joint_move_in_wrong_direction=False, cartesian_spline_motion_generator_violation=False, joint_via_motion_generator_planning_joint_limit_violation=False, base_acceleration_initialization_timeout=False, base_acceleration_invalid_reading=False, __msgtype__='franka_msgs/msg/Errors'), last_motion_errors=franka_msgs__msg__Errors(joint_position_limits_violation=False, cartesian_position_limits_violation=False, self_collision_avoidance_violation=False, joint_velocity_violation=False, cartesian_velocity_violation=False, force_control_safety_violation=False, joint_reflex=False, cartesian_reflex=True, max_goal_pose_deviation_violation=False, max_path_pose_deviation_violation=False, cartesian_velocity_profile_safety_violation=False, joint_position_motion_generator_start_pose_invalid=False, joint_motion_generator_position_limits_violation=False, joint_motion_generator_velocity_limits_violation=False, joint_motion_generator_velocity_discontinuity=False, joint_motion_generator_acceleration_discontinuity=False, cartesian_position_motion_generator_start_pose_invalid=False, cartesian_motion_generator_elbow_limit_violation=False, cartesian_motion_generator_velocity_limits_violation=False, cartesian_motion_generator_velocity_discontinuity=False, cartesian_motion_generator_acceleration_discontinuity=False, cartesian_motion_generator_elbow_sign_inconsistent=False, cartesian_motion_generator_start_elbow_invalid=False, cartesian_motion_generator_joint_position_limits_violation=False, cartesian_motion_generator_joint_velocity_limits_violation=False, 
cartesian_motion_generator_joint_velocity_discontinuity=False, cartesian_motion_generator_joint_acceleration_discontinuity=False, cartesian_position_motion_generator_invalid_frame=False, force_controller_desired_force_tolerance_violation=False, controller_torque_discontinuity=False, start_elbow_sign_inconsistent=False, communication_constraints_violation=False, power_limit_violation=False, joint_p2p_insufficient_torque_for_planning=False, tau_j_range_violation=False, instability_detected=False, joint_move_in_wrong_direction=False, cartesian_spline_motion_generator_violation=False, joint_via_motion_generator_planning_joint_limit_violation=False, base_acceleration_initialization_timeout=False, base_acceleration_invalid_reading=False, __msgtype__='franka_msgs/msg/Errors'), ROBOT_MODE_OTHER=0, ROBOT_MODE_IDLE=1, ROBOT_MODE_MOVE=2, ROBOT_MODE_GUIDING=3, ROBOT_MODE_REFLEX=4, ROBOT_MODE_USER_STOPPED=5, ROBOT_MODE_AUTOMATIC_ERROR_RECOVERY=6, __msgtype__='franka_msgs/msg/FrankaState')
"""

if __name__ == "__main__":

    rosbag_path = "d:/backup/2023-06-16/ros1-dumps/"

    print("Scanning dir:", rosbag_path)

    filter_files = ["move_z_plus_minus.bag"] #["move_y_plus_minus.bag"] #, "move_x_plus_minus.bag"]
    filter_topics = ["/franka_state_controller/franka_states"] # ["/joint_states"]

    for file in Path(rosbag_path).iterdir():
        dataset_name = file.name
        if dataset_name in filter_files:
            counter = 0
            with AnyReader([file]) as reader:
                for connection, timestamp, rawdata in reader.messages(connections=reader.connections):
                    topic = connection.topic
                    if topic in filter_topics:
                        msg = reader.deserialize(rawdata, connection.msgtype)
                        """
                        print("name:", msg.name)
                        print("position:", msg.position)
                        print("velocity:", msg.velocity)
                        print("effort:", msg.effort)
                        """
                        # print(topic)
                        print(msg.O_T_EE[12:]) # Measured end effector pose in base frame. Pose is represented as a 4x4 matrix in column-major format.
                        # print(msg.O_F_ext_hat_K)
                        # print()
                        target_path = f"{topic.replace('/','__')}.{counter:06}"
                        """
                        with open(Path("target") / Path(target_path), "w", encoding="utf-8") as outfile:
                            yaml.dump(msg, outfile)
                        """
                        counter += 1