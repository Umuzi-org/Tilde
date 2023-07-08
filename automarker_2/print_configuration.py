from automarker.marker import get_all_marker_configs


def run():
    for configuration in get_all_marker_configs():
        print(
            f"{configuration.title}[{configuration.content_item_id}] {configuration.flavours} {configuration.status}"
        )


if __name__ == "__main__":
    run()
