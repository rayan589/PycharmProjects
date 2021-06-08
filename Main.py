# Main.py
from datetime import datetime
import os
import pandas as pd
import DetectChars
import DetectPlates
import cv2

# module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def main():

    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()     # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")              # show error message
        return                                                          # and exit program
    # end if

    imgOriginalScene  = cv2.imread("/Users/macbookpro/Downloads/OpenCV_3_License_Plate_Recognition_Python-master/LicPlateImages/2.png")               # open image

    if imgOriginalScene is None:                            # if image was not read successfully
        print("\nerror: image not read from file \n\n")     # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    cv2.imshow("imgOriginalScene", imgOriginalScene)            # show scene image

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:                                                       # else
                # if we get in here list of possible plates has at leat one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print("\nno characters were detected\n\n")      # show message
            return                                          # and exit program
        # end if


        print("\nlicense plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out


        cv2.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file

        df = pd.read_excel('/Users/macbookpro/PycharmProjects/OpenCV_3_License_Plate_Recognition_Python/Database.xlsx')
        if licPlate.strChars in df.LP.values:
           print("Access Authorized!")
        else:
            print("Access Denied!")
            date1 = datetime.now().strftime("at %I:%M:%S_%p on %m/%d/%Y")
            mp = "\nLicence plate number: ",licPlate.strChars, f" Tried to enter {date1}\n"

            file1 = open("/Users/macbookpro/PycharmProjects/OpenCV_3_License_Plate_Recognition_Python/LP_Timeline.txt", "a")
            file1.write("".join(mp))
            file1.close()


        for i in df.index:
            if licPlate.strChars in df['LP'][i]:
                print("Welcome", df['Name'][i], "!")
                date = datetime.now().strftime("at %I:%M:%S_%p on %m/%d/%Y")
                gh="\n",df['Name'][i], f" Entered {date}\n"

                file1 = open("/Users/macbookpro/Documents/LP_Timeline.txt", "a")
                file1.write("".join(gh))
                file1.close()
    # end if else

    cv2.waitKey(0)					# hold windows open until user presses a key

    return





# end main


###################################################################################################
if __name__ == "__main__":
    main()


















