from graph import stream_graph_updates, graph


def main():
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            print("\nExiting...")
            break
        if user_input.lower() in ("exit", "quit", "q", "bye"):
            break
        stream_graph_updates(user_input)


if __name__ == "__main__":
    main()
