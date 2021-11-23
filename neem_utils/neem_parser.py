from typing import List

from neem_interface_python.neem_interface import NEEMInterface
from neem_interface_python.rosprolog_client import Prolog, atom
from scipy.spatial.transform import Rotation


class Datapoint:
    def __init__(self, timestamp: float, reference_frame: str, pos: List[float], ori: Rotation,
                 wrench: List[float] = None):
        self.timestamp = timestamp
        self.reference_frame = reference_frame
        self.pos = pos
        self.ori = ori
        self.wrench = wrench


class Action:
    def __init__(self, name: str, type_: str, datapoints: List[Datapoint]):
        self.name = name
        self.type = type_
        self.datapoints = datapoints


class NEEM:
    def __init__(self, actions: List[Action]):
        self.actions = actions


class NEEMParser:
    def __init__(self):
        self.neem_interface = NEEMInterface()
        self.prolog = Prolog()

    def parse_neem(self, neem_dir) -> NEEM:
        self.neem_interface.load_neem(neem_dir)
        actions = self.neem_interface.get_all_actions()
        neem = NEEM(actions=[])
        for act in actions:
            action_type = self.prolog.once(f"instance_of({atom(act)}, ActionType)")["ActionType"]
            interval = self.neem_interface.get_interval_for_action(act)
            if interval is None:
                continue
            action_start, action_end = interval

            # Always get the TF trajectory
            tf_traj = self.neem_interface.get_tf_trajectory("ee_link", action_start, action_end)
            datapoints = []
            for dp in tf_traj:
                ori = Rotation.from_quat(dp["term"][2][2])
                datapoint = Datapoint(timestamp=dp["term"][1], reference_frame=dp["term"][2][0],
                                      pos=dp["term"][2][1], ori=ori)
                datapoints.append(datapoint)

            # Optionally add wrench data, if available
            try:
                wrench_traj = self.neem_interface.get_wrench_trajectory("ee_link", action_start, action_end)
                assert len(wrench_traj) == len(datapoints)
                for i, dp in enumerate(wrench_traj):
                    datapoints[i].wrench = [item for sublist in dp["term"][2] for item in sublist]   # TODO: THIS IS WRONG
            except Exception as e:
                print(f"No FT data available: {e}")
            neem.actions.append(Action(act, action_type, datapoints))
        return neem


if __name__ == '__main__':
    NEEMParser().parse_neem("/home/lab019/alt/catkin_ws/src/neem_code/testing/neems/1629978803.8462603")