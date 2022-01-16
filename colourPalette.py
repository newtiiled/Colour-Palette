import sys
import os
import click
import math
import numpy as py
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans

py.random.seed(0)

def makePalette(orgImage, outImage, numColours):
    if (not numColours.isdigit()):
        raise("The number of colours must be an integer")
    numCo = int(numColours)

    img = Image.open(orgImage)
    
    # Resize image if too large
    size = img.size
    if (size[0] > 500 and size[1] > 500):
        img = img.Image.resize((size[0]/2, size[1]/2))
    width, height = img.size
    
    # Convert image to 3D array
    arrImg = py.array(img)

    # Convert 3D array to 2D array
    reds, greens, blues = [], [], []
    for line in arrImg:
        for pixel in line:
            reds.append(pixel[0])
            greens.append(pixel[1])
            blues.append(pixel[2])

    # Make dataframe of all reds, greens, blues in image
    data = pd.DataFrame({"R" : reds, "G" : greens, "B" : blues})

    # Use k-means clustering to find dominant colours within image
    kmeans = KMeans(n_clusters=numCo, random_state=0).fit(data)
    rawColours = kmeans.cluster_centers_

    # Convert colours from cluster in proper int form
    colours = []
    for colour in rawColours:
        colours.append((math.floor(colour[0]),
                        math.floor(colour[1]),
                        math.floor(colour[2])))

    # Ready new palette image
    newWidth = numCo * 100
    newHeight = 100
    palette = Image.new('RGB', (newWidth, newHeight), (255, 255, 255))

    # Paste colours onto blank image
    for i in range(len(colours)):
        tempImg = Image.new('RGB', (100, 100), colours[i])
        palette.paste(tempImg, (i * 100, 0))
    
    palette.save(outImage)

def colourPalette(orgImage, numColours):
    if (not os.path.exists(orgImage)):
        raise("The image does not exist")

    filepath = orgImage.split("/")

    # Get name of image
    path = ""
    for i in range(len(filepath)):
        if (i == len(filepath) - 1):
            title = filepath[i]
        else:
            path = path + filepath[i] + "/"
    
    name, typeImg = title.split(".")

    outImage = path + name + "_palette." + typeImg
    makePalette(orgImage, outImage, numColours)

def main(orgImage, numColours):
    try:
        colourPalette(orgImage, numColours)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])