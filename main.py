from views.main_view import MainView


def main():
    exit = False
    instanceMainView = MainView()
    while not exit:
        exit = instanceMainView.show_menu()


if __name__ == "__main__":
    main()
