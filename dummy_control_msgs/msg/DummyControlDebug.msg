int32 frame_no

int64 timestamp

float64[] effort
float64[] velocity
float64[] position
float64[] command
float64[] gravity
float64[] effort_without_gravity

float64[] calc_force
float64[] calc_twist
float64[] calc_joint_velocity
float64[] calc_joint_position
float64[] calc_joint_acceleration
float64[] calc_torque


float64[] jacobian

float64[] ee_rotation
float64[] ee_position

geometry_msgs/Twist twist_commanded
geometry_msgs/Twist twist_measured
geometry_msgs/Twist twist_filtered
geometry_msgs/Twist twist_error

geometry_msgs/Pose ee_commanded
geometry_msgs/Pose ee_measured
geometry_msgs/Pose ee_error

float64[7] torque_saturated
float64[7] torque_commanded
float64[7] torque_measured
float64[7] torque_error
float64[7] curr_gravity

float64[] q_r
float64[] dq_r
float64[] ddq_r