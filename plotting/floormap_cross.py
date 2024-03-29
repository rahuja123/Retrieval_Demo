from .camera_mapping import get_cluster_position, get_cluster
import cv2

def floormap_cross(img_path,camera_names, img_cord=(610,457)):
    print(img_path)
    img= cv2.imread(img_path,1)
    print(img.shape)

    img= cv2.resize(img, img_cord)
    current_cordinates=()
    prev_cordinates=()

    for camera in camera_names:
        current_cordinates= get_cluster_position(get_cluster(camera))
        current_cordinates= tuple(int(s) for s in current_cordinates)
        img= cv2.drawMarker(img, current_cordinates, [0,0,245], markerType=cv2.MARKER_TILTED_CROSS , markerSize=15, thickness=2)

        # if prev_cordinates:
        #     img= cv2.arrowedLine(img, prev_cordinates, current_cordinates, [255,0,0], thickness=2, tipLength=0.05, line_type=8)

        prev_cordinates= current_cordinates


    cv2.imwrite('final.png', img)



if __name__ == '__main__':
    img_path = "/Users/rahul_mac/Desktop/NTU/NTU_Indoor_Demo_GUI/static/overview_B3_cluster.png"
    floormap_cross(img_path, camera_names=["S2.1-B4-L-B", "S2.1-B4-L-T", "S2.1-B4-R-B", "S1-B4c-T", "S1-B4c-B","S1-B4a-T","S1-B4a-B" ,"S1-B4b-R-TR" ,"S1-B4b-R-TR", "S1-B4b-R-TR" ])



"""

S1-B4b-R-TR
S1-B4b-R-TL
S1-B4b-R-B
S1-B4b-R-T
S1-B4b-R-BR
S1-B4b-R-BL
S1-B4b-L-TR
S1-B4b-L-TL
S1-B4b-L-B
S1-B4b-L-T
S1-B4b-L-BR
S1-B4b-L-BL
S2.1-B4-T
S2.1-B4-L-T
S2.1-B4-L-M
S2.1-B4-L-B
S2.1-B4-B
S2.1-B4-R-T
S2.1-B4-R-M
S2.1-B4-R-B
S2.2-B4-T
S2.2-B4-L-T
S2.2-B4-L-M
S2.2-B4-L-B
S2.2-B4-B
S2.2-B4-R-T
S2.2-B4-R-M
S2.2-B4-R-B
S2-B4a-T
S2-B4a-B
S2-B4c-T
S2-B4c-B
S2-B4b-L-T
S2-B4b-L-BR
S2-B4b-L-BL
S2-B4b-L-TR
S2-B4b-L-TL
S2-B4b-L-B
S2-B4b-R-T
S2-B4b-R-BR
S2-B4b-R-BL
S2-B4b-R-TR
S2-B4b-R-TL
S2-B4b-R-B

"""
