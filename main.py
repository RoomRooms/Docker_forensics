import docker
import sys
import os
import re
import datetime


def containers_list(client):
    option = input("Do you want to see all the containers?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        containers = client.containers.list(all=True)
    else:
        containers = client.containers.list()

    for container in containers:
        print(f"ID : {container.short_id}")
        print(f"Name : {container.name}")
        print(f"Image : {container.image}")
        print(f"Status : {container.status}\n")

    option = input("Do you want to save list?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        os.makedirs("DF/Containers/", exist_ok=True)
        with open("DF/Containers/Containers_list.txt", "w") as f:
            for container in containers:
                f.write(f"ID : {container.short_id}\n")
                f.write(f"Name : {container.name}\n")
                f.write(f"Image : {container.image}\n")
                f.write(f"Status : {container.status}\n\n")


def container_info(client):
    c_id = input("Enter the Container ID\n> ")
    container = client.containers.get(c_id)
    os.makedirs("DF/Containers/"+c_id, exist_ok=True)
    with open("DF/Containers/"+c_id+"/Information.txt", 'w') as f:
        info = container.attrs

        option = input(f"Do you want to show the {c_id} information?\n> ")
        if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
            for key, value in info.items():
                print(f"{key}: {value}")
            print()

        for key, value in info.items():
            f.write(f"{key}: {value}\n")


def container_export(client):
    c_id = input("Enter the Container ID\n> ")
    container = client.containers.get(c_id)

    os.makedirs("DF/Containers/"+c_id, exist_ok=True)
    with open("DF/Containers/"+c_id+"/"+c_id+".tar", "wb") as f:
        bits = container.export()
        for chunk in bits:
            f.write(chunk)


def container_process(client):
    c_id = input("Enter the Container ID\n> ")
    container = client.containers.get(c_id)
    ps = container.top()

    os.makedirs("DF/Containers/"+c_id, exist_ok=True)
    with open("DF/Containers/"+c_id+"/process_info.txt", "w") as f:
        for i in ps['Titles']:
            f.write(f"{i}\t\t")
        f.write(f"\n")
        for p in ps["Processes"]:
            for i in p:
                f.write(f"{i}\t\t")
            f.write(f"\n")

    option = input(f"Do you want to show the {c_id} information?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for i in ps['Titles']:
            print(f"{i}\t\t", end="")
        print(f"\n")
        for p in ps["Processes"]:
            for i in p:
                print(f"{i}\t", end="")
            print(f"\n")


def container_logs(client):
    c_id = input("Enter the Container ID\n> ")
    container = client.containers.get(c_id)

    c_log = container.logs()
    c_log = c_log.decode('utf-8')
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (except CSI)
            [@-Z\\-_]
        |     # or [ for CSI, followed by a control sequence
            \[
            [0-?]*  # parameter bytes
            [ -/]*  # intermediate bytes
            [@-~]   # final byte
        )
    ''', re.VERBOSE)

    c_log = ansi_escape.sub("", c_log)
    while '\b' in c_log:
        c_log = re.sub(r'.\b', '', c_log, count=1)

    os.makedirs("DF/Containers/"+c_id, exist_ok=True)
    with open("DF/Containers/"+c_id+"/Logs.txt", "w") as f:
        f.write(f"{c_log}")

    option = input(f"Do you want to show the {c_id} information?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        print(c_log)


def containers(client):
    Menu_actions = {
        1: containers_list,
        2: container_info,
        3: container_export,
        4: container_process,
        5: container_logs,
    }

    Menu = ("Select Menu.\n"
            "1. Containers List\n"
            "2. Container Info\n"
            "3. Container Export\n"
            "4. Container Process\n"
            "5. Container Logs"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            containers(client)

    except ValueError:
        print("It's not number.")
        containers(client)


def images_list(client):
    images = client.images.list()

    for img in images:
        print(f"{img.tags[0]}")
    print()

    option = input("Do you want to save list?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        os.makedirs("DF/Images/", exist_ok=True)
        with open("DF/Images/Images_list.txt", "w") as f:
            for img in images:
                f.write(f"{img.tags[0]}\n")


def image_history(client):
    i_id = input("Enter the Image name\n> ")
    image = client.images.get(i_id)
    history = image.history()
    s_name = i_id.replace(":", "-")

    os.makedirs("DF/Images/" + s_name, exist_ok=True)
    with open("DF/Images/" + s_name + "/History.txt", "w") as f:
        for i in history:
            f.write(f"{i}\n")

    option = input(f"Do you want to show the {image.tags[0]} history?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for i in history:
            print(f"{i}")
        print()


def image_inspect(client):
    i_id = input("Enter the Image name\n> ")
    image = client.images.get(i_id)
    details = image.attrs

    s_name = i_id.replace(":", "-")
    os.makedirs("DF/Images/"+s_name, exist_ok=True)
    with open("DF/Images/"+s_name+"/Inspect.txt", "w") as f:
        for key, value in details.items():
            f.write(f"{key} : {value}\n")

    option = input(f"Do you want to show the {image.tags[0]} inspect?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for key, value in details.items():
            print(f"{key} : {value}")
        print()


def image_export(client):
    i_id = input("Enter the Image name\n> ")
    image = client.images.get(i_id)
    s_name = i_id.replace(":", "-")

    os.makedirs("DF/Images/" + s_name, exist_ok=True)
    with open("DF/Images/"+s_name+"/"+s_name+".tar", "wb") as f:
        for chunk in image.save():
            f.write(chunk)


def images(client):
    Menu_actions = {
        1: images_list,
        2: image_history,
        3: image_inspect,
        4: image_export,
    }

    Menu = ("Select Menu.\n"
            "1. Images_list\n"
            "2. Image_history\n"
            "3. Image_inspect\n"
            "4. Image_export"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            images(client)

    except ValueError:
        print("It's not number.")
        images(client)


def networks_list(client):
    networks = client.networks.list()

    for network in networks:
        print(f"{network.name} : {network.short_id}")
    print()

    option = input("Do you want to save list?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        os.makedirs("DF/Networks/", exist_ok=True)
        with open("DF/Networks/Networks_list.txt", "w") as f:
            for network in networks:
                f.write(f"{network.name} : {network.short_id}\n")


def network_inspect(client):
    n_id = input("Enter the Network name\n> ")
    network = client.networks.get(n_id)
    details = network.attrs

    os.makedirs("DF/Networks/" + n_id, exist_ok=True)
    with open("DF/Networks/" + n_id + "/Inspect.txt", "w") as f:
        for key, value in details.items():
            f.write(f"{key} : {value}\n")

    option = input(f"Do you want to show the {network.name} inspect?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for key, value in details.items():
            print(f"{key} : {value}")
        print()


def networks(client):
    Menu_actions = {
        1: networks_list,
        2: network_inspect,
    }

    Menu = ("Select Menu.\n"
            "1. Networks_list\n"
            "2. Network_inspect"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            networks(client)

    except ValueError:
        print("It's not number.")
        networks(client)


def volumes_list(client):
    volumes = client.volumes.list()
    for volume in volumes:
        print(f"{volume.name}")
    print()

    option = input("Do you want to save list?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        os.makedirs("DF/Volumes/", exist_ok=True)
        with open("DF/Volumes/Volumes_list.txt", "w") as f:
            for volume in volumes:
                f.write(f"{volume.name}\n")


def volume_inspect(client):
    v_id = input("Enter the Volume name\n> ")
    volume = client.volumes.get(v_id)
    details = volume.attrs

    os.makedirs("DF/Volumes/" + volume.name, exist_ok=True)
    with open("DF/Volumes/" + volume.name + "/Inspect.txt", "w") as f:
        for key, value in details.items():
            f.write(f"{key} : {value}\n")

    option = input(f"Do you want to show the {volume.name} inspect?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for key, value in details.items():
            print(f"{key} : {value}")
        print()

def volumes(client):
    Menu_actions = {
        1: volumes_list,
        2: volume_inspect,
    }

    Menu = ("Select Menu.\n"
            "1. Volumes_list\n"
            "2. Volume_inspect"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            volumes(client)

    except ValueError:
        print("It's not number.")
        volumes(client)


def plugins_list(client):
    print("Sorry, not yet")
    # plugins = client.plugins.list()
    # for plugin in plugins:
    #     print(f"{plugin.name}")
    # print()

    # option = input("Do you want to save list?\n> ")
    # if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
    #     os.makedirs("DF/Plugins/", exist_ok=True)
    #     with open("DF/Plugins/Plugins_list.txt", "w") as f:
    #         for plugin in plugins:
    #             f.write(f"{plugin.name}\n")


def plugin_inspect(client):
    print("Sorry, not yet")
    # p_id = input("Enter the Plugin name\n> ")
    # plugin = client.plugins.get(p_id)
    # details = plugin.attrs
    #
    # os.makedirs("DF/Plugins/" + plugin.name, exist_ok=True)
    # with open("DF/Plugins/" + plugin.name + "/Inspect.txt", "w") as f:
    #     for key, value in details.items():
    #         f.write(f"{key} : {value}\n")
    #
    # option = input(f"Do you want to show the {plugin.name} inspect?\n> ")
    # if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
    #     for key, value in details.items():
    #         print(f"{key} : {value}")
    #     print()


def plugins(client):
    Menu_actions = {
        1: plugins_list,
        2: plugin_inspect,
    }

    Menu = ("Select Menu.\n"
            "1. Plugins_list\n"
            "2. Plugin_inspect"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            plugins(client)

    except ValueError:
        print("It's not number.")
        plugins(client)


def docker_daemon_system_information(client):
    sys_info = client.info()

    os.makedirs("DF/System/", exist_ok=True)
    with open("DF/System/System_info.txt", "w") as f:
        for key, value in sys_info.items():
            f.write(f"{key} : {value}\n")

    option = input(f"Do you want to show the system information?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        for key, value in sys_info.items():
            print(f"{key} : {value}")
        print()


def docker_version(client):
    ver_info = client.version()

    text = ""
    for ver, info in ver_info.items():
        if isinstance(info, list):
            text += f"{ver} : \n"
            for inf in info:
                if isinstance(inf, dict):
                    for key, value in inf.items():
                        if isinstance(value, dict):
                            text += f"\t{key} : \n"
                            for k, v in value.items():
                                text += f"\t\t{k} : {v}\n"
                        else:
                            text += f"\t{key} : {value}\n"
                text += "\n"
        elif isinstance(info, dict):
            text += f"{ver} : \n"
            for key, value in info.items():
                text += f"\t{key} : {value}\n\n"
        else:
            text += f"{ver} : {info}\n"
    text += "\n"

    os.makedirs("DF/System", exist_ok=True)
    with open("DF/System/Version.txt", "w") as f:
        f.write(text)

    option = input(f"Do you want to show the Version information?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        print(text)


def docker_disk_information(client):
    disk = client.df()
    text = ""
    for key, value in disk.items():
        if isinstance(value, list):
            text += f"{key} : \n"
            for v in value:
                if isinstance(v, dict):
                    for k, v2 in v.items():
                        if isinstance(v2, list):
                            text += f"\t{k} : \n"
                            for v3 in v2:
                                if isinstance(v3, dict):
                                    for k2, v4 in v3.items():
                                        text += f"\t\t{k2} : {v4}\n"
                                else:
                                    text += f"\t\t{v3}\n"
                        elif isinstance(v2, dict):
                            text += f"\t{k} : \n"
                            for k2, v3 in v2.items():
                                if isinstance(v3, dict):
                                    text += f"\t\t{k2} : \n"
                                    for k3, v4 in v3.items():
                                        if isinstance(v4, dict):
                                            text += f"\t\t\t{k3} : \n"
                                            for k4, v5 in v4.items():
                                                text += f"\t\t\t\t{k4} : {v5}\n"
                                        else:
                                            text += f"\t\t\t{k3} : {v4}\n"
                                else:
                                    text += f"\t\t{k2} : {v3}\n"
                        else:
                            text += f"\t{k} : {v2}\n"
                text += "\n"
        else:
            text += f"{key} : {value}\n"
    text += "\n"

    os.makedirs("DF/System", exist_ok=True)
    with open("DF/System/Disk_info.txt", "w") as f:
        f.write(text)

    option = input(f"Do you want to show the disk information?\n> ")
    if option == "yes" or option == "Yes" or option == "Y" or option == 'y':
        print(text)


def live_docker_events(client):
    for event in client.events(decode=True):
        # 이벤트 발생 시간을 포맷팅
        event_time = datetime.datetime.utcfromtimestamp(event['time']).strftime('%Y-%m-%d %H:%M:%S')

        # 이벤트 정보를 출력
        print(f"Time: {event_time}")
        print(f"Type: {event['Type']}")
        print(f"Action: {event['Action']}")

        # Actor 정보 (이벤트를 발생시킨 주체)
        actor = event.get('Actor', {})
        actor_id = actor.get('ID', 'N/A')
        actor_attributes = actor.get('Attributes', {})

        print(f"Actor ID: {actor_id}")
        print(f"Actor Attributes: {actor_attributes}")
        print("-" * 60)


def system(client):
    Menu_actions = {
        1: docker_daemon_system_information,
        2: docker_version,
        3: docker_disk_information,
        4: live_docker_events,
    }

    Menu = ("Select Menu.\n"
            "1. docker_daemon_system_information\n"
            "2. docker_version\n"
            "3. docker_disk_information\n"
            "4. live_docker_events"
            )
    print(Menu)

    try:
        choice = int(input("> "))
        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            system(client)

    except ValueError:
        print("It's not number.")
        system(client)


def sys_exit(client):
    sys.exit(0)


def check_IP(IP):
    IPs, Port = IP.split(":")
    IP_Addr = map(int, IPs.split("."))

    for i in IP_Addr:
        if 0 > i or i > 255:
            return False

    if 0 > int(Port) or int(Port) > 65535:
        return False

    return True


def main():
    # IP = input("Enter target IP address and Port (ip:port)\n> ")
    # if not check_IP(IP):
    #     print("Error!\n"
    #           "please IP Address and Port number (IP:Port)")
    #     sys.exit(0)

    IP = "211.252.26.126:2375"
    client = docker.DockerClient(base_url='tcp://'+IP)

    Menu_actions = {
        1: containers,
        2: images,
        3: networks,
        4: volumes,
        5: plugins,
        6: system,
        7: sys_exit,
    }

    Menu = ("What do you want Info?\n"
            "1. Containers\n"
            "2. Images\n"
            "3. Networks\n"
            "4. Volumes\n"
            "5. Plugins\n"
            "6. System\n"
            "7. Exit")

    while True:
        print(Menu)
        try:
            choice = int(input("> "))
        except ValueError:
            print("It's not number.")
            continue

        action = Menu_actions.get(choice)
        if action:
            action(client)
        else:
            print("It's not on the menu.")
            continue

if __name__ == "__main__":
    main()