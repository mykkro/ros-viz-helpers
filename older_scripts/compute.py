import sys
import time
import numpy as np
import pandas as pd
from pathlib import Path
import keyboard
# Pinocchio
import pinocchio as pin
from pinocchio.visualize import MeshcatVisualizer
# Meshcat
import meshcat
import meshcat.geometry as g
import meshcat.transformations as tf
import meshcat_shapes
import tempfile
from numpy.linalg import pinv


from commandr import Commandr


def extract_vectors(columns, row, names):
    out = {}
    for name in names:
        eligible_names = []
        for c in columns:
            if c.split(".")[0] == name:
                eligible_names.append(c)
        values = np.array([row[en] for en in eligible_names])
        out[name] = values
    return out

def add_new_column(df, name, count):
    for i in range(count):
        df[f"{name}.{i}"] = 0.0

def set_value(df, i, name, value):
    for j, val in enumerate(value):
        df.at[i, f"{name}.{j}"] = val



if __name__ == "__main__":

    # 

    # Example usage:
    #  python compute.py -i target/move_y.csv -u panda/urdf/panda2_inertias.urdf -o target/move_y_comp.csv


    cmdr = Commandr("compute", title="Compute")
    cmdr.add_argument("input", "-i", type="str")
    cmdr.add_argument("output", "-o", type="str", required=True)
    cmdr.add_argument("urdf", "-u", type="str", required=True)

    args, configs = cmdr.parse()

    input_path = args["input"]
    output_path = args["output"]
    default_urdf_path = args["urdf"]

    mesh_path = "panda/meshes"
    ros_url_prefix = "package://panda2_description/meshes"

    # Paths to urdf

    # URDF file (pathlib is a little nicer but not mandatory)
    urdf_file_path = Path(default_urdf_path)
    abs_path_prefix = str(Path(mesh_path).resolve().as_posix())

    # https://stackoverflow.com/questions/70837669/how-can-i-parse-package-in-a-urdf-file-path
    # Start with openning a temp dir (context manger makes it easy to handle)
    with tempfile.TemporaryDirectory() as tmpdirname:
    
        # Where your tmpfile will be
        tmp_file_path = Path(tmpdirname)/urdf_file_path.name

        # Write each line in fout replacing the ros url prefix with abs path
        with open(urdf_file_path, 'r') as fin:
            with open(tmp_file_path, 'w') as fout:
                for line in fin:
                    fout.write(line.replace(ros_url_prefix, abs_path_prefix))

        model = pin.buildModelFromUrdf(str(tmp_file_path))
        data = model.createData()

    print("No. of frames:", len(model.frames))

    print("ALL FRAMES:")
    for i, frame in enumerate(model.frames):
        print(f"{i:4} NAME = {frame.name:20}\t PARENT = {frame.parent} PREVIOUS = {frame.previousFrame}\t TYPE = {frame.type}")

    print()
    print("JOINTS:")
    for i, frame in enumerate(model.frames):
        if str(frame.type) == "JOINT":
            print(f"{i:4} NAME = {frame.name:20}\t PARENT = {frame.parent} PREVIOUS = {frame.previousFrame}\t TYPE = {frame.type}")

    print()

    # create dictionary: joint name -> q index
    joint_indices_dict = {}
    for name, jnt in zip(model.names, model.joints):
        joint_indices_dict[name] = jnt.idx_q

    ee_indx = model.getFrameId("panda_hand_tcp")

    # initial configuration
    q = pin.neutral(model)

    if input_path is not None:
        df = pd.read_csv(input_path)
        newdf = df.copy()

        add_new_column(newdf, "dq_filtered", 7)
        add_new_column(newdf, "ee_pos", 3)
        add_new_column(newdf, "ee_rot_xyzw", 4)
        add_new_column(newdf, "ee_twist", 6)

        # add synthetic columns
        print("TRAJECTORY:")
        print(f"No. of frames: {len(df)}")
        
        dq_filtered_ = np.array([0,0,0,0,0,0,0])
        alpha_dq_filter_ = 0.50 # 0.99

        last_time_ns = None
        dt = 0
        for i, row in df.iterrows():
            time_ns = row["time_ns"]
            if last_time_ns is not None:
                # difference between two consecutive frames, in seconds (it should be ~ 30ms)
                dt = (time_ns - last_time_ns)/1e9
            last_time_ns = time_ns
            print(time_ns, dt)
            d = extract_vectors(df.columns, row, ["q", "dq", "tau_J", "O_T_EE", "effort", "tau_J"])
            for key, val in d.items():
                print("   ", key, val)

            q_ = d["q"]
            dq_= d["dq"]
            dq_filtered_ = (1 - alpha_dq_filter_) * dq_filtered_ + alpha_dq_filter_ * dq_
            eff_ = d["effort"][:7]
            tau_J = d["tau_J"]
            eff_delta = eff_ - tau_J

            O_T_EE2 = np.array(d["O_T_EE"]).reshape(4,4,order='F')

            # update configuration
            for k in range(7):
                q[k] = q_[k]

            pin.forwardKinematics(model, data, q)
            pin.computeJointJacobians(model, data, q)
            pin.updateFramePlacements(model, data)
            # https://github.com/stack-of-tasks/pinocchio/issues/1140
            frame_J = pin.getFrameJacobian(model,data,ee_indx,pin.ReferenceFrame.LOCAL_WORLD_ALIGNED)
            local_to_world_transform = pin.SE3.Identity()
            local_to_world_transform.rotation = data.oMf[ee_indx].rotation
            frame = model.frames[ee_indx]
            # frame_placement = frame.placement
            # parent_joint = frame.parent
            # frame_v = local_to_world_transform.act(frame_placement.actInv(data.v[parent_joint]))
            J_dot_v = pin.Motion(frame_J.dot(dq_filtered_)) # pin.Motion

            # print("Frame velocity:\n",frame_v)
            # print("J_dot_v:\n",J_dot_v)
            ee_twist = np.hstack([J_dot_v.linear, J_dot_v.angular])
            print("    ee_twist:", ee_twist)

            J_pinv = pinv(frame_J)
            print("    jacobian:", frame_J.shape) # (6,7)
            print("    pseudoinverse:", J_pinv.shape) # (7,6)

            oMf = data.oMf[ee_indx]
            t_matrix = tf.translation_matrix(oMf.translation)
            r_matrix = oMf.rotation
            t_matrix[0:3, 0:3] = r_matrix    
            # print((t_matrix - O_T_EE2))
            otee_error = np.abs(t_matrix - O_T_EE2).sum()

            # conpute EE position and quaternion
            ee_pos = oMf.translation

            quat = pin.Quaternion(r_matrix)
            angle = pin.AngleAxis(r_matrix).angle
            axis =  pin.AngleAxis(r_matrix).axis            
            set_value(newdf, i, "ee_pos", ee_pos)
            ee_rot_xyzw = [quat.x, quat.y, quat.z, quat.w]
            set_value(newdf, i, "ee_rot_xyzw", ee_rot_xyzw)
            set_value(newdf, i, "ee_twist", ee_twist)
            set_value(newdf, i, "dq_filtered", dq_filtered_)
            set_value(newdf, i, "eff_delta", eff_delta)

            print("    O_T_EE error:", otee_error)
            print()

        newdf.to_csv(output_path, index=False)

        exit()


        if False:

            viz.loadViewerModel()

            data = viz.data


            q2 = [0.0,-0.7853981633974483,0.0,-2.356194490192345,0.0,1.5707963267948966,0.7853981633974483]

            for fname, fvalue in zip(names_list, q2):
                if fname != "time_ns":
                    q[joint_indices_dict[fname]] = fvalue

            pin.forwardKinematics(model, viz.data, q)
            pin.updateFramePlacements(model, viz.data)

            # Display Visuals or Collision
            DISPLAY_VISUALS = True
            DISPLAY_COLLISIONS = False
            viz.displayCollisions(DISPLAY_COLLISIONS)
            viz.displayVisuals(DISPLAY_VISUALS)


            start_trace_time = trace_list[0][0]

            step = 0.01 


            def create_text():
                # Create reference frame
                meshcat_shapes.frame(viz.viewer["world"]["reference"], axis_length=0.2, axis_thickness=0.01, opacity=0.8, origin_radius=0.02)
                viz.viewer["world"]["reference"].set_transform(tf.translation_matrix(np.array([0.5, - 0.5, 0])))

                # Find ee index in oMf
                ee_indx = model.getFrameId("panda_hand_tcp")
                
                # Display ee axis
                oMf = viz.data.oMf[ee_indx]  # < ---(9) this index works for oMi
                t_matrix = tf.translation_matrix(oMf.translation)
                r_matrix = oMf.rotation
                t_matrix[0:3, 0:3] = r_matrix

                # Calculate matrixes
                t_matrix_x = tf.translation_matrix(np.array([0, -0.2, 0]))
                t_matrix_y = tf.translation_matrix(np.array([0, -0.25, 0]))
                t_matrix_z = tf.translation_matrix(np.array([0, -0.3, 0]))
                t_matrix_quat = tf.translation_matrix(np.array([0, -0.05, 0]))
                t_matrix_angle = tf.translation_matrix(np.array([0, -0.1, 0]))
                t_matrix_axis = tf.translation_matrix(np.array([0, -0.15, 0]))
                
                #  Update ee position
                ee_x_coord = round(oMf.translation[0], 3)
                ee_y_coord = round(oMf.translation[1], 3)
                ee_z_coord = round(oMf.translation[2], 3)

                quat = pin.Quaternion(r_matrix)
                angle = pin.AngleAxis(r_matrix).angle
                axis =  pin.AngleAxis(r_matrix).axis

                # Display ee coords
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["ee_coord_x"], f"X = {ee_x_coord}", font_size=10)
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["ee_coord_y"], f"Y = {ee_y_coord}", font_size=10)
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["ee_coord_z"], f"Z = {ee_z_coord}", font_size=10)
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["quat"], f"X = {round(quat.x, 3)} Y = {round(quat.y, 3)} Z = {round(quat.z, 3)} W = {round(quat.w,3)}", font_size=10)
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["angle"], f"angle = {round(angle, 3)}", font_size=10)
                meshcat_shapes.textarea(viz.viewer["world"]["reference"]["axis"], f"axis = [{round(axis[0],3)}, {round(axis[1],3)}, {round(axis[2],3)}]", font_size=10)

                # Update coordinate text position
                viz.viewer["world"]["reference"]["ee_coord_x"].set_transform(t_matrix_x)
                viz.viewer["world"]["reference"]["ee_coord_y"].set_transform(t_matrix_y)
                viz.viewer["world"]["reference"]["ee_coord_z"].set_transform(t_matrix_z)
                viz.viewer["world"]["reference"]["quat"].set_transform(t_matrix_quat)
                viz.viewer["world"]["reference"]["angle"].set_transform(t_matrix_angle)
                viz.viewer["world"]["reference"]["axis"].set_transform(t_matrix_axis)

            running = True

            while running:

                trace_ndx = 0
                last_trace_ndx = None
                render_time = 0

                while running and (trace_ndx < len(trace_list)):

                    # Find row that will be displayed    
                    while True:
                        if trace_ndx >= len(trace_list):
                            break
                        time_from_start_s = (trace_list[trace_ndx][0] - start_trace_time) / 1e9

                        if time_from_start_s < render_time:
                            trace_ndx += 1

                        else:
                            last_trace_ndx = trace_ndx
                            trace_ndx += 1
                            break

                    if last_trace_ndx is not None:
                        trace = trace_list[last_trace_ndx]
                        # display it            
                        # Find the index of this trace
                        print(f"Displaying Trace {last_trace_ndx}")
                        timestamp_ns = None
                        # Change q vector to this trace
                        qq = []
                        q2 = trace
                        for fname, fvalue in zip(names_list, q2):
                            if fname != "time_ns":
                                q[joint_indices_dict[fname]] = fvalue
                                qq.append(fvalue)
                            else:
                                timestamp_ns = int(fvalue)

                        print("  Timestamp:", timestamp_ns)
                        print("  Position:", qq)

                        # Update model using pinocchio forward kinematics
                        pin.forwardKinematics(model, viz.data, q)
                        pin.updateFramePlacements(model, viz.data)

                        # compute other data by Pinocchio...
                        
                        # Update Trace Label
                        meshcat_shapes.textarea(viz.viewer["world"]["label"], f"Trace{last_trace_ndx}", font_size=20)
                        t_matrix = tf.translation_matrix(np.array([0, -0.66, 0]))
                        viz.viewer["world"]["label"].set_transform(t_matrix)
                        
                        # Update position of Joint labels and Joint frames
                        for frame, oMf in zip(model.frames, data.oMf):
                            # Joints
                            if str(frame.type) == "JOINT":
                                meshcat_shapes.textarea(viz.viewer[frame.name]["name"], f"{frame.name}", font_size=10)
                                meshcat_shapes.frame(viz.viewer[frame.name]["frame"],axis_length=0.2, axis_thickness=0.01, opacity=0.8, origin_radius=0.02)
                                t_matrix_name = tf.translation_matrix(oMf.translation + np.array([0, -0.25, 0]))
                                t_matrix_frame = tf.translation_matrix(oMf.translation)
                                r_matrix_frame = oMf.rotation
                                t_matrix_frame[0:3, 0:3] = r_matrix_frame
                                viz.viewer[frame.name]["name"].set_transform(t_matrix_name)
                                viz.viewer[frame.name]["frame"].set_transform(t_matrix_frame)
                            # EE
                            if str(frame.name) == "panda_hand_tcp":
                                meshcat_shapes.textarea(viz.viewer[frame.name]["name"], f"{frame.name}", font_size=10)
                                meshcat_shapes.frame(viz.viewer[frame.name]["frame"],axis_length=0.2, axis_thickness=0.01, opacity=0.8, origin_radius=0.02)
                                t_matrix_name = tf.translation_matrix(oMf.translation + np.array([0, -0.25, 0]))
                                t_matrix_frame = tf.translation_matrix(oMf.translation)
                                r_matrix_frame = oMf.rotation
                                t_matrix_frame[0:3, 0:3] = r_matrix_frame
                                viz.viewer[frame.name]["name"].set_transform(t_matrix_name)
                                viz.viewer[frame.name]["frame"].set_transform(t_matrix_frame)

                        create_text()
                        viz.display(q)

                        if keyboard.is_pressed("q"):
                            running = False
                            break

                        time.sleep(step)
                    render_time += step * speed_coefficient
                    
                if repeat:     
                    continue
                else:
                    exit()