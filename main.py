import ast
import symtable
# import astpretty
import os
import pprint

TEST_DJANGO = True

if TEST_DJANGO:
    from django_config import *
else:
    from config import *


# global variables
project_file_dict = {}
not_found_modules = set()

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
            if root.startswith(ROOT_DIR):
                import_root = root[len(ROOT_DIR):]
                import_path = os.path.join(import_root, filename).replace("/", ".")
                assert import_path not in project_file_dict
                project_file_dict[import_path] = path

def relative_to_absolute(symbol:dict):
    """relative import path to absolute import path"""
    if symbol["level"] == 0:
        return symbol

    path, level = symbol["path"], symbol["level"]
    while level > 0:
        path = os.path.abspath(os.path.join(path, ".."))
        level -= 1
    if path.startswith(ROOT_DIR):
        path = path[len(ROOT_DIR):]
        assert symbol["module"] != None
        module_path = ".".join((path, symbol["module"])).replace("/", ".")
        symbol["module"] = module_path
    return symbol

def gen_ast(path: str) -> ast.AST:
    file_ast = None
    try:
        src = open(path, "r")
        file_ast = ast.parse(src.read(), "ast.log", "exec")
    except Exception as e:
        print(path, repr(e))
    return file_ast


def parse_import_symbol(path: str) -> dict:
    file_ast = gen_ast(path)
    if not file_ast:
        return {}

    import_nodes = []
    for node in (n for n in file_ast.body if isinstance(n, ast.ImportFrom)):
        import_nodes.append(node)

    import_list = []
    filter_symbols = ["*"]
    for node in import_nodes:
        module = node.module
        level = node.level
        lineno = node.lineno
        names = [alias.name for alias in node.names if alias.name not in filter_symbols]
        # deal with form such as:
        # 1. form . import xxx
        # 2. from .. import xxx
        # 3. from .mmm import xxx
        # 4. from ..mmm import xxx
        # xxx may be 1. a symbol in __init__.py
        #            2. a file in the package
        if module is None:
            new_names = []
            tmp = level
            dir = path
            while tmp > 0:
                dir = os.path.abspath(os.path.join(dir, ".."))
                tmp -= 1
            for name in names:
                dirname = os.path.join(dir, name)
                filename = os.path.join(dir, "{}.py".format(name))
                # filter names which are module name
                if not os.path.exists(dirname) and not os.path.exists(filename):
                    new_names.append(name)
            names = new_names
            module = "__init__"
        if module in IGNORE_MODULE: # filter ignore modules
            continue
        import_module = {"path":path, "module": module, "lineno": lineno,
                            "level":level, "names":names}
        if level > 0:
            import_module = relative_to_absolute(import_module)
        import_list.append(import_module)
    return import_list


def parse_export_symbol(symbols:dict) -> dict:
    if not symbols:
        return {}

    module = symbols["module"]
    if module in project_file_dict:
        path = project_file_dict[module]
        invalid_symbols = check_symbols(path, symbols)
        if len(invalid_symbols) > 0:
            path = symbols["path"][len(IGNORE_PATH_PREFIX):]
            print("[INVALID] %s:%s\n\t%s" %(path, symbols["lineno"], invalid_symbols))

        return {"path": symbols["path"], "invalid_import": invalid_symbols}
    else:
        not_found_modules.add(module)


def check_symbols(path: str, symbols:dict) -> dict:
    file_symtable = None
    try:
        src = open(path, "r").readlines()
        src = "".join(src)
        file_symtable = symtable.symtable(src, path, "exec")
    except Exception as e:
        print(file, repr(e))
    if not file_symtable:
        return {}

    invalid_symbols = []
    for name in symbols["names"]:
        try:
            if file_symtable.lookup(name).is_namespace():
                # print("namespace: ", name)
                pass
            else:
                # print("not namespace: ", name)
                invalid_symbols.append(name)
        except Exception as e:
            print(symbols["path"], path, repr(e))
    return invalid_symbols
 

if __name__ == "__main__":
    gen_project_import_map(ROOT_DIR)
    file_list = []

    cmd = 'find {} -name "*.py" | grep -v "__init__" > ./list_pyfile.txt'.format(ROOT_DIR)
    res = os.system(cmd)
    if res != 0:
        print("run cmd failed.")
        exit(1)

    with open("./list_pyfile.txt", "r") as f:
        paths = f.readlines()
        paths = [path.strip() for path in paths]
        for file in paths:
            ign_flag = False
            for ign_path in IGNORE_PATH:
                if ign_path in file:
                    ign_flag = True
                    break
            if not ign_flag:
                file_list.append(file)

    for path in file_list:
        import_list = parse_import_symbol(path)
        for item in import_list:
            parse_export_symbol(item)

    # print("===================== project_file_dict: ")
    # pprint.pprint(project_file_dict)
    # print("===================== not found modules: ")
    # pprint.pprint(not_found_modules)
