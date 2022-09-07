import ast
import symtable
import astpretty
import os


project_file_dict = {}

def gen_project_import_map(root_dir: str) -> None:
    if not os.path.isdir(root_dir):
        print("ERROR: %s is not a directory." % root_dir)
        return

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            filename, ext = os.path.splitext(file)
            if ext != ".py":
                continue
            path = os.path.join(root, file)
            import_path = os.path.join(root.lstrip("./"), filename).replace("/", ".")

            assert import_path not in project_file_dict
            project_file_dict[import_path] = path


def gen_ast(path: str) -> ast.AST:
    file_ast = None
    try:
        src = open(path, "r")
        file_ast = ast.parse(src.read(), "ast.log", "exec")
    except Exception as e:
        print(file, e)
    return file_ast


def parse_import_symbol(path: str) -> dict:
    file_ast = gen_ast(path)
    if not file_ast:
        return {}

    import_nodes = []
    for node in (n for n in file_ast.body if isinstance(n, ast.ImportFrom)):
        import_nodes.append(node)

    import_list = []
    for node in import_nodes:
        module = node.module
        level = node.level
        lineno = node.lineno
        names = [alias.name for alias in node.names]
        import_list.append({"path":path, "module": module, "lineno": lineno,
                            "level":level, "names":names})

    # print("import_list: ", import_list)
    return import_list


def parse_export_symbol(symbols:dict) -> dict:
    if not symbols:
        return {}

    module = symbols["module"]
    if module in project_file_dict:
        path = project_file_dict[module]
        invalid_symbols = check_symbols(path, symbols)
        if len(invalid_symbols) > 0:
            print("[INVALID] %s:%s %s"
                  %(symbols["path"], symbols["lineno"], invalid_symbols))

        return {"path": symbols["path"], "invalid_import": invalid_symbols}


def check_symbols(path: str, symbols:dict) -> dict:
    file_symtable = None
    try:
        src = open(path, "r").readlines()
        src = "".join(src)
        file_symtable = symtable.symtable(src, path, "exec")
    except Exception as e:
        print(file, e)
    if not file_symtable:
        return {}

    invalid_symbols = []
    for name in symbols["names"]:
        if file_symtable.lookup(name).is_namespace():
            # print("namespace: ", name)
            pass
        else:
            # print("not namespace: ", name)
            invalid_symbols.append(name)
    return invalid_symbols

 

if __name__ == "__main__":
    # file_ast = gen_ast("source.py")
    # astpretty.pprint(file_ast)
    # exit()

    root_dir = "."
    gen_project_import_map(root_dir)

    file_list = [
        "imp.py",
    ]
    for path in file_list:
        import_list = parse_import_symbol(path)
        for item in import_list:
            parse_export_symbol(item)
            
