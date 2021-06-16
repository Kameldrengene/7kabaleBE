import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load Yolo
net = cv2.dnn.readNet("ModelFiles/yolo-obj_new.weights", "ModelFiles/yolo-obj.cfg")
classes = []
with open("ModelFiles/card.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread("real.jpg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
height, width, channels = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

net.setInput(blob)
outs = net.forward(output_layers)

# Showing informations on the screen
class_ids = []
confidences = []
boxes = []
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            # Object detected
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Rectangle coordinates
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
print(indexes)
font = cv2.FONT_HERSHEY_PLAIN

cards = []
diff = 75

for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[class_ids[i]]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
        cards.append((label, x, y, w, h))

        # if len(cards) > 1:
        for j in range(len(cards)):
            if cards[j][0] == label:
                if cards[j][1] < x:
                    cards.pop()
                    break
                elif x < cards[j][1]:
                    cards[j] = cards.pop()
                    break

                if cards[j][2] < y:
                    cards.pop()
                    break

print("Cards:")
print(cards)


# take second element for sort
def takeSecond(elem):
    return elem[1]


cards.sort(key=takeSecond)

pilecoords = []
deck = []
finspaces = []

# gnswidth = 0
# gnsheight = 0
# totalwidth = 0
# totalheight = 0
# for i in range(len(cards)):
#     totalwidth += cards[i][3]
#     totalheight+=cards[i][4]
# gnswidth = int(totalwidth/len(cards))
# gnsheight = int(totalheight/len(cards))

deckXYmin = (0,0)
deckXYmax = (int(width*1/3),int(height*1/3))
finspacesXYmin = ((int(width*(1/3)))+100,0)
finspacesXYmax = (width,int(height*(1/3)))

length = len(cards)
count = 0
while count < length:
    if cards[count][1] < deckXYmax[0] and cards[count][2] < deckXYmax[1]:
        deck.append(cards[count])
        cards.remove(cards[count])
        length = length - 1
        count = count - 1
    if cards[count][1] > finspacesXYmin[0] and cards[count][2] < finspacesXYmax[1]:
        finspaces.append(cards[count])
        cards.remove(cards[count])
        length = length - 1
        count = count - 1
    count = count + 1

print("Deck:")
print(deck)
print("Finspaces:")
print(finspaces)




xcoord = 0
offset = 100  # ret værdien efter størrelsen af billedet
exist = True

for i in range(len(cards)):
    if (xcoord < cards[i][1]):
        xcoord = cards[i][1]
        if len(pilecoords) == 0:
            pilecoords.append(xcoord)

        for j in range(len(pilecoords)):
            if pilecoords[j] + offset < xcoord:
                exist = False
            else:
                exist = True

        if not exist:
            pilecoords.append(xcoord)

        exist = True

print("Piles:")
print(len(pilecoords))  # antal piles
print(pilecoords)

def takeThird(elem):
    return elem[2]


cards.sort(key=takeThird)

piles = []
for i in range(len(pilecoords)):
    rightOff = pilecoords[i]+offset
    leftOff = pilecoords[i]-offset
    pile = []
    for j in range(len(cards)):
        if (cards[j][1] <= rightOff) and (cards[j][1] >= leftOff):
            pile.append(cards[j])
    piles.append(pile)

print("Cards in Piles:")
print(piles)
plt.imshow(img)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
