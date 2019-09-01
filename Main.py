import os
CUDA_VISIBLE_DEVICES=0
os.environ["CUDA_VISIBLE_DEVICES"] = "0" # set gpu number

keep_going = True
while keep_going:
    option = 0
    while option <= 0 or option >= 6:
        print(" _________________________________________")
        print("| Select Option:                          |")
        print("|\t1. Make Prediction on Video       |")
        print("|\t2. Real-time Predictions          |")
        print("|\t3. Evaluate                       |")
        print("|\t4. Train                          |")
        print("|\t5. Generate dataset list files    |")
        print("|_________________________________________|")

        print("> ", end="")
        option = int(input())



    if option == 1:  # deploy
        print("Enter the path to video: ")
        print("> ", end="")
        video_path = input()
        print("Enter path to save results (Press Enter to save at default location): ")
        print("> ", end="")
        results_path = input()
        if results_path == "":
            os.system("python Deploy.py " + "\"" + video_path + "\"")
        else:
            os.system("python Deploy.py " + "\"" + video_path + "\"" + " " + "\"" + results_path + "\"")
        print("Deploying:")

    if option == 2:  # deploy
        print("********************************")
        print("Activating real-time predictions")
        print("********************************")
        os.system("python DeployLive.py")


    elif option == 3:  # evaluate
        print("Enter the path to dataset test file (can be generated using same script) OR press enter to load it from "
              "default location:")
        print("> ", end="")
        path = input()
        if path == "":
            path = r"D:\Internship\Codes\ViolenceDetection\datalists\evallist.txt"
        print("Enter frame threshold (number of continues frames required to predict violence) "
              "OR Press Enter to find threshold:")
        print("> ", end="")
        threshold = input()
        print("Evaluating:")
        os.system("python Evaluate.py " + "\"" + path + "\"" + " " + "\"" + threshold + "\"")

    elif option == 4:  # train
        print("Training:\n")
        os.system("python Train.py")

    elif option == 5:
        print("Enter the path to dataset folder containing Violence and Nonviolence named folders "
              "(Press Enter if it is stored in default folder):")
        print("> ", end="")
        path_to_dataset = input()
        if path_to_dataset == "":
            os.system("python .\\tools\\Train_Val_Test_spliter.py")
        elif path_to_dataset != "":
            os.system("python .\\tools\\Train_Val_Test_spliter.py " + "\"" + path_to_dataset + "\"")
        print("Successfully generated the dataset list files.")

print("Do you want to perform another operation? (Y/N)")
choice = input().lower()
if choice == "t":
    keep_going = True
else:
    keep_going = False

