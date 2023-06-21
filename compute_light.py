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
    #  python compute_light.py -i target/move_y.csv -u panda/urdf/panda2_inertias.urdf -o target/move_y_comp.csv


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
            d = extract_vectors(df.columns, row, ["position", "velocity", "effort"])
            for key, val in d.items():
                print("   ", key, val)

            q_ = d["position"]
            dq_= d["velocity"]
            eff_ = d["effort"][:7]

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


        newdf.to_csv(output_path, index=False)
