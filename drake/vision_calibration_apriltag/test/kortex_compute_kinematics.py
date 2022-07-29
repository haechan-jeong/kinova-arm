#! /usr/bin/env python3

"""_summary_
    This script is adapted from the Kortex SDK examples.
Returns:
    _type_: _description_
"""

###
# KINOVA (R) KORTEX (TM)
#
# Copyright (c) 2018 Kinova inc. All rights reserved.
#
# This software may be modified and distributed
# under the terms of the BSD 3-Clause license.
#
# Refer to the LICENSE file for details.
#
###

import sys
import os

from kortex_api.autogen.client_stubs.BaseClientRpc import BaseClient

from kortex_api.autogen.messages import Base_pb2
from kortex_api.Exceptions.KServerException import KServerException

import numpy as np

#
#
# Example core functions
#

def example_forward_kinematics(base):
    # Current arm's joint angles (in home position)
    try:
        print("Getting Angles for every joint...")
        input_joint_angles = base.GetMeasuredJointAngles()
    except KServerException as ex:
        print("Unable to get joint angles")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    print("Joint ID : Joint Angle")
    joint_angle_list = list()
    for joint_angle in input_joint_angles.joint_angles:
        joint_angle_list.append(joint_angle.value)
    
    print('Joint Angles:', joint_angle_list, '\n')
    
    # Computing Foward Kinematics (Angle -> cartesian convert) from arm's current joint angles
    try:
        print("Computing Foward Kinematics using joint angles...")
        pose = base.ComputeForwardKinematics(input_joint_angles)
    except KServerException as ex:
        print("Unable to compute forward kinematics")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    print("Pose calculated : ")

    translation_matrix = np.array([[1.0, 0.0, 0.0, pose.x],
                                   [0.0, 1.0, 0.0, pose.y],
                                   [0.0, 0.0, 1.0, pose.z],
                                   [0.0, 0.0, 0.0, 1.0]])
    rotation_matrix_x = np.array([[1.0, 0.0, 0.0, 0.0],
                                  [0.0, np.cos(pose.theta_x), -np.sin(pose.theta_x), 0.0],
                                  [0.0, np.sin(pose.theta_x),  np.cos(pose.theta_x), 0.0],
                                  [0.0, 0.0, 0.0, 1.0]])
    rotation_matrix_y = np.array([[ np.cos(pose.theta_x), 0.0, np.sin(pose.theta_x), 0.0],
                                  [0.0, 1.0, 0.0, 0.0],
                                  [-np.sin(pose.theta_x), 0.0, np.cos(pose.theta_x), 0.0],
                                  [0.0, 0.0, 0.0, 1.0]])
    rotation_matrix_z = np.array([[np.cos(pose.theta_x), -np.sin(pose.theta_x), 0.0, 0.0],
                                  [np.sin(pose.theta_x),  np.cos(pose.theta_x), 0.0, 0.0],
                                  [0.0, 0.0, 1.0, 0.0],
                                  [0.0, 0.0, 0.0, 1.0]])
    
    forward_matrix = translation_matrix @ rotation_matrix_x @ rotation_matrix_y @ rotation_matrix_z
    print(forward_matrix)
    print()

    # Save the pose matrix to numpy file
    np.save('forward_kinematics.npy', forward_matrix)


    return True

def example_inverse_kinematics(base):
    # get robot's pose (by using forward kinematics)
    try:
        input_joint_angles = base.GetMeasuredJointAngles()
        pose = base.ComputeForwardKinematics(input_joint_angles)
    except KServerException as ex:
        print("Unable to get current robot pose")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    # Object containing cartesian coordinates and Angle Guess
    input_IkData = Base_pb2.IKData()
    
    # Fill the IKData Object with the cartesian coordinates that need to be converted
    input_IkData.cartesian_pose.x = pose.x
    input_IkData.cartesian_pose.y = pose.y
    input_IkData.cartesian_pose.z = pose.z
    input_IkData.cartesian_pose.theta_x = pose.theta_x
    input_IkData.cartesian_pose.theta_y = pose.theta_y
    input_IkData.cartesian_pose.theta_z = pose.theta_z

    # Fill the IKData Object with the guessed joint angles
    for joint_angle in input_joint_angles.joint_angles :
        jAngle = input_IkData.guess.joint_angles.add()
        # '- 1' to generate an actual "guess" for current joint angles
        jAngle.value = joint_angle.value - 1
    
    try:
        print("Computing Inverse Kinematics using joint angles and pose...")
        computed_joint_angles = base.ComputeInverseKinematics(input_IkData)
    except KServerException as ex:
        print("Unable to compute inverse kinematics")
        print("Error_code:{} , Sub_error_code:{} ".format(ex.get_error_code(), ex.get_error_sub_code()))
        print("Caught expected error: {}".format(ex))
        return False

    print("Joint ID : Joint Angle")
    joint_identifier = 0
    for joint_angle in computed_joint_angles.joint_angles :
        print(joint_identifier, " : ", joint_angle.value)
        joint_identifier += 1
    return True

def main():
    # Import the utilities helper module
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    import utilities

    # Parse arguments
    args = utilities.parseConnectionArguments()
    
    # Create connection to the device and get the router
    with utilities.DeviceConnection.createTcpConnection(args) as router:

        # Create required services
        base = BaseClient(router)

        # Example core
        success = True
        success = example_forward_kinematics(base)

        ## This function is not used for current purposes. Therefore, it is disabled for now. ##
        if False: success &= example_inverse_kinematics(base)
        
        return 0 if success else 1

if __name__ == "__main__":
    main()