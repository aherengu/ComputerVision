{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 22,
   "id": "bd9bc1cc-3858-4168-8e52-80c285cdafdc",
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "id": "bf725c38-f799-490f-b988-043aac9f257d",
   "metadata": {},
   "outputs": [],
   "source": [
    "road=cv2.imread(\"DATA/road_image.jpg\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "id": "283101f2-e6c7-44bf-857e-0722e67b3756",
   "metadata": {},
   "outputs": [],
   "source": [
    "road_copy=road.copy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "id": "fcdad40f-3fc3-455d-a2b1-090a4ab9c119",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(600, 800)"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "road_copy.shape[:2]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 26,
   "id": "47e46bf4-1d2b-4726-b11f-9e3773ce3918",
   "metadata": {},
   "outputs": [],
   "source": [
    "marker_image=np.zeros(road_copy.shape[:2],dtype=np.int32)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "id": "c7ea818b-dcc1-4590-9499-5c70a8948663",
   "metadata": {},
   "outputs": [],
   "source": [
    "segments=np.zeros(road_copy.shape,dtype=np.uint8)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 28,
   "id": "d480c3fd-feca-4f23-b65a-0fe8d85a6dfc",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(600, 800)"
      ]
     },
     "execution_count": 28,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "marker_image.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 29,
   "id": "fc2f21d7-fbb9-46e9-81e8-2ad397ef2734",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(600, 800, 3)"
      ]
     },
     "execution_count": 29,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "segments.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 30,
   "id": "2a2fb524-9e1d-4bdb-955d-584ddadcb587",
   "metadata": {},
   "outputs": [],
   "source": [
    "from matplotlib import cm"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 31,
   "id": "6924371a-4cbe-4b11-b386-834022c73c51",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1.0)"
      ]
     },
     "execution_count": 31,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "cm.tab10(0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 32,
   "id": "78f92bbd-1d1d-428a-979f-81ee826cfcea",
   "metadata": {},
   "outputs": [],
   "source": [
    "def create_rgb(i):\n",
    "    return tuple(np.array(cm.tab10(i)[:3])*255) #for opencv u can convert to bgr"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 33,
   "id": "3fa1644c-f19b-4eae-8c05-fb6c4fc4192c",
   "metadata": {},
   "outputs": [],
   "source": [
    "colors=[]\n",
    "for i in range(10):\n",
    "    colors.append(create_rgb(i))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "557c79ca-ce09-4fa5-bddb-5177ef354c5e",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[(31.0, 119.0, 180.0),\n",
       " (255.0, 127.0, 14.0),\n",
       " (44.0, 160.0, 44.0),\n",
       " (214.0, 39.0, 40.0),\n",
       " (148.0, 103.0, 189.0),\n",
       " (140.0, 86.0, 75.0),\n",
       " (227.0, 119.0, 194.0),\n",
       " (127.0, 127.0, 127.0),\n",
       " (188.0, 189.0, 34.0),\n",
       " (23.0, 190.0, 207.0)]"
      ]
     },
     "execution_count": 34,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "colors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 35,
   "id": "f1735802-d264-4692-8734-5327ee6fd79e",
   "metadata": {},
   "outputs": [],
   "source": [
    "n_markers=10 #0-9\n",
    "current_marker=1\n",
    "marks_updated=False"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 36,
   "id": "472e5e3b-f9cc-4807-8959-85484c467402",
   "metadata": {},
   "outputs": [],
   "source": [
    "def mouse_callback(event,x,y,flags,param):\n",
    "    global marks_updated\n",
    "    if event== cv2.EVENT_LBUTTONDOWN:\n",
    "        cv2.circle(marker_image,(x,y),10,current_marker,-1)\n",
    "        cv2.circle(road_copy,(x,y),10,colors[current_marker],-1)\n",
    "        marks_updated=True"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 37,
   "id": "e20b81f0-4496-47af-9a2f-1142244c908c",
   "metadata": {},
   "outputs": [],
   "source": [
    "cv2.namedWindow(\"Image\")\n",
    "cv2.setMouseCallback(\"Image\",mouse_callback)\n",
    "\n",
    "while True:\n",
    "    cv2.imshow(\"Watershed Segments\",segments)\n",
    "    cv2.imshow(\"Image\",road_copy)\n",
    "    k=cv2.waitKey(1)\n",
    "    if k==27:\n",
    "        break\n",
    "    elif k==ord(\"c\"):\n",
    "        road_copy=road.copy()\n",
    "        marker_image=np.zeros(road.shape[:2],dtype=np.int32)\n",
    "        segments=np.zeros(road.shape,dtype=np.uint8)\n",
    "    elif k>0 and chr(k).isdigit():\n",
    "        current_marker=int(chr(k))\n",
    "\n",
    "\n",
    "\n",
    "    if marks_updated:\n",
    "        marker_image_copy=marker_image.copy()\n",
    "        cv2.watershed(road,marker_image_copy)\n",
    "        segments=np.zeros(road.shape,dtype=np.uint8)\n",
    "        for color_ind in range(n_markers):\n",
    "            segments[marker_image_copy==(color_ind)]= colors[color_ind]\n",
    "\n",
    "\n",
    "\n",
    "\n",
    "cv2.destroyAllWindows()\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "e9cc6a23-adb8-40bb-b681-c00f1ae38b3d",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:python-cvcourse]",
   "language": "python",
   "name": "conda-env-python-cvcourse-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
