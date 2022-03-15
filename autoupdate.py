import requests
import os


class Updater:
    def __init__(self):
        self.current_version = "v1.2-beta"
        print("")
        r = requests.get("https://github.com/Starcraft426/TowerDefense/releases")
        htmlcontent = r.text

        self.commands = htmlcontent.split("<pre>")[1:]
        self.commands = [a.split("</pre>")[0] for a in self.commands]
        self.commands = [a.split("\n") for a in self.commands]
        self.commands.sort(reverse=False)
        self.versions = [a[0].split("VERSION ")[-1] for a in self.commands]

        self.versions_to_update = None
        self.initial_path = os.getcwd()

        self.update()

    def update(self):
        try:
            file = open("testfile.txt", "w+")
            file.write("test")
            file.close()
            os.remove("testfile.txt")
        except:
            print("Update failed: Unable to modify files on the current directory")
            print("Skipping...")
            return

        if self.current_version != self.versions[-1]:
            self.versions_to_update = self.versions[self.versions.index(self.current_version)+1:]
            self.commands = self.commands[self.versions.index(self.current_version)+1:]
            print(self.commands)
            for a in range(len(self.versions_to_update)):
                print(f"\n\n=====  Updating to version: {self.versions_to_update[a]}  =====\n")
                for b in self.commands[a]:
                    b = b.split(" ")
                    if b[0] == "ADD":
                        if len(b) > 2:
                            r_file = requests.get(
                                f"https://raw.githubusercontent.com/Starcraft426/TowerDefense/main/{b[3]}" +
                                f"{b[1]}?raw=true")
                        else:
                            r_file = requests.get(
                                f"https://raw.githubusercontent.com/Starcraft426/TowerDefense/main/{b[1]}?raw=true")
                        filecontent = r_file.text
                        if filecontent == "404: Not Found":
                            print("Error, file not found, file had been probably deleted")
                        else:
                            if len(b) > 2:
                                for path in b[3].split("/")[:-1]:
                                    if not os.path.exists(path):
                                        os.makedirs(path)
                                    os.chdir(path)
                            file = open(b[1], "w+")
                            file.writelines(filecontent.split("\n"))
                            file.close()
                            print(f"Sucessfully added {b[1]} at {b[3]}")
                            os.chdir(self.initial_path)
                    elif b[0] == "MODIFY":
                        if len(b) > 2:
                            r_file = requests.get(
                                f"https://raw.githubusercontent.com/Starcraft426/TowerDefense/main/{b[3]}" +
                                f"{b[1]}?raw=true")
                        else:
                            r_file = requests.get(
                                f"https://raw.githubusercontent.com/Starcraft426/TowerDefense/main/{b[1]}?raw=true")
                        filecontent = r_file.text
                        if filecontent == "404: Not Found":
                            print("Error, file not found, file had been probably deleted or may be missing")
                        else:
                            try:
                                if len(b) > 2:
                                    os.chdir(b[3])
                                    file = open(b[1], "w")
                                    file.writelines(filecontent.split("\n"))
                                    file.close()
                                    os.chdir(self.initial_path)
                            except:
                                print(f"An error as occurred modifying {b[1]} at {b[3]}")
                    elif b[0] == "REMOVE":
                        try:
                            if len(b) > 2:
                                os.remove(f"{b[3]}{b[1]}")
                                print(f"sucessfully removed {b[1]} at {b[3]}")
                            else:
                                os.remove(f"{b[1]}")
                                print(f"sucessfully removed {b[1]}")
                            
                        except:
                            if len(b) > 2:
                                print(f"{b[1]} not found at {b[3]}")
                            else:
                                print(f"{b[1]} not found on root")
                print(f"Finished to update to {self.versions_to_update[a]}")
            r_file = requests.get("https://raw.githubusercontent.com/Starcraft426/TowerDefense/main/autoupdate.py" +
                                  "?raw=true")
            filecontent = r_file.text
            if not filecontent == "404: Not Found":
                file = open("autoupdate.py", "w")
                file.writelines(filecontent.split("\n"))
                file.close()
        else:
            print("The game is up to date")


if __name__ == "__main__":
    Updater()
