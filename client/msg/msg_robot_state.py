import json 

class MsgRobotState:
    """
    Class representing robot state data structure with default values.
    """

    MSG_ROBOT_STATE = {
        "robot_id": str,
        "robot_type": int,
        "battery": float,
        "linear_vx": float,
        "linear_vy": float,
        "linear_ax": float,
        "linear_ay": float,
        "angular_vz": float,
        "task_state": int,
        "task_type": int,
        "time_lag":int
    }

    def __init__(self, **kwargs):
        """
        Initializes the robot state object with provided keyword arguments 
        and default values.

        Args:
            **kwargs: Dictionary containing robot state data (optional).
        """

        # Set default values for all attributes
        for key, value_type in self.MSG_ROBOT_STATE.items():
            setattr(self, key, None if value_type is str else 0.0 if value_type in (float, int) else False)

        # Update with provided keyword arguments
        for key, value in kwargs.items():
            if key not in self.MSG_ROBOT_STATE:
                raise ValueError(f"Invalid key '{key}' in robot state data")
            setattr(self, key, value)

    def to_json(self) -> str:
        """
        Converts the robot state object to a JSON string.
        """
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_data: str) -> "MsgRobotState":
        """
        Decodes a JSON string into a RobotState object.

        Args:
            json_data: The JSON string representing robot state data.

        Returns:
            A RobotState object populated with the data from the JSON.

        Raises:
            ValueError: If the JSON data is invalid or contains unexpected keys.
        """

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")

        # Check for unexpected keys
        unexpected_keys = set(data.keys()) - set(cls.MSG_ROBOT_STATE.keys())
        if unexpected_keys:
            raise ValueError(f"Unexpected keys in JSON data: {', '.join(unexpected_keys)}")

        # Create and return the RobotState object
        return cls(**data)  # Unpack the dictionary as keyword arguments

if __name__ == "__main__":
    # Example usage with some and without arguments
    robot_state_1 = MsgRobotState(robot_id="RBT-123", battery=75.2)
    robot_state_2 = MsgRobotState()  # Uses all defaults
    robot_state_empty = MsgRobotState()  # use for store the data

    json_data_1 = robot_state_1.to_json()
    json_data_2 = robot_state_2.to_json()

    print(json_data_1)
    print(json_data_2)


    robot_state_empty = MsgRobotState.from_json(json_data_1)
    print(robot_state_empty.robot_id)