import numpy as np

def calculate_angle(a, b, c):
    """
    Calculate angle at joint B formed by points A-B-C.
    Uses: angle = arccos((BA·BC) / (|BA||BC|))
    Points are (x, y) or (x, y, z) tuples/arrays.
    """
    a = np.array(a[:2])
    b = np.array(b[:2])
    c = np.array(c[:2])

    ba = a - b
    bc = c - b

    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)

    if norm_ba == 0 or norm_bc == 0:
        return 0.0

    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))
    return round(float(angle), 1)


def extract_landmark(landmarks, index, w, h):
    """Extract normalized landmark and convert to pixel coords."""
    lm = landmarks[index]
    return (lm.x * w, lm.y * h, lm.z)


def get_joint_angles(landmarks, w, h):
    """Calculate all major joint angles from MediaPipe landmarks."""
    try:
        import mediapipe as mp
        mp_pose = mp.solutions.pose
        L = mp_pose.PoseLandmark

        def lm(idx):
            return extract_landmark(landmarks, idx, w, h)

        angles = {}

        # Left knee
        try:
            angles['left_knee'] = calculate_angle(
                lm(L.LEFT_HIP), lm(L.LEFT_KNEE), lm(L.LEFT_ANKLE))
        except Exception:
            pass

        # Right knee
        try:
            angles['right_knee'] = calculate_angle(
                lm(L.RIGHT_HIP), lm(L.RIGHT_KNEE), lm(L.RIGHT_ANKLE))
        except Exception:
            pass

        # Left elbow
        try:
            angles['left_elbow'] = calculate_angle(
                lm(L.LEFT_SHOULDER), lm(L.LEFT_ELBOW), lm(L.LEFT_WRIST))
        except Exception:
            pass

        # Right elbow
        try:
            angles['right_elbow'] = calculate_angle(
                lm(L.RIGHT_SHOULDER), lm(L.RIGHT_ELBOW), lm(L.RIGHT_WRIST))
        except Exception:
            pass

        # Left shoulder
        try:
            angles['left_shoulder'] = calculate_angle(
                lm(L.LEFT_ELBOW), lm(L.LEFT_SHOULDER), lm(L.LEFT_HIP))
        except Exception:
            pass

        # Right shoulder
        try:
            angles['right_shoulder'] = calculate_angle(
                lm(L.RIGHT_ELBOW), lm(L.RIGHT_SHOULDER), lm(L.RIGHT_HIP))
        except Exception:
            pass

        # Left hip
        try:
            angles['left_hip'] = calculate_angle(
                lm(L.LEFT_SHOULDER), lm(L.LEFT_HIP), lm(L.LEFT_KNEE))
        except Exception:
            pass

        # Right hip
        try:
            angles['right_hip'] = calculate_angle(
                lm(L.RIGHT_SHOULDER), lm(L.RIGHT_HIP), lm(L.RIGHT_KNEE))
        except Exception:
            pass

        return angles
    except Exception as e:
        return {}
