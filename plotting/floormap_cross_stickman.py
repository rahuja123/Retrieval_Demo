from .camera_mapping import get_cluster_position, get_cluster
import cv2
import numpy

background= r'../assets/images/overview_B3_cluster_1.png'
logo= 'plotting/stickman.png'


def transparentOverlay(src, overlay, pos=(0, 0), scale=0.7):
    """
    :param src: Input Color Background Image
    :param overlay: transparent Image (BGRA)
    :param pos:  position where the image to be blit.
    :param scale : scale factor of transparent image.
    :return: Resultant Image
    """
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w, _ = overlay.shape  # Size of foreground
    rows, cols, _ = src.shape  # Size of background Image
    y, x = pos[0], pos[1]  # Position of foreground/overlay image

    # loop over all pixels and apply the blending equation
    for i in range(h):
        for j in range(w):
            if x + i >= rows or y + j >= cols:
                continue
            alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
            src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
    return src


def floormap_cross_numbers(img_path,camera_names, img_cord=(610,457)):

    opacity=1

    img= cv2.imread(img_path,-1)
    waterImg = cv2.imread(logo, -1)
    print(img.shape)
    img= cv2.resize(img, img_cord)

    current_cordinates=()
    prev_cordinates=()
    cluster_name_check=[]
    counter=1
    for camera in camera_names:
        cluster_name= get_cluster(camera)
        current_cordinates= get_cluster_position(cluster_name)
        current_cordinates= tuple(int(s) for s in current_cordinates)
        if prev_cordinates==current_cordinates:
            continue


        # img= cv2.drawMarker(img, current_cordinates, [7,12,145], markerType=cv2.MARKER_TILTED_CROSS , markerSize=20, thickness=3)
        font = cv2.FONT_HERSHEY_SIMPLEX
        if cluster_name in cluster_name_check:
            img= cv2.putText(img,", "+str(counter), tuple(numpy.subtract(current_cordinates, (-5,-30))), font, 0.5, (0,0,0), 2, cv2.LINE_4)
            img= cv2.putText(img,"  "+camera.split('-')[1][:2], tuple(numpy.subtract(current_cordinates, (-5,-50))), font, 0.5, (0,0,0), 2, cv2.LINE_4)
        else:
            tempImg = img.copy()
            print(tempImg.shape)

            overlay = transparentOverlay(tempImg, waterImg, tuple(numpy.subtract(current_cordinates, (15,15))))
            output = img.copy()
            # apply the overlay
            cv2.addWeighted(overlay, opacity, output, 1 - opacity, 0, img)
            # img= cv2.drawMarker(img, current_cordinates, [7,12,145], markerType=cv2.MARKER_TILTED_CROSS , markerSize=20, thickness=3)
            img= cv2.putText(img,str(counter), tuple(numpy.subtract(current_cordinates, (5,-30))), font, 0.5, (0,0,0), 2, cv2.LINE_4)
            img= cv2.putText(img,camera.split('-')[1][:2], tuple(numpy.subtract(current_cordinates, (5,-50))), font, 0.5, (0,0,2), 2, cv2.LINE_4)

        counter+=1
        cluster_name_check.append(cluster_name)


        # if prev_cordinates:
        #     img= cv2.arrowedLine(img, prev_cordinates, current_cordinates, [255,0,0], thickness=2, tipLength=0.05, line_type=8)

        prev_cordinates= current_cordinates

    # cv2.imwrite('output_number_cross.png', img)
    cv2.imwrite('static/output_number_cross.png', img)



if __name__ == '__main__':
    img_path = "/Users/rahul_mac/projects/Retrieval_Demo/assets/images/overview_B3_cluster_1.png"
    floormap_cross_numbers(img_path, camera_names=["S21-B4-L-B", "S21-B4-R-B", "S1-B4c-T", "S1-B4c-B","S1-B4a-T","S1-B4a-B" ,"S1-B4b-R-TR" ,"S1-B4b-R-TR", "S1-B4b-R-TR", "S21-B4-L-T" ])
