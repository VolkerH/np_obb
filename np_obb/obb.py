# Calculate oriented bounding boxes for sets of points
# and for binary mask images/label images
# Volker.Hilsenstein@monash.edu
# This is based on the following stackoverflow answer
# by stackoverflow user Quasiomondo (Mario Klingemann)
# https://stackoverflow.com/questions/32892932/create-the-oriented-bounding-box-obb-with-python-and-numpy

import numpy as np
import skimage.morphology

def get_obb_from_points(points):
    """ given a set of points, calculate the oriented bounding 
    box. 
    
    Parameters:
    points: numpy array of point coordinates with shape (n,2)
            where n is the number of points

    Output:
        tuple of corners, centre
    """
    # TODO: this could probably also be made to work 
    # in 3D with minimal changes

    
    cov_points = np.cov(points,y = None,rowvar = 0,bias = 1)
    v, vect = np.linalg.eig(cov_points)
    tvect = np.transpose(vect)

    #use the inverse of the eigenvectors as a rotation matrix and
    # rotate the points so they align with the x and y axes
    points_rotated = np.dot(points,np.linalg.inv(tvect))
    # get the minimum and maximum x and y 
    mina = np.min(points_rotated,axis=0)
    maxa = np.max(points_rotated,axis=0)
    diff = (maxa - mina)*0.5
    # the centre is just half way between the min and max xy
    center = mina + diff

    # get the 4 corners by subtracting and adding half the bounding boxes height and width to the center
    # TODO this can be made nicer
    corners = np.array([center+[-diff[0],-diff[1]],center+[diff[0],-diff[1]],center+[diff[0],diff[1]],center+[-diff[0],diff[1]],center+[-diff[0],-diff[1]]])
    # use the the eigenvectors as a rotation matrix and
    # rotate the corners and the center back
    corners = np.dot(corners,tvect)
    center = np.dot(center,tvect)

    return corners, center

def get_obb_from_labelim(label_im, labels=None):
    """ given a label image, calculate the oriented 
    bounding box of each connected component with 
    label in labels. If labels is None, all labels > 0
    will be analyzed.

    Parameters:
        label_im: numpy array with labelled connected components (integer)

    Output:
        obbs: dictionary of oriented bounding boxes. The dictionary 
        keys correspond to the respective labels
    """
    if labels is None:
        labels = set(np.unique(label_im)) - {0}
    results = {}
    for label in labels:
        results[label] = get_obb_from_mask(label_im == label)
    return results

def get_obb_from_mask(mask_im):
    """Oriented bounding box of object in binary mask image.
    
    This is done by finding the convex hull, then transforming 
    the pixel coordinates from the image into a list of
    points and then calling :func: `get_obb_from_points`
    
    Poor performance is expected if there are multiple objects
    in the mask image.
    
    Parameters:
        mask_im: binary numpy array
    """
    convex_hull = skimage.morphology.convex_hull_object(mask_im)
    points = np.argwhere(convex_hull > 0)
    return np_obb.get_obb_from_points(points)
