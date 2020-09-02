# this script goes through the very general 'pants' directory and
# seperates more specific types of pants 

import os, sys, shutil

pant_type_paths = {
    'jeans':'jeans',
    'sweatpants':'sweatpants',
    'dress_pants':'dress_pants',
    'pants':'pants'
}

jeans_kw = [
    "denim",
    "distressed",
    "jean"
]

dress_pants = [
    "suit",
    "dress",
    "tux"
]

sweatpants_kw = [
    "track",
    "fleece",
    "drawstring",
    "training",
    "lounge",
    "sleep",
    "wind",
    "warm-up",
    "tricot",
    "soccer",
    "active",
    "run"
]

# makes sure the expected directories already exist or creates them if 
# they don't
def dirPrep(outerDir):
    cwd = os.getcwd()
    for key, value in pant_type_paths.items():
        curDir = outerDir + value
        if not (os.path.isdir(curDir)):
            os.mkdir(curDir)
        

# moves specified image to specified directory (category of pants)
def moveImage(imagePath, directory):
    print(imagePath, directory)

def main():
    if (len(sys.argv)!=2 or sys.argv[1][len(sys.argv[1])-1]!='/'):
        print(f"USAGE: {__file__} [outerDirectory]/")
        exit()
    outerDir = os.getcwd()+'/'+sys.argv[1]
    pathToPants = outerDir+'pants'
    if(os.path.isdir(pathToPants)):
        for filename in os.listdir(pathToPants):
            if any(x in filename.lower() for x in jeans_kw):
                shutil.move(sys.argv[1]+'pants/'+filename,sys.argv[1]+'jeans/')
            elif any(x in filename.lower() for x in sweatpants_kw):
                shutil.move(sys.argv[1]+'pants/'+filename,sys.argv[1]+'sweatpants/')
            elif any(x in filename.lower() for x in dress_pants):
                shutil.move(sys.argv[1]+'pants/'+filename,sys.argv[1]+'dress_pants/')

main()