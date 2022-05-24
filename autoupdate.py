import requests
import os
import threading


class TimedOut(Exception):
    pass


class UpdateThread(threading.Thread):
    def __init__(self, updater):
        super().__init__()
        self.updater = updater

    def run(self):
        self.updater.request = requests.get("https://github.com/Starcraft426/TowerDefense/releases")


class Updater:
    def __init__(self):
        self.current_version = "v1.2-beta"
        print("")
        self.skip = False
        self.request = None
        try:
            timer = 0
            thread = UpdateThread(self)
            thread.start()
            thread.join(20.0)
            if self.request:
                htmlcontent = self.request.text
            else:
                raise TimedOut

            self.commands = htmlcontent.split("<pre>")[1:]
            self.commands = [a.split("</pre>")[0] for a in self.commands]
            self.commands = [a.split("\n") for a in self.commands]
            self.commands.sort(reverse=False)
            self.versions = [a[0].split("VERSION ")[-1] for a in self.commands]

            self.versions_to_update = None
            self.initial_path = os.getcwd()

            self.update()
        except requests.exceptions.ProxyError:
            print("Cannot connect the proxy.")
            print("Skipping...")
        except requests.exceptions.SSLError:
            print("An SSL error as occured whle connecting to the database")
            print("Skipping...")
        except TimedOut:
            print("Maximum connection time reached.")
            print("Skipping...")

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
                            except Exception as e:
                                print(f"An error as occurred modifying {b[1]} at {b[3]}: {e}")
                    elif b[0] == "REMOVE":
                        if len(b) > 2:
                            if os.path.exists(f"{b[3]}{b[1]}"):
                                if b[1][-1] == "/":
                                    os.rmdir(f"{b[3]}{b[1][:-1]}")
                                    print(f"sucessfully removed {b[1]} at {b[3]}")
                                else:
                                    os.remove(f"{b[3]}{b[1]}")
                                    print(f"sucessfully removed {b[1]} at {b[3]}")
                            else:
                                if len(b) > 2:
                                    print(f"{b[1]} not found at {b[3]}")
                                else:
                                    print(f"{b[1]} not found on root")
                        else:
                            if os.path.exists(f"{b[1]}"):
                                if b[1][-1] == "/":
                                    os.rmdir(f"{b[1][:-1]}")
                                    print(f"sucessfully removed {b[1]}")
                                else:
                                    os.remove(f"{b[1]}")
                                    print(f"sucessfully removed {b[1]}")
                            else:
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
            print("\n===== Finished to update the game =====\n")
        else:
            print("The game is up to date")


def raise_exeption():
    raise TimedOut


if __name__ == "__main__":
    Updater()
