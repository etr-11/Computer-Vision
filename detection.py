import cv2
import numpy as np


IMAGE_PTS = np.array(
    [
        [0, 192],
        [1165, 192],
        [1165, 628],
        [0, 628],
    ],
    dtype=np.float32,
)

WORLD_PTS = np.array(
    [
    [0, 0],
    [1280, 0],
    [1280, 720],
    [0, 720]
    ], dtype=np.float32
)

WORLD_SIZE = (1280, 720)  

def generate_row(
    x_start: int,
    x_end: int,
    y: int,
    slot_width: int,
    slot_height: int,
    gap: int,
) -> list[tuple[int, int, int, int]]:

    #Генерирует прямоугольники мест для одного ряда.

    spots: list[tuple[int, int, int, int]] = []
    x = x_start
    while x + slot_width <= x_end:
        spots.append((x, y, slot_width, slot_height))
        x += slot_width + gap
    return spots

ROW_SPECS = [
    dict(y=96,  x_start=15, x_end=680, slot_width=21, slot_height=60, gap=4),
    dict(y=240, x_start=37, x_end=680, slot_width=18, slot_height=60, gap=5),
]

PARKING_SPOTS: list[tuple[int, int, int, int]] = []
for spec in ROW_SPECS:
    PARKING_SPOTS.extend(
        generate_row(
            x_start=spec["x_start"],
            x_end=spec["x_end"],
            y=spec["y"],
            slot_width=spec["slot_width"],
            slot_height=spec["slot_height"],
            gap=spec["gap"],
        )
    )


def compute_homography() -> np.ndarray:
    H, _ = cv2.findHomography(IMAGE_PTS, WORLD_PTS)
    return H


def warp_to_top_view(frame: np.ndarray, H: np.ndarray) -> np.ndarray:
    return cv2.warpPerspective(frame, H, WORLD_SIZE)


def analyse_parking(video_path: str = "parking.mp4") -> None:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Не удалось открыть видео: {video_path}")
        return

    H = compute_homography()

    free_count = 0
    total_spots = len(PARKING_SPOTS)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        warped = warp_to_top_view(frame, H)
        gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        gray_blur = cv2.GaussianBlur(gray, (3, 3), 0)

        current_free = 0

        for idx, (x, y, w, h) in enumerate(PARKING_SPOTS):
            roi = gray_blur[y : y + h, x : x + w]
            if roi.size == 0:
                continue

            edges = cv2.Canny(roi, 50, 150)
            edge_ratio = cv2.countNonZero(edges) / float(w * h)

            is_occupied = edge_ratio > 0.13

            color = (0, 0, 255) if is_occupied else (0, 255, 0)
            if not is_occupied:
                current_free += 1

            cv2.rectangle(warped, (x, y), (x + w, y + h), color, 1)
            cv2.putText(
                warped,
                f"{idx+1}",
                (x + 2, y + 12),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                color,
                1,
                cv2.LINE_AA,
            )

        free_count = current_free
        cv2.putText(
            warped,
            f"Free: {free_count}/{total_spots}",
            (5, WORLD_SIZE[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow("Parking occupancy (top view)", warped)
        key = cv2.waitKey(30) & 0xFF
        if key == 27 or key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    analyse_parking()
