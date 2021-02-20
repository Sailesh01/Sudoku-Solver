
from utils import *
from sudokuSolver import *


def solve_sudoku(img_path):
    img_height = 450
    img_width = 450
    model = initialize_model()

    img = cv2.imread(img_path)
    img = cv2.resize(img, (img_width, img_height))
    img_blank = np.zeros((img_height, img_width, 3), np.uint8)
    img_threshold = preprocess(img)

    img_contours = img.copy()
    img_big_contour = img.copy()
    contours, hierarchy = cv2.findContours(img_threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    biggest, maxArea = biggest_contour(contours)
    if biggest.size != 0:
        biggest = reorder(biggest)
        cv2.drawContours(img_big_contour, biggest, -1, (0, 0, 255), 25)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0], [img_width, 0], [0, img_height], [img_width, img_height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_warp_colored = cv2.warpPerspective(img, matrix, (img_width, img_height))
        img_detected_digits = img_blank.copy()
        img_warp_colored = cv2.cvtColor(img_warp_colored, cv2.COLOR_BGR2GRAY)

        img_solved_digits = img_blank.copy()
        boxes = split_boxes(img_warp_colored)
        numbers = get_prediction(boxes, model)
        img_detected_digits = display_numbers(img_detected_digits, numbers, color=(255, 0, 255))
        numbers = np.asarray(numbers)
        posArray = np.where(numbers > 0, 0, 1)

        board = np.array_split(numbers, 9)
        try:
            solve(board)
        except:
            pass

        flat_list = []
        for sublist in board:
            for item in sublist:
                flat_list.append(item)

        final_flatten = flat_list*posArray
        img_solved_digits = display_numbers(img_solved_digits, final_flatten)

        pts2 = np.float32(biggest)
        pts1 = np.float32([[0, 0], [img_width, 0], [0, img_height], [img_width, img_height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img_warp_colored_inv = img.copy()
        img_warp_colored_inv = cv2.warpPerspective(img_solved_digits, matrix, (img_width, img_height))
        inv_perspective = cv2.addWeighted(img_warp_colored_inv, 1, img, 0.5, 1)
        filename = "output_img.jpg"
        cv2.imwrite(filename, inv_perspective)
        return filename

    else:
        return False


    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    img_path = r"C:\Users\rasai\PycharmProjects\Sudoku_solver\sudoku.jpg"
    solve_sudoku(img_path)
