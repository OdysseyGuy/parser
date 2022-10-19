class Node:
    def __init__(self) -> None:
        pass


class SymbolTable(dict[str, list[Node]]):
    '''
    Table for indentifier lookup. Maps a string to `Node`.
    '''
    def insert(self, name: str, node: Node) -> None:
        self.setdefault(name, []).append(node)


    def delete(self, name: str):
        return self[name].pop()


    def lookup(self, name: str) -> Node | None:
        nodes = self.get(name)
        if nodes:
            return nodes[-1]
        return None
