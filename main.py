from data.voirie import get_voirie
from data.filter import filter_impasses


def main():
    G = get_voirie()
    G_propre = filter_impasses(G)


if __name__ == "__main__":
    main()
