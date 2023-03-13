import cv2

# Load the 4-channel PNG image
img = cv2.imread("resources/pong_table.png", cv2.IMREAD_UNCHANGED)

# Check the number of channels
if img.shape[2] == 4:
    # Split the channels into 4 separate arrays
    b, g, r, a = cv2.split(img)

    # Merge the first 3 channels (Blue, Green, Red) to form a 3-channel image
    img = cv2.merge([b, g, r])

# Save the 3-channel image
cv2.imwrite("resources/pong_table_3_channel.png", img)
