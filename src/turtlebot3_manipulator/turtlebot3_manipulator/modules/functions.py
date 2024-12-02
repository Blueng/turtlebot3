import serial
import time
import numpy as np
import cv2 as cv
import glob

from manipulator_interface.msg import LogMsg

arduino_port = '/dev/ttyACM0'
arduino = None

#---------------------------------------------------------------------- arduino start
def connect_arduino():
    """아두이노와 연결을 설정합니다."""
    global arduino
    try:
        arduino = serial.Serial(arduino_port, 115200, timeout=1)
        time.sleep(2)
        msg = f"[INFO] Arduino가 {arduino_port}에서 연결되었습니다."
    except Exception as e:
        msg = f"[ERROR] Arduino에 연결할 수 없습니다: {e}"
        arduino = None
    finally:
        return msg

def mtr_send_clk(number):
    """모터 제어 신호를 전송합니다."""
    global arduino
    if arduino is None or not arduino.is_open:
        msg = connect_arduino() 
    else:
        msg = "[INFO] connect arduino successe"
    
    if arduino is not None and isinstance(number, int):
        data = f"{number}\n"
        try:
            arduino.write(data.encode())
            msg1 = f"[INFO] 전송됨: {data.strip()}"
        except Exception as e:
            msg1 = f"[ERROR] 데이터 전송 중 오류 발생: {e}"
            close_arduino()
    else:
        msg1 = "[WARN] 숫자만 전송 가능하거나 Arduino 연결이 필요합니다."

    return [msg, msg1]

def close_arduino():
    """아두이노 연결을 종료합니다."""
    global arduino
    if arduino is not None:
        try:
            arduino.close()
            msg = "[INFO] Arduino 연결을 닫았습니다."
        except Exception as e:
            msg = f"[ERROR] Arduino 연결 닫기 중 오류 발생: {e}"
    else: 
        msg = "[WARN] Arduino가 이미 닫혔습니다."
        
    arduino = None
    return msg
            
#---------------------------------------------------------------------- arduino end    

#---------------------------------------------------------------------- arUco detect start    
def calibrate_and_undistort(image_path, pattern_size=(6, 8), display_results=False):
    """
    Perform camera calibration and undistort the input image.

    Parameters:
        image_path (str): Path to the input image.
        pattern_size (tuple): Chessboard pattern size (width, height) in internal corners.
        display_results (bool): If True, displays the original and undistorted images side by side.

    Returns:
        undistorted_image (numpy.ndarray): The undistorted version of the input image.
    """
    # Termination criteria for corner sub-pixel accuracy
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Prepare object points (3D points in real-world space)
    objp = np.zeros((pattern_size[0] * pattern_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points
    objpoints = []
    imgpoints = []

    # Load input image
    img = cv.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image at {image_path}")

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, pattern_size, None)

    if not ret:
        raise ValueError("Failed to find chessboard corners. Check the pattern size or image quality.")

    # Refine corners and add to points arrays
    corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    objpoints.append(objp)
    imgpoints.append(corners2)

    # Perform camera calibration
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    if not ret:
        raise RuntimeError("Camera calibration failed.")

    # Undistort the image
    h, w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
    undistorted_img = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

    # Crop the image to the valid ROI
    x, y, w, h = roi
    undistorted_img = undistorted_img[y:y+h, x:x+w]

    # Optionally display results
    if display_results:
        original_height = img.shape[0]
        aspect_ratio = undistorted_img.shape[1] / undistorted_img.shape[0]
        new_width = int(original_height * aspect_ratio)
        resized_undistorted = cv.resize(undistorted_img, (new_width, original_height), interpolation=cv.INTER_LINEAR)
        h_concat = np.hstack((img, resized_undistorted))
        h_concat = cv.resize(h_concat, None, fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
        cv.imshow('Original and Undistorted Image', h_concat)
        cv.waitKey(0)
        cv.destroyAllWindows()

    return undistorted_img