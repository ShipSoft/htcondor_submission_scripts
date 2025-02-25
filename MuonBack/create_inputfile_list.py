import ROOT
import glob
import csv

def process_files():
    
    eventsPerJob=50000
    
    # Match all files in the directory
    preproduction = "/eos/experiment/ship/data/Mbias/background-prod-2018/pythia8_Geant4_10.0_withCharmandBeauty*_mu.root"
    files = glob.glob(preproduction)

    total_entries=0
        
    with open('inputfile_list_1spill.txt', 'w') as filekey: 
        csvwriter = csv.writer(filekey)
        file_rows=[]
        for file in files:
            #print(f"{file} has {tree.GetEntries()} entries")
            file_in = ROOT.TFile.Open(file,'read')
            tree = file_in.Get("cbmsim")
            
            total_entries+=tree.GetEntries()

            nevents_to_read=tree.GetEntries()
            startEvent=0
            while nevents_to_read >= eventsPerJob:
    
                #csvwriter.writerow([file,startEvent,eventsPerJob])
                file_rows.append([file, startEvent, eventsPerJob])
                #print(file,startEvent,eventsPerJob)
                nevents_to_read -= eventsPerJob
                startEvent += eventsPerJob
            
            file_rows.append([file, startEvent, nevents_to_read-1])
            print(file,startEvent,nevents_to_read-1)
            
            file_in.Close()
        for i in range(1):#10spill
            csvwriter.writerows(file_rows)  

    print(f"total_entries: {total_entries}")
        

if __name__ == "__main__":
    process_files()
